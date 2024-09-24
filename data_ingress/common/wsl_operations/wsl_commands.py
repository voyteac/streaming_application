from subprocess import CompletedProcess
import subprocess
from typing import Optional

from data_ingress.common.logging_.to_log_file import log_debug
from data_ingress.common.wsl_operations.wsl_exceptions import WslCommandExecutionFailed

class CommandExecutor:
    def execute_command(self, command: str) -> Optional[CompletedProcess]:
        log_debug(self.execute_command, f'Command to be executed: {command}')
        try:
            result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
        except subprocess.CalledProcessError as cmd_failed:
            raise WslCommandExecutionFailed(f'Error executing WSL command: {command} with error:\n{cmd_failed}')
        else:
            log_debug(self.execute_command, f'Results of the command execution: {result}')
            return result
