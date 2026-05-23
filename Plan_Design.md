# 📐 Planning Lengkap: "The Modern Math Dashboard"
## Kalkulator Aljabar Linear — GUI Design & UX Masterplan

---

## 📋 Ringkasan Proyek

Transformasi total aplikasi Kalkulator Aljabar Linear dari sistem berbasis pop-up (`tkinter` standar) menjadi **Single-Window Dashboard** modern menggunakan `CustomTkinter`. Fokus utama: **usability**, **visual clarity**, dan **professional feel**.

---

## 🟢 Bagian 1: Stack Teknologi

| Komponen | Library | Fungsi |
|----------|---------|--------|
| Framework UI | `CustomTkinter` | Tampilan modern, rounded corners, dark/light mode |
| Core Math (Eksak) | `Sympy` | Pecahan, eigenvalue simbolik, polinomial karakteristik |
| Core Math (Numerik) | `Numpy` | SVD, operasi floating-point |
| Icon & Image | `Pillow` | Ikon sidebar, logo aplikasi |
| Font Rendering | `tkinter.font` | Fallback font system |
| Clipboard | `pyperclip` | Copy hasil ke clipboard (cross-platform) |

---

## 🔵 Bagian 2: Arsitektur Aplikasi

### 2.1 Single-Window System (Menggantikan Pop-up)

```
┌─────────────────────────────────────────────────────────────────┐
│  WINDOW (1200x750, resizable, min: 900x600)                    │
├────────────┬────────────────────────────────────────────────────┤
│            │                                                    │
│  SIDEBAR   │              MAIN CONTENT AREA                     │
│  (220px)   │                                                    │
│            │  ┌──────────────────────────────────────────────┐  │
│  ┌──────┐  │  │  HEADER: Judul Fitur + Breadcrumb            │  │
│  │ LOGO │  │  ├──────────────────────────────────────────────┤  │
│  └──────┘  │  │                                              │  │
│            │  │  INPUT SECTION                                │  │
│  ┌──────┐  │  │  - Dimension Selector (Row x Col)            │  │
│  │ SPL  │  │  │  - Dynamic Matrix Grid                       │  │
│  ├──────┤  │  │  - Method Selector (Radio/Segmented)         │  │
│  │ DET  │  │  │  - Action Buttons                            │  │
│  ├──────┤  │  │                                              │  │
│  │ INV  │  │  ├──────────────────────────────────────────────┤  │
│  ├──────┤  │  │                                              │  │
│  │ LU   │  │  │  RESULT CONSOLE                              │  │
│  ├──────┤  │  │  - Step-by-step output                       │  │
│  │EIGEN │  │  │  - Final result                              │  │
│  ├──────┤  │  │  - Copy button                               │  │
│  │DIAG  │  │  │                                              │  │
│  ├──────┤  │  └──────────────────────────────────────────────┘  │
│  │ SVD  │  │                                                    │
│  └──────┘  │                                                    │
│            │                                                    │
│  [🌙/☀️]  │                                                    │
└────────────┴────────────────────────────────────────────────────┘
```

### 2.2 Navigasi & State Management

- **Frame Switching**: Setiap menu memiliki dedicated `CTkFrame` yang di-show/hide (bukan destroy/recreate).
- **State Preservation**: Input matriks TETAP tersimpan saat user pindah menu dan kembali.
- **Active Menu Indicator**: Tombol sidebar yang aktif diberi highlight warna aksen.
- **Smooth Transition**: Fade-in effect saat berganti halaman (opsional, via `after()` scheduling).

### 2.3 Struktur Class (Modular)

```
ModernAlinApp (CTk)
├── SidebarFrame
│   ├── LogoSection
│   ├── MenuButtons (7 tombol)
│   └── ThemeSwitch
├── ContentManager
│   ├── SPLPage
│   ├── DeterminanPage
│   ├── InversPage
│   ├── LUPage
│   ├── EigenPage
│   ├── DiagonalisasiPage
│   └── SVDPage
├── MatrixInputWidget (reusable component)
├── ResultConsoleWidget (reusable component)
└── Helpers (format_matriks, normalisasi, dll)
```

---

## 🟡 Bagian 3: Skema Warna & Tema

### 3.1 Dark Mode — "Deep Space" (Default)

