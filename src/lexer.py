import re
from typing import List
from src.token import Token, TokenType

# Himpunan keyword yang dipetakan dari REFERENSI_BAHASA.md (Sunda Kasar)
KEYWORDS = {
    'Bener', 'Bohong', 'Euweuh',  # Boolean / Nilai Khusus
    'jeung', 'atawa', 'lain', 'lamun', 'lamun_deui', 'sanesna', 'kanggo', 'salila',
    'dina', 'eureun', 'terus_weh', 'lewat', 'jieun', 'balikeun', 'hasilkeun',
    'fungsi_leutik', 'kelas', 'urang', 'kolot', 'cobaan', 'kacuali', 'ahirna',
    'lemparkeun', 'pastikeun', 'mawa', 'ti', 'minangka', 'jeng', 'babarengan',
    'tangguan', 'cocogkeun', 'kasus', 'kabeh', 'lain_lokal', 'hapus', 'nyaeta'
}

# Himpunan fungsi bawaan (built-in functions)
BUILTINS = {
    'nyarita', 'tanya', 'angka', 'desimal', 'kecap', 'logika', 'kompleks',
    'daptar', 'kumpulan', 'himpunan', 'kamus', 'himpunan_baku', 'mutlak',
    'buleudkeun', 'pangkatkeun', 'bagisesa', 'jumlah', 'panggedena', 'pangleutikna',
    'panjang', 'rentang', 'daptarkeun', 'gabungkeun', 'ulang', 'salajengna',
    'balikeun_urut', 'urutkeun', 'sadayana', 'salahsiji', 'jenis', 'uji_jenis',
    'uji_turunan', 'tanda', 'bisa_dipake', 'hurup', 'urutan', 'aski', 'biner',
    'oktal', 'heksa', 'nyokot_sipat', 'atur_sipat', 'aya_sipat',
    'hapus_sipat', 'globalna', 'lokalna', 'variabalna', 'arah',
    'evaluasi', 'jalankeun', 'kompilasi', 'buka', 'bait', 'susunan_bait',
    'tingali_memori', 'petakeun', 'saringkeun', 'properti', 'metode_statis',
    'metode_kelas', '__mawa__', 'titik_eureun', 'format',
    'wakia', 'acak', 'tulung', 'potong', 'objek'
}

class LexerError(Exception):
    def __init__(self, message: str, line: int, column: int):
        super().__init__(f"LexerError dina baris {line}, kolom {column}: {message}")

class Lexer:
    def __init__(self, source_code: str):
        self.source_code = source_code
        self.pos = 0
        self.line = 1
        self.column = 1
        
        # Spesifikasi Regex (berurutan, rule terpanjang didahulukan)
        self.rules = [
            ('SKIP', r'[ \t]+'),
            ('COMMENT', r'#.*'),
            ('NEWLINE', r'\n'),
            ('STRING', r'"[^"]*"|\'[^\']*\''),
            ('NUMBER', r'\d+\.\d+|\d+'),
            ('ID', r'[a-zA-Z_][a-zA-Z0-9_]*'),
            ('OPERATOR', r'==|!=|<=|>=|<|>|\+|-|\*|/|='),
            ('LBRACE', r'\{'),
            ('RBRACE', r'\}'),
            ('LPAREN', r'\('),
            ('RPAREN', r'\)'),
            ('COMMA', r','),
            ('MISMATCH', r'.')
        ]
        
        self.regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in self.rules)
        self.scanner = re.compile(self.regex)

    def tokenize(self) -> List[Token]:
        tokens = []
        for match in self.scanner.finditer(self.source_code):
            kind = match.lastgroup
            value = match.group()
            
            if kind == 'SKIP' or kind == 'COMMENT':
                self.column += len(value)
                continue
            elif kind == 'NEWLINE':
                self.line += 1
                self.column = 1
                continue
            elif kind == 'MISMATCH':
                raise LexerError(f"Karakter Henteu Valid '{value}'", self.line, self.column)
            
            token_type = self._determine_token_type(kind, value)
            tokens.append(Token(token_type, value, self.line, self.column))
            self.column += len(value)
            
        tokens.append(Token(TokenType.EOF, "", self.line, self.column))
        return tokens
        
    def _determine_token_type(self, kind: str, value: str) -> TokenType:
        if kind == 'ID':
            if value in KEYWORDS:
                return TokenType.KEYWORD
            elif value in BUILTINS:
                return TokenType.BUILTIN
            else:
                return TokenType.IDENTIFIER
                
        mapping = {
            'STRING': TokenType.STRING,
            'NUMBER': TokenType.NUMBER,
            'OPERATOR': TokenType.OPERATOR,
            'LBRACE': TokenType.LBRACE,
            'RBRACE': TokenType.RBRACE,
            'LPAREN': TokenType.LPAREN,
            'RPAREN': TokenType.RPAREN,
            'COMMA': TokenType.COMMA
        }
        return mapping[kind]
