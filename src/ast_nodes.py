# ast_nodes.py
# nodos del astt arbol sintactico este modulo nada mas define
# las clases que usa el parser/semantica/codegen

from dataclasses import dataclass
from typing import List, Optional

#  Program-level

@dataclass
class Program:
    statements: List["Stmt"]   # lista de stmts del programa orden normal


#  Statements stmts 

class Stmt:
    pass   # solo es clase base, no hace nada


@dataclass
class VarDecl(Stmt):
    var_type: str   # int o bool
    name: str       # nombre de la var


@dataclass
class Assign(Stmt):
    name: str       # var destino
    expr: "Expr"    # expr a evaluar


@dataclass
class IfStmt(Stmt):
    cond: "Expr"        # condicion booleana
    then_block: "Block" # bloque si true
    else_block: Optional["Block"]  # else puede ser None


@dataclass
class WhileStmt(Stmt):
    cond: "Expr"     # condicion del loop
    body: "Block"    # stmts del cuerpo


@dataclass
class PrintStmt(Stmt):
    expr: "Expr"     # expr a imprimir


@dataclass
class Block(Stmt):
    statements: List[Stmt]   # un bloque solo es una lista de stmts


#  Expressions (exprs) 

class Expr:
    inferred_type: Optional[str] = None  # int o bool la semantica lo llena


@dataclass
class IntLiteral(Expr):
    value: int   # literal entero


@dataclass
class BoolLiteral(Expr):
    value: bool  # literal bool


@dataclass
class VarRef(Expr):
    name: str   # referencia a var


@dataclass
class BinaryOp(Expr):
    op: str      # '+', '-', '*', '/', '<', && etc
    left: Expr
    right: Expr  # expr derecha


@dataclass
class UnaryOp(Expr):
    op: str      # '!' o similar
    expr: Expr
