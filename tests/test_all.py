"""
=============================================================================
TEST_ALL.PY — Fase 6: Testing & Finalisasi
=============================================================================
Test suite untuk memverifikasi semua fitur kalkulator aljabar linear.
Jalankan: python tests/test_all.py
=============================================================================
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import sympy as sp
import numpy as np
from logic.step_engine import (
    gauss_elimination, gauss_jordan_elimination,
    gauss_jordan_inverse, determinant_by_elimination,
    solve_spl_gauss, solve_spl_gauss_jordan,
    format_step_matrix
)
from utils.formatter import (
    format_matriks, format_matriks_simple, format_augmented,
    format_numpy_matrix, format_polinom, normalisasi
)


class TestResults:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.errors = []

    def ok(self, name):
        self.passed += 1
        print(f"  ✓ {name}")

    def fail(self, name, detail=""):
        self.failed += 1
        self.errors.append((name, detail))
        print(f"  ✗ {name} — {detail}")

    def summary(self):
        total = self.passed + self.failed
        print(f"\n{'='*60}")
        print(f"HASIL: {self.passed}/{total} passed, {self.failed} failed")
        if self.errors:
            print(f"\nFailed tests:")
            for name, detail in self.errors:
                print(f"  - {name}: {detail}")
        print(f"{'='*60}")
        return self.failed == 0


results = TestResults()


# =============================================================================
# TEST 1: SPL — Solusi Unik
# =============================================================================
print("\n" + "="*60)
print("TEST GROUP 1: SPL (Sistem Persamaan Linear)")
print("="*60)

# 1.1 Gauss — 3x3 solusi unik
A = sp.Matrix([[2, 1, -1], [4, 5, 1], [1, 2, 3]])
b = sp.Matrix([[5], [13], [12]])
sol, steps = solve_spl_gauss(A, b)
if sol["type"] == "unique" and sol["values"] == [6, -3, 4]:
    # Verify: A*x = b
    x = sp.Matrix(sol["values"])
    if A * x == b:
        results.ok("SPL Gauss 3x3 — solusi unik [6, -3, 4]")
    else:
        results.fail("SPL Gauss 3x3", "Verifikasi A*x != b")
else:
    results.fail("SPL Gauss 3x3", f"Got: {sol}")

# 1.2 Gauss-Jordan — 3x3 solusi unik
sol2, steps2 = solve_spl_gauss_jordan(A, b)
if sol2["type"] == "unique" and sol2["values"] == [6, -3, 4]:
    results.ok("SPL Gauss-Jordan 3x3 — solusi unik [6, -3, 4]")
else:
    results.fail("SPL Gauss-Jordan 3x3", f"Got: {sol2}")

# 1.3 SPL tanpa solusi (inkonsisten)
A_inc = sp.Matrix([[1, 2, 3], [2, 4, 6], [1, 1, 1]])
b_inc = sp.Matrix([[1], [3], [2]])
sol3, _ = solve_spl_gauss(A_inc, b_inc)
if sol3["type"] == "none":
    results.ok("SPL inkonsisten — tidak ada solusi")
else:
    results.fail("SPL inkonsisten", f"Expected 'none', got '{sol3['type']}'")

# 1.4 SPL solusi tak hingga
A_inf = sp.Matrix([[1, 2, 3], [2, 4, 6], [0, 0, 0]])
b_inf = sp.Matrix([[1], [2], [0]])
sol4, _ = solve_spl_gauss(A_inf, b_inf)
if sol4["type"] == "infinite":
    results.ok("SPL solusi tak hingga — terdeteksi")
else:
    results.fail("SPL solusi tak hingga", f"Expected 'infinite', got '{sol4['type']}'")

# 1.5 SPL 2x2
A_2 = sp.Matrix([[3, 2], [1, -1]])
b_2 = sp.Matrix([[7], [1]])
sol5, _ = solve_spl_gauss(A_2, b_2)
if sol5["type"] == "unique":
    x = sp.Matrix(sol5["values"])
    if A_2 * x == b_2:
        results.ok("SPL Gauss 2x2 — solusi terverifikasi")
    else:
        results.fail("SPL Gauss 2x2", "Verifikasi gagal")
else:
    results.fail("SPL Gauss 2x2", f"Got: {sol5}")

# 1.6 SPL 4x4
A_4 = sp.Matrix([
    [1, 1, 1, 1],
    [2, 3, 1, 1],
    [1, 2, 3, 1],
    [1, 1, 1, 4]
])
b_4 = sp.Matrix([[10], [13], [18], [19]])
sol6, _ = solve_spl_gauss(A_4, b_4)
if sol6["type"] == "unique":
    x = sp.Matrix(sol6["values"])
    if A_4 * x == b_4:
        results.ok("SPL Gauss 4x4 — solusi terverifikasi")
    else:
        results.fail("SPL Gauss 4x4", f"A*x != b, x={sol6['values']}")
else:
    results.fail("SPL Gauss 4x4", f"Got: {sol6}")


# =============================================================================
# TEST 2: DETERMINAN
# =============================================================================
print("\n" + "="*60)
print("TEST GROUP 2: Determinan")
print("="*60)

# 2.1 Determinan 3x3
M3 = sp.Matrix([[2, 1, -1], [4, 5, 1], [1, 2, 3]])
det3, steps_d = determinant_by_elimination(M3)
expected_det3 = M3.det()
if det3 == expected_det3:
    results.ok(f"Determinan 3x3 = {det3}")
else:
    results.fail("Determinan 3x3", f"Got {det3}, expected {expected_det3}")

# 2.2 Determinan matriks singular
M_sing = sp.Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
det_sing, _ = determinant_by_elimination(M_sing)
if det_sing == 0:
    results.ok("Determinan singular = 0")
else:
    results.fail("Determinan singular", f"Got {det_sing}, expected 0")

# 2.3 Determinan 4x4
M4 = sp.Matrix([
    [1, 2, 3, 4],
    [5, 6, 7, 8],
    [2, 6, 4, 8],
    [3, 1, 1, 2]
])
det4, _ = determinant_by_elimination(M4)
expected_det4 = M4.det()
if det4 == expected_det4:
    results.ok(f"Determinan 4x4 = {det4}")
else:
    results.fail("Determinan 4x4", f"Got {det4}, expected {expected_det4}")

# 2.4 Determinan 2x2
M2 = sp.Matrix([[3, 7], [1, -4]])
det2, _ = determinant_by_elimination(M2)
if det2 == M2.det():
    results.ok(f"Determinan 2x2 = {det2}")
else:
    results.fail("Determinan 2x2", f"Got {det2}")

# 2.5 Determinan 1x1
M1 = sp.Matrix([[5]])
det1, _ = determinant_by_elimination(M1)
if det1 == 5:
    results.ok("Determinan 1x1 = 5")
else:
    results.fail("Determinan 1x1", f"Got {det1}")

# 2.6 Determinan dengan pecahan
M_frac = sp.Matrix([[sp.Rational(1,2), 1], [3, sp.Rational(1,3)]])
det_frac, _ = determinant_by_elimination(M_frac)
if det_frac == M_frac.det():
    results.ok(f"Determinan pecahan = {det_frac}")
else:
    results.fail("Determinan pecahan", f"Got {det_frac}")


# =============================================================================
# TEST 3: INVERS
# =============================================================================
print("\n" + "="*60)
print("TEST GROUP 3: Invers Matriks")
print("="*60)

# 3.1 Invers 3x3
inv3, inv_steps = gauss_jordan_inverse(M3)
if M3 * inv3 == sp.eye(3):
    results.ok("Invers 3x3 — A*A⁻¹ = I ✓")
else:
    results.fail("Invers 3x3", "A*A⁻¹ != I")

# 3.2 Invers 2x2
M2_inv = sp.Matrix([[4, 7], [2, 6]])
inv2, _ = gauss_jordan_inverse(M2_inv)
if M2_inv * inv2 == sp.eye(2):
    results.ok("Invers 2x2 — A*A⁻¹ = I ✓")
else:
    results.fail("Invers 2x2", "A*A⁻¹ != I")

# 3.3 Invers matriks singular → error
try:
    gauss_jordan_inverse(M_sing)
    results.fail("Invers singular", "Seharusnya raise ValueError")
except ValueError as e:
    results.ok(f"Invers singular — ValueError: {e}")

# 3.4 Invers 4x4
inv4, _ = gauss_jordan_inverse(M4)
if M4 * inv4 == sp.eye(4):
    results.ok("Invers 4x4 — A*A⁻¹ = I ✓")
else:
    results.fail("Invers 4x4", "A*A⁻¹ != I")


# =============================================================================
# TEST 4: LU DECOMPOSITION
# =============================================================================
print("\n" + "="*60)
print("TEST GROUP 4: Dekomposisi LU")
print("="*60)

# 4.1 LU 3x3
L, U, perm = M3.LUdecomposition()
P = sp.eye(3)
for i, j in perm:
    P.row_swap(i, j)
if P * M3 == L * U:
    results.ok("LU 3x3 — PA = LU ✓")
else:
    results.fail("LU 3x3", "PA != LU")

# 4.2 LU 4x4
L4, U4, perm4 = M4.LUdecomposition()
P4 = sp.eye(4)
for i, j in perm4:
    P4.row_swap(i, j)
if P4 * M4 == L4 * U4:
    results.ok("LU 4x4 — PA = LU ✓")
else:
    results.fail("LU 4x4", "PA != LU")


# =============================================================================
# TEST 5: EIGEN
# =============================================================================
print("\n" + "="*60)
print("TEST GROUP 5: Eigenvalue & Eigenvector")
print("="*60)

# 5.1 Eigen 2x2
E2 = sp.Matrix([[4, 1], [2, 3]])
eigenvals = E2.eigenvals()
eigenvects = E2.eigenvects()
if sp.Integer(5) in eigenvals and sp.Integer(2) in eigenvals:
    results.ok("Eigen 2x2 — λ = 5, 2 ✓")
else:
    results.fail("Eigen 2x2", f"Got eigenvals: {eigenvals}")

# 5.2 Eigen 3x3 simetris
E3 = sp.Matrix([[2, -1, 0], [-1, 2, -1], [0, -1, 2]])
eigenvals3 = E3.eigenvals()
total_mult = sum(eigenvals3.values())
if total_mult == 3:
    results.ok(f"Eigen 3x3 simetris — {len(eigenvals3)} eigenvalues, total mult = 3")
else:
    results.fail("Eigen 3x3 simetris", f"Total multiplicity = {total_mult}")

# 5.3 Eigenvector verification
for val, mult, vects in E2.eigenvects():
    for v in vects:
        if sp.simplify(E2 * v - val * v) == sp.zeros(2, 1):
            results.ok(f"Eigenvector λ={val} — Av = λv ✓")
        else:
            results.fail(f"Eigenvector λ={val}", "Av != λv")


# =============================================================================
# TEST 6: DIAGONALISASI
# =============================================================================
print("\n" + "="*60)
print("TEST GROUP 6: Diagonalisasi")
print("="*60)

# 6.1 Matriks yang bisa didiagonalisasi
D_test = sp.Matrix([[4, 1], [2, 3]])
eigen_data = D_test.eigenvects()
total_vects = sum(len(v[2]) for v in eigen_data)
if total_vects == 2:
    results.ok("Diagonalisasi 2x2 — 2 eigenvectors (bisa)")
else:
    results.fail("Diagonalisasi 2x2", f"Only {total_vects} eigenvectors")

# 6.2 Matriks yang TIDAK bisa didiagonalisasi
D_no = sp.Matrix([[1, 1], [0, 1]])  # Defective matrix
eigen_no = D_no.eigenvects()
total_no = sum(len(v[2]) for v in eigen_no)
if total_no < 2:
    results.ok("Non-diagonalizable — terdeteksi (eigenvectors < n)")
else:
    results.fail("Non-diagonalizable", f"Got {total_no} eigenvectors")

# 6.3 Verifikasi A = PDP⁻¹
P_cols = []
D_vals = []
for val, mult, vects in D_test.eigenvects():
    for v in vects:
        P_cols.append(normalisasi(v))
        D_vals.append(val)
P_mat = sp.Matrix.hstack(*[sp.Matrix(v) for v in P_cols])
D_mat = sp.diag(*D_vals)
if sp.simplify(P_mat * D_mat * P_mat.inv() - D_test) == sp.zeros(2):
    results.ok("Verifikasi A = PDP⁻¹ ✓")
else:
    results.fail("Verifikasi PDP⁻¹", "A != PDP⁻¹")


# =============================================================================
# TEST 7: SVD
# =============================================================================
print("\n" + "="*60)
print("TEST GROUP 7: SVD")
print("="*60)

# 7.1 SVD 3x3
M_svd = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]], dtype=float)
U, s, Vt = np.linalg.svd(M_svd)
Sigma = np.zeros((3, 3))
np.fill_diagonal(Sigma, s)
reconstructed = U @ Sigma @ Vt
error = np.max(np.abs(M_svd - reconstructed))
if error < 1e-10:
    results.ok(f"SVD 3x3 — rekonstruksi error = {error:.2e}")
else:
    results.fail("SVD 3x3", f"Error = {error}")

# 7.2 SVD non-persegi (3x2)
M_rect = np.array([[1, 2], [3, 4], [5, 6]], dtype=float)
U2, s2, Vt2 = np.linalg.svd(M_rect)
Sigma2 = np.zeros((3, 2))
np.fill_diagonal(Sigma2, s2)
recon2 = U2 @ Sigma2 @ Vt2
error2 = np.max(np.abs(M_rect - recon2))
if error2 < 1e-10:
    results.ok(f"SVD 3x2 (non-persegi) — error = {error2:.2e}")
else:
    results.fail("SVD 3x2", f"Error = {error2}")

# 7.3 SVD rank
rank = np.sum(s > 1e-10)
if rank == 2:  # Matrix [[1,2,3],[4,5,6],[7,8,9]] has rank 2
    results.ok(f"SVD rank detection — rank = {rank}")
else:
    results.fail("SVD rank", f"Expected 2, got {rank}")


# =============================================================================
# TEST 8: FORMATTER
# =============================================================================
print("\n" + "="*60)
print("TEST GROUP 8: Formatter & Utilities")
print("="*60)

# 8.1 format_matriks
out = format_matriks(sp.Matrix([[1, 2], [3, 4]]))
if "┌" in out and "┘" in out and "1" in out:
    results.ok("format_matriks — bordered output")
else:
    results.fail("format_matriks", "Missing borders")

# 8.2 format_matriks_simple
out2 = format_matriks_simple(sp.Matrix([[1, -2], [3, 4]]))
if "[ 1" in out2 and "-2" in out2:
    results.ok("format_matriks_simple — bracket output")
else:
    results.fail("format_matriks_simple", f"Got: {out2}")

# 8.3 format_step_matrix augmented
aug = sp.Matrix([[1, 2, 3, 5], [4, 5, 6, 7]])
out3 = format_step_matrix(aug, augmented_cols=1)
if "│" in out3:
    results.ok("format_step_matrix augmented — separator │ present")
else:
    results.fail("format_step_matrix augmented", "Missing │")

# 8.4 normalisasi
v = normalisasi(sp.Matrix([sp.Rational(1, 2), 1, sp.Rational(3, 2)]))
if v == [1, 2, 3]:
    results.ok("normalisasi [1/2, 1, 3/2] → [1, 2, 3]")
else:
    results.fail("normalisasi", f"Got {v}")

# 8.5 normalisasi negatif
v2 = normalisasi(sp.Matrix([-2, 4, -6]))
if v2 == [-1, 2, -3]:
    results.ok("normalisasi [-2, 4, -6] → [-1, 2, -3]")
else:
    results.fail("normalisasi negatif", f"Got {v2}")

# 8.6 format_numpy_matrix
np_out = format_numpy_matrix(np.array([[1.5, 2.0], [3.0, 4.5]]), decimals=2)
if "1.50" in np_out and "4.50" in np_out:
    results.ok("format_numpy_matrix — decimal formatting")
else:
    results.fail("format_numpy_matrix", f"Got: {np_out}")


# =============================================================================
# TEST 9: EDGE CASES
# =============================================================================
print("\n" + "="*60)
print("TEST GROUP 9: Edge Cases")
print("="*60)

# 9.1 Matriks 1x1
M_1x1 = sp.Matrix([[7]])
det_1, _ = determinant_by_elimination(M_1x1)
if det_1 == 7:
    results.ok("Determinan 1x1 = 7")
else:
    results.fail("Determinan 1x1", f"Got {det_1}")

# 9.2 Matriks identitas
I3 = sp.eye(3)
det_i, _ = determinant_by_elimination(I3)
if det_i == 1:
    results.ok("Determinan I₃ = 1")
else:
    results.fail("Determinan I₃", f"Got {det_i}")

# 9.3 Invers identitas = identitas
inv_i, _ = gauss_jordan_inverse(I3)
if inv_i == I3:
    results.ok("Invers I₃ = I₃")
else:
    results.fail("Invers I₃", "inv(I) != I")

# 9.4 Matriks dengan angka besar
M_big = sp.Matrix([[100, 200], [300, 401]])
det_big, _ = determinant_by_elimination(M_big)
if det_big == M_big.det():
    results.ok(f"Determinan angka besar = {det_big}")
else:
    results.fail("Determinan angka besar", f"Got {det_big}")

# 9.5 Matriks dengan pecahan
M_frac2 = sp.Matrix([
    [sp.Rational(1, 3), sp.Rational(2, 5)],
    [sp.Rational(3, 7), sp.Rational(4, 9)]
])
inv_frac, _ = gauss_jordan_inverse(M_frac2)
if M_frac2 * inv_frac == sp.eye(2):
    results.ok("Invers matriks pecahan — A*A⁻¹ = I ✓")
else:
    results.fail("Invers pecahan", "A*A⁻¹ != I")

# 9.6 SPL 5x5
A5 = sp.Matrix([
    [2, 1, 0, 0, 0],
    [1, 3, 1, 0, 0],
    [0, 1, 4, 1, 0],
    [0, 0, 1, 5, 1],
    [0, 0, 0, 1, 6]
])
x_expected = sp.Matrix([1, 2, 3, 4, 5])
b5 = A5 * x_expected
sol_5, _ = solve_spl_gauss(A5, b5)
if sol_5["type"] == "unique":
    x5 = sp.Matrix(sol_5["values"])
    if x5 == x_expected:
        results.ok("SPL 5x5 — solusi benar [1,2,3,4,5]")
    else:
        results.fail("SPL 5x5", f"Got {sol_5['values']}")
else:
    results.fail("SPL 5x5", f"Type: {sol_5['type']}")


# =============================================================================
# TEST 10: IMPORT & STRUCTURE
# =============================================================================
print("\n" + "="*60)
print("TEST GROUP 10: Import & Structure")
print("="*60)

try:
    from config import DARK, LIGHT, MENU_ITEMS, FONT_LOGO
    results.ok("config.py — all constants importable")
except Exception as e:
    results.fail("config.py", str(e))

try:
    from components import (SidebarFrame, MatrixInputWidget, ResultConsoleWidget,
                           MethodSelector, ErrorBanner, Tooltip, StatusBar)
    results.ok("components — all 7 widgets importable")
except Exception as e:
    results.fail("components", str(e))

try:
    from pages import (SPLPage, DeterminanPage, InversPage,
                      LUPage, EigenPage, DiagonalPage, SVDPage)
    results.ok("pages — all 7 pages importable")
except Exception as e:
    results.fail("pages", str(e))

try:
    from app import ModernAlinApp
    results.ok("app.py — ModernAlinApp importable")
except Exception as e:
    results.fail("app.py", str(e))


# =============================================================================
# SUMMARY
# =============================================================================
success = results.summary()
sys.exit(0 if success else 1)
