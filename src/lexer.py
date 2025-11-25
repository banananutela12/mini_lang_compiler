# lexer.py
# modulo que parte el codigo en tokenes aqui solo se separa todo

import re
from dataclasses import dataclass

@dataclass
class Token:
    kind: str   # 'ID', 'INT', 'KW', 'OP', '{', '}', '(', ')', ';', ',', 'EOF'
    value: str
    line: int
    col: int

# palabras clave del leng ojo true/false como bools
KEYWORDS = {"int", "bool", "if", "else", "while", "print", "true", "false"}

# regex basicos nota: orden importa aqu
TOKEN_SPEC = [
    ("NUMBER",   r"\d+"),                     # ints
    ("ID",       r"[a-zA-Z_][a-zA-Z0-9_]*"),  # ids normalitos
    ("OP",       r"<=|>=|==|!=|&&|\|\||[+\-*/<>=!]")  # ops
]

# espacios (no los necesitamos)
WHITESPACE = re.compile(r"[ \t]+")
NEWLINE = re.compile(r"\n")

# simbolos que van solitos
SYMBOLS = {
    '{': '{',
    '}': '}',
    '(': '(',
    ')': ')',
    ';': ';',
    ',': ','
}


class Lexer:
    def __init__(self, text: str):
        self.text = text
        self.pos = 0
        self.line = 1
        self.col = 1
        self.length = len(text)

    # ver siguientes char 
    def _peek(self, n=1):
        if self.pos + n <= self.length:
            return self.text[self.pos:self.pos+n]
        return ""

    # avanzar posición actualiza col/line
    def _advance(self, n=1):
        for _ in range(n):
            if self.pos >= self.length:
                return
            ch = self.text[self.pos]
            self.pos += 1
            if ch == '\n':
                self.line += 1
                self.col = 1
            else:
                self.col += 1

    # intenta hacer match con regex
    def _match_regex(self, pattern: re.Pattern):
        m = pattern.match(self.text, self.pos)
        if m:
            return m.group(0)
        return None

    # ignora espacios y comentarios
    def _skip_whitespace_and_comments(self):
        while self.pos < self.length:
            # whitespace normalito
            m_ws = WHITESPACE.match(self.text, self.pos)
            if m_ws:
                self._advance(len(m_ws.group(0)))
                continue

            # salto de linea
            m_nl = NEWLINE.match(self.text, self.pos)
            if m_nl:
                self._advance(len(m_nl.group(0)))
                continue

            if self._peek(2) == "//":
                # avanzar hasta el fin de la linea
                while self.pos < self.length and self.text[self.pos] != '\n':
                    self._advance()
                continue

            break

    # regresa el siguiente token
    def next_token(self) -> Token:
        self._skip_whitespace_and_comments()

        if self.pos >= self.length:
            return Token("EOF", "", self.line, self.col)

        ch = self.text[self.pos]

        # smbolos simples
        if ch in SYMBOLS:
            tok = Token(SYMBOLS[ch], ch, self.line, self.col)
            self._advance()
            return tok

        # numero
        m = TOKEN_SPEC[0][1]  # regex de NUMBER
        m_num = re.match(m, self.text[self.pos:])
        if m_num:
            value = m_num.group(0)
            tok = Token("INT", value, self.line, self.col)
            self._advance(len(value))
            return tok

        # id o keyword
        m_id = re.match(TOKEN_SPEC[1][1], self.text[self.pos:])
        if m_id:
            value = m_id.group(0)
            kind = "KW" if value in KEYWORDS else "ID"
            tok = Token(kind, value, self.line, self.col)
            self._advance(len(value))
            return tok

        # operadores (==, <=, &&, etc)
        m_op = re.match(TOKEN_SPEC[2][1], self.text[self.pos:])
        if m_op:
            value = m_op.group(0)
            tok = Token("OP", value, self.line, self.col)
            self._advance(len(value))
            return tok

        # si llega aqui, es caracter inesperado
        raise SyntaxError(f"Unexpected char '{ch}' at {self.line}:{self.col}")
