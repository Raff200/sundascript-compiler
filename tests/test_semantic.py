import unittest
from src.lexer import Lexer
from src.parser import Parser
from src.ast_builder import ASTBuilder
from src.semantic import SemanticAnalyzer, SemanticError

class TestSemantic(unittest.TestCase):
    def _analyze(self, source: str):
        lexer = Lexer(source)
        parser = Parser(lexer.tokenize())
        cst = parser.parse_program()
        builder = ASTBuilder()
        ast = builder.build(cst)
        analyzer = SemanticAnalyzer()
        analyzer.analyze(ast)
        return analyzer

    def test_valid_program(self):
        """Program yang valid harus lolos tanpa error"""
        source = '''
        x = 10
        nyarita(x)
        '''
        analyzer = self._analyze(source)
        self.assertTrue(analyzer.symbol_table.lookup('x'))

    def test_undeclared_variable(self):
        """Pake variabel yang belum dideklarasi harus error"""
        source = 'nyarita(variabel_teu_aya)'
        with self.assertRaises(SemanticError) as context:
            self._analyze(source)
        self.assertIn("can acan dideklarasikeun", str(context.exception))

    def test_function_scope(self):
        """Parameter fungsi harus valid di dalam scope fungsi"""
        source = '''
        jieun salam(ngaran) {
            nyarita(ngaran)
        }
        '''
        self._analyze(source)  # Should not raise

    def test_break_outside_loop(self):
        """Break di luar loop harus error"""
        source = 'eureun'
        with self.assertRaises(SemanticError) as context:
            self._analyze(source)
        self.assertIn("di luar perulangan", str(context.exception))

    def test_continue_outside_loop(self):
        """Continue di luar loop harus error"""
        source = 'terus_weh'
        with self.assertRaises(SemanticError) as context:
            self._analyze(source)
        self.assertIn("di luar perulangan", str(context.exception))

    def test_break_inside_loop(self):
        """Break di dalam loop harus valid"""
        source = '''
        x = 0
        salila (x < 10) {
            eureun
        }
        '''
        self._analyze(source)  # Should not raise

    def test_nested_scope(self):
        """Variabel di scope luar bisa diakses di scope dalam"""
        source = '''
        x = 10
        lamun (x > 5) {
            nyarita(x)
        }
        '''
        self._analyze(source)  # Should not raise

    def test_class_declaration(self):
        """Kelas harus terdaftar di symbol table"""
        source = '''
        kelas Jalma {
            jieun __init__(urang) {
                lewat
            }
        }
        '''
        analyzer = self._analyze(source)
        self.assertTrue(analyzer.symbol_table.lookup('Jalma'))

if __name__ == '__main__':
    unittest.main()
