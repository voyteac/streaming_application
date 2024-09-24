from django.db import connection
from django.db import OperationalError
from streaming_app.config import database
from data_ingress.common.logging_.to_log_file import log_error, log_info


class PostgresqlHandler:
    def __init__(self):
        self.table_name: str = database.table_name

        self.truncate_table_command: str = f'TRUNCATE TABLE {self.table_name} RESTART IDENTITY CASCADE;'
        self.count_rows_in_table: str = f'SELECT COUNT(*) FROM {self.table_name};'

    def clear_table(self) -> None:
        try:
            with connection.cursor() as cursor:
                row_count: int = self.get_number_of_rows_in_table()
                if row_count != 0:
                    cursor.execute(self.truncate_table_command)
                    self.double_check_whether_table_was_cleared()
                else:
                    log_info(self.clear_table, f'Table {self.table_name} was ALREADY empty')
        except OperationalError as e:
            raise RuntimeError(f"Database error: {e}")

    def get_number_of_rows_in_table(self) -> int:
        with connection.cursor() as cursor:
            cursor.execute(self.count_rows_in_table)
            return cursor.fetchone()[0]

    def double_check_whether_table_was_cleared(self) -> None:
        double_checked_number_of_rows_in_table: int = self.get_number_of_rows_in_table()
        if double_checked_number_of_rows_in_table != 0:
            log_info(self.clear_table, f'Table {self.table_name} has been truncated.')
        else:
            log_error(self.clear_table, f'Table {self.table_name} was NOT cleand')


postgresql_handler = PostgresqlHandler()
