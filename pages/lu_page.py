# =============================================================================
# LU_PAGE.PY — Halaman Dekomposisi LU
# =============================================================================

import customtkinter as ctk
import sympy as sp
from config import FONT_HEADING, FONT_BUTTON
from components.matrix_input import MatrixInputWidget
from components.result_console import ResultConsoleWidget
from components.error_banner import ErrorBanner
from utils.formatter import format_matriks_simple


class LUPage(ctk.CTkFrame):
    """
    Halaman Dekomposisi LU: PA = LU
    """

    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self._build_layout()

    def _build_layout(self):
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=30, pady=(25, 10))
        ctk.CTkLabel(header, text="△  Dekomposisi LU", font=FONT_HEADING, anchor="w").pack(side="left")

        ctk.CTkFrame(self, height=1, fg_color=("gray75", "gray30")).pack(fill="x", padx=30, pady=(0, 15))

        content = ctk.CTkScrollableFrame(self, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=30, pady=(0, 15))

        self.error_banner = ErrorBanner(content)
        self.error_banner.pack(fill="x", pady=(0, 5))

        # Info
        ctk.CTkLabel(
            content,
            text="Dekomposisi PA = LU\nP = Permutasi, L = Lower Triangular, U = Upper Triangular",
            font=("Segoe UI", 11),
            text_color=("gray50", "gray60"),
            justify="left",
        ).pack(anchor="w", pady=(0, 15))

        self.matrix_input = MatrixInputWidget(content, default_rows=3, default_cols=3, label="Matriks (n×n)")
        self.matrix_input.pack(fill="x", pady=(0, 15))

        btn_frame = ctk.CTkFrame(content, fg_color="transparent")
        btn_frame.pack(fill="x", pady=(0, 15))
        ctk.CTkButton(btn_frame, text="⚡ Hitung LU", font=FONT_BUTTON, height=40, corner_radius=8, command=self._on_calculate).pack(side="left")

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
            self._compute_lu(M)
        except Exception as e:
            self.result_console.insert_error(str(e))
            self.error_banner.show_error(f"Dekomposisi gagal: {e}")

    def _compute_lu(self, M):
        """Hitung dekomposisi LU."""
        n = M.rows

        self.result_console.insert("Dekomposisi PA = LU\n\n", "step")
        self.result_console.insert("Matriks A:\n", "info")
        self.result_console.insert_matrix(format_matriks_simple(M))
        self.result_console.insert_separator()

        # Sympy LU decomposition
        L, U, perm = M.LUdecomposition()

        # Build permutation matrix
        P = sp.eye(n)
        for i, j in perm:
            P.row_swap(i, j)

        # Display results
        self.result_console.insert("\nMatriks P (Permutasi):\n", "step")
        self.result_console.insert_matrix(format_matriks_simple(P))

        self.result_console.insert("\nMatriks L (Lower Triangular):\n", "step")
        self.result_console.insert_matrix(format_matriks_simple(L))

        self.result_console.insert("\nMatriks U (Upper Triangular):\n", "step")
        self.result_console.insert_matrix(format_matriks_simple(U))

        # Verifikasi
        self.result_console.insert_separator()
        PA = P * M
        LU = L * U
        self.result_console.insert("\nVerifikasi PA = LU:\n", "step")
        self.result_console.insert("PA:\n", "info")
        self.result_console.insert_matrix(format_matriks_simple(PA))
        self.result_console.insert("\nLU:\n", "info")
        self.result_console.insert_matrix(format_matriks_simple(LU))

        if PA == LU:
            self.result_console.insert_result("PA = LU ✓ (Terverifikasi)")
        else:
            self.result_console.insert_result("Dekomposisi selesai")
