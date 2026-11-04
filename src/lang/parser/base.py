from lang.ast import Program
from lang.errors import SyntacticError
from lang.tokens import (
    Delimiter,
    Keyword,
    Operator,
    Span,
    Token,
    TokenDelimiter,
    TokenEOF,
    TokenIdentifier,
    TokenKeyword,
    TokenOperator,
)


class ParserBase:
    def __init__(self, tokens: list[Token]):
        self.tokens: list[Token] = tokens
        self.pos: int = 0

    def current(self) -> Token:
        return self.tokens[self.pos]

    def peek(self, offset: int = 1) -> Token | None:
        posicao = self.pos + offset
        if posicao < len(self.tokens):
            return self.tokens[posicao]
        return None

    def advance(self) -> Token:
        token = self.current()
        if type(token) is not TokenEOF:
            self.pos += 1
        return token

    def is_at_end(self) -> bool:
        return type(self.current()) is TokenEOF

    def error(self, msg: str, span: Span | None = None) -> SyntacticError:
        if span is None:
            span = self.current().span

        return SyntacticError(msg, span.line, span.col)

    # Métodos utilitários de checagem e consumo com enums
    def check_keyword(self, kind: Keyword) -> bool:
        match self.current():
            case TokenKeyword(k):
                return k == kind
            case _:
                return False

    def match_keyword(self, kind: Keyword) -> bool:
        if self.check_keyword(kind):
            self.advance()
            return True
        return False

    def expect_keyword(self, kind: Keyword, msg: str) -> TokenKeyword:
        if self.check_keyword(kind):
            return self.advance()  # type: ignore
        raise self.error(msg)

    def check_delimiter(self, kind: Delimiter) -> bool:
        match self.current():
            case TokenDelimiter(k):
                return k == kind
            case _:
                return False

    def match_delimiter(self, kind: Delimiter) -> bool:
        if self.check_delimiter(kind):
            self.advance()
            return True
        return False

    def expect_delimiter(self, kind: Delimiter, msg: str) -> TokenDelimiter:
        if self.check_delimiter(kind):
            return self.advance()  # type: ignore
        raise self.error(msg)

    def check_operator(self, kind: Operator) -> bool:
        match self.current():
            case TokenOperator(k):
                return k == kind
            case _:
                return False

    def match_operator(self, kind: Operator) -> bool:
        if self.check_operator(kind):
            self.advance()
            return True
        return False

    def expect_operator(self, kind: Operator, msg: str) -> TokenOperator:
        if self.check_operator(kind):
            return self.advance()  # type: ignore
        raise self.error(msg)

    def expect_identifier(self, msg: str) -> TokenIdentifier:
        tk = self.current()
        if type(tk) is TokenIdentifier:
            return self.advance()  # type: ignore
        raise self.error(msg)

    # Recuperação de erro em modo pânico
    def synchronize(self) -> None:
        self.advance()
        while not self.is_at_end():
            match self.current():
                case TokenDelimiter(Delimiter.SEMICOLON, _):
                    self.advance()
                    break
                case (
                    TokenKeyword(Keyword.FUNCTION, _)
                    | TokenKeyword(Keyword.VAR, _)
                    | TokenKeyword(Keyword.IF, _)
                    | TokenKeyword(Keyword.LOOP, _)
                    | TokenKeyword(Keyword.RETURN, _)
                ):
                    break
                case _:
                    self.advance()

    # Ponto de entrada
    def parse(self) -> Program: ...
