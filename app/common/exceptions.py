class BaseError(BaseException):
    """
    Base package for errors.
    """
    def __init__(self, code, message, friendly_message, http_status):
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
