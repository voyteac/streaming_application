from typing import Dict, List, Any

from data_ingress.common.logging_.to_log_file import log_debug


class DockerServiceConfigJsonParser:
    def __init__(self, data: Dict[str, Any]):
        self.data = data

    def get_service_info_name(self) -> str:
        return self.data.get('service_info', {}).get('name', 'unknown_service')

    def get_containers_names(self) -> List[str]:
        return [container['name'] for container in self.data.get('containers', [])]

    def get_session_storage_key(self) -> str:
        return self.data.get('session', {}).get('storage_key', 'unknown_key')

    def get_session_status_started(self) -> str:
        log_debug(self.get_session_status_started, self.data.get('session', {}).get('status_started', 'unknown'))
        return self.data.get('session', {}).get('status_started', 'unknown')

    def get_session_status_stopped(self) -> str:
        log_debug(self.get_session_status_stopped, self.data.get('session', {}).get('status_stopped', 'unknown'))
        return self.data.get('session', {}).get('status_stopped', 'unknown')

    def get_redirect_pattern(self) -> str:
        return self.data.get('redirect', {}).get('pattern', 'unknown_pattern')

    def get_ui_message_up(self) -> str:
        log_debug(self.get_session_status_stopped, self.data.get('ui_message', {}).get('service_up', 'unknown'))
        return self.data.get('ui_message', {}).get('service_up', 'unknown')

    def get_ui_message_down(self) -> str:
        log_debug(self.get_session_status_stopped, self.data.get('ui_message', {}).get('service_down', 'unknown'))
        return self.data.get('ui_message', {}).get('service_down', 'unknown')