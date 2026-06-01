# =============================================================================
# STEP_ENGINE.PY — Step-by-Step Elimination Engine
# =============================================================================
# Engine yang melakukan eliminasi Gauss / Gauss-Jordan secara manual
# sambil merekam setiap operasi baris (OBE) beserta matriks hasilnya.
#
# Digunakan oleh: SPL, Determinan (Reduksi), Invers (Gauss-Jordan)
# =============================================================================

import sympy as sp
from copy import deepcopy


class Step:
    """Representasi satu langkah operasi baris."""

    def __init__(self, operation, matrix, description=""):
        """
        Args:
            operation: String operasi (e.g. "R2 ← R2 - 2·R1")
            matrix: sympy Matrix setelah operasi
            description: Keterangan tambahan (opsional)
        """
        self.operation = operation
        self.matrix = matrix.copy()
        self.description = description

    def __repr__(self):
        return f"Step({self.operation})"


def gauss_elimination(matrix, augmented_cols=0, show_steps=True):
    """
    Eliminasi Gauss → Row Echelon Form (REF).
    Merekam setiap langkah operasi baris.

    Args:
        matrix: sympy Matrix (bisa augmented)
        augmented_cols: jumlah kolom augmented di kanan (untuk display)
        show_steps: bila False, lewati perekaman langkah (steps tetap []).
            Logika matematika tidak berubah — hanya overhead deep-copy
            matriks per langkah yang dihilangkan untuk matriks besar.

    Returns:
        (result_matrix, steps, pivot_cols, sign_changes)
        - result_matrix: Matrix dalam bentuk REF
        - steps: list of Step objects
        - pivot_cols: list of pivot column indices
        - sign_changes: jumlah row swap (untuk determinan)
    """
    M = matrix.copy()
    rows, cols = M.shape
    steps = []
    pivot_cols = []
    sign_changes = 0

    # Kolom yang diproses (exclude augmented columns)
    work_cols = cols - augmented_cols

    pivot_row = 0

    for col in range(work_cols):
        if pivot_row >= rows:
            break

        # ─── Find Pivot (partial pivoting) ───
        # Cari elemen non-zero terbesar di kolom ini (dari pivot_row ke bawah)
        best_row = None
        best_val = sp.Integer(0)

        for r in range(pivot_row, rows):
            val = abs(M[r, col])
            if val != 0 and (best_row is None or val > best_val):
                best_row = r
                best_val = val

        if best_row is None:
            # Kolom ini semua nol, skip
            continue

        # ─── Row Swap (jika perlu) ───
        if best_row != pivot_row:
            M.row_swap(best_row, pivot_row)
            sign_changes += 1
            if show_steps:
                steps.append(Step(
                    f"R{pivot_row+1} ↔ R{best_row+1}",
                    M,
                    "Tukar baris untuk mendapatkan pivot"
                ))

        pivot_cols.append(col)

        # ─── Eliminate Below ───
        for r in range(pivot_row + 1, rows):
            if M[r, col] != 0:
                factor = sp.Rational(M[r, col], M[pivot_row, col])
                # Operasi baris: R_r = R_r - factor * R_pivot
                for c in range(cols):
                    M[r, c] = M[r, c] - factor * M[pivot_row, c]

                if show_steps:
                    # Format factor untuk display
                    factor_str = _format_factor(factor)
                    steps.append(Step(
                        f"R{r+1} ← R{r+1} - {factor_str}·R{pivot_row+1}",
                        M,
                        f"Eliminasi elemen baris {r+1}, kolom {col+1}"
                    ))

        pivot_row += 1

    return M, steps, pivot_cols, sign_changes


def gauss_jordan_elimination(matrix, augmented_cols=0, show_steps=True):
    """
    Eliminasi Gauss-Jordan → Reduced Row Echelon Form (RREF).
    Merekam setiap langkah operasi baris.

    Args:
        matrix: sympy Matrix (bisa augmented)
        augmented_cols: jumlah kolom augmented di kanan
        show_steps: bila False, lewati perekaman langkah (steps tetap []).

    Returns:
        (result_matrix, steps, pivot_cols)
    """
    # Fase 1: Forward elimination (Gauss)
    M, forward_steps, pivot_cols, _ = gauss_elimination(
        matrix, augmented_cols, show_steps=show_steps
    )
    steps = list(forward_steps)

    rows, cols = M.shape

    # Fase 2: Normalize pivots to 1
    for i, pcol in enumerate(pivot_cols):
        if i >= rows:
            break
        pivot_val = M[i, pcol]
        if pivot_val != 0 and pivot_val != 1:
            factor = pivot_val
            for c in range(cols):
                M[i, c] = M[i, c] / factor
            if show_steps:
                factor_str = _format_factor(factor)
                steps.append(Step(
                    f"R{i+1} ← (1/{factor_str})·R{i+1}",
                    M,
                    f"Normalisasi pivot baris {i+1} menjadi 1"
                ))

    # Fase 3: Back substitution (eliminate above pivots)
    for i in range(len(pivot_cols) - 1, 0, -1):
        pcol = pivot_cols[i]
        if i >= rows:
            continue

        for r in range(i - 1, -1, -1):
            if M[r, pcol] != 0:
                factor = M[r, pcol]
                for c in range(cols):
                    M[r, c] = M[r, c] - factor * M[i, c]

                if show_steps:
                    factor_str = _format_factor(factor)
                    steps.append(Step(
                        f"R{r+1} ← R{r+1} - {factor_str}·R{i+1}",
                        M,
                        f"Eliminasi elemen di atas pivot kolom {pcol+1}"
                    ))

    return M, steps, pivot_cols


