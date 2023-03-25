import time


def update_partition(athena_client) -> bool:
    response = athena_client.start_query_execution(
        QueryString=f"MSCK REPAIR TABLE `lor-match-data-db`;",
        QueryExecutionContext={
            'Database': 'lor'
        },
        ResultConfiguration={
            'OutputLocation': 's3://lor-match-data-athena-output/',
        }
    )

    state = 'RUNNING'
    max_execution = 10
    execution_id = response['QueryExecutionId']

    while (max_execution > 0 and state in ['RUNNING', 'QUEUED']):
        max_execution = max_execution - 1
        response = athena_client.get_query_execution(
            QueryExecutionId=execution_id)

        if 'QueryExecution' in response and \
                'Status' in response['QueryExecution'] and \
                'State' in response['QueryExecution']['Status']:
            state = response['QueryExecution']['Status']['State']
            if state == 'FAILED':
                return False
            elif state == 'SUCCEEDED':
                return True
        time.sleep(1)

    return False
