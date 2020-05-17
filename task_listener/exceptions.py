class ParsingError(BaseException):
    splitting_part = None
    url = None

    def __init__(self, splitting_part, url=None):
        self.splitting_part = splitting_part
        self.url = url
