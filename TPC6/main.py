import ply.lex as lex
from sys import argv

class MyLexer():
    states = (
        ('comment', 'exclusive'),
    )
    tokens = (
        "FUNCTION",
        "WHILE",
        "INT",
        "MULTI_LINE_COMMENT_START",
        "MULTI_LINE_COMMENT_END",
        "COMMENTS",
        "SINGLE_COMMENT_LINE",
        "SEMI_COLON",
        "COMMA",
        "MULTIPLY",
        "DIVIDE",
        "MINUS",
        "GREATER",
        "PAROPEN",
        "PARCLOSE",
        "CBRACKETOPEN",
        "CBRACKETCLOSE",
        "EQUAL",
        "NOME",
        "FOR",
        "IN",
        "PROGRAM",
        "RANGE_POINTS",
        "NUMBER",
        "BRACKETOPEN",
        "BRACKETCLOSE",
        "IF",
        "MINOR",
    )

    def __init__(self):
        self.lexer: lex.Lexer = lex.lex(module=self)

        self.pars = 0
        self.cbrackets = 0
        self.brackets = 0

        self.reserved_words = {
            "function": "FUNCTION",
            "while": "WHILE",
            "int": "INT",
            "for": "FOR",
            "in": "IN",
            "program": "PROGRAM",
            "if": "IF",
            "else": "ELSE",
                }

    t_ANY_ignore = ' \t\n'

    t_MINOR = "<"
    t_SINGLE_COMMENT_LINE = "//.*"
    t_SEMI_COLON = ";"
    t_COMMA = ","
    t_comment_COMMENTS = r"[^(\/\*)]+"
    t_RANGE_POINTS = r'\.\.'
    t_NUMBER = r'\d+'
    t_MULTIPLY = r'\*'
    t_DIVIDE = r'\/'
    t_MINUS = r'\-'
    t_GREATER = r'\>'
    t_EQUAL = r'\='

    def t_BRACKETOPEN(self, t):
        r"\["
        self.brackets += 1
        return t

    def t_BRACKETCLOSE(self, t):
        r"\]"
        if self.brackets == 0:
            print("Unexpected ]")
            return t
        self.brackets -= 1
        return t

    def t_PAROPEN(self, t):
        r"\("
        self.pars += 1
        return t

    def t_PARCLOSE(self, t):
        r"\)"
        if self.pars == 0:
            print("Unexpected )")
            return t
        self.pars -= 1
        return t

    def t_CBRACKETOPEN(self, t):
        r"\{"
        self.cbrackets += 1
        return t

    def t_CBRACKETCLOSE(self, t):
        r"\}"
        if self.cbrackets == 0:
            print("Unexpected }")
            return t
        self.cbrackets -= 1
        return t

    def t_MULTI_LINE_COMMENT_START(self, t):
        r"\/\*"
        t.lexer.begin('comment')
        return t

    def t_comment_MULTI_LINE_COMMENT_END(self, t):
        r"\*\/"
        t.lexer.begin('INITIAL')
        return t

    def t_NOME(self, t):
        r"\b[a-zA-Z_][a-zA-Z0-9_]*\b"
        t.type = self.reserved_words.get(t.value, "NOME")
        return t

    def t_ANY_error(self, t):
        print("Illegal character", t.value[0])
        t.lexer.skip(1)
        return t

    def tokenize(self, data):
        self.lexer.input(data)

def main():
    if len(argv) == 1:
        print("No file specified")
        return

    file = argv[1]
    lexer = MyLexer()
    with open(file, "r") as file:
        lexer.tokenize(file.read())

    while tok := lexer.lexer.token():
        print(tok)

if __name__ == "__main__":
    main()
