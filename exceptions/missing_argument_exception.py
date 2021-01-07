class MissingArgumentException(Exception):

    def __init__(self, message):
        super(MissingArgumentException, self).__init__(message)