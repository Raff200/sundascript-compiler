# Referensi Bahasa SundaScript

Dokumen ini berisi daftar lengkap pemetaan (*mapping*) kata kunci (keywords) dan fungsi bawaan (built-in functions) dari bahasa Python ke bahasa SundaScript (dialek Sunda Kasar).

## 1. Kata Kunci Dasar (Keywords)

### Boolean & Nilai Khusus
* `True` ➔ `Bener`
* `False` ➔ `Bohong`
* `None` ➔ `Euweuh`

### Logika
* `and` ➔ `jeung`
* `or` ➔ `atawa`
* `not` ➔ `lain`

### Percabangan
* `if` ➔ `lamun`
* `elif` ➔ `lamun_deui`
* `else` ➔ `sanesna`

### Perulangan
* `for` ➔ `kanggo`
* `while` ➔ `salila`
* `in` ➔ `dina`
* `break` ➔ `eureun`
* `continue` ➔ `terus_weh`
* `pass` ➔ `lewat`

### Fungsi
* `def` ➔ `jieun`
* `return` ➔ `balikeun`
* `yield` ➔ `hasilkeun`
* `lambda` ➔ `fungsi_leutik`

### Class / Pemrograman Berorientasi Objek (OOP)
* `class` ➔ `kelas`
* `self` ➔ `urang`
* `super` ➔ `kolot`

### Penanganan Error (Exception Handling)
* `try` ➔ `cobaan`
* `except` ➔ `kacuali`
* `finally` ➔ `ahirna`
* `raise` ➔ `lemparkeun`
* `assert` ➔ `pastikeun`

### Import & Modul
* `import` ➔ `mawa`
* `from` ➔ `ti`
* `as` ➔ `minangka`

### Scope / Konteks
* `global` ➔ `kabeh`
* `nonlocal` ➔ `lain_lokal`
* `with` ➔ `jeng`

### Asynchronous (Python 3.5+)
* `async` ➔ `babarengan`
* `await` ➔ `tangguan`

### Pattern Matching (Python 3.10+)
* `match` ➔ `cocogkeun`
* `case` ➔ `kasus`

### Lainnya
* `del` ➔ `hapus`
* `is` ➔ `nyaeta`

---

## 2. Fungsi Bawaan (Built-in Functions)

### Input / Output
* `print` ➔ `nyarita`
* `input` ➔ `tanya`

### Konversi Tipe Data
* `int` ➔ `angka`
* `float` ➔ `desimal`
* `str` ➔ `kecap`
* `bool` ➔ `logika`
* `complex` ➔ `kompleks`

### Koleksi / Struktur Data
* `list` ➔ `daptar`
* `tuple` ➔ `kumpulan`
* `set` ➔ `himpunan`
* `dict` ➔ `kamus`
* `frozenset` ➔ `himpunan_baku`

### Operasi Angka
* `abs` ➔ `mutlak`
* `round` ➔ `buleudkeun`
* `pow` ➔ `pangkatkeun`
* `divmod` ➔ `bagisesa`
* `sum` ➔ `jumlah`
* `max` ➔ `panggedena`
* `min` ➔ `pangleutikna`

### Iterasi
* `len` ➔ `panjang`
* `range` ➔ `rentang`
* `enumerate` ➔ `daptarkeun`
* `zip` ➔ `gabungkeun`
* `iter` ➔ `ulang`
* `next` ➔ `salajengna`
* `reversed` ➔ `balikeun_urut`
* `sorted` ➔ `urutkeun`

### Pengecekan Logika Tipe / Refleksi
* `all` ➔ `sadayana`
* `any` ➔ `salahsiji`
* `type` ➔ `jenis`
* `isinstance` ➔ `uji_jenis`
* `issubclass` ➔ `uji_turunan`
* `id` ➔ `tanda`
* `callable` ➔ `bisa_dipake`

### Karakter & Encoding
* `chr` ➔ `hurup`
* `ord` ➔ `urutan`
* `ascii` ➔ `aski`
* `bin` ➔ `biner`
* `oct` ➔ `oktal`
* `hex` ➔ `heksa`

### Utilitas Objek & Atribut
* `getattr` ➔ `nyokot_sipat`
* `setattr` ➔ `atur_sipat`
* `hasattr` ➔ `aya_sipat`
* `delattr` ➔ `hapus_sipat`

### Namespace & Memori
* `globals` ➔ `globalna`
* `locals` ➔ `lokalna`
* `vars` ➔ `variabalna`
* `dir` ➔ `arah`
* `bytes` ➔ `bait`
* `bytearray` ➔ `susunan_bait`
* `memoryview` ➔ `tingali_memori`

### Utilitas Eksekusi & Kelas
* `eval` ➔ `evaluasi`
* `exec` ➔ `jalankeun`
* `compile` ➔ `kompilasi`
* `open` ➔ `buka`
* `map` ➔ `petakeun`
* `filter` ➔ `saringkeun`
* `property` ➔ `properti`
* `staticmethod` ➔ `metode_statis`
* `classmethod` ➔ `metode_kelas`
* `__import__` ➔ `__mawa__`
* `breakpoint` ➔ `titik_eureun`
* `format` ➔ `format`
* `repr` ➔ `wakia`
* `hash` ➔ `acak`
* `help` ➔ `tulung`
* `slice` ➔ `potong`
* `object` ➔ `objek`
