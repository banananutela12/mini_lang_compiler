# codegen.py
# modulo que genera tac aqui se arman las instrucs finales
# esto lo usa el VM para correr el programa

from typing import List, Dict, Tuple
from src.ast_nodes import *


class TACGenerator:
    def __init__(self):
        self.temp_count = 0      # temps para exprs
        self.label_count = 0     # labels pa saltos
        self.instructions: List[str] = []
        self.var_storage: Dict[str, str] = {}  # var  nombre en la VM

    def new_temp(self) -> str:
        # genera un temp nuevo simple
        self.temp_count += 1
        return f"t{self.temp_count}"

    def new_label(self) -> str:
        # etiqueta nueva para if/while
        self.label_count += 1
        return f"L{self.label_count}"

    def emit(self, instr: str):
        # mete una instruccion tac4 a la lista
        self.instructions.append(instr)

    def generate(self, program: Program) -> List[str]:
        # asignar storage para cada var aqui solo el mismo nombre
        for stmt in program.statements:
            if isinstance(stmt, VarDecl):
                if stmt.name not in self.var_storage:
                    self.var_storage[stmt.name] = stmt.name

        # generar tac de cada stmt
        for stmt in program.statements:
            self.gen_stmt(stmt)
        return self.instructions

    def gen_stmt(self, stmt: Stmt):
        if isinstance(stmt, VarDecl):
            # declaracion sola no tira Tac
            pass

        elif isinstance(stmt, Assign):
            src = self.gen_expr(stmt.expr)
            dest = self.var_storage[stmt.name]
            self.emit(f"{dest} := {src}")

        elif isinstance(stmt, PrintStmt):
            # print  instruccion directa
            val = self.gen_expr(stmt.expr)
            self.emit(f"print {val}")

        elif isinstance(stmt, IfStmt):
            cond_val = self.gen_expr(stmt.cond)
            then_label = self.new_label()
            else_label = self.new_label() if stmt.else_block else None
            end_label = self.new_label()

            # if saltos simples
            if stmt.else_block:
                self.emit(f"if {cond_val} == 0 goto {else_label}")
                self.emit(f"{then_label}:")
                self.gen_block(stmt.then_block)
                self.emit(f"goto {end_label}")
                self.emit(f"{else_label}:")
                self.gen_block(stmt.else_block)
                self.emit(f"{end_label}:")
            else:
                self.emit(f"if {cond_val} == 0 goto {end_label}")
                self.gen_block(stmt.then_block)
                self.emit(f"{end_label}:")

        elif isinstance(stmt, WhileStmt):
            start_label = self.new_label()
            end_label = self.new_label()

            self.emit(f"{start_label}:")
            cond_val = self.gen_expr(stmt.cond)
            self.emit(f"if {cond_val} == 0 goto {end_label}")
            self.gen_block(stmt.body)
            self.emit(f"goto {start_label}")
            self.emit(f"{end_label}:")

        elif isinstance(stmt, Block):
            self.gen_block(stmt)
        else:
            raise RuntimeError(f"stmt raro en codegen: {type(stmt)}")

    def gen_block(self, block: Block):
        for s in block.statements:
            self.gen_stmt(s)

    def gen_expr(self, expr: Expr) -> str:
        # literales
        if isinstance(expr, IntLiteral):
            return str(expr.value)

        if isinstance(expr, BoolLiteral):
            return "1" if expr.value else "0"

        if isinstance(expr, VarRef):
            return self.var_storage[expr.name]

        # unary ops (! , -)
        if isinstance(expr, UnaryOp):
            v = self.gen_expr(expr.expr)
            tmp = self.new_temp()

            if expr.op == "-":
                self.emit(f"{tmp} := 0 - {v}")
            elif expr.op == "!":
                # negacion bool simple
                t1 = self.new_temp()
                self.emit(f"{t1} := {v} != 0")
                self.emit(f"{tmp} := 1 - {t1}")
            else:
                raise RuntimeError(f"op unaria no conocida: {expr.op}")

            return tmp

        # binary ops (+, <, &&, etc)
        if isinstance(expr, BinaryOp):
            left = self.gen_expr(expr.left)
            right = self.gen_expr(expr.right)
            tmp = self.new_temp()
            op = expr.op

            if op in ("+", "-", "*", "/"):
                self.emit(f"{tmp} := {left} {op} {right}")

            elif op in ("<", "<=", ">", ">=", "==", "!="):
                self.emit(f"{tmp} := {left} {op} {right}")

            elif op in ("&&", "||"):
                # basic impl: usar ints 0/1
                if op == "&&":
                    self.emit(f"{tmp} := ({left} != 0) && ({right} != 0)")
                else:
                    self.emit(f"{tmp} := ({left} != 0) || ({right} != 0)")

            else:
                raise RuntimeError(f"binary op no conocido: {op}")

            return tmp

        raise RuntimeError(f"expr rara en codegen: {type(expr)}")