| Elemen | Hex | Keterangan |
|--------|-----|------------|
| Background Utama | `#1A1A2E` | Deep navy-black |
| Sidebar | `#16213E` | Slightly lighter navy |
| Card/Panel | `#0F3460` | Blue-tinted dark |
| Aksen Primer | `#E94560` | Coral-red untuk tombol utama |
| Aksen Sekunder | `#533483` | Purple untuk hover/active |
| Aksen Sukses | `#2D8A4E` | Green untuk hasil berhasil |
| Aksen Error | `#E74C3C` | Red untuk error state |
| Teks Utama | `#ECF0F1` | Off-white |
| Teks Sekunder | `#95A5A6` | Muted gray |
| Input Field BG | `#1E2A3A` | Slightly lighter dari card |
| Input Field Border | `#3498DB` | Blue border saat focus |

### 3.2 Light Mode — "Clean Slate"

| Elemen | Hex | Keterangan |
|--------|-----|------------|
| Background Utama | `#F8F9FA` | Near-white |
| Sidebar | `#FFFFFF` | Pure white dengan shadow |
| Card/Panel | `#FFFFFF` | White dengan subtle border |
| Aksen Primer | `#2563EB` | Royal blue |
| Aksen Sekunder | `#7C3AED` | Purple |
| Teks Utama | `#1F2937` | Near-black |
| Teks Sekunder | `#6B7280` | Medium gray |

### 3.3 Typography

| Penggunaan | Font | Size | Weight |
|------------|------|------|--------|
| Logo/Judul App | Segoe UI / SF Pro | 24px | Bold |
| Judul Halaman | Segoe UI | 20px | Bold |
| Label/Body | Segoe UI | 13px | Regular |
| Matrix Cell | Consolas / JetBrains Mono | 14px | Regular |
| Result Console | Consolas / Courier New | 12px | Regular |
| Button Text | Segoe UI | 13px | Semibold |

> **Catatan**: Menggunakan system font (Segoe UI di Windows, SF Pro di macOS) agar tidak perlu embed font eksternal. Fallback: Arial.

---

## 🟠 Bagian 4: Komponen UI Detail

### 4.1 Dynamic Matrix Grid Input

```
┌─────────────────────────────────────────┐
│  Dimensi Matriks:                       │
│  Baris: [▼ 3]   Kolom: [▼ 4]          │
│                                         │
│  ┌─────┬─────┬─────┬─────┐            │
│  │  1  │  2  │  3  │  4  │  ← Row 1   │
│  ├─────┼─────┼─────┼─────┤            │
│  │  0  │  1  │  2  │  3  │  ← Row 2   │
│  ├─────┼─────┼─────┼─────┤            │
│  │  5  │  0  │  1  │  7  │  ← Row 3   │
│  └─────┴─────┴─────┴─────┘            │
│                                         │
│  [Clear All]  [Random Fill]  [Paste]   │
└─────────────────────────────────────────┘
```

**Spesifikasi:**
- Setiap cell adalah `CTkEntry` berukuran 60x35px
- Validasi real-time: hanya terima angka, pecahan (1/3), desimal, dan tanda minus
- Cell invalid → border merah + tooltip "Input tidak valid"
- Tab navigation: Tab pindah ke cell berikutnya (kiri→kanan, atas→bawah)
- Arrow key navigation antar cell
- Batas dimensi: 1-10 baris, 1-10 kolom (untuk performa UI)
- Default value: 0 (bukan kosong)
- **Paste from Excel**: Deteksi tab-separated values dari clipboard

### 4.2 Method Selector (Segmented Control)

```
┌──────────────────────────────────────┐
│  Metode:                             │
│  ┌─────────┬──────────────┬────────┐ │
│  │  Gauss  │ Gauss-Jordan │ Invers │ │
│  └─────────┴──────────────┴────────┘ │
└──────────────────────────────────────┘
```

- Menggunakan `CTkSegmentedButton` (bukan radio button pop-up)
- Visual feedback langsung saat dipilih
- Tooltip pada hover menjelaskan setiap metode

### 4.3 Result Console

```
┌──────────────────────────────────────────────┐
│  📋 Hasil Perhitungan              [Copy] [×]│
├──────────────────────────────────────────────┤
│                                              │
│  ▶ Langkah 1: R2 ← R2 - 2·R1               │
│  ┌                    ┐                      │
│  │  1    2    3  │  4 │                      │
│  │  0   -3   -3  │ -5 │                      │
│  │  5    0    1  │  7 │                      │
│  └                    ┘                      │
│                                              │
│  ▶ Langkah 2: R3 ← R3 - 5·R1               │
│  ...                                         │
│                                              │
│  ═══════════════════════════════════         │
│  ✅ Solusi: x₁ = 2, x₂ = -1, x₃ = 3       │
│                                              │
└──────────────────────────────────────────────┘
```

