# http://web.eecs.utk.edu/~azh/blog/teenytinycompiler1.html
from lex import *

def main():
    input = "IF+-123 foo*THEN/"
    lexer = Lexer(input)

    token = lexer.getToken()
    while token.type != TokenType.EOF:
        print(token.type)
        token = lexer.getToken()

main()