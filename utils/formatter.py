# =============================================================================
# FORMATTER.PY — Helper functions untuk format output matriks & ekspresi
# =============================================================================

import sympy as sp
import numpy as np


def format_matriks(M, align=True):
    """
    Format sympy Matrix menjadi string aligned.
    Contoh output:
    ┌              ┐
    │  1   2   3  │
    │  0  -1   4  │
    │  5   0   1  │
    └              ┘
    """
    M = sp.Matrix(M)
    rows = M.tolist()

    # Convert semua elemen ke string
    str_rows = []
    for row in rows:
        str_rows.append([str(sp.nsimplify(val)) for val in row])

    if not str_rows:
        return "[ ]"

    # Hitung lebar kolom
    col_widths = []
    num_cols = len(str_rows[0])
    for c in range(num_cols):
        max_w = max(len(str_rows[r][c]) for r in range(len(str_rows)))
        col_widths.append(max_w)

    # Build output
    lines = []
    total_width = sum(col_widths) + (num_cols - 1) * 3 + 4  # padding

    lines.append("┌" + " " * total_width + "┐")
    for row in str_rows:
        cells = "   ".join(val.rjust(col_widths[i]) for i, val in enumerate(row))
        lines.append(f"│  {cells}  │")
    lines.append("└" + " " * total_width + "┘")

    return "\n".join(lines)


def format_matriks_simple(M):
    """Format matriks sederhana tanpa border (untuk inline)."""
    M = sp.Matrix(M)
    lines = []
    for row in M.tolist():
        lines.append("[ " + "   ".join(str(sp.nsimplify(val)) for val in row) + " ]")
    return "\n".join(lines)


def format_augmented(A, b):
    """
    Format matriks augmented [A|b].
    """
    A = sp.Matrix(A)
    b = sp.Matrix(b)
    rows_a = A.tolist()
    rows_b = b.tolist()

    # String conversion
    str_a = [[str(sp.nsimplify(v)) for v in row] for row in rows_a]
    str_b = [[str(sp.nsimplify(v)) for v in row] for row in rows_b]

    # Column widths for A
    cols_a = len(str_a[0]) if str_a else 0
    widths_a = []
    for c in range(cols_a):
        widths_a.append(max(len(str_a[r][c]) for r in range(len(str_a))))

    # Column widths for b
    cols_b = len(str_b[0]) if str_b else 0
    widths_b = []
    for c in range(cols_b):
        widths_b.append(max(len(str_b[r][c]) for r in range(len(str_b))))

    lines = []
    for r in range(len(str_a)):
        part_a = "  ".join(str_a[r][c].rjust(widths_a[c]) for c in range(cols_a))
        part_b = "  ".join(str_b[r][c].rjust(widths_b[c]) for c in range(cols_b))
        lines.append(f"[ {part_a}  │ {part_b} ]")

    return "\n".join(lines)


def format_polinom(expr):
    """Format polinomial karakteristik dengan simbol λ."""
    lam = sp.Symbol('λ')
    expr = expr.subs(sp.Symbol('lambda'), lam)
    return str(expr)


def format_numpy_matrix(M, decimals=4):
    """Format numpy array menjadi string aligned."""
    if isinstance(M, np.ndarray):
        M = np.round(M, decimals)
        rows = M.tolist()
    else:
        rows = M

    str_rows = []
    for row in rows:
        str_rows.append([f"{val:>8.{decimals}f}" if isinstance(val, float) else str(val) for val in row])

    if not str_rows:
        return "[ ]"

    lines = []
    for row in str_rows:
        lines.append("[ " + "  ".join(row) + " ]")

    return "\n".join(lines)


def normalisasi(v):
    """
    Normalisasi eigenvector ke bilangan bulat terkecil.
    Contoh: [1/2, 1, 3/2] → [1, 2, 3]
    """
    v = sp.Matrix(v)
    v_list = [sp.nsimplify(x) for x in v]

    # Cari LCM dari semua denominator
    denoms = []
    for x in v_list:
        if hasattr(x, 'q'):
            denoms.append(x.q)
        elif isinstance(x, sp.Rational):
            denoms.append(x.q)

    if denoms:
        lcm = denoms[0]
        for d in denoms[1:]:
            lcm = sp.ilcm(lcm, d)
        v_list = [x * lcm for x in v_list]

    # Convert ke int
    try:
        v_int = [int(x) for x in v_list]
    except (ValueError, TypeError):
        return [str(x) for x in v_list]

    # Bagi dengan GCD
    gcd = abs(v_int[0])
    for val in v_int[1:]:
        gcd = sp.igcd(gcd, abs(val))

    if gcd != 0:
        v_int = [x // gcd for x in v_int]

    return v_int
