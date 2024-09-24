from data_ingress.common.logging_.to_log_file import log_error


class ErrorDuringGpbEventDecompose(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message
        log_error(self.__class__, f'Decomposing GPB event notification to JSON - Failed: {self.message}')

class ErrorDuringDecomposingUniqueClientId(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message
        log_error(self.__class__, f'Decomposing unique_client_id - Failed')