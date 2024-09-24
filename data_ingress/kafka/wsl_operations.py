from subprocess import CompletedProcess
import subprocess
from typing import Optional

from data_ingress.logging_.to_log_file import log_debug



class WslCommandExecutionFailed(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message


def execute_command_on_wsl(command: str) -> Optional[CompletedProcess]:
    log_debug(execute_command_on_wsl, f'Command to be executed: {command}')
    try:
        result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
    except subprocess.CalledProcessError as cmd_failed:
        raise WslCommandExecutionFailed(f'Error executing WSL command: {command} with error:\n{cmd_failed}')
    else:
        log_debug(execute_command_on_wsl, f'Results of the command execution: {result}')
        return result
