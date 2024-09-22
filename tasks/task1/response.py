TEXT_HEADER = [(b'content-type', b'text/plain'),]
JSON_HEADER = [(b'content-type', b'application/json')]

class Response:
    def __init__(self, status, body, header=TEXT_HEADER):
        self.status = status
        self.body = body
        self.header = header
