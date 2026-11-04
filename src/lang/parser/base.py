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


class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens: list[Token] = tokens
        self.pos: int = 0

    def current(self) -> Token:
        """Retorna o token atual sem consumi-lo."""
        return self.tokens[self.pos]

    def peek(self, n: int = 1) -> Token | None:
        """Retorna o token 'n' posições à frente, sem avançar. Retorna None se ultrapassar os tokens."""
        posicao = self.pos + n
        if posicao < len(self.tokens):
            return self.tokens[posicao]
        return None

    def advance(self) -> Token:
        """Consome e retorna o token atual, avançando em uma posição (exceto se for EOF)."""
        token = self.current()
        if type(token) is not TokenEOF:
            self.pos += 1
        return token

    def is_at_end(self) -> bool:
        """Verifica se o token atual é o final do arquivo."""
        return type(self.current()) is TokenEOF

    def error(self, msg: str, span: Span | None = None) -> SyntacticError:
        """Cria e retorna uma exceção SyntacticError com a mensagem e as coordenadas (linha e coluna) do token."""
        if span is None:
            span = self.current().span

        return SyntacticError(msg, span.line, span.col)

    # Métodos utilitários de checagem e consumo
    # check: apenas inspeciona o token atual sem avançar
    # match: consome se for o token esperado (para regras opcionais)
    # expect: consome se for o token esperado ou lança erro sintático (para regras obrigatórias)

    def check_keyword(self, kind: Keyword) -> bool:
        """Retorna True se o token atual for uma palavra-chave do tipo especificado, sem avançar."""
        match self.current():
            case TokenKeyword(k):
                return k == kind
            case _:
                return False

    def match_keyword(self, kind: Keyword) -> bool:
        """
        Se o token atual for a palavra-chave especificada, consome-o e retorna True, avançando para o próximo token.
        Caso contrário, retorna False.
        """
        if self.check_keyword(kind):
            self.advance()
            return True
        return False

    def expect_keyword(self, kind: Keyword, msg: str) -> TokenKeyword:
        """
        Se o token atual for a palavra-chave especificada, consome-o e retorna o valor do token, avançando para o próximo token.
        Caso contrário, dispara um erro sintático.
        """
        if self.check_keyword(kind):
            return self.advance()  # type: ignore
        raise self.error(msg)

    def check_delimiter(self, kind: Delimiter) -> bool:
        """Retorna True se o token atual for um delimitador do tipo especificado, sem avançar."""
        match self.current():
            case TokenDelimiter(k):
                return k == kind
            case _:
                return False

    def match_delimiter(self, kind: Delimiter) -> bool:
        """
        Se o token atual for o delimitador especificado, consome-o e retorna True, avançando para o próximo token.
        Caso contrário, retorna False.
        """
        if self.check_delimiter(kind):
            self.advance()
            return True
        return False

    def expect_delimiter(self, kind: Delimiter, msg: str) -> TokenDelimiter:
        """
        Se o token atual for o delimitador especificada, consome-o e retorna o valor do token, avançando para o próximo token.
        Caso contrário, dispara um erro sintático.
        """
        if self.check_delimiter(kind):
            return self.advance()  # type: ignore
        raise self.error(msg)

    def check_operator(self, kind: Operator) -> bool:
        """Retorna True se o token atual for um operador do tipo especificado, sem avançar."""
        match self.current():
            case TokenOperator(k):
                return k == kind
            case _:
                return False

    def match_operator(self, kind: Operator) -> bool:
        """
        Se o token atual for o operador especificado, consome-o e retorna True, avançando para o próximo token.
        Caso contrário, retorna False.
        """
        if self.check_operator(kind):
            self.advance()
            return True
        return False

    def expect_operator(self, kind: Operator, msg: str) -> TokenOperator:
        """
        Se o token atual for o operador especificado (ex: '=', '+'), consome-o e retorna o valor do token, avançando para o próximo token.
        Dispara erro sintático se não coincidir.
        """
        if self.check_operator(kind):
            return self.advance()  # type: ignore
        raise self.error(msg)

    def expect_identifier(self, msg: str) -> TokenIdentifier:
        """
        Se o token atual for um identificador (nome de variável, função, etc.) consome-o e retorna o valor do token, avançando para o próximo token.
        Dispara erro sintático se for outro token.
        """
        tk = self.current()
        if type(tk) is TokenIdentifier:
            return self.advance()  # type: ignore
        raise self.error(msg)

    def synchronize(self) -> None:
        """
        Descarta tokens até encontrar um token para recomeçar a análise (útil para continuar a análise mesmo depois de encontrar um erro,
        assim podemos mostrar vários erros de uma vez).
        """
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

    def parse(self) -> Program:
        """Executa a análise sintática completa do arquivo e retorna o nó raiz da AST (Program)."""
        ...