**Spesifikasi:**
- Font monospace (Consolas 12px) untuk alignment matriks
- Syntax highlighting: langkah (biru), matriks (putih), hasil akhir (hijau)
- Scrollable dengan smooth scrolling
- Tombol "Copy" → salin seluruh output sebagai plain text
- Tombol "Copy LaTeX" → salin dalam format LaTeX
- Auto-scroll ke hasil akhir setelah kalkulasi selesai
- Clear button untuk reset output

### 4.4 Sidebar Navigation

**Spesifikasi:**
- Lebar fixed: 220px
- Tombol menu: full-width, left-aligned text, icon di kiri
- Hover effect: background berubah ke warna aksen (opacity 20%)
- Active state: background solid aksen + left border indicator (3px)
- Separator line antara grup menu
- Theme toggle di bagian paling bawah (switch widget)

---

## 🔴 Bagian 5: Fitur Per Halaman (Detail Lengkap)

### 5.1 Halaman SPL (Sistem Persamaan Linear)

**Input:**
- Matriks A (koefisien): Grid m×n
- Vektor b (konstanta): Grid m×1 (otomatis muncul di samping kanan matriks A, dipisahkan garis vertikal)
- Method selector: `Gauss` | `Gauss-Jordan` | `Matriks Balikan`

**Output:**
- Step-by-step eliminasi (setiap operasi baris ditampilkan)
- Matriks augmented di setiap langkah
- Solusi akhir dalam format: x₁ = ..., x₂ = ..., dst.
- Kasus khusus: "Tidak ada solusi" atau "Solusi tak hingga (parameterik)"

**Validasi:**
- Matriks Balikan: cek apakah A persegi dan non-singular
- Tampilkan pesan error inline (bukan pop-up)

### 5.2 Halaman Determinan

**Input:**
- Matriks persegi (n×n)
- Method selector: `Kofaktor` | `Reduksi Baris` | `Sarrus (3×3 only)`

**Output:**
- Kofaktor: tampilkan minor dan kofaktor tiap elemen baris pertama
- Reduksi Baris: tampilkan setiap operasi baris + faktor pengali
- Sarrus: tampilkan diagram visual (diagonal positif/negatif)
- Hasil akhir: `det(A) = ...`

**Validasi:**
- Sarrus: disable/gray-out jika matriks bukan 3×3
- Non-persegi: tampilkan warning inline

### 5.3 Halaman Invers

**Input:**
- Matriks persegi (n×n)
- Method selector: `Adjugate` | `Gauss-Jordan` | `Built-in`

**Output:**
- Adjugate: tampilkan matriks kofaktor → transpose → bagi det
- Gauss-Jordan: tampilkan [A|I] → step-by-step → [I|A⁻¹]
- Hasil akhir: matriks invers

**Validasi:**
- Cek persegi + non-singular sebelum hitung
- Error inline jika singular

### 5.4 Halaman Dekomposisi LU

**Input:**
- Matriks persegi (n×n)

**Output:**
- Matriks P (permutasi)
- Matriks L (lower triangular)
- Matriks U (upper triangular)
- Verifikasi: PA = LU (tampilkan hasil perkalian)

### 5.5 Halaman Eigenvalue & Eigenvector

**Input:**
- Matriks persegi (n×n)

**Output:**
- Polinomial karakteristik: p(λ) = ...
- Eigenvalues: λ₁, λ₂, ... dengan multiplisitas
- Eigenvectors: untuk setiap λ, tampilkan basis eigenspace
- Format vektor: bilangan bulat (sudah dinormalisasi)

### 5.6 Halaman Diagonalisasi

**Input:**
- Matriks persegi (n×n)

**Output:**
- Cek apakah bisa didiagonalisasi
- Jika ya: P, D, P⁻¹
- Verifikasi: A = PDP⁻¹
- Jika tidak: pesan jelas mengapa tidak bisa

### 5.7 Halaman SVD (Singular Value Decomposition)

**Input:**
- Matriks m×n (tidak harus persegi)

**Output:**
- U (m×m orthogonal)
- Σ (m×n diagonal)
- Vᵀ (n×n orthogonal)
- Singular values: σ₁ ≥ σ₂ ≥ ... ≥ 0
- Rank matriks

---

## 🟣 Bagian 6: UX Polish & Micro-interactions

### 6.1 Loading & Feedback

- **Loading spinner**: Muncul saat kalkulasi berat (SVD matriks besar, eigen simbolik)
- **Success indicator**: Flash hijau pada result console saat selesai
- **Error indicator**: Flash merah + shake animation pada input yang salah
- **Progress text**: "Menghitung..." di result console selama proses

### 6.2 Keyboard Shortcuts

