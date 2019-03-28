import boto3

from treq.exceptions import GeneralExceptions

class ManageeRequirements(object):
    def __init__(self, session):
        self.session = boto3.Session(profile_name=session)
        self.s3_client = self.session.client('s3')
        self.s3_res = self.session.resource('s3')
        self.dynamodb_res = self.session.resource('dynamodb')
        self.dynamodb_client = self.session.client('dynamodb')

    def _enable_bucket_versioning(self, name):
        versioning = self.s3_res.BucketVersioning(name)
        versioning.enable()

    def bucket(self, name):
        status = None
        try:
            self.s3_client.create_bucket(Bucket=name)
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
                    'Rules': [
                        {
                            'ApplyServerSideEncryptionByDefault': {
                                'SSEAlgorithm': 'AES256',
                            }
                        },
                    ]
                }
            )
        return status

    def dynamodb(self, name):
        try:
            table = self.dynamodb_res.create_table(
                TableName=name,
                KeySchema=[
                    {
                        'AttributeName': 'LockID',
                        'KeyType': 'HASH'
                    },
                ],
                AttributeDefinitions=[
                    {
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
            return '{} table created'.format(name)
        except Exception:
            return '{} table already exists'.format(name)

    @property
    def get_buckets(self):
        buckets_list = []

        for bucket in self.s3_res.buckets.all():
            if bucket.name not in buckets_list:
                buckets_list.append(bucket.name)
        return buckets_list

    @property
    def get_dynamodb_tables(self):
        tables_list =  []

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