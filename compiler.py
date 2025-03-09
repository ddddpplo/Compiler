from enum import Enum
import os

class TokenType(Enum):
    KEYWORD = 0
    SEMICOLON = 1
    INTEGER = 2
    FLOAT = 3
    SYMBOL = 4
    BRACKET = 5

class Token:
    def __init__(self, type: TokenType, value: str):
        self.type = type
        self.value = value

class Procedure:
    def __init__(self, name: str):
        self.name = name
        self.lines = []

KEYWORDS = ["exit", "return", "if", "else"]

input_filename = "test.txt"#input("Enter filename to compile: ")
asm_filename = os.path.splitext(input_filename)[0] + ".asm"

input_file = open(input_filename, "r")
asm_file = open(asm_filename, "w")

source = input_file.read()

def tokenize(source: str):
    tokens = []
    i = 0
    token_buffer = ""
    while i < len(source):
        if source[i].isalpha():
            while source[i].isalnum():
                token_buffer += source[i]
                i += 1
            if token_buffer in KEYWORDS:
                tokens.append(Token(TokenType.KEYWORD, token_buffer))
            else:
                tokens.append(Token(TokenType.SYMBOL, token_buffer))
            token_buffer = ""
        if source[i].isnumeric():
            has_decimal = False
            while source[i].isnumeric() or (source[i] == "."):
                if source[i] == ".":
                    has_decimal = True
                token_buffer += source[i]
                i += 1
            if has_decimal:
                tokens.append(Token(TokenType.FLOAT, token_buffer))
            else:
                tokens.append(Token(TokenType.INTEGER, token_buffer))
            token_buffer = ""
        if source[i] == ";":
            tokens.append(Token(TokenType.SEMICOLON, source[i]))
        if source[i] in "(){}[]":
            tokens.append(Token(TokenType.BRACKET, source[i]))
        i += 1
    return tokens

def compile(tokens: list):
    output = ""
    extern_symbols = ["ExitProcess PROTO"]
    data = []
    procedures = [Procedure("main")]
    num_tokens = len(tokens)
    current_proc = 0
    for i, token in enumerate(tokens):
        if token.type == TokenType.KEYWORD:
            if token.value == "exit" and i + 2 < num_tokens:
                if tokens[i + 1].type == TokenType.INTEGER and tokens[i + 2].type == TokenType.SEMICOLON:
                    procedures[current_proc].lines.append("sub rsp, 40")
                    procedures[current_proc].lines.append(f"mov rcx, {tokens[i + 1].value}")
                    procedures[current_proc].lines.append("call ExitProcess")
    for line in extern_symbols:
        output += line + "\n"
    output += ".data\n"
    for line in data:
        output += line + "\n"
    output += ".code\n"
    for procedure in procedures:
        output += procedure.name + " PROC\n"
        for line in procedure.lines:
            output += "\t" + line + "\n"
        output += procedure.name + " ENDP\n"
    output += "END\n"
    return output


tokens = tokenize(source)
for token in tokens:
    print(token.type, token.value)

asm_file.write(compile(tokens))