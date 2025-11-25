# lexer.py
import re
from dataclasses import dataclass

@dataclass
class Token:
    kind: str   # 'ID', 'INT', 'KW', 'OP', '{', '}', '(', ')', ';', ',', 'EOF'
    value: str
    line: int
    col: int

KEYWORDS = {"int", "bool", "if", "else", "while", "print", "true", "false"}

TOKEN_SPEC = [
    ("NUMBER",   r"\d+"),
    ("ID",       r"[a-zA-Z_][a-zA-Z0-9_]*"),
    ("OP",       r"<=|>=|==|!=|&&|\|\||[+\-*/<>=!]")
]

WHITESPACE = re.compile(r"[ \t]+")
NEWLINE = re.compile(r"\n")

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

    def _peek(self, n=1):
        if self.pos + n <= self.length:
            return self.text[self.pos:self.pos+n]
        return ""

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

    def _match_regex(self, pattern: re.Pattern):
        m = pattern.match(self.text, self.pos)
        if m:
            return m.group(0)
        return None

    def _skip_whitespace_and_comments(self):
        while self.pos < self.length:
            # whitespace
            m_ws = WHITESPACE.match(self.text, self.pos)
            if m_ws:
                self._advance(len(m_ws.group(0)))
                continue
            # newlines
            m_nl = NEWLINE.match(self.text, self.pos)
            if m_nl:
                self._advance(len(m_nl.group(0)))
                continue
            # comments: //...
            if self._peek(2) == "//":
                while self.pos < self.length and self.text[self.pos] != '\n':
                    self._advance()
                continue
            break

    def next_token(self) -> Token:
        self._skip_whitespace_and_comments()
        if self.pos >= self.length:
            return Token("EOF", "", self.line, self.col)

        ch = self.text[self.pos]

        # Symbols
        if ch in SYMBOLS:
            tok = Token(SYMBOLS[ch], ch, self.line, self.col)
            self._advance()
            return tok

        # Number
        m = TOKEN_SPEC[0][1]  # NUMBER regex string
        m_num = re.match(m, self.text[self.pos:])
        if m_num:
            value = m_num.group(0)
            tok = Token("INT", value, self.line, self.col)
            self._advance(len(value))
            return tok

        # Identifier or keyword
        m_id = re.match(TOKEN_SPEC[1][1], self.text[self.pos:])
        if m_id:
            value = m_id.group(0)
            kind = "KW" if value in KEYWORDS else "ID"
            tok = Token(kind, value, self.line, self.col)
            self._advance(len(value))
            return tok

        # Operators
        m_op = re.match(TOKEN_SPEC[2][1], self.text[self.pos:])
        if m_op:
            value = m_op.group(0)
            tok = Token("OP", value, self.line, self.col)
            self._advance(len(value))
            return tok

        raise SyntaxError(f"Unexpected character '{ch}' at {self.line}:{self.col}")
