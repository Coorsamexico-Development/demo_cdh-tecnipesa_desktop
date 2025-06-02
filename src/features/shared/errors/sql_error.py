class SqlError(Exception):
    def __init__(self, title = 'Sin Titulo', message = '', query = '' ):
        super().__init__(message)
        self.title = title
        self.message = message
        self.query = query