# Kalkulator Aljabar Linier

**Linear Algebra Dashboard Pro** — Aplikasi kalkulator aljabar linear modern berbasis GUI dengan tampilan step-by-step.

## Fitur

- **SPL** — Sistem Persamaan Linear (Gauss, Gauss-Jordan, Matriks Balikan)
- **Determinan** — Kofaktor, Reduksi Baris, Sarrus
- **Invers** — Adjugate, Gauss-Jordan step-by-step, Built-in
- **Dekomposisi LU** — PA = LU dengan verifikasi
- **Eigenvalue & Eigenvector** — Polinomial karakteristik, eigenspace
- **Diagonalisasi** — A = PDP⁻¹ dengan verifikasi
- **SVD** — Singular Value Decomposition

## Screenshot

Dark mode dashboard dengan input matriks visual dan output step-by-step.

## Instalasi

```bash
pip install customtkinter sympy numpy
```

## Menjalankan

```bash
python main.py
```

## Tech Stack

- Python 3.9+
- CustomTkinter (GUI modern)
- SymPy (komputasi simbolik)
- NumPy (komputasi numerik)

## Keyboard Shortcuts

| Shortcut | Aksi |
|----------|------|
| Ctrl+1~7 | Navigasi menu |
| Ctrl+Enter | Hitung |
| Ctrl+L | Clear input |
| Ctrl+Shift+C | Copy hasil |
| Escape | Kembali ke Dashboard |

## Testing

```bash
python tests/test_all.py
```

44/44 tests passed.

## Lisensi

MIT
