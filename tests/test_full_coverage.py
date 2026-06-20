import unittest
from src.lexer import Lexer
from src.parser import Parser
from src.ast_builder import ASTBuilder
from src.semantic import SemanticAnalyzer
from src.optimizer import ASTOptimizer
from src.codegen import CodeGenerator

class TestFullCoverage(unittest.TestCase):
    """
    Full Coverage Test — End-to-end testing dari source code SundaScript
    sampai ke eksekusi Python yang valid.
    """
    
    def _full_compile(self, source: str) -> str:
        """Run full compilation pipeline"""
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        cst = parser.parse_program()
        builder = ASTBuilder()
        ast = builder.build(cst)
        analyzer = SemanticAnalyzer()
        analyzer.analyze(ast)
        optimizer = ASTOptimizer()
        ast = optimizer.optimize(ast)
        codegen = CodeGenerator()
        return codegen.generate(ast)

    def test_factorial_program(self):
        """Full pipeline test: program faktorial"""
        source = '''
        jieun faktorial(n) {
            lamun (n <= 1) {
                balikeun 1
            }
            balikeun n * faktorial(n - 1)
        }
        hasil = faktorial(5)
        nyarita(hasil)
        '''
        code = self._full_compile(source)
        self.assertIn('def faktorial(n):', code)
        self.assertIn('print(hasil)', code)
        # Execute and verify
        namespace = {}
        exec(code, namespace)

    def test_loop_with_break(self):
        """Full pipeline test: loop jeung eureun"""
        source = '''
        x = 0
        salila (x < 100) {
            lamun (x == 5) {
                eureun
            }
            x = x + 1
        }
        nyarita(x)
        '''
        code = self._full_compile(source)
        namespace = {}
        exec(code, namespace)

    def test_if_elif_else(self):
        """Full pipeline test: percabangan lengkap"""
        source = '''
        x = 15
        lamun (x > 20) {
            nyarita("Gede pisan")
        } lamun_deui (x > 10) {
            nyarita("Lumayan")
        } sanesna {
            nyarita("Leutik")
        }
        '''
        code = self._full_compile(source)
        self.assertIn('elif', code)
        self.assertIn('else:', code)

    def test_nested_functions(self):
        """Full pipeline test: nested function calls"""
        source = '''
        jieun kali(a, b) {
            balikeun a * b
        }
        jieun tambah(a, b) {
            balikeun a + b
        }
        hasil = tambah(kali(2, 3), kali(4, 5))
        nyarita(hasil)
        '''
        code = self._full_compile(source)
        namespace = {}
        exec(code, namespace)

    def test_for_loop(self):
        """Full pipeline test: kanggo loop"""
        source = '''
        kanggo (i dina rentang(5)) {
            nyarita(i)
        }
        '''
        code = self._full_compile(source)
        self.assertIn('for i in range(5):', code)

    def test_optimization_pipeline(self):
        """Verify optimization passes through full pipeline"""
        source = 'x = 10 * 5 + 2'
        code = self._full_compile(source)
        # After constant folding, should be x = 52
        self.assertIn('x = 52', code)

if __name__ == '__main__':
    unittest.main()
