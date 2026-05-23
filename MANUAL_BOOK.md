# 📖 MANUAL BOOK
## Linear Algebra Dashboard Pro
### Kalkulator Aljabar Linear pada Persamaan Linear

---

## 📋 Daftar Isi

1. [Pendahuluan](#1-pendahuluan)
2. [Persyaratan Sistem](#2-persyaratan-sistem)
3. [Instalasi & Menjalankan Aplikasi](#3-instalasi--menjalankan-aplikasi)
4. [Tampilan Antarmuka](#4-tampilan-antarmuka)
5. [Panduan Input Matriks](#5-panduan-input-matriks)
6. [Fitur 1: Sistem Persamaan Linear (SPL)](#6-fitur-1-sistem-persamaan-linear-spl)
7. [Fitur 2: Determinan](#7-fitur-2-determinan)
8. [Fitur 3: Invers Matriks](#8-fitur-3-invers-matriks)
9. [Fitur 4: Dekomposisi LU](#9-fitur-4-dekomposisi-lu)
10. [Fitur 5: Eigenvalue & Eigenvector](#10-fitur-5-eigenvalue--eigenvector)
11. [Fitur 6: Diagonalisasi](#11-fitur-6-diagonalisasi)
12. [Fitur 7: SVD (Singular Value Decomposition)](#12-fitur-7-svd-singular-value-decomposition)
13. [Keyboard Shortcuts](#13-keyboard-shortcuts)
14. [Fitur Tambahan](#14-fitur-tambahan)
15. [Troubleshooting](#15-troubleshooting)

---

## 1. Pendahuluan

**Linear Algebra Dashboard Pro** adalah aplikasi kalkulator aljabar linear modern berbasis GUI yang dirancang untuk membantu mahasiswa dan dosen dalam menyelesaikan berbagai permasalahan aljabar linear. Aplikasi ini menampilkan proses perhitungan secara **step-by-step** sehingga pengguna tidak hanya mendapatkan jawaban akhir, tetapi juga memahami setiap langkah penyelesaiannya.

### Keunggulan Aplikasi:
- **Single-Window Dashboard** — Semua fitur dalam satu jendela, tanpa pop-up
- **Step-by-Step** — Setiap operasi baris ditampilkan secara detail
- **Visual Matrix Grid** — Input matriks menggunakan kotak-kotak visual
- **Dark/Light Mode** — Tema yang nyaman di mata
- **7 Fitur Lengkap** — SPL, Determinan, Invers, LU, Eigen, Diagonalisasi, SVD
- **Copy & Export** — Salin hasil dalam format Plain Text atau LaTeX

---

## 2. Persyaratan Sistem

### Minimum:
| Komponen | Spesifikasi |
|----------|-------------|
| OS | Windows 10/11, macOS 10.14+, Linux |
| Python | 3.9 atau lebih baru |
| RAM | 4 GB |
| Resolusi | 1280×720 (minimum 900×600) |

### Library Python yang Dibutuhkan:
| Library | Versi | Fungsi |
|---------|-------|--------|
| `customtkinter` | ≥ 5.0 | Framework GUI modern |
| `sympy` | ≥ 1.12 | Komputasi simbolik (pecahan, eigen) |
| `numpy` | ≥ 1.24 | Komputasi numerik (SVD) |

---

## 3. Instalasi & Menjalankan Aplikasi

### Langkah 1: Install Python
Pastikan Python 3.9+ sudah terinstall. Cek dengan:
```
python --version
```

### Langkah 2: Install Dependencies
Buka terminal/command prompt, navigasi ke folder project, lalu jalankan:
```
pip install customtkinter sympy numpy
```

### Langkah 3: Jalankan Aplikasi
```
cd "e:\Folder Tugas-Q\AlJabar Linear\CODING"
python main.py
```

Aplikasi akan terbuka dengan tampilan dashboard utama.

---

## 4. Tampilan Antarmuka

### 4.1 Layout Utama

```
┌────────────┬──────────────────────────────────────────────┐
│            │                                              │
│  SIDEBAR   │           CONTENT AREA                       │
│            │                                              │
│  ┌──────┐  │  ┌──────────────────────────────────────┐   │
│  │ Logo │  │  │  Header (Judul Halaman)               │   │
│  └──────┘  │  ├──────────────────────────────────────┤   │
│            │  │  Method Selector                      │   │
│  [SPL    ] │  │  Matrix Input Grid                    │   │
│  [Det    ] │  │  [⚡ Hitung]                          │   │
│  [Invers ] │  │  Result Console (Output)              │   │
│  [LU     ] │  └──────────────────────────────────────┘   │
│  [Eigen  ] │                                              │
│  [Diag   ] │                                              │
│  [SVD    ] │                                              │
│            │                                              │
│  [🌙 Dark] │  ┌──────────────────────────────────────┐   │
│            │  │  Status Bar                           │   │
└────────────┴──┴──────────────────────────────────────┘───┘
```

### 4.2 Komponen Utama

| Komponen | Lokasi | Fungsi |
|----------|--------|--------|
| **Sidebar** | Kiri | Navigasi antar fitur (7 menu) |
| **Content Area** | Tengah-Kanan | Area kerja utama |
| **Method Selector** | Atas content | Pilih metode perhitungan |
| **Matrix Input** | Tengah content | Input matriks visual |
| **Result Console** | Bawah content | Output hasil + langkah |
| **Status Bar** | Paling bawah | Info halaman + shortcut hints |
| **Theme Toggle** | Bawah sidebar | Switch Dark/Light mode |

### 4.3 Navigasi

- **Klik tombol di sidebar** untuk berpindah halaman
- **Ctrl+1 s/d Ctrl+7** untuk navigasi cepat via keyboard
- **Escape** untuk kembali ke halaman utama (Dashboard)
- Sidebar akan **collapse otomatis** jika window diperkecil (< 1000px)

---

## 5. Panduan Input Matriks

### 5.1 Mengatur Dimensi

Di bagian atas area input matriks, terdapat dropdown:
- **Baris**: Pilih jumlah baris (1-10)
- **Kolom**: Pilih jumlah kolom (1-10)

Grid akan otomatis berubah sesuai dimensi yang dipilih.

### 5.2 Mengisi Nilai

Klik pada cell matriks dan ketik nilai. Format yang diterima:

| Format | Contoh | Keterangan |
|--------|--------|------------|
| Integer | `5`, `-3`, `0` | Bilangan bulat |
| Desimal | `1.5`, `-0.33` | Bilangan desimal |
| Pecahan | `1/3`, `-2/5` | Pecahan (akan dihitung eksak) |

### 5.3 Navigasi Antar Cell

| Tombol | Aksi |
|--------|------|
| `Tab` | Pindah ke cell berikutnya (kiri→kanan, atas→bawah) |
| `Shift+Tab` | Pindah ke cell sebelumnya |
| `↑` `↓` `←` `→` | Navigasi arah |
| Klik cell | Langsung fokus ke cell tersebut |

### 5.4 Quick Actions (Tombol Cepat)

Di bawah grid matriks terdapat tombol-tombol:

| Tombol | Fungsi |
|--------|--------|
| **Clear** | Reset semua cell ke 0 |
| **Random** | Isi dengan angka acak (-9 s/d 9) |
| **Identity** | Isi dengan matriks identitas |
| **Transpose** | Transpose matriks (tukar baris↔kolom) |
| **Paste** | Paste dari clipboard (Excel/spreadsheet) |

### 5.5 Paste dari Excel/Spreadsheet

1. Di Excel, select range matriks yang ingin di-copy
2. Tekan `Ctrl+C`
3. Di aplikasi, klik tombol **Paste** atau tekan `Ctrl+V` saat fokus di grid
4. Data akan otomatis terisi ke grid

Format yang didukung: tab-separated (Excel) dan space-separated.

### 5.6 Validasi Input

- Cell dengan input **valid** → border normal
- Cell dengan input **invalid** → border merah
- Cell kosong otomatis dianggap **0**
- Saat fokus masuk ke cell, seluruh teks ter-select (mudah untuk replace)

---

## 6. Fitur 1: Sistem Persamaan Linear (SPL)

### Akses: Klik "SPL" di sidebar atau tekan `Ctrl+1`

### 6.1 Deskripsi
Menyelesaikan sistem persamaan linear Ax = b dengan tiga metode berbeda.

### 6.2 Input yang Diperlukan
- **Matriks A** (Koefisien): Matriks m×n berisi koefisien variabel
- **Vektor b** (Konstanta): Vektor m×1 berisi konstanta ruas kanan

### 6.3 Metode yang Tersedia

#### a) Gauss (Eliminasi Gauss)
- Mengubah matriks augmented [A|b] ke bentuk **Row Echelon Form (REF)**
- Menampilkan setiap operasi baris elementer (OBE)
- Kemudian melakukan **back substitution** untuk mendapatkan solusi

#### b) Gauss-Jordan
- Mengubah matriks augmented [A|b] ke bentuk **Reduced Row Echelon Form (RREF)**
- Solusi langsung terbaca dari kolom terakhir
- Lebih banyak langkah tapi solusi lebih jelas

#### c) Matriks Balikan
- Menghitung x = A⁻¹ · b
- **Syarat**: Matriks A harus persegi dan non-singular (det ≠ 0)
- Menampilkan A⁻¹ dan hasil perkalian

### 6.4 Contoh Penggunaan

**Soal**: Selesaikan SPL berikut:
```
2x + y - z = 5
4x + 5y + z = 13
x + 2y + 3z = 12
```

**Langkah**:
1. Klik **SPL** di sidebar
2. Pilih metode **Gauss**
3. Set Matriks A: Baris=3, Kolom=3
4. Isi Matriks A:
   ```
   2   1  -1
   4   5   1
   1   2   3
   ```
5. Set Vektor b: Baris=3, Kolom=1
6. Isi Vektor b:
   ```
   5
   13
   12
   ```
7. Klik **⚡ Hitung SPL**

**Output**: Aplikasi akan menampilkan setiap langkah eliminasi dan solusi akhir:
```
Solusi unik: x1 = 6, x2 = -3, x3 = 4
```

### 6.5 Kasus Khusus
- **Tidak ada solusi**: Jika ditemukan baris [0 0 ... 0 | c] dengan c ≠ 0
- **Solusi tak hingga**: Jika jumlah pivot < jumlah variabel (ada variabel bebas)

---

## 7. Fitur 2: Determinan

### Akses: Klik "Determinan" di sidebar atau tekan `Ctrl+2`

### 7.1 Deskripsi
Menghitung determinan matriks persegi dengan tiga metode berbeda.

### 7.2 Input yang Diperlukan
- **Matriks persegi** (n×n): Pastikan jumlah baris = jumlah kolom

### 7.3 Metode yang Tersedia

#### a) Kofaktor (Ekspansi Baris Pertama)
- Menggunakan rumus: det(A) = Σ (-1)^(1+j) · a₁ⱼ · det(M₁ⱼ)
- Menampilkan setiap minor dan kofaktor
- Cocok untuk matriks kecil (2×2, 3×3, 4×4)

#### b) Reduksi Baris (Step-by-Step)
- Eliminasi ke bentuk segitiga atas
- det = (-1)^(jumlah swap) × produk diagonal
- Menampilkan setiap operasi baris

#### c) Sarrus (Khusus 3×3)
- Menggunakan metode Sarrus (diagonal positif - diagonal negatif)
- **Hanya tersedia untuk matriks 3×3**
- Menampilkan setiap diagonal dan perhitungannya

### 7.4 Contoh Penggunaan

**Soal**: Hitung determinan matriks:
```
| 1  2  3 |
| 4  5  6 |
| 7  8  0 |
```

**Langkah**:
1. Klik **Determinan** di sidebar
2. Pilih metode **Sarrus (3×3)**
3. Isi matriks 3×3 dengan nilai di atas
4. Klik **⚡ Hitung Determinan**

**Output**: Menampilkan diagonal positif, diagonal negatif, dan hasil akhir.

### 7.5 Catatan
- Jika matriks bukan persegi → muncul error banner
- Jika memilih Sarrus tapi matriks bukan 3×3 → muncul error

---

## 8. Fitur 3: Invers Matriks

### Akses: Klik "Invers" di sidebar atau tekan `Ctrl+3`

### 8.1 Deskripsi
Menghitung invers matriks persegi non-singular.

### 8.2 Input yang Diperlukan
- **Matriks persegi** (n×n) dengan det ≠ 0

### 8.3 Metode yang Tersedia

#### a) Adjugate
- Rumus: A⁻¹ = (1/det(A)) × adj(A)
- Menampilkan: Matriks Kofaktor → Adjugate (transpose) → Invers
- Cocok untuk pemahaman konsep

#### b) Gauss-Jordan (Step-by-Step)
- Augmentasi [A|I] lalu eliminasi ke [I|A⁻¹]
- **Menampilkan setiap langkah OBE secara detail**
- Metode yang paling informatif untuk belajar

#### c) Built-in
- Langsung menghitung menggunakan fungsi bawaan
- Menampilkan hasil + verifikasi A × A⁻¹ = I
- Paling cepat untuk matriks besar

### 8.4 Contoh Penggunaan

**Soal**: Hitung invers matriks:
```
| 2  1 |
| 5  3 |
```

**Langkah**:
1. Klik **Invers** di sidebar
2. Pilih metode **Gauss-Jordan**
3. Set dimensi 2×2
4. Isi matriks
5. Klik **⚡ Hitung Invers**

**Output**: Menampilkan [A|I] → langkah-langkah → [I|A⁻¹], lalu verifikasi.

### 8.5 Error yang Mungkin Muncul
- "Matriks harus persegi!" — jika baris ≠ kolom
- "Matriks singular (det = 0), invers tidak ada" — jika determinan = 0

---

## 9. Fitur 4: Dekomposisi LU

### Akses: Klik "Dekomposisi LU" di sidebar atau tekan `Ctrl+4`

### 9.1 Deskripsi
Mendekomposisi matriks persegi menjadi PA = LU, dimana:
- **P** = Matriks permutasi
- **L** = Matriks segitiga bawah (Lower triangular)
- **U** = Matriks segitiga atas (Upper triangular)

### 9.2 Input yang Diperlukan
- **Matriks persegi** (n×n)

### 9.3 Output
- Matriks P, L, dan U
- Verifikasi: PA = LU (ditampilkan hasil perkalian)

### 9.4 Contoh Penggunaan

**Langkah**:
1. Klik **Dekomposisi LU** di sidebar
2. Isi matriks persegi (misal 3×3)
3. Klik **⚡ Hitung LU**

**Output**:
```
Matriks P (Permutasi):
[ 1  0  0 ]
[ 0  0  1 ]
[ 0  1  0 ]

Matriks L (Lower Triangular):
[ 1    0    0 ]
[ 1/2  1    0 ]
[ 1/4  3/4  1 ]

Matriks U (Upper Triangular):
[ 4   5   1 ]
[ 0  -1/2  5/2 ]
[ 0   0    9/4 ]

Verifikasi PA = LU ✓
```

---

## 10. Fitur 5: Eigenvalue & Eigenvector

### Akses: Klik "Eigen" di sidebar atau tekan `Ctrl+5`

### 10.1 Deskripsi
Menghitung eigenvalue (nilai eigen) dan eigenvector (vektor eigen) dari matriks persegi.

### 10.2 Input yang Diperlukan
- **Matriks persegi** (n×n)

### 10.3 Output
1. **Polinomial Karakteristik**: p(λ) = det(A - λI)
2. **Eigenvalues**: Semua nilai λ beserta multiplisitas aljabar
3. **Eigenvectors**: Basis eigenspace untuk setiap λ (dinormalisasi ke bilangan bulat)
4. **Info Diagonalisasi**: Apakah matriks bisa didiagonalisasi

### 10.4 Contoh Penggunaan

**Soal**: Cari eigenvalue dan eigenvector dari:
```
| 4  1 |
| 2  3 |
```

**Langkah**:
1. Klik **Eigen** di sidebar
2. Set dimensi 2×2
3. Isi matriks
4. Klik **⚡ Hitung Eigen**

**Output**:
```
Polinomial Karakteristik:
  p(λ) = λ² - 7λ + 10

Eigenvalues:
  λ = 2  (multiplisitas aljabar = 1)
  λ = 5  (multiplisitas aljabar = 1)

Eigenvectors:
  Untuk λ = 2:
    v1 = (-1, 2)

  Untuk λ = 5:
    v1 = (1, 1)

Matriks BISA didiagonalisasi (n eigenvector independen)
```

### 10.5 Catatan
- Eigenvector ditampilkan dalam bentuk bilangan bulat terkecil
- Multiplisitas aljabar vs geometri ditampilkan untuk setiap eigenvalue

---

## 11. Fitur 6: Diagonalisasi

### Akses: Klik "Diagonalisasi" di sidebar atau tekan `Ctrl+6`

### 11.1 Deskripsi
Mendiagonalisasi matriks: A = P·D·P⁻¹, dimana:
- **P** = Matriks yang kolomnya adalah eigenvector
- **D** = Matriks diagonal yang berisi eigenvalue
- **P⁻¹** = Invers dari P

### 11.2 Input yang Diperlukan
- **Matriks persegi** (n×n)

### 11.3 Output
- Jika **bisa** didiagonalisasi: P, D, P⁻¹, dan verifikasi A = PDP⁻¹
- Jika **tidak bisa**: Penjelasan mengapa (jumlah eigenvector < n)

### 11.4 Contoh Penggunaan

**Langkah**:
1. Klik **Diagonalisasi** di sidebar
2. Isi matriks persegi
3. Klik **⚡ Diagonalisasi**

### 11.5 Kapan Matriks Tidak Bisa Didiagonalisasi?
- Ketika multiplisitas geometri < multiplisitas aljabar untuk suatu eigenvalue
- Contoh: Matriks [[1, 1], [0, 1]] — hanya punya 1 eigenvector independen

---

## 12. Fitur 7: SVD (Singular Value Decomposition)

### Akses: Klik "SVD" di sidebar atau tekan `Ctrl+7`

### 12.1 Deskripsi
Mendekomposisi matriks (tidak harus persegi) menjadi A = U·Σ·Vᵀ, dimana:
- **U** = Matriks orthogonal (m×m)
- **Σ** = Matriks diagonal singular values (m×n)
- **Vᵀ** = Transpose matriks orthogonal (n×n)

### 12.2 Input yang Diperlukan
- **Matriks m×n** (boleh persegi maupun non-persegi)

### 12.3 Output
- Matriks U, Σ, Vᵀ (dalam bentuk desimal)
- Daftar singular values: σ₁ ≥ σ₂ ≥ ... ≥ 0
- Rank matriks
- Verifikasi rekonstruksi A = U·Σ·Vᵀ

### 12.4 Contoh Penggunaan

**Soal**: Hitung SVD dari matriks 3×2:
```
| 1  2 |
| 3  4 |
| 5  6 |
```

**Langkah**:
1. Klik **SVD** di sidebar
2. Set dimensi: Baris=3, Kolom=2
3. Isi matriks
4. Klik **⚡ Hitung SVD**

### 12.5 Catatan
- SVD menggunakan komputasi **numerik** (numpy), bukan simbolik
- Hasil ditampilkan dalam bentuk desimal (4 digit)
- Rank dihitung berdasarkan singular values yang > threshold

---

## 13. Keyboard Shortcuts

### Navigasi

| Shortcut | Aksi |
|----------|------|
| `Ctrl+1` | Buka halaman SPL |
| `Ctrl+2` | Buka halaman Determinan |
| `Ctrl+3` | Buka halaman Invers |
| `Ctrl+4` | Buka halaman Dekomposisi LU |
| `Ctrl+5` | Buka halaman Eigen |
| `Ctrl+6` | Buka halaman Diagonalisasi |
| `Ctrl+7` | Buka halaman SVD |
| `Escape` | Kembali ke Dashboard |

### Aksi

| Shortcut | Aksi |
|----------|------|
| `Ctrl+Enter` | Hitung (execute) |
| `Ctrl+L` | Clear semua input |
| `Ctrl+Shift+C` | Copy hasil ke clipboard |
| `Ctrl+V` | Paste matriks dari clipboard |

### Navigasi Cell Matriks

| Shortcut | Aksi |
|----------|------|
| `Tab` | Cell berikutnya |
| `Shift+Tab` | Cell sebelumnya |
| `↑` | Cell atas |
| `↓` | Cell bawah |
| `←` | Cell kiri (jika cursor di awal) |
| `→` | Cell kanan (jika cursor di akhir) |

---

## 14. Fitur Tambahan

### 14.1 Dark/Light Mode

- Klik switch **🌙 Dark Mode** di bagian bawah sidebar
- Mode akan langsung berubah tanpa restart
- Dark mode: nyaman untuk penggunaan malam hari
- Light mode: nyaman untuk penggunaan siang hari

### 14.2 Copy Hasil

Di bagian atas Result Console terdapat tombol:
- **Copy** — Salin seluruh output sebagai plain text
- **LaTeX** — Salin matriks dalam format LaTeX (`\begin{bmatrix}...\end{bmatrix}`)
- **Clear** — Hapus semua output

Setelah copy berhasil, header console akan berubah hijau sesaat sebagai konfirmasi.

### 14.3 Error Handling

Semua error ditampilkan sebagai **banner inline** (bukan pop-up):
- 🔴 **Error** (merah): Input tidak valid, matriks singular, dll.
- 🟡 **Warning** (kuning): Peringatan (matriks mendekati singular)
- 🟢 **Success** (hijau): Perhitungan berhasil
- 🔵 **Info** (biru): Informasi tambahan

Banner akan otomatis hilang setelah 5 detik, atau bisa ditutup manual dengan tombol ×.

### 14.4 Responsive Sidebar

- Jika window diperkecil (lebar < 1000px), sidebar otomatis collapse menjadi icon-only
- Jika window diperbesar kembali, sidebar expand ke ukuran normal
- Minimum ukuran window: 900×600

### 14.5 Status Bar

Di bagian paling bawah window:
- **Kiri**: Menampilkan halaman yang sedang aktif
- **Tengah**: Hint keyboard shortcuts
- **Kanan**: Status terakhir (misal: "✓ Hasil disalin ke clipboard")

---

## 15. Troubleshooting

### Masalah Umum

| Masalah | Solusi |
|---------|--------|
| Aplikasi tidak bisa dibuka | Pastikan Python 3.9+ terinstall dan semua library sudah di-install |
| Error "No module named customtkinter" | Jalankan: `pip install customtkinter` |
| Error "No module named sympy" | Jalankan: `pip install sympy` |
| Tampilan terlalu kecil | Perbesar window (minimum 900×600) |
| Font tidak muncul dengan benar | Pastikan font "Segoe UI" dan "Consolas" tersedia di sistem |
| Matriks tidak bisa di-paste | Pastikan data di clipboard berformat tab-separated atau space-separated |
| Perhitungan lambat | Normal untuk matriks besar (>6×6) terutama pada fitur Eigen dan SVD |
| Theme tidak berubah | Klik switch di sidebar bawah, pastikan posisi switch berubah |

### Pesan Error dan Artinya

| Pesan Error | Arti | Solusi |
|-------------|------|--------|
| "Matriks harus persegi!" | Jumlah baris ≠ kolom | Samakan dimensi baris dan kolom |
| "Matriks singular (det = 0)" | Determinan = 0 | Matriks tidak punya invers, gunakan metode lain |
| "Input tidak valid di baris X, kolom Y" | Cell berisi karakter yang tidak dikenali | Isi hanya angka, pecahan (1/3), atau desimal |
| "Jumlah baris A harus sama dengan baris b" | Dimensi A dan b tidak cocok | Samakan jumlah baris A dengan baris b |
| "Tidak ada solusi" | SPL inkonsisten | Sistem persamaan tidak memiliki solusi |
| "Metode Sarrus hanya untuk 3×3" | Dimensi bukan 3×3 | Ubah dimensi ke 3×3 atau pilih metode lain |

### Menjalankan Test

Untuk memverifikasi semua fitur berjalan dengan benar:
```
cd "e:\Folder Tugas-Q\AlJabar Linear\CODING"
python tests/test_all.py
```

Hasil yang diharapkan: **44/44 tests passed, 0 failed**

---

## 📝 Catatan Akhir

Aplikasi ini dikembangkan menggunakan arsitektur modular:
- **`main.py`** — Entry point
- **`app.py`** — Main window & navigation
- **`components/`** — Widget UI reusable
- **`pages/`** — Halaman fitur (7 halaman)
- **`logic/`** — Engine perhitungan step-by-step
- **`utils/`** — Helper functions

Untuk pertanyaan atau laporan bug, silakan hubungi pengembang.

---

*Linear Algebra Dashboard Pro — Dibuat dengan ❤️ menggunakan Python & CustomTkinter*