def gauss_jordan_inverse(matrix, show_steps=True):
    """
    Hitung invers via Gauss-Jordan: [A|I] → [I|A⁻¹].
    Merekam setiap langkah.

    Args:
        matrix: sympy Matrix persegi (n×n)
        show_steps: bila False, lewati perekaman langkah (steps tetap []).

    Returns:
        (inverse_matrix, steps) atau raises ValueError jika singular
    """
    n = matrix.rows
    I = sp.eye(n)
    aug = matrix.row_join(I)

    steps = []
    M = aug.copy()
    cols = 2 * n

    for col in range(n):
        # ─── Find Pivot ───
        pivot_row = None
        for r in range(col, n):
            if M[r, col] != 0:
                pivot_row = r
                break

        if pivot_row is None:
            raise ValueError("Matriks singular, invers tidak ada")

        # ─── Row Swap ───
        if pivot_row != col:
            M.row_swap(pivot_row, col)
            if show_steps:
                steps.append(Step(
                    f"R{col+1} ↔ R{pivot_row+1}",
                    M,
                    "Tukar baris untuk pivot"
                ))

        # ─── Normalize Pivot ───
        pivot_val = M[col, col]
        if pivot_val != 1:
            factor_str = _format_factor(pivot_val) if show_steps else None
            for c in range(cols):
                M[col, c] = M[col, c] / pivot_val
            if show_steps:
                steps.append(Step(
                    f"R{col+1} ← (1/{factor_str})·R{col+1}",
                    M,
                    f"Normalisasi pivot baris {col+1}"
                ))

        # ─── Eliminate All Other Rows ───
        for r in range(n):
            if r != col and M[r, col] != 0:
                factor = M[r, col]
                factor_str = _format_factor(factor) if show_steps else None
                for c in range(cols):
                    M[r, c] = M[r, c] - factor * M[col, c]
                if show_steps:
                    steps.append(Step(
                        f"R{r+1} ← R{r+1} - {factor_str}·R{col+1}",
                        M,
                        f"Eliminasi baris {r+1}"
                    ))

    # Extract inverse (right half)
    inverse = M[:, n:]
    return inverse, steps


def determinant_by_elimination(matrix, show_steps=True):
    """
    Hitung determinan via eliminasi baris ke segitiga atas.
    Merekam setiap langkah.

    Args:
        matrix: sympy Matrix persegi (n×n)
        show_steps: bila False, lewati perekaman langkah ANTARA (intermediate).
            Step struktural penting (kasus det=0 & ringkasan akhir) tetap
            direkam agar pemanggil dapat menampilkan matriks segitiga & hasil.

    Returns:
        (determinant_value, steps)
    """
    n = matrix.rows
    M = matrix.copy()
    steps = []
    sign_changes = 0
    scale_factors = []  # Track scaling yang dilakukan

    for col in range(n):
        # Find pivot
        pivot_row = None
        for r in range(col, n):
            if M[r, col] != 0:
                pivot_row = r
                break

        if pivot_row is None:
            # Determinan = 0
            steps.append(Step(
                f"Kolom {col+1} = 0 (di bawah diagonal)",
                M,
                "Determinan = 0"
            ))
            return sp.Integer(0), steps

        # Row swap
        if pivot_row != col:
            M.row_swap(pivot_row, col)
            sign_changes += 1
            if show_steps:
                steps.append(Step(
                    f"R{col+1} ↔ R{pivot_row+1}",
                    M,
                    f"Tukar baris (sign flip #{sign_changes})"
                ))

        # Eliminate below
        for r in range(col + 1, n):
            if M[r, col] != 0:
                factor = sp.Rational(M[r, col], M[col, col])
                for c in range(n):
                    M[r, c] = M[r, c] - factor * M[col, c]

                if show_steps:
                    factor_str = _format_factor(factor)
                    steps.append(Step(
                        f"R{r+1} ← R{r+1} - {factor_str}·R{col+1}",
                        M,
                        f"Eliminasi a[{r+1},{col+1}]"
                    ))

    # Determinan = (-1)^swaps × product of diagonal
    diag_product = sp.Integer(1)
    for i in range(n):
        diag_product *= M[i, i]

    det = ((-1) ** sign_changes) * diag_product

    steps.append(Step(
        f"det = (-1)^{sign_changes} × diagonal product",
        M,
        f"det = {det}"
    ))

    return det, steps


