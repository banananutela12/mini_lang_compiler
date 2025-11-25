# semantics.py
# checador semántico: aqui revisamos tipos vars declaradas

from typing import Dict
from src.ast_nodes import *

class SemanticError(Exception):
    pass

class SemanticAnalyzer:
    def __init__(self):
        self.env: Dict[str, str] = {}  # name -> 'int' or 'bool'

    def analyze(self, program: Program):
        for stmt in program.statements:
            self.check_stmt(stmt)

    def check_stmt(self, stmt: Stmt):
        # declaración: int x;  bool ok;
        if isinstance(stmt, VarDecl):
            if stmt.name in self.env:
                raise SemanticError(f"Variable '{stmt.name}' already declared")
            if stmt.var_type not in ("int", "bool"):
                raise SemanticError(f"Unknown type '{stmt.var_type}'")
            self.env[stmt.name] = stmt.var_type  # guardar tipo

        elif isinstance(stmt, Assign):
            if stmt.name not in self.env:
                raise SemanticError(f"Undeclared variable '{stmt.name}'")
            t_expr = self.check_expr(stmt.expr)
            t_var = self.env[stmt.name]
            if t_expr != t_var:
                raise SemanticError(
                    f"Type mismatch in assignment to '{stmt.name}': {t_var} = {t_expr}"
                )

        elif isinstance(stmt, IfStmt):
            t_cond = self.check_expr(stmt.cond)
            if t_cond != "bool":
                raise SemanticError("Condition in if must be bool")
            self.check_block(stmt.then_block)
            if stmt.else_block:
                self.check_block(stmt.else_block)

        elif isinstance(stmt, WhileStmt):
            t_cond = self.check_expr(stmt.cond)
            if t_cond != "bool":
                raise SemanticError("Condition in while must be bool")
            self.check_block(stmt.body)

        elif isinstance(stmt, PrintStmt):
            _ = self.check_expr(stmt.expr)

        elif isinstance(stmt, Block):
            for s in stmt.statements:
                self.check_stmt(s)

        else:
            raise SemanticError(f"Unknown statement type: {type(stmt)}")

    def check_block(self, block: Block):
        for s in block.statements:
            self.check_stmt(s)

    def check_expr(self, expr: Expr) -> str:
        if isinstance(expr, IntLiteral):
            expr.inferred_type = "int"
            return "int"

        if isinstance(expr, BoolLiteral):
            expr.inferred_type = "bool"
            return "bool"

        if isinstance(expr, VarRef):
            if expr.name not in self.env:
                raise SemanticError(f"Undeclared variable '{expr.name}'")
            expr.inferred_type = self.env[expr.name]
            return expr.inferred_type

        if isinstance(expr, UnaryOp):
            t_sub = self.check_expr(expr.expr)
            if expr.op == "-":
                if t_sub != "int":
                    raise SemanticError("Unary - expects int")
                expr.inferred_type = "int"
            elif expr.op == "!":
                if t_sub != "bool":
                    raise SemanticError("Unary ! expects bool")
                expr.inferred_type = "bool"
            else:
                raise SemanticError(f"Unknown unary operator {expr.op}")
            return expr.inferred_type

        if isinstance(expr, BinaryOp):
            t_left = self.check_expr(expr.left)
            t_right = self.check_expr(expr.right)
            op = expr.op

            if op in ("+", "-", "*", "/"):
                if t_left != "int" or t_right != "int":
                    raise SemanticError("Arithmetic operators expect int operands")
                expr.inferred_type = "int"

            elif op in ("<", "<=", ">", ">=", "==", "!="):
                if t_left != t_right:
                    raise SemanticError("Comparison operands must have same type")
                expr.inferred_type = "bool"

            elif op in ("&&", "||"):
                if t_left != "bool" or t_right != "bool":
                    raise SemanticError("Logical operators expect bool operands")
                expr.inferred_type = "bool"

            else:
                raise SemanticError(f"Unknown binary operator {op}")

            return expr.inferred_type

        raise SemanticError(f"Unknown expression type: {type(expr)}")
