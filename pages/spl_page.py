# =============================================================================
# SPL_PAGE.PY — Halaman Sistem Persamaan Linear (dengan Step Engine)
# =============================================================================

import customtkinter as ctk
import sympy as sp
from config import FONT_HEADING, FONT_BODY, FONT_BUTTON, FONT_SMALL
from components.matrix_input import MatrixInputWidget
from components.result_console import ResultConsoleWidget
from components.method_selector import MethodSelector
from components.error_banner import ErrorBanner
from logic.step_engine import (
    solve_spl_gauss, solve_spl_gauss_jordan,
    format_step_matrix
)
from utils.formatter import format_matriks_simple


class SPLPage(ctk.CTkFrame):
    """
    Halaman SPL dengan step-by-step engine.
    Metode: Gauss, Gauss-Jordan, Matriks Balikan
    """

    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self._build_layout()

    def _build_layout(self):
        # ─── Header ───
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=30, pady=(25, 10))
        ctk.CTkLabel(header, text="⊞  Sistem Persamaan Linear (SPL)", font=FONT_HEADING, anchor="w").pack(side="left")

        ctk.CTkFrame(self, height=1, fg_color=("gray75", "gray30")).pack(fill="x", padx=30, pady=(0, 15))

        # ─── Scrollable Content ───
        content = ctk.CTkScrollableFrame(self, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=30, pady=(0, 15))

        # Error Banner
        self.error_banner = ErrorBanner(content)
        self.error_banner.pack(fill="x", pady=(0, 5))

        # Method Selector
        self.method_selector = MethodSelector(
            content,
            options=["Gauss", "Gauss-Jordan", "Matriks Balikan"],
            default="Gauss",
            tooltips={
                "Gauss": "Eliminasi ke bentuk REF + back substitution",
                "Gauss-Jordan": "Eliminasi ke bentuk RREF (solusi langsung terbaca)",
                "Matriks Balikan": "Solusi via x = A⁻¹·b (hanya matriks persegi non-singular)",
            },
        )
        self.method_selector.pack(fill="x", pady=(0, 15))

        # ─── Matrix Inputs (A dan b) ───
        matrix_frame = ctk.CTkFrame(content, fg_color="transparent")
        matrix_frame.pack(fill="x", pady=(0, 15))
        matrix_frame.grid_columnconfigure(0, weight=3)
        matrix_frame.grid_columnconfigure(1, weight=1)

        self.matrix_a = MatrixInputWidget(matrix_frame, default_rows=3, default_cols=3, label="Matriks A (Koefisien)")
        self.matrix_a.grid(row=0, column=0, sticky="nsew", padx=(0, 15))

        self.matrix_b = MatrixInputWidget(matrix_frame, default_rows=3, default_cols=1, label="Vektor b (Konstanta)")
        self.matrix_b.grid(row=0, column=1, sticky="nsew")

        # ─── Calculate Button ───
        btn_frame = ctk.CTkFrame(content, fg_color="transparent")
        btn_frame.pack(fill="x", pady=(0, 15))
        self.calc_button = ctk.CTkButton(
            btn_frame, text="⚡ Hitung SPL", font=FONT_BUTTON,
            height=40, corner_radius=8, command=self._on_calculate
        )
        self.calc_button.pack(side="left")
        ctk.CTkLabel(btn_frame, text="Ctrl+Enter", font=("Segoe UI", 10),
                     text_color=("gray50", "gray60")).pack(side="left", padx=(10, 0))

        # ─── Result Console ───
        self.result_console = ResultConsoleWidget(content)
        self.result_console.pack(fill="both", expand=True, pady=(0, 10))

    def _on_calculate(self):
        """Handle perhitungan SPL."""
        self.error_banner.hide()
        self.result_console.clear()

        # Get matrices
        try:
            A = self.matrix_a.get_matrix()
            b = self.matrix_b.get_matrix()
        except ValueError as e:
            self.error_banner.show_error(str(e))
            return

        # Validasi dimensi
        if A.rows != b.rows:
            self.error_banner.show_error(
                f"Jumlah baris A ({A.rows}) harus sama dengan baris b ({b.rows})"
            )
            return

        method = self.method_selector.get()

        try:
            if method == "Gauss":
                self._solve_gauss(A, b)
            elif method == "Gauss-Jordan":
                self._solve_gauss_jordan(A, b)
            elif method == "Matriks Balikan":
                self._solve_inverse(A, b)
        except Exception as e:
            self.result_console.insert_error(str(e))
            self.error_banner.show_error(f"Perhitungan gagal: {e}")

    def _solve_gauss(self, A, b):
        """Eliminasi Gauss dengan step-by-step engine."""
        aug = A.row_join(b)
        self.result_console.insert("Metode: Eliminasi Gauss\n\n", "step")
        self.result_console.insert("Matriks Augmented [A|b]:\n", "info")
        self.result_console.insert(format_step_matrix(aug, augmented_cols=b.cols) + "\n", "matrix")
        self.result_console.insert_separator()

        # Solve with step engine
        solution, steps = solve_spl_gauss(A, b)

        # Display steps
        for i, step in enumerate(steps):
            self.result_console.insert(f"\n▶ Langkah {i+1}: ", "step")
            self.result_console.insert(f"{step.operation}\n", "step")
            if step.description:
                self.result_console.insert(f"  ({step.description})\n", "info")
            self.result_console.insert(
                format_step_matrix(step.matrix, augmented_cols=b.cols) + "\n", "matrix"
            )

        # Display solution
        self._display_solution(solution)

    def _solve_gauss_jordan(self, A, b):
        """Eliminasi Gauss-Jordan dengan step-by-step engine."""
        aug = A.row_join(b)
        self.result_console.insert("Metode: Eliminasi Gauss-Jordan\n\n", "step")
        self.result_console.insert("Matriks Augmented [A|b]:\n", "info")
        self.result_console.insert(format_step_matrix(aug, augmented_cols=b.cols) + "\n", "matrix")
        self.result_console.insert_separator()

        # Solve with step engine
        solution, steps = solve_spl_gauss_jordan(A, b)

        # Display steps
        for i, step in enumerate(steps):
            self.result_console.insert(f"\n▶ Langkah {i+1}: ", "step")
            self.result_console.insert(f"{step.operation}\n", "step")
            if step.description:
                self.result_console.insert(f"  ({step.description})\n", "info")
            self.result_console.insert(
                format_step_matrix(step.matrix, augmented_cols=b.cols) + "\n", "matrix"
            )

        # Display solution
        self._display_solution(solution)

    def _solve_inverse(self, A, b):
        """Solusi via x = A⁻¹·b."""
        if A.rows != A.cols:
            self.error_banner.show_error("Matriks A harus persegi untuk metode Matriks Balikan")
            return

        det = A.det()
        if det == 0:
            self.error_banner.show_error("Matriks A singular (det = 0), tidak bisa dihitung inversnya")
            return

        self.result_console.insert("Metode: x = A⁻¹ · b\n\n", "step")
        self.result_console.insert(f"det(A) = {det}\n\n", "info")

        A_inv = A.inv()
        self.result_console.insert("A⁻¹:\n", "step")
        self.result_console.insert(format_matriks_simple(A_inv) + "\n", "matrix")
        self.result_console.insert_separator()

        x = A_inv * b
        self.result_console.insert("\nx = A⁻¹·b:\n", "step")
        self.result_console.insert(format_matriks_simple(x) + "\n", "matrix")

        # Format solusi
        sol_parts = []
        for i in range(x.rows):
            sol_parts.append(f"x{i+1} = {sp.nsimplify(x[i, 0])}")
        self.result_console.insert_result(", ".join(sol_parts))

    def _display_solution(self, solution):
        """Display solution info dari step engine."""
        self.result_console.insert_separator()

        if solution["type"] == "unique":
            values = solution["values"]
            sol_parts = [f"x{i+1} = {sp.nsimplify(v)}" for i, v in enumerate(values)]
            self.result_console.insert_result("Solusi unik: " + ", ".join(sol_parts))

        elif solution["type"] == "none":
            self.result_console.insert(f"\n❌ {solution['message']}\n", "error")

        elif solution["type"] == "infinite":
            self.result_console.insert(f"\n∞ {solution['message']}\n", "step")
            # Tampilkan variabel bebas
            if "pivot_cols" in solution:
                n_vars = solution["matrix"].cols - 1
                pivot_cols = solution["pivot_cols"]
                free_vars = [i for i in range(n_vars) if i not in pivot_cols]
                if free_vars:
                    free_str = ", ".join(f"x{i+1}" for i in free_vars)
                    self.result_console.insert(f"  Variabel bebas: {free_str}\n", "info")
