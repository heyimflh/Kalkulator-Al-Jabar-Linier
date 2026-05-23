# =============================================================================
# EIGEN_PAGE.PY — Halaman Eigenvalue & Eigenvector
# =============================================================================

import customtkinter as ctk
import sympy as sp
from config import FONT_HEADING, FONT_BUTTON
from components.matrix_input import MatrixInputWidget
from components.result_console import ResultConsoleWidget
from components.error_banner import ErrorBanner
from utils.formatter import format_matriks_simple, format_polinom, normalisasi


class EigenPage(ctk.CTkFrame):
    """
    Halaman Eigen:
    - Polinomial karakteristik
    - Eigenvalues dengan multiplisitas
    - Eigenvectors (dinormalisasi ke integer)
    """

    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self._build_layout()

    def _build_layout(self):
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=30, pady=(25, 10))
        ctk.CTkLabel(header, text="λ  Eigenvalue & Eigenvector", font=FONT_HEADING, anchor="w").pack(side="left")

        ctk.CTkFrame(self, height=1, fg_color=("gray75", "gray30")).pack(fill="x", padx=30, pady=(0, 15))

        content = ctk.CTkScrollableFrame(self, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=30, pady=(0, 15))

        self.error_banner = ErrorBanner(content)
        self.error_banner.pack(fill="x", pady=(0, 5))

        ctk.CTkLabel(
            content,
            text="Menghitung polinomial karakteristik, eigenvalues, dan eigenvectors",
            font=("Segoe UI", 11),
            text_color=("gray50", "gray60"),
        ).pack(anchor="w", pady=(0, 15))

        self.matrix_input = MatrixInputWidget(content, default_rows=3, default_cols=3, label="Matriks (n×n)")
        self.matrix_input.pack(fill="x", pady=(0, 15))

        btn_frame = ctk.CTkFrame(content, fg_color="transparent")
        btn_frame.pack(fill="x", pady=(0, 15))
        ctk.CTkButton(btn_frame, text="⚡ Hitung Eigen", font=FONT_BUTTON, height=40, corner_radius=8, command=self._on_calculate).pack(side="left")

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

        try:
            self._compute_eigen(M)
        except Exception as e:
            self.result_console.insert_error(str(e))
            self.error_banner.show_error(f"Perhitungan gagal: {e}")

    def _compute_eigen(self, M):
        """Hitung eigenvalues dan eigenvectors."""
        self.result_console.insert("Matriks A:\n", "info")
        self.result_console.insert_matrix(format_matriks_simple(M))
        self.result_console.insert_separator()

        # Polinomial Karakteristik
        lam = sp.Symbol('λ')
        char_poly = sp.expand(M.charpoly(lam).as_expr())

        self.result_console.insert("\nPolinomial Karakteristik:\n", "step")
        self.result_console.insert(f"  p(λ) = {format_polinom(char_poly)}\n\n", "matrix")

        # Eigenvalues
        self.result_console.insert("Eigenvalues:\n", "step")
        eigenvals = M.eigenvals()
        for val, mult in eigenvals.items():
            self.result_console.insert(f"  λ = {val}", "result")
            if mult > 1:
                self.result_console.insert(f"  (multiplisitas aljabar = {mult})", "info")
            self.result_console.insert("\n", None)

        # Eigenvectors
        self.result_console.insert_separator()
        self.result_console.insert("\nEigenvectors:\n", "step")

        eigenvects = M.eigenvects()
        for val, mult, vects in eigenvects:
            self.result_console.insert(f"\n  Untuk λ = {val}:\n", "step")
            self.result_console.insert(f"  Multiplisitas aljabar = {mult}\n", "info")
            self.result_console.insert(f"  Multiplisitas geometri = {len(vects)}\n", "info")
            self.result_console.insert(f"  Basis eigenspace:\n", "info")

            for i, v in enumerate(vects):
                normalized = normalisasi(v)
                self.result_console.insert(f"    v{i+1} = {tuple(normalized)}\n", "result")

        self.result_console.insert_separator()
        total_vects = sum(len(v[2]) for v in eigenvects)
        self.result_console.insert(f"\nTotal eigenvectors independen: {total_vects}\n", "info")

        if total_vects == M.rows:
            self.result_console.insert_result("Matriks BISA didiagonalisasi (n eigenvector independen)")
        else:
            self.result_console.insert(f"⚠️ Matriks TIDAK bisa didiagonalisasi ({total_vects} < {M.rows})\n", "error")
