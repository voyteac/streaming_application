client_host: str = 'localhost'
server_host: str = 'localhost'
port: int = 9094
received_data_buffer: int = 1024
default_number_of_tcp_clients: int = 1
data_generation_pause_period: float = 0.5
msg_send_retry_delay: int = 1

max_connection_retries = 3
connection_attempt_retry_count = 0