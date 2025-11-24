# codegen.py
from typing import List, Dict, Tuple
from ast_nodes import *

class TACGenerator:
    def __init__(self):
        self.temp_count = 0
        self.label_count = 0
        self.instructions: List[str] = []
        self.var_storage: Dict[str, str] = {}  # name -> storage name (for VM)

    def new_temp(self) -> str:
        self.temp_count += 1
        return f"t{self.temp_count}"

    def new_label(self) -> str:
        self.label_count += 1
        return f"L{self.label_count}"

    def emit(self, instr: str):
        self.instructions.append(instr)

    def generate(self, program: Program) -> List[str]:
        # assign storage names (here just same as identifier)
        for stmt in program.statements:
            if isinstance(stmt, VarDecl):
                if stmt.name not in self.var_storage:
                    self.var_storage[stmt.name] = stmt.name

        for stmt in program.statements:
            self.gen_stmt(stmt)
        return self.instructions

    def gen_stmt(self, stmt: Stmt):
        if isinstance(stmt, VarDecl):
            # No direct TAC needed for pure declaration
            pass

        elif isinstance(stmt, Assign):
            src = self.gen_expr(stmt.expr)
            dest = self.var_storage[stmt.name]
            self.emit(f"{dest} := {src}")

        elif isinstance(stmt, PrintStmt):
            val = self.gen_expr(stmt.expr)
            self.emit(f"print {val}")

        elif isinstance(stmt, IfStmt):
            cond_val = self.gen_expr(stmt.cond)
            then_label = self.new_label()
            else_label = self.new_label() if stmt.else_block else None
            end_label = self.new_label()

            # if false goto else or end
            if stmt.else_block:
                # we implement: if cond goto then_label else goto else_label
                self.emit(f"if {cond_val} == 0 goto {else_label}")
                # then block
                self.emit(f"{then_label}:")
                self.gen_block(stmt.then_block)
                self.emit(f"goto {end_label}")
                # else block
                self.emit(f"{else_label}:")
                self.gen_block(stmt.else_block)
                self.emit(f"{end_label}:")
            else:
                self.emit(f"if {cond_val} == 0 goto {end_label}")
                self.gen_block(stmt.then_block)
                self.emit(f"{end_label}:")

        elif isinstance(stmt, WhileStmt):
            start_label = self.new_label()
            cond_label = self.new_label()
            end_label = self.new_label()

            self.emit(f"{start_label}:")
            # evaluate condition
            cond_val = self.gen_expr(stmt.cond)
            self.emit(f"if {cond_val} == 0 goto {end_label}")
            # body
            self.gen_block(stmt.body)
            self.emit(f"goto {start_label}")
            self.emit(f"{end_label}:")

        elif isinstance(stmt, Block):
            self.gen_block(stmt)
        else:
            raise RuntimeError(f"Unknown statement in codegen: {type(stmt)}")

    def gen_block(self, block: Block):
        for s in block.statements:
            self.gen_stmt(s)

    def gen_expr(self, expr: Expr) -> str:
        if isinstance(expr, IntLiteral):
            return str(expr.value)
        if isinstance(expr, BoolLiteral):
            return "1" if expr.value else "0"
        if isinstance(expr, VarRef):
            return self.var_storage[expr.name]
        if isinstance(expr, UnaryOp):
            v = self.gen_expr(expr.expr)
            tmp = self.new_temp()
            if expr.op == "-":
                self.emit(f"{tmp} := 0 - {v}")
            elif expr.op == "!":
                # !b => (b == 0) ? 1 : 0  (implement as 1 - (b != 0))
                t1 = self.new_temp()
                self.emit(f"{t1} := {v} != 0")
                self.emit(f"{tmp} := 1 - {t1}")
            else:
                raise RuntimeError(f"Unknown unary op {expr.op}")
            return tmp
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
                # simple version: evaluate both and use operators as ints (0/1)
                if op == "&&":
                    self.emit(f"{tmp} := ({left} != 0) && ({right} != 0)")
                else:
                    self.emit(f"{tmp} := ({left} != 0) || ({right} != 0)")
            else:
                raise RuntimeError(f"Unknown binary op {op}")
            return tmp
        raise RuntimeError(f"Unknown expr in codegen: {type(expr)}")