| Shortcut | Aksi |
|----------|------|
| `Ctrl+Enter` | Hitung / Execute |
| `Ctrl+L` | Clear semua input |
| `Ctrl+Shift+C` | Copy hasil ke clipboard |
| `Ctrl+1` s/d `Ctrl+7` | Pindah ke menu 1-7 |
| `Tab` | Pindah cell matriks (next) |
| `Shift+Tab` | Pindah cell matriks (prev) |
| `Arrow Keys` | Navigasi antar cell |
| `Ctrl+V` | Paste matriks dari clipboard |

### 6.3 Tooltips & Help

- Setiap tombol metode punya tooltip (muncul setelah hover 500ms)
- Tombol "?" kecil di pojok kanan atas setiap halaman → menampilkan penjelasan singkat fitur
- Placeholder text di matrix cell: "0" (abu-abu muda)

### 6.4 Error Handling (Inline, Bukan Pop-up)

```
┌──────────────────────────────────────────┐
│  ⚠️ Matriks harus persegi untuk          │
│     menghitung determinan.               │
│     Ukuran saat ini: 3×4                 │
└──────────────────────────────────────────┘
```

- Error ditampilkan sebagai banner di atas result console
- Warna: background merah muda, border merah, icon ⚠️
- Auto-dismiss setelah 5 detik atau saat user mulai input baru
- TIDAK ADA `messagebox` pop-up (mengganggu flow)

### 6.5 Responsive Layout

- **Minimum window**: 900×600
- **Sidebar collapse**: Jika window < 1000px lebar, sidebar collapse jadi icon-only (60px)
- **Matrix grid scroll**: Jika matriks > 6×6, grid bisa di-scroll horizontal/vertikal
- **Result console resize**: Bisa di-drag border atas untuk resize area output

---

## 🟤 Bagian 7: Fitur Tambahan (Value-Add)

### 7.1 Quick Actions Bar

Di atas matrix input, ada toolbar kecil:
- **[Clear]** — Reset semua cell ke 0
- **[Random]** — Isi matriks dengan angka random (-9 s/d 9)
- **[Identity]** — Isi dengan matriks identitas
- **[Transpose]** — Transpose matriks yang sudah diinput
- **[Paste]** — Paste dari clipboard (Excel/spreadsheet format)

### 7.2 History Panel (Opsional)

- Sidebar kanan yang bisa di-toggle (hidden by default)
- Menyimpan 10 kalkulasi terakhir
- Klik item → restore input dan output
- Berguna untuk membandingkan hasil

### 7.3 Export Options

- **Copy as Plain Text**: Format aligned dengan spasi
- **Copy as LaTeX**: `\begin{bmatrix} ... \end{bmatrix}`
- **Copy as Python**: `np.array([[...], [...]])`

### 7.4 Input Presets / Templates

- Dropdown "Contoh Matriks" untuk testing cepat:
  - Matriks Identitas 3×3
  - Matriks Singular
  - Matriks Simetris
  - Matriks dengan eigenvalue kompleks

---

## 📑 Bagian 8: Roadmap Pengembangan (Fase Eksekusi)

### Fase 1: Foundation (Hari 1-2)
- [ ] Setup project structure (file terpisah per modul)
- [ ] Install dependencies: `customtkinter`, `sympy`, `numpy`, `pillow`, `pyperclip`
- [ ] Buat main window + grid layout
- [ ] Buat SidebarFrame dengan semua tombol menu
- [ ] Implementasi frame switching (show/hide)
- [ ] Implementasi theme toggle (dark/light)

### Fase 2: Core Components (Hari 3-4)
- [ ] Buat `MatrixInputWidget` (reusable)
  - Dimension selector
  - Dynamic grid generation
  - Cell validation (real-time)
  - Tab/Arrow navigation
  - Paste from clipboard
- [ ] Buat `ResultConsoleWidget` (reusable)
  - Scrollable text area
  - Syntax highlighting (tag-based)
  - Copy buttons
- [ ] Buat `MethodSelector` (segmented button wrapper)
- [ ] Buat `ErrorBanner` (inline error display)

### Fase 3: Feature Pages (Hari 5-7)
- [ ] SPL Page (3 metode + step-by-step)
- [ ] Determinan Page (3 metode)
- [ ] Invers Page (3 metode + step-by-step Gauss-Jordan)
- [ ] LU Page
- [ ] Eigen Page (polynomial + values + vectors)
- [ ] Diagonalisasi Page
- [ ] SVD Page

