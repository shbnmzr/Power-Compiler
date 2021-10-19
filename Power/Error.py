class Error:
    def __init__(self, ErrorName, ErrorDetails):
        self.ErrorName = ErrorName
        self.ErrorDetails = ErrorDetails
    def __str__(self):
        return f'{self.ErrorName}: {self.ErrorDetails}'
    
class LexicalError(Error):
    def __init__(self, ErrorDetails, ErroneousToken):
        super().__init__('Illegal Character', f'Found at line {ErrorDetails}\n\t\'{ErroneousToken}\' is not a valid token')