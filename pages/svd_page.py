# =============================================================================
# SVD_PAGE.PY — Halaman Singular Value Decomposition
# =============================================================================

import customtkinter as ctk
import sympy as sp
import numpy as np
from config import FONT_HEADING, FONT_BUTTON
from components.matrix_input import MatrixInputWidget
from components.result_console import ResultConsoleWidget
from components.error_banner import ErrorBanner
from utils.formatter import format_numpy_matrix


class SVDPage(ctk.CTkFrame):
    """
    Halaman SVD: A = UΣVᵀ
    Menggunakan numpy untuk komputasi numerik.
    """

    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self._build_layout()

    def _build_layout(self):
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=30, pady=(25, 10))
        ctk.CTkLabel(header, text="Σ  Singular Value Decomposition", font=FONT_HEADING, anchor="w").pack(side="left")

        ctk.CTkFrame(self, height=1, fg_color=("gray75", "gray30")).pack(fill="x", padx=30, pady=(0, 15))

        content = ctk.CTkScrollableFrame(self, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=30, pady=(0, 15))

        self.error_banner = ErrorBanner(content)
        self.error_banner.pack(fill="x", pady=(0, 5))

        ctk.CTkLabel(
            content,
            text="SVD: A = U·Σ·Vᵀ\nMatriks tidak harus persegi. Hasil dalam bentuk numerik (desimal).",
            font=("Segoe UI", 11),
            text_color=("gray50", "gray60"),
            justify="left",
        ).pack(anchor="w", pady=(0, 15))

        self.matrix_input = MatrixInputWidget(content, default_rows=3, default_cols=3, label="Matriks (m×n)")
        self.matrix_input.pack(fill="x", pady=(0, 15))

        btn_frame = ctk.CTkFrame(content, fg_color="transparent")
        btn_frame.pack(fill="x", pady=(0, 15))
        ctk.CTkButton(btn_frame, text="⚡ Hitung SVD", font=FONT_BUTTON, height=40, corner_radius=8, command=self._on_calculate).pack(side="left")

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

        try:
            self._compute_svd(M)
        except Exception as e:
            self.result_console.insert_error(str(e))
            self.error_banner.show_error(f"Perhitungan gagal: {e}")

    def _compute_svd(self, M):
        """Hitung SVD menggunakan numpy."""
        m, n = M.shape

        self.result_console.insert(f"Matriks A ({m}×{n}):\n", "info")
        # Convert to numpy
        M_np = np.array(M.tolist(), dtype=float)
        self.result_console.insert_matrix(format_numpy_matrix(M_np, decimals=2))
        self.result_console.insert_separator()

        # Compute SVD
        U, s, Vt = np.linalg.svd(M_np)

        # Build Sigma matrix
        Sigma = np.zeros((m, n))
        np.fill_diagonal(Sigma, s)

        # Display U
        self.result_console.insert(f"\nMatriks U ({m}×{m}) — orthogonal:\n", "step")
        self.result_console.insert_matrix(format_numpy_matrix(U))

        # Display Sigma
        self.result_console.insert(f"\nMatriks Σ ({m}×{n}) — diagonal:\n", "step")
        self.result_console.insert_matrix(format_numpy_matrix(Sigma))

        # Display Vt
        self.result_console.insert(f"\nMatriks Vᵀ ({n}×{n}) — orthogonal:\n", "step")
        self.result_console.insert_matrix(format_numpy_matrix(Vt))

        # Singular values
        self.result_console.insert_separator()
        self.result_console.insert("\nSingular Values:\n", "step")
        for i, sv in enumerate(s):
            self.result_console.insert(f"  σ{i+1} = {sv:.6f}\n", "result")

        # Rank
        tol = max(m, n) * np.finfo(float).eps * s[0]
        rank = np.sum(s > tol)
        self.result_console.insert(f"\nRank matriks: {rank}\n", "info")

        # Verifikasi
        self.result_console.insert_separator()
        reconstructed = U @ Sigma @ Vt
        error = np.max(np.abs(M_np - reconstructed))
        self.result_console.insert(f"\nVerifikasi A = U·Σ·Vᵀ:\n", "step")
        self.result_console.insert(f"  Max error rekonstruksi: {error:.2e}\n", "info")

        if error < 1e-10:
            self.result_console.insert_result(f"SVD berhasil ✓ (rank = {rank})")
        else:
            self.result_console.insert_result(f"SVD selesai (rank = {rank})")
