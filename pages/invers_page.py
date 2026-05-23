# =============================================================================
# INVERS_PAGE.PY — Halaman Invers Matriks (dengan Step Engine)
# =============================================================================

import customtkinter as ctk
import sympy as sp
from config import FONT_HEADING, FONT_BUTTON
from components.matrix_input import MatrixInputWidget
from components.result_console import ResultConsoleWidget
from components.method_selector import MethodSelector
from components.error_banner import ErrorBanner
from logic.step_engine import gauss_jordan_inverse, format_step_matrix
from utils.formatter import format_matriks_simple


class InversPage(ctk.CTkFrame):
    """
    Halaman Invers dengan step-by-step engine.
    Metode: Adjugate, Gauss-Jordan, Built-in
    """

    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self._build_layout()

    def _build_layout(self):
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=30, pady=(25, 10))
        ctk.CTkLabel(header, text="⊟  Invers Matriks", font=FONT_HEADING, anchor="w").pack(side="left")

        ctk.CTkFrame(self, height=1, fg_color=("gray75", "gray30")).pack(fill="x", padx=30, pady=(0, 15))

        content = ctk.CTkScrollableFrame(self, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=30, pady=(0, 15))

        self.error_banner = ErrorBanner(content)
        self.error_banner.pack(fill="x", pady=(0, 5))

        self.method_selector = MethodSelector(
            content,
            options=["Adjugate", "Gauss-Jordan", "Built-in"],
            default="Gauss-Jordan",
            tooltips={
                "Adjugate": "A⁻¹ = (1/det(A)) × adj(A) — tampilkan kofaktor",
                "Gauss-Jordan": "[A|I] → [I|A⁻¹] — step-by-step eliminasi",
                "Built-in": "Langsung hitung + verifikasi A·A⁻¹ = I",
            },
        )
        self.method_selector.pack(fill="x", pady=(0, 15))

        self.matrix_input = MatrixInputWidget(content, default_rows=3, default_cols=3, label="Matriks (n×n)")
        self.matrix_input.pack(fill="x", pady=(0, 15))

        btn_frame = ctk.CTkFrame(content, fg_color="transparent")
        btn_frame.pack(fill="x", pady=(0, 15))
        ctk.CTkButton(btn_frame, text="⚡ Hitung Invers", font=FONT_BUTTON,
                      height=40, corner_radius=8, command=self._on_calculate).pack(side="left")

        self.result_console = ResultConsoleWidget(content)
        self.result_console.pack(fill="both", expand=True, pady=(0, 10))

    def _on_calculate(self):
        self.error_banner.hide()
        self.result_console.clear()

        try:
            M = self.matrix_input.get_matrix()
        except ValueError as e:
            self.error_banner.show_error(str(e))
            return

        if M.rows != M.cols:
            self.error_banner.show_error(f"Matriks harus persegi! Ukuran: {M.rows}×{M.cols}")
            return

        det = M.det()
        if det == 0:
            self.error_banner.show_error("Matriks singular (det = 0), invers tidak ada")
            return

        method = self.method_selector.get()

        try:
            if method == "Adjugate":
                self._inv_adjugate(M, det)
            elif method == "Gauss-Jordan":
                self._inv_gauss_jordan(M)
            elif method == "Built-in":
                self._inv_builtin(M, det)
        except Exception as e:
            self.result_console.insert_error(str(e))

    def _inv_adjugate(self, M, det):
        """Invers via adjugate: A⁻¹ = (1/det) × adj(A)."""
        n = M.rows
        self.result_console.insert("Metode: Adjugate\n", "step")
        self.result_console.insert("A⁻¹ = (1/det(A)) × adj(A)\n\n", "info")

        # Determinan
        self.result_console.insert(f"det(A) = {det}\n\n", "info")

        # Matriks Kofaktor (step-by-step untuk matriks kecil)
        if n <= 4:
            self.result_console.insert("Matriks Kofaktor C:\n", "step")
            self.result_console.insert("  Cᵢⱼ = (-1)^(i+j) × det(Mᵢⱼ)\n\n", "info")

            cof = sp.zeros(n)
            for i in range(n):
                for j in range(n):
                    minor = M.minor_submatrix(i, j)
                    minor_det = sp.Matrix(minor).det()
                    sign = (-1) ** (i + j)
                    cof[i, j] = sign * minor_det

            self.result_console.insert(format_step_matrix(cof) + "\n", "matrix")
        else:
            cof = M.cofactor_matrix()
            self.result_console.insert("Matriks Kofaktor:\n", "step")
            self.result_console.insert(format_step_matrix(cof) + "\n", "matrix")

        # Adjugate = transpose kofaktor
        adj = cof.T
        self.result_console.insert("\nAdj(A) = Cᵀ (transpose kofaktor):\n", "step")
        self.result_console.insert(format_step_matrix(adj) + "\n", "matrix")

        # Invers
        inv = adj / det
        self.result_console.insert_separator()
        self.result_console.insert(f"\nA⁻¹ = (1/{det}) × Adj(A):\n", "step")
        self.result_console.insert(format_step_matrix(inv) + "\n", "matrix")
        self.result_console.insert_result("Invers berhasil dihitung via Adjugate")

    def _inv_gauss_jordan(self, M):
        """Invers via Gauss-Jordan [A|I] → [I|A⁻¹] — step-by-step."""
        n = M.rows
        I = sp.eye(n)
        aug = M.row_join(I)

        self.result_console.insert("Metode: Gauss-Jordan\n", "step")
        self.result_console.insert("Augmentasi [A | I]:\n\n", "info")
        self.result_console.insert(format_step_matrix(aug, augmented_cols=n) + "\n", "matrix")
        self.result_console.insert_separator()

        # Use step engine
        try:
            inverse, steps = gauss_jordan_inverse(M)
        except ValueError as e:
            self.result_console.insert_error(str(e))
            return

        # Display steps
        for i, step in enumerate(steps):
            self.result_console.insert(f"\n▶ Langkah {i+1}: ", "step")
            self.result_console.insert(f"{step.operation}\n", "step")
            if step.description:
                self.result_console.insert(f"  ({step.description})\n", "info")
            self.result_console.insert(format_step_matrix(step.matrix, augmented_cols=n) + "\n", "matrix")

        # Final result
        self.result_console.insert_separator()
        self.result_console.insert(f"\nHasil [I | A⁻¹] → A⁻¹:\n", "step")
        self.result_console.insert(format_step_matrix(inverse) + "\n", "matrix")

        # Verifikasi
        self.result_console.insert(f"\nVerifikasi A × A⁻¹:\n", "info")
        product = M * inverse
        self.result_console.insert(format_step_matrix(product) + "\n", "matrix")
        self.result_console.insert_result("Invers berhasil dihitung via Gauss-Jordan ✓")

    def _inv_builtin(self, M, det):
        """Invers via built-in sympy + verifikasi."""
        self.result_console.insert("Metode: Built-in (sympy)\n\n", "step")
        self.result_console.insert(f"det(A) = {det}\n\n", "info")

        inv = M.inv()
        self.result_console.insert("A⁻¹:\n", "step")
        self.result_console.insert(format_step_matrix(inv) + "\n", "matrix")

        # Verifikasi
        self.result_console.insert_separator()
        self.result_console.insert("\nVerifikasi A × A⁻¹ = I:\n", "step")
        product = M * inv
        self.result_console.insert(format_step_matrix(product) + "\n", "matrix")

        is_identity = (product == sp.eye(M.rows))
        if is_identity:
            self.result_console.insert_result("A × A⁻¹ = I ✓ (Terverifikasi)")
        else:
            self.result_console.insert_result("Invers berhasil dihitung")
