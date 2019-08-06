import boto3

from trequire.exceptions import GeneralExceptions


class SessionService(object):
    def __init__(self, profile, region):
        self.session = boto3.Session(profile_name=profile, region_name=region)

    def resource(self, service_name, client=False):
        if client:
            return self.session.client(service_name)
        return self.session.resource(service_name)


class ManageRequirements(object):
    def __init__(self, profile, region):
        session = SessionService(profile, region)

        self.s3_res = session.resource('s3')
        self.s3_client = session.resource('s3', client=True)
        self.dynamodb_res = session.resource('dynamodb')
        self.dynamodb_client = session.resource('dynamodb', client=True)
        self.iam_client = session.resource('iam', client=True)
        self.region = region

    def _enable_bucket_versioning(self, name):
        versioning = self.s3_res.BucketVersioning(name)
        versioning.enable()

    def bucket(self, name):
        '''
        Create s3 bucket
        '''
        status = None
        tag_list = {
            'TagSet': [{
                'Key': 'Created by',
                'Value': 'trequire tool'
            }]
        }

        try:
            self.s3_client.create_bucket(Bucket=name,
                                         CreateBucketConfiguration={'LocationConstraint': self.region})
            status = '{} bucket created'.format(name)
        except Exception as exc:
            raise GeneralExceptions(exc)
        else:
            self._enable_bucket_versioning(name)
            # Set ACL on bucket
            self.s3_res.BucketAcl(name)
            # Enable encryption
            self.s3_client.put_bucket_encryption(
                Bucket=name,
                ServerSideEncryptionConfiguration={
                    'Rules': [{
                        'ApplyServerSideEncryptionByDefault': {
                            'SSEAlgorithm': 'AES256',
                        }
                    }]
                }
            )
            self.s3_client.put_bucket_tagging(Bucket=name, Tagging=tag_list)
        return status

    def dynamodb(self, name):
        '''
        Create dynamodb table
        '''
        tag_list = [{
            'Key': 'Created by',
            'Value': 'trequire tool'
        }]
        try:
            table = self.dynamodb_res.create_table(
                TableName=name,
                KeySchema=[{
                        'AttributeName': 'LockID',
                        'KeyType': 'HASH'
                    },
                ],
                AttributeDefinitions=[{
                        'AttributeName': 'LockID',
                        'AttributeType': 'S'
                    },
                ],
                ProvisionedThroughput={
                    'ReadCapacityUnits': 20,
                    'WriteCapacityUnits': 20
                }
            )

            table.meta.client.get_waiter('table_exists').wait(TableName=name)
            self.dynamodb_client.tag_resource(ResourceArn=table.table_arn,
                                              Tags=tag_list)
            return '{} table created'.format(name)
        except Exception as e:
            if 'Cannot create preexisting table' in str(e):
                return '{} table already exists'.format(name)
            else:
                raise e

    @property
    def get_buckets(self):
        buckets_list = []

        for bucket in self.s3_res.buckets.all():
            if bucket.name not in buckets_list:
                buckets_list.append(bucket.name)
        return buckets_list

    @property
    def get_dynamodb_tables(self):
        tables_list = []

        for table in self.dynamodb_res.tables.all():
            if table.name not in tables_list:
                tables_list.append(table.name)

        return tables_list

    def remove_bucket(self, name):
        status = None
        try:
            self.s3_client.delete_bucket(Bucket=name)
            status = 'Removed'
        except Exception as exc:
            raise GeneralExceptions(exc)

        return status

    def remove_dynamodb_table(self, name):
        status = None
        try:
            self.dynamodb_client.delete_table(TableName=name)
            status = 'Removed'
        except Exception as exc:
            raise GeneralExceptions(exc)

        return status

    def iam_users(self):
        users_list = {}

        paginator = self.iam_client.get_paginator('list_users')
        for users in paginator.paginate():
            for user in users['Users']:
                if user['UserName'] not in users_list:
                    users_list.update({
                        user['UserName']: user['UserId']
                        })

        return users_list

    def add_user(self, name):
        tags_list = [{
            'Key': 'Created by',
            'Value': 'trequire tool'
        }]
        status = 'Success'

        try:
            self.iam_client.create_user(UserName=name, Tags=tags_list)
        except Exception as e:
            status = 'Failed'
            raise e

        return status

    def enable_access_key(self, name):
        keys_list = {}
        try:
            create_access_key = self.iam_client.create_access_key(UserName=name)
            for keys in create_access_key.values():
                if 'SecretAccessKey' in keys:
                    keys_list.update({
                        'access_key': keys['AccessKeyId'],
                        'secret_key': keys['SecretAccessKey']
                    })
        except Exception as e:
            raise e

        return keys_list

    def remove_user(self, name):
        status = 'Failed'
        get_access_ids = self._get_access_id(name)

        try:
            if len(get_access_ids) > 0:
                for access_id in get_access_ids:
                    self.iam_client.delete_access_key(UserName=name, AccessKeyId=access_id)
            self.iam_client.delete_user(UserName=name)
            status = 'Success'
        except Exception as e:
            raise e

        return status

    def _get_access_id(self, user):
        access_keys = self.iam_client.list_access_keys(UserName=user)
        access_id_list = []

        for access_info in access_keys['AccessKeyMetadata']:
            access_id_list.append(access_info['AccessKeyId'])

        return access_id_list
