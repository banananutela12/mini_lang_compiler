# parser.py
# parser del leng, aqui armamos el AST a partir de los tokens

from typing import List
from src.lexer import Lexer, Token
from src.ast_nodes import *

class Parser:
    def __init__(self, text: str):
        # lexer listo para partir el texto
        self.lexer = Lexer(text)
        self.curr = self.lexer.next_token()   # token actual (lo que estamos viendo)

    # funcion para consumir token esperado
    def _eat(self, kind=None, value=None):
        # checamos tipo/valor rapido
        if kind is not None and self.curr.kind != kind:
            raise SyntaxError(f"Expected {kind}, got {self.curr.kind} at {self.curr.line}:{self.curr.col}")
        if value is not None and self.curr.value != value:
            raise SyntaxError(f"Expected '{value}', got '{self.curr.value}' at {self.curr.line}:{self.curr.col}")
        self.curr = self.lexer.next_token()   # avanzar al sig token

    # programa -> lista de statements/decls
    def parse(self) -> Program:
        stmts: List[Stmt] = []
        while self.curr.kind != "EOF":
            stmts.append(self.parse_decl_or_stmt())
        return Program(stmts)

    # ver si es declaracion (int x;) o stmt normal
    def parse_decl_or_stmt(self) -> Stmt:
        # tipo de variable int/bool
        if self.curr.kind == "KW" and self.curr.value in ("int", "bool"):
            var_type = self.curr.value
            self._eat("KW")
            if self.curr.kind != "ID":
                raise SyntaxError("Expected identifier in declaration")
            name = self.curr.value
            self._eat("ID")
            self._eat(";")
            return VarDecl(var_type, name)

        # si no era declaracion, es stmt
        return self.parse_stmt()

    # statements (bloque, if, while, print, asig)
    def parse_stmt(self) -> Stmt:
        # bloque { ... }
        if self.curr.kind == "{":
            return self.parse_block()

        # if
        if self.curr.kind == "KW" and self.curr.value == "if":
            return self.parse_if()

        # while
        if self.curr.kind == "KW" and self.curr.value == "while":
            return self.parse_while()

        # print
        if self.curr.kind == "KW" and self.curr.value == "print":
            return self.parse_print()

        # asignacion: ID = expr;
        if self.curr.kind == "ID":
            name = self.curr.value
            self._eat("ID")
            # debe  '='
            if self.curr.kind != "OP" or self.curr.value != "=":
                raise SyntaxError("Expected '=' in assignment")
            self._eat("OP")
            expr = self.parse_expr()
            self._eat(";")
            return Assign(name, expr)

        raise SyntaxError(f"Unexpected token in statement: {self.curr.kind} {self.curr.value}")


    def parse_block(self) -> Block:
        self._eat("{")
        stmts: List[Stmt] = []
        while self.curr.kind != "}":
            stmts.append(self.parse_decl_or_stmt())
        self._eat("}")
        return Block(stmts)

    # if (expr)  else 
    def parse_if(self) -> IfStmt:
        self._eat("KW", "if")
        self._eat("(")
        cond = self.parse_expr()
        self._eat(")")
        then_block = self.parse_block()

        # else opcional
        else_block = None
        if self.curr.kind == "KW" and self.curr.value == "else":
            self._eat("KW", "else")
            else_block = self.parse_block()

        return IfStmt(cond, then_block, else_block)

    # while (cond) bloque
    def parse_while(self) -> WhileStmt:
        self._eat("KW", "while")
        self._eat("(")
        cond = self.parse_expr()
        self._eat(")")
        body = self.parse_block()
        return WhileStmt(cond, body)

    # print(expr)
    def parse_print(self) -> PrintStmt:
        self._eat("KW", "print")
        self._eat("(")
        expr = self.parse_expr()
        self._eat(")")
        self._eat(";")
        return PrintStmt(expr)

    #  EXPRESIONES 
    def parse_expr(self):
        return self.parse_or()

    # or: expr1 || expr2
    def parse_or(self):
        node = self.parse_and()
        while self.curr.kind == "OP" and self.curr.value == "||":
            op = self.curr.value
            self._eat("OP")
            right = self.parse_and()
            node = BinaryOp(op, node, right)
        return node

    # and: expr1 && expr2
    def parse_and(self):
        node = self.parse_rel()
        while self.curr.kind == "OP" and self.curr.value == "&&":
            op = self.curr.value
            self._eat("OP")
            right = self.parse_rel()
            node = BinaryOp(op, node, right)
        return node

    # relacional: < <= > >= == !=
    def parse_rel(self):
        node = self.parse_add()
        while self.curr.kind == "OP" and self.curr.value in ("<", "<=", ">", ">=", "==", "!="):
            op = self.curr.value
            self._eat("OP")
            right = self.parse_add()
            node = BinaryOp(op, node, right)
        return node

    # suma/resta
    def parse_add(self):
        node = self.parse_mul()
        while self.curr.kind == "OP" and self.curr.value in ("+", "-"):
            op = self.curr.value
            self._eat("OP")
            right = self.parse_mul()
            node = BinaryOp(op, node, right)
        return node

    # multiplicacion/div
    def parse_mul(self):
        node = self.parse_unary()
        while self.curr.kind == "OP" and self.curr.value in ("*", "/"):
            op = self.curr.value
            self._eat("OP")
            right = self.parse_unary()
            node = BinaryOp(op, node, right)
        return node

    # unary !x o -x
    def parse_unary(self):
        if self.curr.kind == "OP" and self.curr.value in ("!", "-"):
            op = self.curr.value
            self._eat("OP")
            expr = self.parse_unary()
            return UnaryOp(op, expr)
        return self.parse_primary()

    # primarios numeros, bools, vars y expr
    def parse_primary(self):
        # ints
        if self.curr.kind == "INT":
            value = int(self.curr.value)
            self._eat("INT")
            return IntLiteral(value)

        # true/false
        if self.curr.kind == "KW" and self.curr.value in ("true", "false"):
            val = (self.curr.value == "true")
            self._eat("KW")
            return BoolLiteral(val)

        # var
        if self.curr.kind == "ID":
            name = self.curr.value
            self._eat("ID")
            return VarRef(name)

        # (expr)
        if self.curr.kind == "(":
            self._eat("(")
            node = self.parse_expr()
            self._eat(")")
            return node

        raise SyntaxError(f"Unexpected token in expression: {self.curr.kind} {self.curr.value}")