### Fase 4: Step-by-Step Engine (Hari 8-9)
- [ ] Implementasi custom Gauss elimination dengan logging tiap langkah
- [ ] Implementasi custom Gauss-Jordan dengan logging
- [ ] Format output langkah: operasi baris + matriks hasil
- [ ] Highlight perubahan di setiap langkah (bold/warna)

### Fase 5: Polish & UX (Hari 10-11)
- [ ] Keyboard shortcuts
- [ ] Tooltips
- [ ] Loading indicators
- [ ] Error animations (shake, flash)
- [ ] Hover effects pada tombol
- [ ] Responsive sidebar collapse
- [ ] Quick actions bar (Clear, Random, Identity, Transpose, Paste)

### Fase 6: Testing & Finalisasi (Hari 12)
- [ ] Test semua fitur dengan edge cases
- [ ] Test matriks singular, non-persegi, besar (8×8+)
- [ ] Test dark/light mode consistency
- [ ] Test keyboard navigation
- [ ] Performance check (matriks 10×10)
- [ ] Final bug fixes

---

## 💻 Bagian 9: Struktur File Proyek

```
CODING/
├── main.py                    # Entry point
├── app.py                     # Class ModernAlinApp (main window)
├── config.py                  # Warna, font, konstanta
├── components/
│   ├── __init__.py
│   ├── sidebar.py             # SidebarFrame
│   ├── matrix_input.py        # MatrixInputWidget
│   ├── result_console.py      # ResultConsoleWidget
│   ├── method_selector.py     # MethodSelector
│   └── error_banner.py        # ErrorBanner
├── pages/
│   ├── __init__.py
│   ├── spl_page.py
│   ├── determinan_page.py
│   ├── invers_page.py
│   ├── lu_page.py
│   ├── eigen_page.py
│   ├── diagonal_page.py
│   └── svd_page.py
├── logic/
│   ├── __init__.py
│   ├── spl_solver.py          # Gauss, Gauss-Jordan, Invers (with steps)
│   ├── determinan_solver.py   # Kofaktor, Reduksi, Sarrus (with steps)
│   ├── invers_solver.py       # Adjugate, GJ, Built-in (with steps)
│   ├── lu_solver.py
│   ├── eigen_solver.py
│   ├── diagonal_solver.py
│   └── svd_solver.py
├── utils/
│   ├── __init__.py
│   ├── formatter.py           # format_matriks, format_polinom, normalisasi
│   ├── validator.py           # Input validation helpers
│   └── clipboard.py           # Copy/paste utilities
└── assets/
    └── icons/                 # SVG/PNG icons untuk sidebar
```

---

## 🎯 Bagian 10: Perbandingan Before vs After

| Aspek | Sebelum (Kode Lama) | Sesudah (Modern Dashboard) |
|-------|---------------------|---------------------------|
| Window | Multi pop-up | Single window |
| Input Matriks | Text box manual | Visual grid cells |
| Navigasi | Tombol di main + pop-up | Sidebar persistent |
| Tema | Pink pastel fixed | Dark/Light switchable |
| Error | `messagebox` pop-up | Inline banner |
| Output | Plain text | Highlighted + step-by-step |
| Keyboard | Tidak ada | Full shortcut support |
| State | Hilang saat pindah menu | Preserved |
| Responsif | Fixed size | Adaptive layout |
| Copy | Tidak ada | Plain/LaTeX/Python |
| Validasi | Saat submit saja | Real-time per cell |

---

## ⚡ Bagian 11: Prinsip Desain

1. **Zero Pop-up Policy**: Semua interaksi terjadi di dalam satu window.
2. **Progressive Disclosure**: Tampilkan yang penting dulu, detail muncul saat dibutuhkan.
3. **Immediate Feedback**: Setiap aksi user mendapat respons visual < 100ms.
4. **Forgiving Input**: Terima berbagai format (1/3, 0.333, -2) tanpa error.
5. **Consistent Layout**: Setiap halaman punya struktur yang sama (input atas, output bawah).
6. **Accessible**: Bisa dioperasikan sepenuhnya via keyboard.
7. **Non-destructive**: Pindah menu tidak menghapus pekerjaan sebelumnya.

---

## 📝 Catatan Implementasi

- **Thread Safety**: Kalkulasi berat (SVD, eigen matriks besar) harus dijalankan di thread terpisah agar UI tidak freeze. Gunakan `threading` + `after()` untuk update UI.
- **Memory**: Simpan state per halaman di dictionary, bukan buat ulang widget setiap kali.
- **Font Fallback**: Cek ketersediaan font saat startup, gunakan fallback jika tidak ada.
- **DPI Awareness**: Set `ctk.deactivate_automatic_dpi_awareness()` jika ada masalah scaling di Windows.
