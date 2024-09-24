from django.db import connection
from django.db import OperationalError
from streaming_app.config import database
from data_ingress.logging_.to_log_file import log_error, log_info

table_name: str = database.table_name

def clear_table() -> None:
    try:
        with connection.cursor() as cursor:
            row_count: int = get_number_of_rows_in_table(table_name)
            if row_count != 0:
                cursor.execute(f'TRUNCATE TABLE {table_name} RESTART IDENTITY CASCADE;')
                double_check_whether_table_was_cleared(table_name)
            else:
                log_info(clear_table, f'Table {table_name} was ALREADY empty')
    except OperationalError as e:
        raise RuntimeError(f"Database error: {e}")


def get_number_of_rows_in_table(table_name_arg: str) -> int:
    with connection.cursor() as cursor:
        cursor.execute(f'SELECT COUNT(*) FROM {table_name_arg};')
        return cursor.fetchone()[0]

def double_check_whether_table_was_cleared(table_name_arg: str) -> None:
    double_checked_number_of_rows_in_table: int = get_number_of_rows_in_table(table_name_arg)
    if double_checked_number_of_rows_in_table != 0:
        log_info(clear_table, f'Table {table_name_arg} has been truncated.')
    else:
        log_error(clear_table, f'Table {table_name_arg} was NOT cleand')

