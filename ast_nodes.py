# ast_nodes.py
from dataclasses import dataclass
from typing import List, Optional

# Program-level

@dataclass
class Program:
    statements: List["Stmt"]

# Statements

class Stmt:
    pass

@dataclass
class VarDecl(Stmt):
    var_type: str  # 'int' or 'bool'
    name: str

@dataclass
class Assign(Stmt):
    name: str
    expr: "Expr"

@dataclass
class IfStmt(Stmt):
    cond: "Expr"
    then_block: "Block"
    else_block: Optional["Block"]

@dataclass
class WhileStmt(Stmt):
    cond: "Expr"
    body: "Block"

@dataclass
class PrintStmt(Stmt):
    expr: "Expr"

@dataclass
class Block(Stmt):
    statements: List[Stmt]

# Expressions

class Expr:
    inferred_type: Optional[str] = None  # 'int' or 'bool'

@dataclass
class IntLiteral(Expr):
    value: int

@dataclass
class BoolLiteral(Expr):
    value: bool

@dataclass
class VarRef(Expr):
    name: str

@dataclass
class BinaryOp(Expr):
    op: str
    left: Expr
    right: Expr

@dataclass
class UnaryOp(Expr):
    op: str
    expr: Expr
