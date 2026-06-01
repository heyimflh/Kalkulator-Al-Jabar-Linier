<div align="center">

# 🧮 Linear Algebra Dashboard Pro

### Kalkulator Aljabar Linear Modern Berbasis GUI dengan Output Step-by-Step

<p>
  <b>Aplikasi desktop Python untuk membantu mahasiswa memahami dan menyelesaikan perhitungan aljabar linear secara visual, rapi, dan interaktif.</b>
</p>

<br>

![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![CustomTkinter](https://img.shields.io/badge/CustomTkinter-Modern_GUI-1f6feb?style=for-the-badge)
![SymPy](https://img.shields.io/badge/SymPy-Symbolic_Math-3B5526?style=for-the-badge)
![NumPy](https://img.shields.io/badge/NumPy-Numerical_Computing-013243?style=for-the-badge&logo=numpy&logoColor=white)
![Status](https://img.shields.io/badge/Status-Active-success?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

<br>

<p>
  <a href="#-tentang-aplikasi">Tentang</a> •
  <a href="#-fitur-utama">Fitur</a> •
  <a href="#-instalasi">Instalasi</a> •
  <a href="#-cara-menggunakan">Cara Menggunakan</a> •
  <a href="#-struktur-project">Struktur Project</a> •
  <a href="#-testing">Testing</a>
</p>

</div>

---

## ✨ Tentang Aplikasi

**Linear Algebra Dashboard Pro** adalah aplikasi kalkulator aljabar linear modern berbasis **Python GUI** yang dirancang untuk membantu pengguna menyelesaikan berbagai perhitungan aljabar linear dengan cara yang lebih mudah dipahami.

Aplikasi ini tidak hanya menampilkan hasil akhir, tetapi juga menampilkan proses penyelesaian secara **step-by-step**, sehingga cocok digunakan untuk:

- Mahasiswa yang sedang belajar Aljabar Linear.
- Dosen atau asisten praktikum yang ingin mendemonstrasikan proses perhitungan.
- Pelajar yang ingin memahami operasi matriks secara visual.
- Pengguna umum yang membutuhkan kalkulator matriks dengan tampilan modern.
- Developer pemula yang ingin mempelajari struktur aplikasi Python GUI modular.

Aplikasi ini dibuat dengan konsep **single-window dashboard**, sehingga semua fitur berada dalam satu jendela utama tanpa banyak pop-up yang membingungkan.

---

## 🌌 Preview Konsep Tampilan

> Tambahkan screenshot aplikasi di folder `assets/` atau `docs/`, lalu ubah path gambar di bawah sesuai nama file screenshot kamu.

<div align="center">

### Dashboard Utama

![Dashboard Preview](docs/screenshot-dashboard.png)

### Contoh Output Step-by-Step

![Step by Step Preview](docs/screenshot-step-by-step.png)

</div>

Jika belum punya screenshot, bagian gambar di atas bisa dibiarkan dulu atau dihapus sementara.

---

## 🎯 Tujuan Project

Project ini dibuat untuk menghadirkan kalkulator aljabar linear yang:

1. **Mudah digunakan** oleh user awam.
2. **Tidak hanya memberi jawaban akhir**, tetapi juga menjelaskan prosesnya.
3. **Memiliki tampilan modern**, tidak seperti aplikasi kalkulator matriks sederhana berbasis terminal.
4. **Mendukung berbagai metode aljabar linear penting**.
5. **Bersifat modular**, sehingga mudah dikembangkan lagi.
6. **Cocok untuk pembelajaran**, tugas kuliah, praktikum, dan demonstrasi materi.

---

## 🚀 Fitur Utama

Aplikasi ini memiliki 7 fitur utama:

| No | Fitur | Keterangan Singkat |
|---:|------|--------------------|
| 1 | **SPL** | Menyelesaikan Sistem Persamaan Linear |
| 2 | **Determinan** | Menghitung determinan matriks |
| 3 | **Invers** | Menghitung invers matriks |
| 4 | **Dekomposisi LU** | Menguraikan matriks menjadi PA = LU |
| 5 | **Eigenvalue & Eigenvector** | Menghitung nilai eigen dan vektor eigen |
| 6 | **Diagonalisasi** | Membentuk A = P D P⁻¹ |
| 7 | **SVD** | Melakukan Singular Value Decomposition |

Selain fitur matematika, aplikasi juga dilengkapi dengan:

- Dashboard modern.
- Sidebar navigation.
- Dark mode dan light mode.
- Input matriks visual berbentuk grid.
- Output step-by-step.
- Result console.
- Copy hasil perhitungan.
- Validasi input otomatis.
- Shortcut keyboard.
- Error banner yang ramah pengguna.
- Struktur project modular.
- Testing untuk memastikan fungsi berjalan dengan benar.

---

# 🧩 Detail Fitur

## 1. SPL — Sistem Persamaan Linear

Fitur **SPL** digunakan untuk menyelesaikan sistem persamaan linear dalam bentuk:

```text
Ax = b
````

Di mana:

* `A` adalah matriks koefisien.
* `x` adalah vektor variabel.
* `b` adalah vektor konstanta.

### Metode yang Tersedia

#### a. Eliminasi Gauss

Metode ini mengubah matriks augmented `[A|b]` menjadi bentuk **Row Echelon Form**.

Aplikasi akan menampilkan:

* Matriks augmented awal.
* Setiap operasi baris elementer.
* Bentuk akhir hasil eliminasi.
* Proses back substitution.
* Solusi akhir.

#### b. Gauss-Jordan

Metode ini mengubah matriks augmented `[A|b]` menjadi **Reduced Row Echelon Form**.

Kelebihannya:

* Solusi bisa langsung dibaca dari matriks akhir.
* Cocok untuk pembelajaran karena prosesnya sangat jelas.
* Menampilkan setiap langkah operasi baris.

#### c. Matriks Balikan

Metode ini menggunakan rumus:

```text
x = A⁻¹ b
```

Syarat:

* Matriks `A` harus persegi.
* Matriks `A` harus memiliki invers.
* Determinan `A` tidak boleh sama dengan 0.

### Kemungkinan Output

Aplikasi dapat mendeteksi beberapa kondisi:

* Solusi unik.
* Tidak ada solusi.
* Solusi tak hingga.
* Dimensi input tidak sesuai.
* Matriks singular atau tidak valid.

---

## 2. Determinan

Fitur **Determinan** digunakan untuk menghitung nilai determinan dari matriks persegi.

### Metode yang Tersedia

#### a. Kofaktor

Metode ekspansi kofaktor cocok untuk memahami konsep dasar determinan.

Aplikasi akan menampilkan:

* Minor matriks.
* Kofaktor.
* Proses ekspansi.
* Hasil akhir determinan.

#### b. Reduksi Baris

Metode ini menggunakan operasi baris untuk mengubah matriks menjadi segitiga atas.

Konsep utama:

```text
det(A) = (-1)^jumlah_swap × hasil_kali_elemen_diagonal
```

Aplikasi akan menampilkan proses eliminasi baris secara bertahap.

#### c. Sarrus

Metode Sarrus hanya berlaku untuk matriks 3×3.

Aplikasi akan menampilkan:

* Diagonal positif.
* Diagonal negatif.
* Perhitungan selisih diagonal.
* Hasil akhir determinan.

### Catatan

Fitur determinan hanya menerima matriks persegi:

```text
2×2, 3×3, 4×4, ..., n×n
```

Jika jumlah baris dan kolom tidak sama, aplikasi akan menampilkan pesan error.

---

## 3. Invers Matriks

Fitur **Invers** digunakan untuk menghitung invers dari suatu matriks persegi.

Syarat matriks memiliki invers:

* Matriks harus persegi.
* Determinan tidak boleh 0.
* Matriks tidak singular.

### Metode yang Tersedia

#### a. Adjugate

Menggunakan rumus:

```text
A⁻¹ = (1 / det(A)) × adj(A)
```

Aplikasi akan menampilkan:

* Determinan.
* Matriks kofaktor.
* Matriks adjugate.
* Hasil invers.

#### b. Gauss-Jordan

Menggunakan bentuk augmented:

```text
[A | I] → [I | A⁻¹]
```

Aplikasi akan menampilkan setiap operasi baris sampai invers ditemukan.

#### c. Built-in

Menggunakan fungsi bawaan dari library matematika untuk menghitung invers secara cepat.

Cocok untuk:

* Matriks ukuran lebih besar.
* Pengguna yang hanya butuh hasil akhir.
* Verifikasi perhitungan manual.

---

## 4. Dekomposisi LU

Fitur **Dekomposisi LU** digunakan untuk memecah matriks menjadi:

```text
PA = LU
```

Di mana:

* `P` adalah matriks permutasi.
* `A` adalah matriks awal.
* `L` adalah lower triangular matrix.
* `U` adalah upper triangular matrix.

### Output yang Ditampilkan

Aplikasi akan menampilkan:

* Matriks `P`.
* Matriks `L`.
* Matriks `U`.
* Verifikasi `PA = LU`.

Fitur ini sangat berguna untuk memahami metode penyelesaian sistem linear dan optimasi komputasi matriks.

---

## 5. Eigenvalue & Eigenvector

Fitur **Eigen** digunakan untuk mencari nilai eigen dan vektor eigen dari suatu matriks persegi.

### Output yang Ditampilkan

Aplikasi akan menampilkan:

1. Matriks input.
2. Polinomial karakteristik.
3. Eigenvalue.
4. Multiplisitas aljabar.
5. Eigenvector.
6. Basis eigenspace.
7. Informasi apakah matriks dapat didiagonalisasi.

### Bentuk Umum

```text
Av = λv
```

Di mana:

* `A` adalah matriks.
* `v` adalah eigenvector.
* `λ` adalah eigenvalue.

---

## 6. Diagonalisasi

Fitur **Diagonalisasi** digunakan untuk membentuk faktorisasi:

```text
A = P D P⁻¹
```

Di mana:

* `P` adalah matriks yang berisi eigenvector sebagai kolom.
* `D` adalah matriks diagonal yang berisi eigenvalue.
* `P⁻¹` adalah invers dari matriks `P`.

### Output yang Ditampilkan

Jika matriks bisa didiagonalisasi, aplikasi akan menampilkan:

* Eigenvalue.
* Eigenvector.
* Matriks `P`.
* Matriks `D`.
* Matriks `P⁻¹`.
* Verifikasi `A = P D P⁻¹`.

Jika matriks tidak bisa didiagonalisasi, aplikasi akan memberikan alasan, misalnya jumlah eigenvector independen tidak cukup.

---

## 7. SVD — Singular Value Decomposition

Fitur **SVD** digunakan untuk mendekomposisi matriks menjadi:

```text
A = U Σ Vᵀ
```

Di mana:

* `U` adalah matriks orthogonal.
* `Σ` adalah matriks diagonal berisi singular values.
* `Vᵀ` adalah transpose dari matriks orthogonal `V`.

### Keunggulan SVD

SVD dapat digunakan untuk matriks:

* Persegi.
* Tidak persegi.
* Rank penuh.
* Rank kurang.
* Matriks numerik.

### Output yang Ditampilkan

Aplikasi akan menampilkan:

* Matriks `U`.
* Matriks `Σ`.
* Matriks `Vᵀ`.
* Singular values.
* Rank matriks.
* Verifikasi rekonstruksi `A = U Σ Vᵀ`.

---

# 🖥️ Tampilan dan UX

## Single-Window Dashboard

Aplikasi menggunakan konsep **single-window dashboard**, artinya seluruh fitur berada dalam satu jendela utama.

Pengguna cukup memilih fitur melalui sidebar, lalu input dan hasil akan muncul di area kerja utama.

```text
┌─────────────────────┬──────────────────────────────────────────┐
│      SIDEBAR        │              CONTENT AREA                │
│                     │                                          │
│  ⊞ SPL              │  Header                                  │
│  ⊡ Determinan       │  Method Selector                         │
│  ⊟ Invers           │  Matrix Input Grid                       │
│  △ LU               │  Action Button                           │
│  λ Eigen            │  Result Console                          │
│  ⋱ Diagonalisasi    │                                          │
│  Σ SVD              │                                          │
│                     │                                          │
│  Dark / Light Mode  │  Status Bar                              │
└─────────────────────┴──────────────────────────────────────────┘
```

---

## Dark Mode dan Light Mode

Aplikasi mendukung dua mode tampilan:

### Dark Mode

Cocok digunakan saat malam hari atau ketika ingin tampilan yang lebih nyaman di mata.

### Light Mode

Cocok digunakan saat siang hari, presentasi, atau dokumentasi laporan.

Mode dapat diubah melalui tombol switch di sidebar.

---

## Matrix Input Grid

Input matriks dibuat dalam bentuk grid visual.

Pengguna dapat:

* Mengatur jumlah baris.
* Mengatur jumlah kolom.
* Mengisi angka langsung pada cell.
* Menggunakan tombol cepat seperti Clear, Random, Identity, Transpose, dan Paste.
* Menavigasi antar-cell menggunakan keyboard.

---

## Result Console

Result console digunakan untuk menampilkan:

* Matriks input.
* Langkah-langkah penyelesaian.
* Operasi baris elementer.
* Hasil akhir.
* Verifikasi hasil.
* Pesan error atau warning.

Output dibuat agar mudah dibaca dan cocok digunakan untuk belajar.

---

# 🧠 Format Input yang Didukung

Aplikasi menerima beberapa format angka:

| Format  | Contoh         | Keterangan            |
| ------- | -------------- | --------------------- |
| Integer | `5`, `-3`, `0` | Bilangan bulat        |
| Desimal | `1.5`, `-0.25` | Bilangan desimal      |
| Pecahan | `1/2`, `-3/4`  | Pecahan eksak         |
| Kosong  | kosong         | Otomatis dianggap `0` |

Contoh input matriks:

```text
2  1  -1
4  5   1
1  2   3
```

---

# ⌨️ Keyboard Shortcuts

## Navigasi Halaman

| Shortcut   | Fungsi                      |
| ---------- | --------------------------- |
| `Ctrl + 1` | Buka halaman SPL            |
| `Ctrl + 2` | Buka halaman Determinan     |
| `Ctrl + 3` | Buka halaman Invers         |
| `Ctrl + 4` | Buka halaman Dekomposisi LU |
| `Ctrl + 5` | Buka halaman Eigen          |
| `Ctrl + 6` | Buka halaman Diagonalisasi  |
| `Ctrl + 7` | Buka halaman SVD            |
| `Escape`   | Kembali ke dashboard utama  |

## Aksi Cepat

| Shortcut           | Fungsi                       |
| ------------------ | ---------------------------- |
| `Ctrl + Enter`     | Jalankan perhitungan         |
| `Ctrl + L`         | Clear input                  |
| `Ctrl + Shift + C` | Copy hasil                   |
| `Ctrl + V`         | Paste matriks dari clipboard |

## Navigasi Cell Matriks

| Shortcut      | Fungsi                    |
| ------------- | ------------------------- |
| `Tab`         | Pindah ke cell berikutnya |
| `Shift + Tab` | Pindah ke cell sebelumnya |
| `↑`           | Pindah ke cell atas       |
| `↓`           | Pindah ke cell bawah      |
| `←`           | Pindah ke cell kiri       |
| `→`           | Pindah ke cell kanan      |

---

# 📦 Tech Stack

Project ini dibuat menggunakan:

| Teknologi                | Fungsi                                       |
| ------------------------ | -------------------------------------------- |
| **Python**               | Bahasa utama aplikasi                        |
| **CustomTkinter**        | Framework GUI modern                         |
| **Tkinter**              | Basis GUI bawaan Python                      |
| **SymPy**                | Perhitungan simbolik dan eksak               |
| **NumPy**                | Perhitungan numerik, terutama SVD            |
| **Threading**            | Menjaga UI tetap responsif saat proses berat |
| **Regex**                | Validasi input matriks                       |
| **Modular Architecture** | Memisahkan UI, logic, pages, dan utilities   |

---

# ✅ Persyaratan Sistem

## Minimum

| Komponen       | Spesifikasi                           |
| -------------- | ------------------------------------- |
| OS             | Windows 10/11, macOS, atau Linux      |
| Python         | Python 3.9 atau lebih baru            |
| RAM            | 4 GB                                  |
| Resolusi Layar | Minimal 900×600                       |
| Storage        | Ringan, hanya membutuhkan ruang kecil |

## Direkomendasikan

| Komponen       | Spesifikasi                |
| -------------- | -------------------------- |
| OS             | Windows 10/11              |
| Python         | Python 3.10+               |
| RAM            | 8 GB                       |
| Resolusi Layar | 1280×720 atau lebih tinggi |

---

# ⚙️ Instalasi

## 1. Clone Repository

Buka terminal atau command prompt, lalu jalankan:

```bash
git clone https://github.com/heyimflh/Kalkulator-Al-Jabar-Linier.git
```

Masuk ke folder project:

```bash
cd Kalkulator-Al-Jabar-Linier
```

---

## 2. Buat Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3. Install Dependencies

Install library yang dibutuhkan:

```bash
pip install customtkinter sympy numpy
```

Jika ingin memastikan pip sudah versi terbaru:

```bash
python -m pip install --upgrade pip
```

---

## 4. Jalankan Aplikasi

```bash
python main.py
```

Jika berhasil, aplikasi akan terbuka dengan tampilan dashboard utama.

---

# 🧭 Cara Menggunakan

## Langkah Umum

1. Jalankan aplikasi dengan `python main.py`.
2. Pilih fitur melalui sidebar.
3. Pilih metode perhitungan jika tersedia.
4. Atur jumlah baris dan kolom matriks.
5. Isi nilai matriks pada grid input.
6. Klik tombol hitung.
7. Lihat hasil dan langkah-langkah pada result console.
8. Copy hasil jika diperlukan untuk laporan atau catatan.

---

# 📚 Contoh Penggunaan

## Contoh 1 — Menyelesaikan SPL

Misalkan ingin menyelesaikan:

```text
2x + y - z = 5
4x + 5y + z = 13
x + 2y + 3z = 12
```

Maka:

### Matriks A

```text
2  1  -1
4  5   1
1  2   3
```

### Vektor b

```text
5
13
12
```

Langkah:

1. Klik menu **SPL**.
2. Pilih metode **Gauss** atau **Gauss-Jordan**.
3. Isi matriks A.
4. Isi vektor b.
5. Klik **Hitung SPL**.
6. Baca hasil pada result console.

---

## Contoh 2 — Menghitung Determinan

Matriks:

```text
1  2  3
4  5  6
7  8  0
```

Langkah:

1. Klik menu **Determinan**.
2. Pilih metode **Sarrus (3×3)**.
3. Isi matriks 3×3.
4. Klik **Hitung Determinan**.
5. Lihat proses diagonal positif, diagonal negatif, dan hasil akhir.

---

## Contoh 3 — Menghitung Invers

Matriks:

```text
2  1
5  3
```

Langkah:

1. Klik menu **Invers**.
2. Pilih metode **Gauss-Jordan**.
3. Isi matriks 2×2.
4. Klik **Hitung Invers**.
5. Lihat proses `[A|I] → [I|A⁻¹]`.

---

## Contoh 4 — Dekomposisi LU

Matriks:

```text
4  3
6  3
```

Langkah:

1. Klik menu **Dekomposisi LU**.
2. Isi matriks persegi.
3. Klik **Hitung LU**.
4. Aplikasi akan menampilkan `P`, `L`, `U`, dan verifikasi `PA = LU`.

---

## Contoh 5 — Eigenvalue dan Eigenvector

Matriks:

```text
4  1
2  3
```

Langkah:

1. Klik menu **Eigen**.
2. Isi matriks 2×2.
3. Klik **Hitung Eigen**.
4. Aplikasi akan menampilkan polinomial karakteristik, eigenvalue, eigenvector, dan informasi diagonalisasi.

---

## Contoh 6 — Diagonalisasi

Matriks:

```text
4  1
2  3
```

Langkah:

1. Klik menu **Diagonalisasi**.
2. Isi matriks persegi.
3. Klik **Diagonalisasi**.
4. Jika bisa didiagonalisasi, aplikasi menampilkan `P`, `D`, `P⁻¹`, dan verifikasi `A = P D P⁻¹`.

---

## Contoh 7 — SVD

Matriks:

```text
1  2
3  4
5  6
```

Langkah:

1. Klik menu **SVD**.
2. Atur matriks menjadi 3×2.
3. Isi nilai matriks.
4. Klik **Hitung SVD**.
5. Aplikasi akan menampilkan `U`, `Σ`, `Vᵀ`, singular values, rank, dan verifikasi.

---

# 🗂️ Struktur Project

Struktur utama project:

```text
Kalkulator-Al-Jabar-Linier/
│
├── main.py
├── app.py
├── config.py
├── README.md
├── MANUAL_BOOK.md
├── Plan_Design.md
│
├── components/
│   ├── __init__.py
│   ├── error_banner.py
│   ├── matrix_input.py
│   ├── method_selector.py
│   ├── result_console.py
│   ├── sidebar.py
│   ├── status_bar.py
│   └── tooltip.py
│
├── logic/
│   ├── __init__.py
│   └── step_engine.py
│
├── pages/
│   ├── __init__.py
│   ├── spl_page.py
│   ├── determinan_page.py
│   ├── invers_page.py
│   ├── lu_page.py
│   ├── eigen_page.py
│   ├── diagonal_page.py
│   └── svd_page.py
│
├── utils/
│   └── ...
│
└── tests/
    └── test_all.py
```

---

# 🧱 Penjelasan Arsitektur

Project ini menggunakan arsitektur modular agar mudah dipahami dan dikembangkan.

## `main.py`

File entry point aplikasi.

Tugasnya:

* Menjalankan aplikasi.
* Memanggil class utama dari `app.py`.
* Menjalankan event loop GUI.

---

## `app.py`

File utama untuk window aplikasi.

Tugasnya:

* Membuat window utama.
* Mengatur layout dashboard.
* Membuat sidebar.
* Membuat content area.
* Mengatur navigasi antar halaman.
* Mengatur shortcut keyboard.
* Mengatur theme toggle.
* Menampilkan halaman welcome/dashboard.

---

## `config.py`

File konfigurasi global.

Berisi:

* Warna dark mode.
* Warna light mode.
* Font.
* Ukuran window.
* Ukuran sidebar.
* Maksimal dimensi matriks.
* Daftar menu utama.

---

## `components/`

Folder ini berisi komponen UI reusable.

### `matrix_input.py`

Komponen input matriks visual.

Fitur:

* Grid input dinamis.
* Selector baris dan kolom.
* Validasi input.
* Navigasi dengan keyboard.
* Clear.
* Random.
* Identity.
* Transpose.
* Paste dari clipboard.

### `result_console.py`

Komponen output hasil.

Fitur:

* Menampilkan hasil perhitungan.
* Menampilkan step-by-step.
* Copy hasil.
* Clear console.
* Format matriks agar mudah dibaca.

### `method_selector.py`

Komponen untuk memilih metode perhitungan.

Contoh:

* Gauss.
* Gauss-Jordan.
* Matriks Balikan.
* Kofaktor.
* Reduksi Baris.
* Sarrus.

### `error_banner.py`

Komponen untuk menampilkan pesan error, warning, info, atau success secara inline.

### `sidebar.py`

Komponen navigasi utama di sisi kiri aplikasi.

### `status_bar.py`

Komponen status bar di bagian bawah aplikasi.

### `tooltip.py`

Komponen bantuan kecil ketika user hover pada elemen tertentu.

---

## `logic/`

Folder ini berisi logika perhitungan.

### `step_engine.py`

Engine utama untuk proses step-by-step.

Digunakan oleh beberapa fitur seperti:

* SPL.
* Determinan dengan reduksi baris.
* Invers dengan Gauss-Jordan.

Fungsi utamanya meliputi:

* Eliminasi Gauss.
* Eliminasi Gauss-Jordan.
* Invers dengan Gauss-Jordan.
* Determinan dengan eliminasi.
* Penyelesaian SPL.
* Format output matriks.

---

## `pages/`

Folder ini berisi halaman fitur.

Setiap fitur memiliki file halaman sendiri:

| File                 | Fungsi                             |
| -------------------- | ---------------------------------- |
| `spl_page.py`        | Halaman Sistem Persamaan Linear    |
| `determinan_page.py` | Halaman Determinan                 |
| `invers_page.py`     | Halaman Invers Matriks             |
| `lu_page.py`         | Halaman Dekomposisi LU             |
| `eigen_page.py`      | Halaman Eigenvalue dan Eigenvector |
| `diagonal_page.py`   | Halaman Diagonalisasi              |
| `svd_page.py`        | Halaman SVD                        |

---

## `utils/`

Folder helper untuk fungsi pendukung seperti formatting matriks, formatting angka, dan utility lain.

---

## `tests/`

Folder untuk pengujian aplikasi.

Digunakan untuk memastikan logic matematika berjalan sesuai ekspektasi.

---

# 🔄 Alur Kerja Aplikasi

Alur sederhana aplikasi:

```text
User memilih fitur
        ↓
User mengisi matriks
        ↓
MatrixInputWidget memvalidasi input
        ↓
Page mengambil data matriks
        ↓
Logic engine melakukan perhitungan
        ↓
ResultConsole menampilkan langkah dan hasil
        ↓
User dapat menyalin hasil
```

---

# 🧪 Testing

Untuk menjalankan test:

```bash
python tests/test_all.py
```

Output yang diharapkan:

```text
44/44 tests passed
```

Jika ada test yang gagal:

1. Pastikan semua dependencies sudah terinstall.
2. Pastikan kamu menjalankan test dari root folder project.
3. Pastikan versi Python sudah sesuai.
4. Cek apakah ada perubahan logic pada file di folder `logic/` atau `pages/`.

---

# 🛠️ Troubleshooting

## 1. Aplikasi tidak bisa dibuka

Pastikan Python sudah terinstall:

```bash
python --version
```

Jika belum ada, install Python terlebih dahulu dari website resmi Python.

---

## 2. Error `No module named customtkinter`

Install CustomTkinter:

```bash
pip install customtkinter
```

---

## 3. Error `No module named sympy`

Install SymPy:

```bash
pip install sympy
```

---

## 4. Error `No module named numpy`

Install NumPy:

```bash
pip install numpy
```

---

## 5. Tampilan terlalu kecil atau terpotong

Solusi:

* Perbesar ukuran window.
* Gunakan resolusi minimal 900×600.
* Jika memungkinkan, gunakan layar dengan resolusi 1280×720 atau lebih besar.

---

## 6. Perhitungan terasa lambat

Beberapa fitur memang bisa lebih berat, terutama:

* Eigenvalue untuk matriks besar.
* Diagonalisasi untuk matriks besar.
* SVD untuk matriks besar.
* Kofaktor untuk matriks besar.

Solusi:

* Gunakan matriks ukuran kecil saat belajar konsep.
* Gunakan metode numerik jika tersedia.
* Hindari matriks terlalu besar jika hanya ingin melihat step-by-step.

---

## 7. Matriks tidak bisa dihitung

Cek beberapa hal berikut:

* Apakah input hanya berisi angka, desimal, atau pecahan?
* Apakah matriks harus persegi untuk fitur yang dipilih?
* Apakah dimensi matriks sudah sesuai?
* Apakah ada cell kosong yang tidak sengaja berisi karakter lain?
* Apakah metode yang dipilih sesuai ukuran matriks?

---

## 8. Error “Matriks harus persegi”

Artinya jumlah baris dan kolom tidak sama.

Contoh valid:

```text
2×2
3×3
4×4
```

Contoh tidak valid untuk fitur tertentu:

```text
2×3
3×2
4×5
```

Fitur yang membutuhkan matriks persegi:

* Determinan.
* Invers.
* LU.
* Eigen.
* Diagonalisasi.

SVD dapat menerima matriks tidak persegi.

---

## 9. Error “Matriks singular”

Artinya matriks tidak memiliki invers.

Biasanya terjadi ketika:

```text
det(A) = 0
```

Matriks singular tidak bisa digunakan untuk:

* Invers.
* SPL metode matriks balikan.
* Beberapa bentuk diagonalisasi tertentu.

---

# 📌 Tips Penggunaan untuk User Awam

## Gunakan Ukuran Matriks Kecil Terlebih Dahulu

Jika baru belajar, gunakan matriks:

```text
2×2
3×3
```

Matriks kecil lebih mudah dipahami dan output step-by-step tidak terlalu panjang.

---

## Gunakan Pecahan untuk Hasil Eksak

Aplikasi mendukung input pecahan seperti:

```text
1/2
-3/4
2/5
```

Ini membantu menghasilkan perhitungan yang lebih rapi dan eksak.

---

## Gunakan Tombol Random untuk Latihan

Tombol **Random** dapat digunakan untuk membuat matriks otomatis.

Cocok untuk:

* Latihan cepat.
* Testing fitur.
* Membuat contoh soal.
* Mengecek kemampuan aplikasi.

---

## Gunakan Identity untuk Membuat Matriks Identitas

Tombol **Identity** akan mengisi matriks dengan bentuk:

```text
1 0 0
0 1 0
0 0 1
```

Ini berguna untuk:

* Belajar invers.
* Belajar operasi matriks.
* Menguji fitur determinan.
* Menguji fitur diagonal.

---

## Gunakan Paste dari Excel

Jika punya data matriks di Excel atau spreadsheet:

1. Blok data matriks.
2. Tekan `Ctrl + C`.
3. Buka aplikasi.
4. Klik tombol **Paste**.
5. Data akan masuk ke grid.

---

# 🧾 Pesan Error dan Artinya

| Pesan                         | Arti                                | Solusi                                     |
| ----------------------------- | ----------------------------------- | ------------------------------------------ |
| Matriks harus persegi         | Baris dan kolom berbeda             | Samakan jumlah baris dan kolom             |
| Matriks singular              | Determinan 0                        | Gunakan matriks lain                       |
| Input tidak valid             | Ada karakter yang bukan angka       | Gunakan integer, desimal, atau pecahan     |
| Metode Sarrus hanya untuk 3×3 | Sarrus dipakai di matriks bukan 3×3 | Ubah matriks ke 3×3 atau pilih metode lain |
| Tidak ada solusi              | SPL tidak konsisten                 | Cek kembali persamaan                      |
| Solusi tak hingga             | Ada variabel bebas                  | Gunakan interpretasi solusi parametrik     |
| Perhitungan gagal             | Terjadi error pada proses hitung    | Cek input dan metode                       |

---

# 🧑‍💻 Untuk Developer

## Menambahkan Fitur Baru

Untuk menambahkan fitur baru:

1. Buat file page baru di folder `pages/`.
2. Buat class page baru menggunakan `ctk.CTkFrame`.
3. Gunakan komponen `MatrixInputWidget`.
4. Gunakan `ResultConsoleWidget` untuk output.
5. Tambahkan menu baru di `config.py`.
6. Tambahkan mapping page di `app.py`.
7. Tambahkan test di folder `tests/`.

---

## Pola Page yang Direkomendasikan

```python
class NewFeaturePage(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self._build_layout()

    def _build_layout(self):
        # build UI here
        pass

    def _on_calculate(self):
        # get matrix
        # validate input
        # call logic
        # render result
        pass
```

---

## Prinsip Arsitektur

Project ini mengikuti prinsip:

* **Separation of Concerns**
  UI, logic, dan utility dipisahkan.

* **Reusable Components**
  Input matriks, console, sidebar, dan banner dibuat sebagai komponen reusable.

* **Single Responsibility**
  Setiap file memiliki tanggung jawab yang jelas.

* **Readable Output**
  Hasil perhitungan diformat agar mudah dipahami.

* **User Friendly Error Handling**
  Error ditampilkan dalam bentuk banner, bukan crash.

---

# 📈 Roadmap Pengembangan

Beberapa ide pengembangan selanjutnya:

## UI/UX

* [ ] Tambahkan splash screen.
* [ ] Tambahkan animasi transisi antar halaman.
* [ ] Tambahkan mode compact untuk layar kecil.
* [ ] Tambahkan fitur export hasil ke `.txt`.
* [ ] Tambahkan fitur export hasil ke `.pdf`.
* [ ] Tambahkan screenshot resmi di README.
* [ ] Tambahkan icon aplikasi.

## Fitur Matematika

* [ ] Rank matriks.
* [ ] Trace matriks.
* [ ] Norm matriks.
* [ ] Gram-Schmidt.
* [ ] QR Decomposition.
* [ ] Projection.
* [ ] Basis dan dimensi ruang vektor.
* [ ] Transformasi linear.
* [ ] Cramer Rule.
* [ ] Least Squares.

## Developer Experience

* [ ] Tambahkan `requirements.txt`.
* [ ] Tambahkan `pyproject.toml`.
* [ ] Tambahkan GitHub Actions untuk testing otomatis.
* [ ] Tambahkan release executable Windows.
* [ ] Tambahkan dokumentasi kontribusi.
* [ ] Tambahkan unit test per modul.

---

# 📄 Rekomendasi File `requirements.txt`

Agar instalasi lebih mudah, kamu bisa membuat file:

```text
requirements.txt
```

Isi:

```txt
customtkinter
sympy
numpy
```

Lalu user cukup menjalankan:

```bash
pip install -r requirements.txt
```

---

# 📦 Build Menjadi Executable

Jika ingin aplikasi bisa dijalankan tanpa membuka Python secara manual, kamu dapat menggunakan PyInstaller.

Install PyInstaller:

```bash
pip install pyinstaller
```

Build aplikasi:

```bash
pyinstaller --onefile --windowed main.py
```

Hasil build akan muncul di folder:

```text
dist/
```

Catatan:

* Pastikan aplikasi berjalan normal sebelum di-build.
* Jika ada asset tambahan, konfigurasi PyInstaller perlu disesuaikan.
* Build executable biasanya perlu dilakukan di OS target.
  Misalnya, build `.exe` dilakukan di Windows.

---

# 🤝 Kontribusi

Kontribusi sangat terbuka.

Kamu dapat membantu dengan cara:

* Melaporkan bug.
* Mengusulkan fitur baru.
* Memperbaiki tampilan UI.
* Menambahkan test.
* Membuat dokumentasi.
* Mengoptimasi perhitungan.
* Membuat versi executable.

## Langkah Kontribusi

1. Fork repository ini.
2. Buat branch baru.

```bash
git checkout -b feature/nama-fitur
```

3. Lakukan perubahan.
4. Commit perubahan.

```bash
git commit -m "Add: nama fitur"
```

5. Push ke branch.

```bash
git push origin feature/nama-fitur
```

6. Buat Pull Request.

---

# 🧑‍🎓 Manfaat untuk Pembelajaran

Aplikasi ini sangat cocok digunakan dalam materi:

* Sistem Persamaan Linear.
* Operasi Matriks.
* Determinan.
* Invers Matriks.
* Eliminasi Gauss.
* Gauss-Jordan.
* Dekomposisi LU.
* Eigenvalue.
* Eigenvector.
* Diagonalisasi.
* Singular Value Decomposition.

Dengan output step-by-step, pengguna dapat melihat bukan hanya hasil akhir, tetapi juga proses matematis di baliknya.

---

# 🏆 Kelebihan Project

* Tampilan modern dan rapi.
* Cocok untuk mahasiswa.
* Mendukung banyak fitur penting aljabar linear.
* Output step-by-step.
* Input matriks visual.
* Mendukung pecahan.
* Ada dark mode dan light mode.
* Struktur project modular.
* Mudah dikembangkan.
* Cocok sebagai project akademik maupun portofolio.

---

# ⚠️ Batasan Aplikasi

Beberapa batasan yang perlu diperhatikan:

* Perhitungan simbolik untuk matriks besar dapat memerlukan waktu lebih lama.
* SVD menggunakan pendekatan numerik.
* Output step-by-step untuk matriks besar bisa sangat panjang.
* Beberapa metode hanya valid untuk matriks persegi.
* Sarrus hanya valid untuk matriks 3×3.
* Eigen dan diagonalisasi untuk matriks besar dapat lebih berat secara komputasi.

---

# 📜 Lisensi

Project ini menggunakan lisensi **MIT**.

Jika file `LICENSE` belum tersedia di repository, disarankan untuk menambahkannya agar informasi lisensi lebih jelas.

---

# 👨‍💻 Author

Dibuat oleh:

**Muhammad Fakhri Abdullah**
GitHub: [@heyimflh](https://github.com/heyimflh)

---

# 🙏 Acknowledgements

Terima kasih untuk teknologi open-source yang digunakan dalam project ini:

* Python
* CustomTkinter
* Tkinter
* SymPy
* NumPy

Project ini dibuat sebagai bentuk eksplorasi dan implementasi pembelajaran Aljabar Linear dalam bentuk aplikasi desktop modern.

---

<div align="center">

## ⭐ Linear Algebra Dashboard Pro

<p>
  Belajar aljabar linear jadi lebih visual, lebih rapi, dan lebih mudah dipahami.
</p>

<p>
  Jika project ini bermanfaat, jangan lupa beri ⭐ di repository.
</p>

</div>

::contentReference[oaicite:2]{index=2}

[1]: https://github.com/heyimflh/Kalkulator-Al-Jabar-Linier.git "GitHub - heyimflh/Kalkulator-Al-Jabar-Linier: Kalkulator Aljabar Linear Modern — GUI Dashboard dengan Step-by-Step · GitHub"
[2]: https://raw.githubusercontent.com/heyimflh/Kalkulator-Al-Jabar-Linier/main/MANUAL_BOOK.md "raw.githubusercontent.com"
