class NotSupportedException(Exception):

    def __init__(self, message):
        super(NotSupportedException, self).__init__(message)