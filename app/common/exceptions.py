class BaseError(BaseException):
    """
    Base package for errors.
    """
    def __init__(self, code, message, http_status, friendly_message=None):
        self.code = code
        self.message = message
        self.friendly_message = friendly_message
        self.http_status = http_status

    def get_error_json(self):
        return {
            "error_code": self.code,
            "message": self.message,
            "http_status": self.http_status
        }

    def get_friendly_message_json(self):
        return {
            "error_code": self.code,
            "message": self.friendly_message,
            "response": ""
        }


class InvalidInputError(BaseError):
    def __init__(self, message):
        super().__init__(
            code='IOE001',
            message='Entrada inválida: {}'.format(message),
            friendly_message='Os dados inseridos são inválidos para essa operação.',
            http_status=400)


class GeneralError(BaseError):
    def __init__(self, service_name, message):
        super().__init__(
            code="GUE000",
            message="Erro no serviço{}: {}".format(service_name, message),
            friendly_message="Erro no serviço {}: {}.".format(service_name, message),
            http_status=500)
