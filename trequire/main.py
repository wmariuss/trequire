import click
from termcolor import colored

from trequire.validation import ConfigValidation
from trequire.aws import ManageRequirements


def get_data(file):
    validate = ConfigValidation()
    data = validate.parse_config(file)
    validate_content = validate.data_validation(data)

    if validate_content:
        return data
    return


@click.group()
@click.version_option()
def cli():
    '''Manage backend resources for Terraform states
    '''
    pass


@cli.command(help='Manage resources based on config file')
@click.option('--file', '-f', type=click.Path(exists=True), help='trequire config file')
def run(file):
    '''Manage resources based on config file
    '''
    if file:
        data = get_data(file)
        requirements = data.get('requirements')
        profile = requirements.get('profile', 'default')

        list_to_add = requirements.get('add', '')
        list_to_remove = requirements.get('remove', '')

        manage = ManageRequirements(profile)
        s3_buckets_list = manage.get_buckets
        dynamodb_tables_list = manage.get_dynamodb_tables
        users_list = manage.iam_users()

        if list_to_add:
            buckets_list_add = list_to_add.get('buckets')
            tables_list_add = list_to_add.get('dynamodb')
            iam_user = list_to_add.get('user')

            # Create s3 bucket(s)
            if buckets_list_add:
                for bucket in buckets_list_add:
                    create_bucket = manage.bucket(bucket)
                    if bucket not in s3_buckets_list:
                        # create_bucket = manage.bucket(bucket)
                        if 'created' in create_bucket:
                            click.echo(colored('[{}] s3 bucket created'.format(bucket), 'green'))
                    else:
                        click.echo(colored('[{}] bucket already exists, but it will be updated'.format(bucket), 'yellow'))

            # Create dynamodb table(s)
            if tables_list_add:
                for table in tables_list_add:
                    if table not in dynamodb_tables_list:
                        create_dynamodb_table = manage.dynamodb(table)
                        if 'created' in create_dynamodb_table:
                            click.echo(colored('[{}] dynamodb table created'.format(table), 'green'))
                    else:
                        click.echo(colored('[{}] dynamodb table already exists'.format(table), 'yellow'))

            if iam_user:
                if iam_user not in users_list:
                    add_user = manage.add_user(iam_user)
                    if 'success' in add_user.lower():
                        click.echo(colored('[{}] IAM user created'.format(iam_user), 'green'))
                        click.echo(colored('Generating access keys for {} user...'.format(iam_user), 'green'))
                        click.echo(colored(manage.enable_access_key(name=iam_user), 'green'))
                else:
                    click.echo(colored('[{}] IAM user exists'.format(iam_user), 'yellow'))

        if list_to_remove:
            buckets_list_remove = list_to_remove.get('buckets')
            tables_list_remove = list_to_remove.get('dynamodb')
            iam_user = list_to_remove.get('user')

            # Delete s3 bucket(s)

            if buckets_list_remove:
                for bucket in buckets_list_remove:
                    if bucket in s3_buckets_list:
                        delete_bucket = manage.remove_bucket(bucket)
                        if 'removed' in delete_bucket.lower():
                            click.echo(colored('[{}] s3 bucket removed'.format(bucket), 'green'))
                    else:
                        click.echo(colored('[{}] s3 bucket is already removed or not exists'.format(bucket), 'yellow'))

            # Delete dynamodb table(s)
            if tables_list_remove:
                for table in tables_list_remove:
                    if table in dynamodb_tables_list:
                        delete_table = manage.remove_dynamodb_table(table)
                        if 'removed' in delete_table.lower():
                            click.echo(colored('[{}] dynamodb table removed'.format(table), 'green'))
                    else:
                        click.echo(colored('[{}] dynamodb table is already removed or not exists'.format(table), 'yellow'))

            if iam_user:
                if iam_user in users_list:
                    remove_user = manage.remove_user(iam_user)
                    if 'success' in remove_user.lower():
                        click.echo(colored('[{}] IAM user removed'.format(iam_user), 'green'))
                else:
                    click.echo(colored('[{}] IAM user is not exists'.format(iam_user), 'yellow'))
