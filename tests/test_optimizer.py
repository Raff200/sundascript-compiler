import unittest
from src.lexer import Lexer
from src.parser import Parser
from src.ast_builder import ASTBuilder
from src.optimizer import ASTOptimizer
from src.ast_nodes import *

class TestOptimizer(unittest.TestCase):
    def _optimize(self, source: str) -> ASTNode:
        lexer = Lexer(source)
        parser = Parser(lexer.tokenize())
        cst = parser.parse_program()
        builder = ASTBuilder()
        ast = builder.build(cst)
        optimizer = ASTOptimizer()
        return optimizer.optimize(ast)

    def test_constant_folding_addition(self):
        """5 + 3 harus jadi 8 pas compile time"""
        ast = self._optimize('x = 5 + 3')
        stmt = ast.statements[0]
        self.assertIsInstance(stmt.value, Literal)
        self.assertEqual(stmt.value.value, 8)

    def test_constant_folding_multiplication(self):
        """10 * 5 + 2 harus jadi 52"""
        ast = self._optimize('x = 10 * 5 + 2')
        stmt = ast.statements[0]
        self.assertIsInstance(stmt.value, Literal)
        self.assertEqual(stmt.value.value, 52)

    def test_constant_folding_comparison(self):
        """5 > 3 harus jadi Bener (True)"""
        ast = self._optimize('x = 5 > 3')
        stmt = ast.statements[0]
        self.assertIsInstance(stmt.value, Literal)
        self.assertEqual(stmt.value.value, True)

    def test_dead_code_false_if(self):
        """lamun (Bohong) harus dihapus"""
        source = '''
        lamun (Bohong) {
            nyarita("Moal kaeksekusi")
        }
        '''
        ast = self._optimize(source)
        # The entire if should be removed (dead code)
        self.assertEqual(len(ast.statements), 0)

    def test_dead_code_true_if(self):
        """lamun (Bener) harus ngehapus sanesna"""
        source = '''
        lamun (Bener) {
            nyarita("Pasti kaeksekusi")
        } sanesna {
            nyarita("Moal kaeksekusi")
        }
        '''
        ast = self._optimize(source)
        stmt = ast.statements[0]
        self.assertIsInstance(stmt, IfStmt)
        self.assertIsNone(stmt.else_branch)

    def test_dead_code_after_return(self):
        """Kode sanggeus return harus dihapus"""
        source = '''
        jieun tes() {
            balikeun 1
            nyarita("Moal kaeksekusi")
        }
        '''
        ast = self._optimize(source)
        func = ast.statements[0]
        self.assertEqual(len(func.body), 1)  # Only return, nyarita removed

    def test_unary_constant_folding(self):
        """Negasi angka harus di-fold"""
        ast = self._optimize('x = -5')
        stmt = ast.statements[0]
        self.assertIsInstance(stmt.value, Literal)
        self.assertEqual(stmt.value.value, -5)

    def test_stress_long_chain(self):
        """Stress test: rantai operasi panjang"""
        # Build chain: 1 + 2 + 3 + ... + 50
        terms = ' + '.join(str(i) for i in range(1, 51))
        source = f'x = {terms}'
        ast = self._optimize(source)
        stmt = ast.statements[0]
        self.assertIsInstance(stmt.value, Literal)
        self.assertEqual(stmt.value.value, sum(range(1, 51)))

if __name__ == '__main__':
    unittest.main()
