import sys
import pprint

from src.lexer import Lexer
from src.parser import Parser
from src.ast_builder import ASTBuilder
from src.semantic import SemanticAnalyzer
from src.optimizer import ASTOptimizer
from src.codegen import CodeGenerator

def print_header(title):
    print("\n" + "="*60)
    print(f" {title} ".center(60, "="))
    print("="*60 + "\n")

def trace_compilation(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        source_code = f.read()

    print_header("Fase 1: Source Code SundaScript")
    print(source_code)

    print_header("Fase 2: Lexical Analysis (Tokens)")
    lexer = Lexer(source_code)
    tokens = lexer.tokenize()
    for t in tokens[:15]:  # Print first 15 for brevity
        print(f"  {t}")
    if len(tokens) > 15:
        print(f"  ... (jeung {len(tokens)-15} token sejenna)")
    print(f"\n  Total token: {len(tokens)}")

    print_header("Fase 3: Syntax Analysis (CST / Parse Tree)")
    parser = Parser(tokens)
    cst = parser.parse_program()
    print("Sukses ngawangun Concrete Syntax Tree (CST)!")
    print(f"Total root statements: {len(cst.children)}")
    print("\nParse Tree (10 baris awal):")
    tree_str = cst.print_tree()
    lines = tree_str.split('\n')
    for line in lines[:10]:
        print(f"  {line}")
    if len(lines) > 10:
        print(f"  ... ({len(lines)-10} baris deui)")

    print_header("Fase 4: AST Construction")
    builder = ASTBuilder()
    ast = builder.build(cst)
    print("Abstract Syntax Tree (AST) geus jadi.")
    print("Nodes level luhur:")
    for stmt in ast.statements:
        print(f"  - {stmt.__class__.__name__}")

    print_header("Fase 5: Semantic Analysis")
    analyzer = SemanticAnalyzer()
    analyzer.analyze(ast)
    print("Validasi semantik sukses (Identifier & Rules dicek).")
    print("Eusi Symbol Table (Global Scope):")
    for name, kind in analyzer.symbol_table.scopes[0].items():
        if kind != 'builtin':  # Sumputkeun builtins supados henteu panjang teuing
            print(f"  - {name} ({kind})")

    print_header("Fase 6: Code Optimization")
    optimizer = ASTOptimizer()
    optimized_ast = optimizer.optimize(ast)
    print("AST geus dioptimasi.")
    print("Cek efek optimasi (Constant Folding 10 * 5 + 2 -> 52):")
    print("  Operasi aritmatika statis diitung pas compile-time,")
    print("  lain pas runtime. Leuwih gancang!")

    print_header("Fase 7: Code Generation (Target: Python)")
    codegen = CodeGenerator()
    python_code = codegen.generate(optimized_ast)
    print(python_code)

    print_header("EKSEKUSI FINAL: Output Program")
    exec(python_code, {})

if __name__ == '__main__':
    if len(sys.argv) > 1:
        trace_compilation(sys.argv[1])
    else:
        trace_compilation("ujian_akhir.sunda")
