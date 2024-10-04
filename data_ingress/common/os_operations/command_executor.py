from subprocess import CompletedProcess
import subprocess
from typing import Optional

from common.logging_.to_log_file import log_debug, log_error_traceback
from data_ingress.common.os_operations.command_executor_exceptions import CommandExecutionFailed

class CommandExecutor:
    def execute_command(self, command: str) -> Optional[CompletedProcess]:
        log_debug(self.execute_command, f'Command to be executed: {command}')
        try:
            result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
        except subprocess.CalledProcessError as cmd_failed:
            log_error_traceback(self.execute_command)
            raise CommandExecutionFailed(f'Error executing command: {command} with error:\n{cmd_failed}')
        else:
            log_debug(self.execute_command, f'Results of the command execution: {result}')
            return result
