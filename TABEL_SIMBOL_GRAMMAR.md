# Tabel Simbol & Grammar SundaScript

Dokumen ini mendefinisikan **Tabel Simbol** dan **Context-Free Grammar (CFG)** yang menjadi fondasi seluruh pipeline kompilasi SundaScript.

---

## 1. Tabel Simbol (Symbol Table)

Tabel simbol menyimpan informasi tentang setiap entitas yang dikenali oleh kompilator.

### Kategori Token

| Kategori Token | Simbol / Pola | Contoh |
|----------------|---------------|--------|
| `NUMBER` | `\d+\.?\d*` | `42`, `3.14` |
| `STRING` | `"..."` atau `'...'` | `"Halo Sunda"` |
| `IDENTIFIER` | `[a-zA-Z_][a-zA-Z0-9_]*` | `x`, `jumlah_data` |
| `KEYWORD` | Kata kunci bahasa | `lamun`, `jieun`, `salila` |
| `BUILTIN` | Fungsi bawaan | `nyarita`, `tanya`, `panjang` |
| `OPERATOR` | Simbol operator | `+`, `-`, `*`, `/`, `=`, `==`, `!=`, `<`, `>`, `<=`, `>=` |
| `LBRACE` | `{` | Buka blok |
| `RBRACE` | `}` | Tutup blok |
| `LPAREN` | `(` | Buka kurung |
| `RPAREN` | `)` | Tutup kurung |
| `COMMA` | `,` | Pemisah |
| `EOF` | End of File | Akhir input |

### Tabel Simbol Runtime (Scope-based)

| Properti | Deskripsi |
|----------|-----------|
| `name` | Nama identifier (variabel/fungsi/kelas) |
| `type` | Jenis: `variable`, `function`, `class`, `parameter`, `builtin`, `module` |
| `scope` | Level scope (0 = global, 1+ = nested) |

Contoh isi tabel simbol saat runtime:

```text
Scope 0 (Global):
  nyarita   → builtin
  panjang   → builtin
  tambah    → function
  x         → variable

Scope 1 (Function: tambah):
  a         → parameter
  b         → parameter
  hasil     → variable
```

---

## 2. Context-Free Grammar (CFG)

Grammar ini mendefinisikan sintaksis SundaScript menggunakan notasi BNF (*Backus-Naur Form*).

### Program
```bnf
<program>         ::= <statement>*

<statement>       ::= <assignment_stmt>
                    | <if_stmt>
                    | <while_stmt>
                    | <for_stmt>
                    | <function_def>
                    | <class_def>
                    | <try_stmt>
                    | <import_stmt>
                    | <from_import_stmt>
                    | <with_stmt>
                    | <async_stmt>
                    | <match_stmt>
                    | <return_stmt>
                    | <simple_ctrl_stmt>
                    | <unary_ctrl_stmt>
                    | <expression_stmt>
```

### Assignment
```bnf
<assignment_stmt> ::= IDENTIFIER "=" <expression>
```

### Percabangan (If Statement)
```bnf
<if_stmt>         ::= "lamun" "(" <expression> ")" <block>
                      ("lamun_deui" "(" <expression> ")" <block>)*
                      ("sanesna" <block>)?
```

### Perulangan (Loop)
```bnf
<while_stmt>      ::= "salila" "(" <expression> ")" <block>

<for_stmt>        ::= "kanggo" "(" IDENTIFIER "dina" <expression> ")" <block>
```

### Fungsi
```bnf
<function_def>    ::= "jieun" IDENTIFIER "(" <params>? ")" <block>

<params>          ::= IDENTIFIER ("," IDENTIFIER)*

<return_stmt>     ::= "balikeun" <expression>?
```

### Kelas (Class)
```bnf
<class_def>       ::= "kelas" IDENTIFIER ("(" IDENTIFIER ")")? <block>
```

### Exception Handling
```bnf
<try_stmt>        ::= "cobaan" <block>
                      ("kacuali" (IDENTIFIER ("minangka" IDENTIFIER)?)? <block>)*
                      ("ahirna" <block>)?
```

### Import
```bnf
<import_stmt>     ::= "mawa" IDENTIFIER ("minangka" IDENTIFIER)?

<from_import_stmt>::= "ti" IDENTIFIER "mawa" IDENTIFIER
```

### Context Manager
```bnf
<with_stmt>       ::= "jeng" <expression> ("minangka" IDENTIFIER)? <block>
```

### Async
```bnf
<async_stmt>      ::= "babarengan" (<function_def> | <for_stmt> | <with_stmt>)
```

### Pattern Matching
```bnf
<match_stmt>      ::= "cocogkeun" <expression> "{" ("kasus" <expression> <block>)* "}"
```

### Kontrol Alur Sederhana
```bnf
<simple_ctrl_stmt>::= "eureun" | "terus_weh" | "lewat"

<unary_ctrl_stmt> ::= ("lemparkeun" | "pastikeun" | "hapus" | "kabeh" | "lain_lokal" | "hasilkeun") <expression>
```

### Blok Kode
```bnf
<block>           ::= "{" <statement>* "}"
```

### Ekspresi (Expression) — Operator Precedence
```bnf
<expression>      ::= <logical>

<logical>         ::= <equality> (("jeung" | "atawa") <equality>)*

<equality>        ::= <comparison> (("==" | "!=" | "nyaeta") <comparison>)*

<comparison>      ::= <term> (("<" | "<=" | ">" | ">=") <term>)*

<term>            ::= <factor> (("+" | "-") <factor>)*

<factor>          ::= <unary> (("*" | "/") <unary>)*

<unary>           ::= ("lain" | "-" | "+") <unary>
                    | "tangguan" <unary>
                    | "fungsi_leutik" <params> "{" <expression> "}"
                    | <primary>

<primary>         ::= NUMBER
                    | STRING
                    | IDENTIFIER ("(" <arguments>? ")")?
                    | BUILTIN ("(" <arguments>? ")")?
                    | "Bener" | "Bohong" | "Euweuh"
                    | "urang" | "kolot"
                    | "(" <expression> ")"

<arguments>       ::= <expression> ("," <expression>)*
```

### Pemanggilan Fungsi
```bnf
<function_call>   ::= (IDENTIFIER | BUILTIN) "(" <arguments>? ")"
```

---

## 3. Diagram Alur Operator Precedence

```text
Prioritas Tertinggi ↑
  ├── primary      : angka, string, identifier, literal
  ├── unary        : -x, +x, lain x
  ├── factor       : *, /
  ├── term         : +, -
  ├── comparison   : <, <=, >, >=
  ├── equality     : ==, !=, nyaeta
  └── logical      : jeung, atawa
Prioritas Terendah ↓
```
