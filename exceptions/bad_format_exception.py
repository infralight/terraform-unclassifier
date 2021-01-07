class BadFormatException(Exception):

    def __init__(self, message):
        super(BadFormatException, self).__init__(message)