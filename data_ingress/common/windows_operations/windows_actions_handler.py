import subprocess
import time
from data_ingress.common.logging_.to_log_file import log_debug, log_info, log_error
from streaming_app.config.tcp_config import data_generation_pause_period

class WindowsActionsHandler:
    def __init__(self):
        self.data_generation_pause_period = data_generation_pause_period


    def check_TCP_port_data_generation_with_retries(self, port: int, max_attempts: int = 5, wait_time: float = 0.5) -> bool:
        for attempt in range(max_attempts):
            try:
                timeout = self.data_generation_pause_period * 2
                result = subprocess.run(['netstat', '-an'], capture_output=True, text=True, timeout=timeout)
                if self.check_port_status(result.stdout, port):
                    log_debug(self.check_TCP_port_data_generation_with_retries, f'Data is generated on port: {port}!')
                    return True
                else:
                    log_debug(self.check_TCP_port_data_generation_with_retries,
                              f"Attempt {attempt + 1}/{max_attempts}: No data generation on port {port}.")
            except subprocess.TimeoutExpired:
                log_error(self.check_TCP_port_data_generation_with_retries,"TimeoutExpired.")
                return False
            except Exception as e:
                log_error(self.check_TCP_port_data_generation_with_retries, f"An error occurred: {e}")
                return False
            time.sleep(wait_time)
        log_info(self.check_TCP_port_data_generation_with_retries, f"No data generation on port: {port} after {max_attempts} attempts.")
        return False

    def check_port_status(self, result_stdout: str, port: int) -> bool:
        states_to_check = ['ESTABLISHED', 'SYN_SENT']
        output_lines = result_stdout.splitlines()
        for line in output_lines:
            if str(port) in line and any(state in line for state in states_to_check):
                return True
        return False

