class RequestError(Exception):
    def __init__(self, title = 'Sin Titulo', message = '', code = 500 ):
        super().__init__(message)
        self.title = title
        self.message = message
        self.code = code