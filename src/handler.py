import os
import datetime
import logging
import boto3
import botocore.exceptions


def is_table_backupable(table_details: dict) -> bool:
    return table_details.get('TableStatus') == 'ACTIVE'


class LoggingMixin(object):
    @property
    def logger(self):
        name = '.'.join([
            self.__module__,
            self.__class__.__name__
        ])
        return logging.getLogger(name)


class LambdaHandler(LoggingMixin):
    def __init__(self, session=None):
        super().__init__()
        self.session = session or boto3.Session()

    def handle_request(event, context):
        self.logger.info(f'received event [{event}]')

        backup_id = datetime.datetime.utcnow().isoformat()
        backup_name = f'automatic-{backup_id}'

        dynamodb = self.session.client('dynamodb')

        list_tables_paginator = dynamodb.get_paginator('list_tables')
        list_tables_paginator_opts = {}
        list_tables_iterator = list_tables_paginator.paginate(**list_tables_paginator_opts)

        for page in list_tables_iterator:
            table_names = page.get('TableNames', [])
            for table_name in table_names:
                describe_table_result = client.describe_table(
                    TableName=table_name
                )
                if is_table_backupable(describe_table_result):
                    try:
                        self.logger.info(f'creating backup with id={backup_id} for table={table_name}')
                        response = dynamodb.create_backup(
                            TableName=table_name,
                            BackupName=backup_name
                        )
                    except botocore.exceptions.ClientError as e:
                        self.logger.warn(f'failed to create backup for table={table_name}: {e}')


def handle_request(event, context):
    handler = LambdaHandler()
    handler_result = handler.handle_request(event, context)
    
    return handler_result

