# =============================================================================
# DIAGONAL_PAGE.PY — Halaman Diagonalisasi
# =============================================================================

import customtkinter as ctk
import sympy as sp
from config import FONT_HEADING, FONT_BUTTON
from components.matrix_input import MatrixInputWidget
from components.result_console import ResultConsoleWidget
from components.error_banner import ErrorBanner
from utils.formatter import format_matriks_simple, normalisasi


class DiagonalPage(ctk.CTkFrame):
    """
    Halaman Diagonalisasi: A = PDP⁻¹
    """

    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self._build_layout()

    def _build_layout(self):
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=30, pady=(25, 10))
        ctk.CTkLabel(header, text="⋱  Diagonalisasi", font=FONT_HEADING, anchor="w").pack(side="left")

        ctk.CTkFrame(self, height=1, fg_color=("gray75", "gray30")).pack(fill="x", padx=30, pady=(0, 15))

        content = ctk.CTkScrollableFrame(self, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=30, pady=(0, 15))

        self.error_banner = ErrorBanner(content)
        self.error_banner.pack(fill="x", pady=(0, 5))

        ctk.CTkLabel(
            content,
            text="Diagonalisasi: A = P·D·P⁻¹\nP = matriks eigenvector, D = matriks diagonal eigenvalue",
            font=("Segoe UI", 11),
            text_color=("gray50", "gray60"),
            justify="left",
        ).pack(anchor="w", pady=(0, 15))

        self.matrix_input = MatrixInputWidget(content, default_rows=3, default_cols=3, label="Matriks (n×n)")
        self.matrix_input.pack(fill="x", pady=(0, 15))

        btn_frame = ctk.CTkFrame(content, fg_color="transparent")
        btn_frame.pack(fill="x", pady=(0, 15))
        ctk.CTkButton(btn_frame, text="⚡ Diagonalisasi", font=FONT_BUTTON, height=40, corner_radius=8, command=self._on_calculate).pack(side="left")

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
            self._compute_diagonal(M)
        except Exception as e:
            self.result_console.insert_error(str(e))
            self.error_banner.show_error(f"Perhitungan gagal: {e}")

    def _compute_diagonal(self, M):
        """Hitung diagonalisasi A = PDP⁻¹."""
        n = M.rows

        self.result_console.insert("Matriks A:\n", "info")
        self.result_console.insert_matrix(format_matriks_simple(M))
        self.result_console.insert_separator()

        # Get eigenvectors
        eigen_data = M.eigenvects()
        total_vects = sum(len(v[2]) for v in eigen_data)

        if total_vects < n:
            self.result_console.insert("\n", None)
            self.result_console.insert("❌ Matriks TIDAK bisa didiagonalisasi\n\n", "error")
            self.result_console.insert(f"Alasan: Hanya ditemukan {total_vects} eigenvector independen,\n", "info")
            self.result_console.insert(f"tetapi dibutuhkan {n} eigenvector untuk matriks {n}×{n}.\n\n", "info")

            # Tampilkan eigenvalues yang bermasalah
            self.result_console.insert("Detail eigenvalues:\n", "step")
            for val, mult, vects in eigen_data:
                geo_mult = len(vects)
                status = "✓" if geo_mult == mult else "✗"
                self.result_console.insert(
                    f"  λ = {val}: aljabar={mult}, geometri={geo_mult} {status}\n", "info"
                )
            self.error_banner.show_warning("Matriks tidak bisa didiagonalisasi")
            return

        # Build P and D
        P_cols = []
        D_vals = []

        self.result_console.insert("\nEigenvectors (kolom P):\n", "step")
        col_idx = 1
        for val, mult, vects in eigen_data:
            for v in vects:
                normalized = normalisasi(v)
                P_cols.append(normalized)
                D_vals.append(val)
                self.result_console.insert(f"  p{col_idx} = {tuple(normalized)}  (λ = {val})\n", "info")
                col_idx += 1

        # Construct matrices
        P = sp.Matrix.hstack(*[sp.Matrix(v) for v in P_cols])
        D = sp.diag(*D_vals)
        P_inv = P.inv()

        self.result_console.insert_separator()

        self.result_console.insert("\nMatriks P (eigenvectors):\n", "step")
        self.result_console.insert_matrix(format_matriks_simple(P))

        self.result_console.insert("\nMatriks D (diagonal eigenvalues):\n", "step")
        self.result_console.insert_matrix(format_matriks_simple(D))

        self.result_console.insert("\nMatriks P⁻¹:\n", "step")
        self.result_console.insert_matrix(format_matriks_simple(P_inv))

        # Verifikasi
        self.result_console.insert_separator()
        self.result_console.insert("\nVerifikasi A = P·D·P⁻¹:\n", "step")
        product = P * D * P_inv
        self.result_console.insert_matrix(format_matriks_simple(product))

        if sp.simplify(product - M) == sp.zeros(n):
            self.result_console.insert_result("A = P·D·P⁻¹ ✓ (Terverifikasi)")
        else:
            self.result_console.insert_result("Diagonalisasi selesai")