def solve_spl_gauss(A, b, show_steps=True):
    """
    Selesaikan SPL Ax=b via eliminasi Gauss.
    
    Returns:
        (solution_info, steps)
        solution_info: dict dengan keys 'type', 'values', 'message'
    """
    aug = A.row_join(b)
    ref, steps, pivot_cols, _ = gauss_elimination(
        aug, augmented_cols=b.cols, show_steps=show_steps
    )

    n_vars = A.cols
    n_rows = A.rows

    # Analisis solusi
    # Cek baris inkonsisten: [0 0 ... 0 | c] dimana c ≠ 0
    for r in range(n_rows):
        all_zero = all(ref[r, c] == 0 for c in range(n_vars))
        if all_zero and ref[r, n_vars] != 0:
            return {
                "type": "none",
                "message": f"Tidak ada solusi (baris {r+1}: 0 = {ref[r, n_vars]})"
            }, steps

    # Cek apakah ada free variables
    if len(pivot_cols) < n_vars:
        return {
            "type": "infinite",
            "message": f"Solusi tak hingga ({n_vars - len(pivot_cols)} variabel bebas)",
            "pivot_cols": pivot_cols,
            "matrix": ref,
        }, steps

    # Unique solution — back substitution
    x = [sp.Integer(0)] * n_vars
    for i in range(len(pivot_cols) - 1, -1, -1):
        pcol = pivot_cols[i]
        val = ref[i, n_vars]
        for c in range(pcol + 1, n_vars):
            val -= ref[i, c] * x[c]
        x[pcol] = sp.nsimplify(val / ref[i, pcol]) if ref[i, pcol] != 0 else val

    return {
        "type": "unique",
        "values": x,
        "message": "Solusi unik ditemukan"
    }, steps


def solve_spl_gauss_jordan(A, b, show_steps=True):
    """
    Selesaikan SPL Ax=b via eliminasi Gauss-Jordan (RREF).
    
    Returns:
        (solution_info, steps)
    """
    aug = A.row_join(b)
    rref, steps, pivot_cols = gauss_jordan_elimination(
        aug, augmented_cols=b.cols, show_steps=show_steps
    )

    n_vars = A.cols
    n_rows = A.rows

    # Cek inkonsistensi
    for r in range(n_rows):
        all_zero = all(rref[r, c] == 0 for c in range(n_vars))
        if all_zero and rref[r, n_vars] != 0:
            return {
                "type": "none",
                "message": f"Tidak ada solusi (baris {r+1}: 0 = {rref[r, n_vars]})"
            }, steps

    # Cek free variables
    if len(pivot_cols) < n_vars:
        return {
            "type": "infinite",
            "message": f"Solusi tak hingga ({n_vars - len(pivot_cols)} variabel bebas)",
            "pivot_cols": pivot_cols,
            "matrix": rref,
        }, steps

    # Unique solution — langsung baca dari RREF
    x = []
    for i in range(min(len(pivot_cols), n_rows)):
        x.append(sp.nsimplify(rref[i, n_vars]))

    return {
        "type": "unique",
        "values": x,
        "message": "Solusi unik ditemukan"
    }, steps


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def _format_factor(factor):
    """Format faktor untuk display yang rapi."""
    factor = sp.nsimplify(factor)
    if factor == 1:
        return "1"
    elif factor == -1:
        return "-1"
    elif isinstance(factor, sp.Rational) and factor.q != 1:
        if factor > 0:
            return f"({factor.p}/{factor.q})"
        else:
            return f"({factor.p}/{factor.q})"
    else:
        s = str(factor)
        if factor < 0:
            return f"({s})"
        return s


def format_step_matrix(matrix, augmented_cols=0, highlight_row=None):
    """
    Format matriks untuk display di console, dengan opsi highlight baris.
    
    Args:
        matrix: sympy Matrix
        augmented_cols: kolom augmented (ditandai dengan │)
        highlight_row: index baris yang di-highlight (opsional)
    """
    rows = matrix.tolist()
    n_cols = matrix.cols
    work_cols = n_cols - augmented_cols

    # Convert ke string
    str_rows = []
    for row in rows:
        str_rows.append([str(sp.nsimplify(val)) for val in row])

    # Hitung lebar kolom
    col_widths = []
    for c in range(n_cols):
        max_w = max(len(str_rows[r][c]) for r in range(len(str_rows)))
        col_widths.append(max(max_w, 3))

    # Build output
    lines = []
    for r, row in enumerate(str_rows):
        if augmented_cols > 0:
            left = "  ".join(row[c].rjust(col_widths[c]) for c in range(work_cols))
            right = "  ".join(row[c].rjust(col_widths[c]) for c in range(work_cols, n_cols))
            line = f"[ {left}  │ {right} ]"
        else:
            cells = "  ".join(row[c].rjust(col_widths[c]) for c in range(n_cols))
            line = f"[ {cells} ]"

        if highlight_row is not None and r == highlight_row:
            line = f"→ {line}"
        else:
            line = f"  {line}"

        lines.append(line)

    return "\n".join(lines)
