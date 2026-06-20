import unittest
from src.lexer import Lexer
from src.parser import Parser
from src.ast_builder import ASTBuilder
from src.ast_nodes import *

class TestAST(unittest.TestCase):
    def _build_ast(self, source: str) -> ASTNode:
        lexer = Lexer(source)
        parser = Parser(lexer.tokenize())
        cst = parser.parse_program()
        builder = ASTBuilder()
        return builder.build(cst)

    def test_assignment_ast(self):
        ast = self._build_ast('x = 5')
        self.assertIsInstance(ast, Program)
        self.assertEqual(len(ast.statements), 1)
        stmt = ast.statements[0]
        self.assertIsInstance(stmt, Assignment)
        self.assertEqual(stmt.target.name, 'x')
        self.assertIsInstance(stmt.value, Literal)
        self.assertEqual(stmt.value.value, 5)

    def test_binary_op_ast(self):
        ast = self._build_ast('x = 2 + 3')
        stmt = ast.statements[0]
        self.assertIsInstance(stmt.value, BinaryOp)
        self.assertEqual(stmt.value.operator, '+')

    def test_if_stmt_ast(self):
        source = '''
        lamun (x > 5) {
            nyarita("Gede")
        } sanesna {
            nyarita("Leutik")
        }
        '''
        ast = self._build_ast(source)
        stmt = ast.statements[0]
        self.assertIsInstance(stmt, IfStmt)
        self.assertIsNotNone(stmt.else_branch)

    def test_function_def_ast(self):
        source = '''
        jieun tambah(a, b) {
            balikeun a + b
        }
        '''
        ast = self._build_ast(source)
        stmt = ast.statements[0]
        self.assertIsInstance(stmt, FunctionDef)
        self.assertEqual(stmt.name.name, 'tambah')
        self.assertEqual(len(stmt.params), 2)

    def test_cst_vs_ast_comparison(self):
        """Double Validation: CST vs AST"""
        source = 'x = (2 + 3) * 5'
        lexer = Lexer(source)
        parser = Parser(lexer.tokenize())
        cst = parser.parse_program()
        
        builder = ASTBuilder()
        ast = builder.build(cst)
        
        print("\n--- CST (Mentah) ---")
        print(cst.print_tree())
        print("--- AST (Abstrak) ---")
        print(ast.print_ast())
        
        # CST has many more nodes (brackets, etc) than AST
        stmt = ast.statements[0]
        self.assertIsInstance(stmt, Assignment)

if __name__ == '__main__':
    unittest.main()
