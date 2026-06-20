from typing import List, Optional
from src.token import Token, TokenType
from src.cst_nodes import ParseNode

class ParserError(Exception):
    def __init__(self, message: str, token: Token):
        super().__init__(f"ParserError dina baris {token.line}, kolom {token.column}: {message} (meunang '{token.value}')")

class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0

    def current_token(self) -> Token:
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return self.tokens[-1]

    def consume(self, expected_type: TokenType = None, expected_value: str = None) -> Token:
        token = self.current_token()
        if expected_type and token.type != expected_type:
            raise ParserError(f"Diperkirakeun {expected_type.name}", token)
        if expected_value and token.value != expected_value:
            raise ParserError(f"Diperkirakeun '{expected_value}'", token)
        self.pos += 1
        return token

    def peek(self) -> Token:
        if self.pos + 1 < len(self.tokens):
            return self.tokens[self.pos + 1]
        return self.tokens[-1]

    def parse_program(self) -> ParseNode:
        node = ParseNode("program")
        while self.current_token().type != TokenType.EOF:
            node.children.append(self.parse_statement())
        return node

    def parse_statement(self) -> ParseNode:
        token = self.current_token()
        if token.type == TokenType.IDENTIFIER:
            next_token = self.peek()
            if next_token.type == TokenType.OPERATOR and next_token.value == '=':
                return self.parse_assignment_stmt()
            elif next_token.type == TokenType.LPAREN:
                return self.parse_function_call_stmt()
            else:
                return self.parse_expression_stmt()
        elif token.type == TokenType.KEYWORD:
            val = token.value
            if val == 'lamun': return self.parse_if_stmt()
            elif val == 'salila': return self.parse_while_stmt()
            elif val == 'kanggo': return self.parse_for_stmt()
            elif val == 'jieun': return self.parse_function_def_stmt()
            elif val == 'balikeun': return self.parse_return_stmt()
            elif val == 'kelas': return self.parse_class_def_stmt()
            elif val == 'cobaan': return self.parse_try_stmt()
            elif val == 'mawa': return self.parse_import_stmt()
            elif val == 'ti': return self.parse_from_import_stmt()
            elif val == 'babarengan': return self.parse_async_stmt()
            elif val == 'cocogkeun': return self.parse_match_stmt()
            elif val in ['eureun', 'terus_weh', 'lewat']: return self.parse_simple_ctrl_stmt(val)
            elif val in ['lemparkeun', 'pastikeun', 'hapus', 'kabeh', 'lain_lokal', 'hasilkeun']: return self.parse_unary_ctrl_stmt(val)
            elif val == 'jeng': return self.parse_with_stmt()
        elif token.type == TokenType.BUILTIN:
            if self.peek().type == TokenType.LPAREN:
                return self.parse_function_call_stmt()

        return self.parse_expression_stmt()

    def parse_assignment_stmt(self) -> ParseNode:
        node = ParseNode("assignment_stmt")
        node.children.append(self.consume(TokenType.IDENTIFIER))
        node.children.append(self.consume(TokenType.OPERATOR, "="))
        node.children.append(self.parse_expression())
        return node

    def parse_if_stmt(self) -> ParseNode:
        node = ParseNode("if_stmt")
        node.children.append(self.consume(TokenType.KEYWORD, "lamun"))
        node.children.append(self.consume(TokenType.LPAREN))
        node.children.append(self.parse_expression())
        node.children.append(self.consume(TokenType.RPAREN))
        self._parse_block(node)
        while self.current_token().value == 'lamun_deui':
            node.children.append(self.consume(TokenType.KEYWORD, "lamun_deui"))
            node.children.append(self.consume(TokenType.LPAREN))
            node.children.append(self.parse_expression())
            node.children.append(self.consume(TokenType.RPAREN))
            self._parse_block(node)
        if self.current_token().value == 'sanesna':
            node.children.append(self.consume(TokenType.KEYWORD, "sanesna"))
            self._parse_block(node)
        return node

    def parse_while_stmt(self) -> ParseNode:
        node = ParseNode("while_stmt")
        node.children.append(self.consume(TokenType.KEYWORD, "salila"))
        node.children.append(self.consume(TokenType.LPAREN))
        node.children.append(self.parse_expression())
        node.children.append(self.consume(TokenType.RPAREN))
        self._parse_block(node)
        return node
        
    def parse_for_stmt(self) -> ParseNode:
        node = ParseNode("for_stmt")
        node.children.append(self.consume(TokenType.KEYWORD, "kanggo"))
        node.children.append(self.consume(TokenType.LPAREN))
        node.children.append(self.consume(TokenType.IDENTIFIER))
        node.children.append(self.consume(TokenType.KEYWORD, "dina"))
        node.children.append(self.parse_expression())
        node.children.append(self.consume(TokenType.RPAREN))
        self._parse_block(node)
        return node

    def parse_function_def_stmt(self) -> ParseNode:
        node = ParseNode("function_def_stmt")
        node.children.append(self.consume(TokenType.KEYWORD, "jieun"))
        node.children.append(self.consume(TokenType.IDENTIFIER))
        node.children.append(self.consume(TokenType.LPAREN))
        node.children.append(self._parse_params())
        node.children.append(self.consume(TokenType.RPAREN))
        self._parse_block(node)
        return node

    def parse_class_def_stmt(self) -> ParseNode:
        node = ParseNode("class_def_stmt")
        node.children.append(self.consume(TokenType.KEYWORD, "kelas"))
        node.children.append(self.consume(TokenType.IDENTIFIER))
        if self.current_token().type == TokenType.LPAREN:
            node.children.append(self.consume(TokenType.LPAREN))
            node.children.append(self.consume(TokenType.IDENTIFIER))
            node.children.append(self.consume(TokenType.RPAREN))
        self._parse_block(node)
        return node

    def parse_try_stmt(self) -> ParseNode:
        node = ParseNode("try_stmt")
        node.children.append(self.consume(TokenType.KEYWORD, "cobaan"))
        self._parse_block(node)
        while self.current_token().value == 'kacuali':
            node.children.append(self.consume(TokenType.KEYWORD, "kacuali"))
            if self.current_token().type == TokenType.IDENTIFIER:
                node.children.append(self.consume(TokenType.IDENTIFIER))
                if self.current_token().value == 'minangka':
                    node.children.append(self.consume(TokenType.KEYWORD, "minangka"))
                    node.children.append(self.consume(TokenType.IDENTIFIER))
            self._parse_block(node)
        if self.current_token().value == 'ahirna':
            node.children.append(self.consume(TokenType.KEYWORD, "ahirna"))
            self._parse_block(node)
        return node

    def parse_import_stmt(self) -> ParseNode:
        node = ParseNode("import_stmt")
        node.children.append(self.consume(TokenType.KEYWORD, "mawa"))
        node.children.append(self.consume(TokenType.IDENTIFIER))
        if self.current_token().value == 'minangka':
            node.children.append(self.consume(TokenType.KEYWORD, "minangka"))
            node.children.append(self.consume(TokenType.IDENTIFIER))
        return node
        
    def parse_from_import_stmt(self) -> ParseNode:
        node = ParseNode("from_import_stmt")
        node.children.append(self.consume(TokenType.KEYWORD, "ti"))
        node.children.append(self.consume(TokenType.IDENTIFIER))
        node.children.append(self.consume(TokenType.KEYWORD, "mawa"))
        node.children.append(self.consume(TokenType.IDENTIFIER))
        return node

    def parse_with_stmt(self) -> ParseNode:
        node = ParseNode("with_stmt")
        node.children.append(self.consume(TokenType.KEYWORD, "jeng"))
        node.children.append(self.parse_expression())
        if self.current_token().value == 'minangka':
            node.children.append(self.consume(TokenType.KEYWORD, "minangka"))
            node.children.append(self.consume(TokenType.IDENTIFIER))
        self._parse_block(node)
        return node

    def parse_async_stmt(self) -> ParseNode:
        node = ParseNode("async_stmt")
        node.children.append(self.consume(TokenType.KEYWORD, "babarengan"))
        if self.current_token().value == 'jieun':
            node.children.append(self.parse_function_def_stmt())
        elif self.current_token().value == 'kanggo':
            node.children.append(self.parse_for_stmt())
        elif self.current_token().value == 'jeng':
            node.children.append(self.parse_with_stmt())
        else:
            raise ParserError("Diperkirakeun 'jieun', 'kanggo', atawa 'jeng' sanggeus 'babarengan'", self.current_token())
        return node

    def parse_match_stmt(self) -> ParseNode:
        node = ParseNode("match_stmt")
        node.children.append(self.consume(TokenType.KEYWORD, "cocogkeun"))
        node.children.append(self.parse_expression())
        node.children.append(self.consume(TokenType.LBRACE))
        while self.current_token().value == 'kasus':
            node.children.append(self.consume(TokenType.KEYWORD, "kasus"))
            node.children.append(self.parse_expression())
            self._parse_block(node)
        node.children.append(self.consume(TokenType.RBRACE))
        return node

    def parse_simple_ctrl_stmt(self, kw: str) -> ParseNode:
        node = ParseNode(f"{kw}_stmt")
        node.children.append(self.consume(TokenType.KEYWORD, kw))
        return node

    def parse_unary_ctrl_stmt(self, kw: str) -> ParseNode:
        node = ParseNode(f"{kw}_stmt")
        node.children.append(self.consume(TokenType.KEYWORD, kw))
        node.children.append(self.parse_expression())
        return node

    def _parse_block(self, parent_node: ParseNode):
        parent_node.children.append(self.consume(TokenType.LBRACE))
        while self.current_token().type != TokenType.RBRACE and self.current_token().type != TokenType.EOF:
            parent_node.children.append(self.parse_statement())
        parent_node.children.append(self.consume(TokenType.RBRACE))

    def _parse_params(self) -> ParseNode:
        params_node = ParseNode("parameters")
        if self.current_token().type != TokenType.RPAREN:
            tok = self.current_token()
            if tok.type == TokenType.IDENTIFIER or (tok.type == TokenType.KEYWORD and tok.value == 'urang'):
                params_node.children.append(self.consume(tok.type))
            else:
                raise ParserError("Diperkirakeun parameter", tok)
                
            while self.current_token().type == TokenType.COMMA:
                params_node.children.append(self.consume(TokenType.COMMA))
                tok = self.current_token()
                if tok.type == TokenType.IDENTIFIER or (tok.type == TokenType.KEYWORD and tok.value == 'urang'):
                    params_node.children.append(self.consume(tok.type))
                else:
                    raise ParserError("Diperkirakeun parameter", tok)
        return params_node

    def parse_function_call_stmt(self) -> ParseNode:
        node = ParseNode("function_call_stmt")
        token = self.current_token()
        if token.type == TokenType.BUILTIN: node.children.append(self.consume(TokenType.BUILTIN))
        else: node.children.append(self.consume(TokenType.IDENTIFIER))
        node.children.append(self.consume(TokenType.LPAREN))
        
        args_node = ParseNode("arguments")
        if self.current_token().type != TokenType.RPAREN:
            args_node.children.append(self.parse_expression())
            while self.current_token().type == TokenType.COMMA:
                args_node.children.append(self.consume(TokenType.COMMA))
                args_node.children.append(self.parse_expression())
        node.children.append(args_node)
        node.children.append(self.consume(TokenType.RPAREN))
        return node
        
    def parse_return_stmt(self) -> ParseNode:
        node = ParseNode("return_stmt")
        node.children.append(self.consume(TokenType.KEYWORD, "balikeun"))
        if self.current_token().type != TokenType.RBRACE:
            node.children.append(self.parse_expression())
        return node

    def parse_expression_stmt(self) -> ParseNode:
        node = ParseNode("expression_stmt")
        node.children.append(self.parse_expression())
        return node

    def parse_expression(self) -> ParseNode:
        return self.parse_logical()

    def parse_logical(self) -> ParseNode:
        node = self.parse_equality()
        while self.current_token().type == TokenType.KEYWORD and self.current_token().value in ['jeung', 'atawa']:
            parent = ParseNode("logical_expression")
            parent.children.append(node)
            parent.children.append(self.consume(TokenType.KEYWORD))
            parent.children.append(self.parse_equality())
            node = parent
        return node

    def parse_equality(self) -> ParseNode:
        node = self.parse_comparison()
        while self.current_token().type == TokenType.OPERATOR and self.current_token().value in ['==', '!='] or (self.current_token().type == TokenType.KEYWORD and self.current_token().value == 'nyaeta'):
            parent = ParseNode("equality_expression")
            parent.children.append(node)
            if self.current_token().type == TokenType.KEYWORD:
                parent.children.append(self.consume(TokenType.KEYWORD))
            else:
                parent.children.append(self.consume(TokenType.OPERATOR))
            parent.children.append(self.parse_comparison())
            node = parent
        return node

    def parse_comparison(self) -> ParseNode:
        node = self.parse_term()
        while self.current_token().type == TokenType.OPERATOR and self.current_token().value in ['<', '<=', '>', '>=']:
            parent = ParseNode("comparison_expression")
            parent.children.append(node)
            parent.children.append(self.consume(TokenType.OPERATOR))
            parent.children.append(self.parse_term())
            node = parent
        return node

    def parse_term(self) -> ParseNode:
        node = self.parse_factor()
        while self.current_token().type == TokenType.OPERATOR and self.current_token().value in ['+', '-']:
            parent = ParseNode("term_expression")
            parent.children.append(node)
            parent.children.append(self.consume(TokenType.OPERATOR))
            parent.children.append(self.parse_factor())
            node = parent
        return node

    def parse_factor(self) -> ParseNode:
        node = self.parse_unary()
        while self.current_token().type == TokenType.OPERATOR and self.current_token().value in ['*', '/']:
            parent = ParseNode("factor_expression")
            parent.children.append(node)
            parent.children.append(self.consume(TokenType.OPERATOR))
            parent.children.append(self.parse_unary())
            node = parent
        return node
        
    def parse_unary(self) -> ParseNode:
        if self.current_token().value == 'lain':
            node = ParseNode("unary_expression")
            node.children.append(self.consume(TokenType.KEYWORD, 'lain'))
            node.children.append(self.parse_unary())
            return node
        if self.current_token().type == TokenType.OPERATOR and self.current_token().value in ['-', '+']:
            node = ParseNode("unary_expression")
            node.children.append(self.consume(TokenType.OPERATOR))
            node.children.append(self.parse_unary())
            return node
        if self.current_token().value == 'tangguan':
            node = ParseNode("await_expression")
            node.children.append(self.consume(TokenType.KEYWORD, 'tangguan'))
            node.children.append(self.parse_unary())
            return node
        if self.current_token().value == 'fungsi_leutik':
            node = ParseNode("lambda_expression")
            node.children.append(self.consume(TokenType.KEYWORD, 'fungsi_leutik'))
            node.children.append(self._parse_params())
            node.children.append(self.consume(TokenType.LBRACE))
            node.children.append(self.parse_expression())
            node.children.append(self.consume(TokenType.RBRACE))
            return node
        return self.parse_primary()

    def parse_primary(self) -> ParseNode:
        token = self.current_token()
        if token.type == TokenType.NUMBER:
            node = ParseNode("primary")
            node.children.append(self.consume(TokenType.NUMBER))
            return node
        elif token.type == TokenType.STRING:
            node = ParseNode("primary")
            node.children.append(self.consume(TokenType.STRING))
            return node
        elif token.type == TokenType.IDENTIFIER:
            if self.peek().type == TokenType.LPAREN:
                return self.parse_function_call_stmt()
            node = ParseNode("primary")
            node.children.append(self.consume(TokenType.IDENTIFIER))
            return node
        elif token.type == TokenType.BUILTIN:
            if self.peek().type == TokenType.LPAREN:
                return self.parse_function_call_stmt()
            # If not followed by LPAREN, maybe just referencing it
            node = ParseNode("primary")
            node.children.append(self.consume(TokenType.BUILTIN))
            return node
        elif token.type == TokenType.KEYWORD and token.value in ['Bener', 'Bohong', 'Euweuh', 'urang', 'kolot']:
            node = ParseNode("primary")
            node.children.append(self.consume(TokenType.KEYWORD))
            return node
        elif token.type == TokenType.LPAREN:
            node = ParseNode("grouping")
            node.children.append(self.consume(TokenType.LPAREN))
            node.children.append(self.parse_expression())
            node.children.append(self.consume(TokenType.RPAREN))
            return node
            
        raise ParserError("Ekspresi henteu kaduga", token)
