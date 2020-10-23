class Lexer:
    def __init__(self, input):
        self.source = input + '\n' # Source code to lex as a string. Append a newline to simplify lexing/ parsing the last token/ statement.
        self.curChar = ''   # Current character in the string
        self.curPos = -1    # Current position in the string
        self.nextChar()

    # Process the next character
    def nextChar(self):
        self.curPos = self.curPos + 1
        self.curChar = '\0' if self.curPos >= len(self.source) else self.source[self.curPos] 

    # Return the lookahead character
    def peek(self):
        if self.curPos + 1 >= len(self.source):
            return '\0'
        return self.source[self.curPos + 1]

    # Invalid token found, print error message and exit
    def abort(self, message):
        import sys
        sys.exit("Lexing error. " + message)

    # Skip whitespace except newlines, which we will use to indiciate the end of a statement.
    def skipWhitespace(self):
        whitespaces = [' ', '\t', '\r']
        while self.curChar in whitespaces:
            self.nextChar()

    # Skip coments in the code
    def skipComment(self):
        if self.curChar == '#':
            while self.curChar != '\n':
                self.nextChar()

    # Return the next token
    def getToken(self):
        # Check the first character of this token to see if we can decide what it is.
        # If it is a multiple character operator (e.g., !=), number, identifier or keyword then we will process the rest.
        self.skipWhitespace()
        self.skipComment()

        if self.curChar == '+':
            token = Token(self.curChar, TokenType.PLUS)
        elif self.curChar == '-':
            token = Token(self.curChar, TokenType.MINUS)
        elif self.curChar == '*':
            token = Token(self.curChar, TokenType.ASTERISK)
        elif self.curChar == '/':
            token = Token(self.curChar, TokenType.SLASH)
        elif self.curChar == '=':
            if self.peek() == '=':
                prev_char = self.curChar
                self.nextChar()
                token = Token(prev_char + self.curChar, TokenType.EQEQ)
            else:
                token = Token(self.curChar, TokenType.EQ)
        elif self.curChar == '>':
            # Check whether this is token is > or >=
            if self.peek() == '=':
                prev_char = self.curChar
                self.nextChar()
                token = Token(prev_char + self.curChar, TokenType.GTEQ)
            else:
                token = Token(self.curChar, TokenType.GT)
        elif self.curChar == '<':
            # Check whether this is token is < or <=
            if self.peek() == '=':
                prev_char = self.curChar
                self.nextChar()
                token = Token(prev_char + self.curChar, TokenType.LTEQ)
            else:
                token = Token(self.curChar, TokenType.LT)
        elif self.curChar == '!':
            if self.peek() == '=':
                prev_char = self.curChar
                self.nextChar()
                token = Token(prev_char + self.curChar, TokenType.NOTEQ)
            else:
                self.abort('Expected !=, got !' + self.peek())
        elif self.curChar == '\n':
            token = Token(self.curChar, TokenType.NEWLINE)
        elif self.curChar == '\0':
            token = Token(self.curChar, TokenType.EOF)
        elif self.curChar == '\"':
            # Get characters between quotations
            self.nextChar()
            startPos = self.curPos
            while self.curChar != '\"':
                # Don't allow special characters in the string. No escape characters, newlines, tabs, or %
                # We will be using C's printf on this string.
                if self.curChar == '\r' or self.curChar == '\n' or self.curChar == '\t' or self.curChar == '\\' or self.curChar == '%':
                    self.abort("Illegal character in string.")
                self.nextChar()
            tokenText = self.source[startPos:self.curPos] # Get the substring
            token = Token(tokenText, TokenType.STRING)
        elif self.curChar.isdigit():
            # Leading character is digit, so this must be a number
            # Get all consecutive digits and decimal is there is one.
            startPos = self.curPos
            while self.peek().isdigit():
                self.nextChar()
            if self.peek() == '.':  # This is a decimal
                self.nextChar()
                # Must have atleast one digit after the decimal
                if not self.peek().isdigit():
                    # Error
                    self.abort("Illegal character in number!")
                while self.peek().isdigit():
                    self.nextChar()
            tokenText = self.source[startPos:self.curPos + 1] # Get the substring
            token = Token(tokenText, TokenType.NUMBER)
        elif self.curChar.isalpha():
            # Leading character is a letter, so this must be an identifier or a keyword.
            # Get all consecutive alpha numberic characters
            startPos = self.curPos
            while self.peek().isalnum():
                self.nextChar()
            
            # Check if token is in the list of keywords
            tokenText = self.source[startPos: self.curPos + 1] # Get the substring
            keyword = Token.checkIfKeyword(tokenText)
            if keyword == None: # Identifier
                token = Token(tokenText, TokenType.IDENT)
            else:   # Keyword
                token = Token(tokenText, keyword)
        else:
            # Unknown token
            self.abort("Unknown token: " + self.curChar)
        self.nextChar()
        return token

# Token contains the original text and type of token
class Token:
    def __init__(self, tokenText, tokenType):
        self.text = tokenText   # The token's actual text. Used for identifiers, strings, and numbers. 
        self.type = tokenType   # The TokenType that this token is classified as.

    @staticmethod
    def checkIfKeyword(tokenText):
        for type in TokenType:
            if type.name == tokenText and type.value >= 100 and type.value < 200:
                return type
        return None

import enum
class TokenType(enum.Enum):
    EOF = -1
    NEWLINE = 0
    NUMBER = 1
    IDENT = 2
    STRING = 3
    
    # Keywords
    LABEL = 101
    GOTO = 102
    PRINT = 103
    INPUT= 104
    LET = 105
    IF = 106
    THEN = 107
    ENDIF = 108
    WHILE = 109
    REPEAT = 110
    ENDWHILE = 111

    # Operators
    EQ = 201
    PLUS = 202
    MINUS = 203
    ASTERISK = 204
    SLASH = 205
    EQEQ = 206
    NOTEQ = 207
    LT = 208
    LTEQ = 209
    GT = 210
    GTEQ = 211