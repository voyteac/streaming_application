import logging
from django.db import connection
from django.db import OperationalError
from streaming_app.config import database

logger = logging.getLogger('streaming_app')


def clear_table():
    table_name = database.table_name
    try:
        with connection.cursor() as cursor:
            row_count = get_number_of_rows_in_table(table_name)
            if row_count != 0:
                cursor.execute(f'TRUNCATE TABLE {table_name} RESTART IDENTITY CASCADE;')
                double_check_whether_table_was_cleared(table_name)
            else:
                logger.info(f'{clear_table.__name__} -> Table {table_name} was ALREADY empty')
    except OperationalError as e:
        raise RuntimeError(f"Database error: {e}")

def get_number_of_rows_in_table(table_name):
    with connection.cursor() as cursor:
        cursor.execute(f'SELECT COUNT(*) FROM {table_name};')
        return cursor.fetchone()[0]

def double_check_whether_table_was_cleared(table_name):
    double_checked_number_of_rows_in_table = get_number_of_rows_in_table(table_name)
    if double_checked_number_of_rows_in_table != 0:
        logger.info(f'{double_check_whether_table_was_cleared.__name__} -> Table {table_name} has been truncated.')
    else:
        logger.error(f'{double_check_whether_table_was_cleared.__name__} -> Table {table_name} was NOT cleand')

