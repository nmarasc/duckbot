# Last Updated: 2.2
from util.diagCodes import DIAG_CODES

# Diag Message class
class DiagMessage:
    # Constructor for diag message
    # Params: code   - diag code for message
    #         fill   - strings to fill in text
    # Return: DiagMessage instance
    def __init__(self, code, *fill):
    #{{{
        self.code = code
        self.text = DIAG_CODES[code]
        self.msg  = self.code + " " + self.text
        if fill and self.text:
            self.msg += ": " + " - ".join(fill)
        elif fill and not self.text:
            self.msg += ": ".join(fill)
    #}}}
