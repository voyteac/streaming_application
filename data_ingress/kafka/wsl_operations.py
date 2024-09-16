import logging
import subprocess
import traceback

logger = logging.getLogger('streaming_app')


def execute_command_on_wsl(command):
    logger.debug(f'{execute_command_on_wsl.__name__} -> Command to be executed: {command}')
    try:
        result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
        logger.debug(f'{execute_command_on_wsl.__name__} -> Results of the command execution: {result}')
        return result
    except subprocess.CalledProcessError as e:
        logger.error(f'{execute_command_on_wsl.__name__} -> Error executing WSL command: {e.stderr}')
        logger.error(f'{execute_command_on_wsl.__name__} -> {traceback.format_exc()}')
        return []
