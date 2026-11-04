from dataclasses import dataclass

from lang.tokens import Keyword, Operator, Span


# Membro 1: Base
@dataclass(frozen=True, slots=True)
class ASTNode:
    span: Span


@dataclass(frozen=True, slots=True)
class Program(ASTNode):
    functions: list[FunctionDecl]


# Membro 2: Expressões
type Expr = (
    BinaryExpr | UnaryExpr | LiteralExpr | VariableExpr | ArrayLiteralExpr | CallExpr
)


@dataclass(frozen=True, slots=True)
class BinaryExpr(ASTNode):
    left: Expr
    operator: Operator
    right: Expr


@dataclass(frozen=True, slots=True)
class UnaryExpr(ASTNode):
    operator: Operator
    operand: Expr


@dataclass(frozen=True, slots=True)
class LiteralExpr(ASTNode):
    value: int | float | str | bool


@dataclass(frozen=True, slots=True)
class VariableExpr(ASTNode):
    id: int


@dataclass(frozen=True, slots=True)
class ArrayLiteralExpr(ASTNode):
    elements: list[Expr]


# Membro 3: Tipos e Declarações
@dataclass(frozen=True, slots=True)
class TypeNode(ASTNode):
    base: Keyword
    is_array: bool
    is_ref: bool


@dataclass(frozen=True, slots=True)
class VarDeclStmt(ASTNode):
    name_id: int
    type_node: TypeNode
    initializer: Expr


@dataclass(frozen=True, slots=True)
class AssignStmt(ASTNode):
    target_id: int
    value: Expr


@dataclass(frozen=True, slots=True)
class DerefAssignStmt(ASTNode):
    target_id: int
    value: Expr


# Membro 4: Controle de Fluxo
@dataclass(frozen=True, slots=True)
class BlockStmt(ASTNode):
    statements: list[ASTNode]


@dataclass(frozen=True, slots=True)
class IfStmt(ASTNode):
    condition: Expr
    then_branch: BlockStmt
    else_branch: BlockStmt | IfStmt | None


@dataclass(frozen=True, slots=True)
class LoopInfiniteStmt(ASTNode):
    body: BlockStmt


@dataclass(frozen=True, slots=True)
class LoopRangeStmt(ASTNode):
    iterator_id: int
    start: Expr
    end: Expr
    body: BlockStmt


@dataclass(frozen=True, slots=True)
class LoopIteratorStmt(ASTNode):
    iterator_id: int
    collection: Expr
    body: BlockStmt


# Membro 5: Funções e Chamadas
@dataclass(frozen=True, slots=True)
class Param(ASTNode):
    name_id: int
    type_node: TypeNode


@dataclass(frozen=True, slots=True)
class FunctionDecl(ASTNode):
    name_id: int
    params: list[Param]
    return_type: TypeNode | None
    body: BlockStmt


@dataclass(frozen=True, slots=True)
class ReturnStmt(ASTNode):
    value: Expr | None


@dataclass(frozen=True, slots=True)
class CallExpr(ASTNode):
    callee_id: int
    arguments: list[Expr]
