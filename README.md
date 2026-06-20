# SundaScript Mini Compiler

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white) ![Status](https://img.shields.io/badge/Status-Tahap_Pengembangan-yellow?style=for-the-badge) ![Lisensi](https://img.shields.io/badge/Lisensi-MIT-green?style=for-the-badge)

SundaScript Mini Compiler adalah proyek kompilator berukuran kecil yang mengadaptasi sebagian kosakata bahasa pemrograman ke dalam **bahasa daerah Sunda Kasar**. Proyek ini dibangun sebagai eksperimen dan implementasi praktikum untuk mata kuliah **Teknik Kompilasi**.

Perlu dicatat bahwa kompilator ini tidak menerjemahkan atau mengubah seluruh fitur bahasa Python secara penuh. Kompilator ini **murni sebuah bahasa *mini*** yang hanya menargetkan dan mendukung **subset kata kunci** serta operasi dasar tertentu untuk memvalidasi alur teori kompilasi dari awal hingga menjadi berkas eksekusi.

## Fitur Utama

- **Sintaksis Lokal Sunda Kasar:** Mendukung kata kunci pemrograman esensial yang diubah ke bahasa Sunda Kasar (seperti `jieun` untuk mendefinisikan fungsi, `lamun` untuk kondisi logika, `salila` untuk perulangan). Rujukan lengkap terdapat pada berkas `REFERENSI_BAHASA.md`.
- **Pipeline Kompilasi 7 Fase:** Alur kerja menerapkan seluruh prinsip kompilasi mulai dari Desain Bahasa, Lexical Analysis, Parsing, AST Construction, Semantic Analysis, Code Optimization, hingga Code Generation.
- **Optimasi Cerdas:** Mendukung *Constant Folding* dan *Dead Code Elimination* untuk mengoptimalkan kode pada saat kompilasi.
- **Standalone Binary:** Dapat dipaketkan menjadi `sunda.exe` yang berjalan langsung di Windows tanpa memerlukan instalasi Python.

## Panduan Penggunaan

### Menjalankan dari Source Code

```bash
# Eksekusi langsung
python sunda.py jalankeun <file.sunda>

# Compile ke file Python
python sunda.py rilis <file.sunda>
```

### Menjalankan dengan `sunda.exe`

```bash
# Eksekusi langsung
sunda.exe jalankeun <file.sunda>

# Compile ke file Python
sunda.exe rilis <file.sunda>
```

### Melihat Diagnostik Kompilasi (Semua Fase)

```bash
python trace_compiler.py ujian_akhir.sunda
```

Perintah di atas akan mencetak output visual dari **seluruh 7 fase kompilasi** mulai dari source code → tokens → parse tree → AST → semantic validation → optimization → Python code → eksekusi.

## Contoh Kode SundaScript

```text
# Fungsi faktorial rekursif
jieun faktorial(n) {
    lamun (n <= 1) {
        balikeun 1
    }
    balikeun n * faktorial(n - 1)
}

nyarita("Faktorial 5:")
nyarita(faktorial(5))

# Perulangan
kanggo (i dina rentang(5)) {
    nyarita(i)
}

# Percabangan
nilai = 85
lamun (nilai >= 80) {
    nyarita("Alus pisan!")
} sanesna {
    nyarita("Kudu diajar deui")
}
```

## Setup Builder (Membangun Ulang Kompilator)

Jika ada pembaruan pada inti kompilator, berkas `sunda.exe` dapat dibangun ulang melalui skrip utama `sunda.py` menggunakan `PyInstaller`:

```bash
pip install pyinstaller
pyinstaller --onefile --name sunda sunda.py
```

Hasil kompilasi akan berada di dalam direktori `dist/`.

## Pengujian (Testing)

### 1. Unit Testing (Automated)

```bash
pip install pytest
python -m pytest tests/ -v
```

### 2. Black Box & Functional Testing
Pengujian ini memvalidasi keluaran akhir tanpa mencampuri mesin kompilator:

```python
import subprocess
import pytest

@pytest.mark.parametrize("kode_sunda, output_harapan", [
    ("nyarita(5 + 5)", "10\n"),
    ("x = 10\nnyarita(x)", "10\n"),
])
def test_fungsional_sunda(tmp_path, kode_sunda, output_harapan):
    jalur_skrip = tmp_path / "test.sunda"
    jalur_skrip.write_text(kode_sunda)
    hasil = subprocess.run(
        ["python", "sunda.py", "jalankeun", str(jalur_skrip)],
        capture_output=True, text=True
    )
    assert hasil.stdout == output_harapan
```

### 3. Stress Testing
Pengujian dengan injeksi operasi aritmatika puluhan ribu token untuk membuktikan *Constant Folding* bekerja tanpa crash.

### 4. Negative Testing
Pengujian kode cacat (kurung tidak ditutup, variabel belum dideklarasi) untuk membuktikan error handling yang *graceful*.

## Struktur Repositori

```text
sundascript-compiler/
│
├── src/                          # Modul Inti Kompilator (Fase 2-7)
│   ├── token.py                  # TokenType & Token dataclass
│   ├── lexer.py                  # Lexical Analysis (Fase 2)
│   ├── cst_nodes.py              # Concrete Syntax Tree nodes
│   ├── parser.py                 # Recursive Descent Parser (Fase 3)
│   ├── ast_nodes.py              # AST node definitions (Fase 4)
│   ├── ast_builder.py            # CST → AST transformer (Fase 4)
│   ├── semantic.py               # Semantic Analysis (Fase 5)
│   ├── optimizer.py              # Code Optimization (Fase 6)
│   └── codegen.py                # Code Generation (Fase 7)
│
├── docs/                         # Dokumentasi per-Fase
│   └── documentations-compiler/
│       ├── fase_1_desain_bahasa.md
│       ├── fase_2_lexer.md
│       ├── fase_3_parser.md
│       ├── fase_4_ast.md
│       ├── fase_5_semantic.md
│       ├── fase_6_optimizer.md
│       └── fase_7_codegen.md
│
├── tests/                        # Unit Testing per-modul
│   ├── test_lexer.py
│   ├── test_parser.py
│   ├── test_ast.py
│   ├── test_semantic.py
│   ├── test_optimizer.py
│   ├── test_codegen.py
│   └── test_full_coverage.py
│
├── contoh/                       # Contoh Script SundaScript
│   ├── contoh_percabangan.sunda
│   ├── contoh_perulangan.sunda
│   ├── contoh_fungsi.sunda
│   ├── contoh_kelas.sunda
│   └── contoh_error_handling.sunda
│
├── sunda.py                      # CLI Entry Point (jalankeun / rilis)
├── trace_compiler.py             # Diagnostik Visual (semua fase)
├── tes.sunda                     # Contoh script sederhana
├── ujian_akhir.sunda             # Contoh script komprehensif
├── REFERENSI_BAHASA.md           # Daftar Kosakata SundaScript
├── TABEL_SIMBOL_GRAMMAR.md       # Tabel Simbol & Grammar (CFG)
├── requirements.txt              # Dependensi Python
├── README.md                     # Dokumentasi Proyek
├── LICENSE                       # Lisensi MIT
└── .gitignore
```

## Alur Pipeline Kompilasi

```text
Source Code (.sunda)
       │
       ▼
┌──────────────┐
│ Fase 1:      │  Desain Bahasa (REFERENSI_BAHASA.md)
│ Language     │  → Pemetaan keyword Python ↔ Sunda Kasar
│ Design       │  → Context-Free Grammar (CFG)
└──────┬───────┘
       ▼
┌──────────────┐
│ Fase 2:      │  Lexer (lexer.py + token.py)
│ Lexical      │  → Source code → Token stream
│ Analysis     │  → Regex-based scanner
└──────┬───────┘
       ▼
┌──────────────┐
│ Fase 3:      │  Parser (parser.py + cst_nodes.py)
│ Syntax       │  → Token stream → Concrete Syntax Tree (CST)
│ Analysis     │  → Recursive Descent Parsing
└──────┬───────┘
       ▼
┌──────────────┐
│ Fase 4:      │  AST (ast_builder.py + ast_nodes.py)
│ Abstract     │  → CST → Abstract Syntax Tree
│ Syntax Tree  │  → Visitor Pattern transformer
└──────┬───────┘
       ▼
┌──────────────┐
│ Fase 5:      │  Semantic Analysis (semantic.py)
│ Semantic     │  → Symbol Table management
│ Analysis     │  → Scope validation & error detection
└──────┬───────┘
       ▼
┌──────────────┐
│ Fase 6:      │  Code Optimization (optimizer.py)
│ Code         │  → Constant Folding
│ Optimization │  → Dead Code Elimination
└──────┬───────┘
       ▼
┌──────────────┐
│ Fase 7:      │  Code Generation (codegen.py)
│ Code         │  → AST → Python 3 source code
│ Generation   │  → Keyword translation back to Python
└──────┬───────┘
       ▼
   Python Code → exec() / save .py
```

## Pembuat

**Muhammad Rafly Kamal Nasution** — Mahasiswa Teknik Kompilasi

## Lisensi

Proyek ini dilisensikan di bawah [MIT License](LICENSE).
