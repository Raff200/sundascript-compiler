import unittest
from src.lexer import Lexer
from src.parser import Parser
from src.ast_builder import ASTBuilder
from src.semantic import SemanticAnalyzer
from src.optimizer import ASTOptimizer
from src.codegen import CodeGenerator

class TestCodegen(unittest.TestCase):
    def _generate(self, source: str) -> str:
        lexer = Lexer(source)
        parser = Parser(lexer.tokenize())
        cst = parser.parse_program()
        builder = ASTBuilder()
        ast = builder.build(cst)
        analyzer = SemanticAnalyzer()
        analyzer.analyze(ast)
        optimizer = ASTOptimizer()
        ast = optimizer.optimize(ast)
        codegen = CodeGenerator()
        return codegen.generate(ast)

    def test_print_generation(self):
        """nyarita harus jadi print"""
        code = self._generate('nyarita("Sampurasun")')
        self.assertIn('print("Sampurasun")', code)

    def test_assignment_generation(self):
        """Assignment harus di-generate dengan bener"""
        code = self._generate('x = 10')
        self.assertIn('x = 10', code)

    def test_function_generation(self):
        """Fungsi harus di-generate jadi def Python"""
        source = '''
        jieun tambah(a, b) {
            balikeun a + b
        }
        '''
        code = self._generate(source)
        self.assertIn('def tambah(a, b):', code)
        self.assertIn('return', code)

    def test_if_generation(self):
        """lamun harus jadi if"""
        source = '''
        x = 10
        lamun (x > 5) {
            nyarita("Gede")
        }
        '''
        code = self._generate(source)
        self.assertIn('if', code)
        self.assertIn('print("Gede")', code)

    def test_while_generation(self):
        """salila harus jadi while"""
        source = '''
        x = 0
        salila (x < 3) {
            nyarita(x)
            x = x + 1
        }
        '''
        code = self._generate(source)
        self.assertIn('while', code)

    def test_for_generation(self):
        """kanggo ... dina harus jadi for ... in"""
        source = '''
        kanggo (i dina rentang(5)) {
            nyarita(i)
        }
        '''
        code = self._generate(source)
        self.assertIn('for i in range(5):', code)

    def test_constant_folding_in_codegen(self):
        """10 * 5 + 2 harus langsung jadi 52"""
        code = self._generate('x = 10 * 5 + 2')
        self.assertIn('x = 52', code)

    def test_builtin_translation(self):
        """Built-in Sunda harus ditranslasi ke Python"""
        code = self._generate('x = panjang("test")')
        self.assertIn('len("test")', code)

if __name__ == '__main__':
    unittest.main()
