# =============================================================================
# DETERMINAN_PAGE.PY — Halaman Determinan (dengan Step Engine)
# =============================================================================

import customtkinter as ctk
import sympy as sp
from config import FONT_HEADING, FONT_BODY, FONT_BUTTON
from components.matrix_input import MatrixInputWidget
from components.result_console import ResultConsoleWidget
from components.method_selector import MethodSelector
from components.error_banner import ErrorBanner
from logic.step_engine import determinant_by_elimination, format_step_matrix
from utils.formatter import format_matriks_simple


class DeterminanPage(ctk.CTkFrame):
    """
    Halaman Determinan dengan step-by-step engine.
    Metode: Kofaktor, Reduksi Baris, Sarrus (3×3)
    """

    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self._build_layout()

    def _build_layout(self):
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=30, pady=(25, 10))
        ctk.CTkLabel(header, text="⊡  Determinan", font=FONT_HEADING, anchor="w").pack(side="left")

        ctk.CTkFrame(self, height=1, fg_color=("gray75", "gray30")).pack(fill="x", padx=30, pady=(0, 15))

        content = ctk.CTkScrollableFrame(self, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=30, pady=(0, 15))

        self.error_banner = ErrorBanner(content)
        self.error_banner.pack(fill="x", pady=(0, 5))

        self.method_selector = MethodSelector(
            content,
            options=["Kofaktor", "Reduksi Baris", "Sarrus (3×3)"],
            default="Kofaktor",
            tooltips={
                "Kofaktor": "Ekspansi kofaktor sepanjang baris pertama",
                "Reduksi Baris": "Eliminasi ke segitiga atas (step-by-step)",
                "Sarrus (3×3)": "Metode Sarrus — hanya untuk matriks 3×3",
            },
        )
        self.method_selector.pack(fill="x", pady=(0, 15))

        self.matrix_input = MatrixInputWidget(content, default_rows=3, default_cols=3, label="Matriks (n×n)")
        self.matrix_input.pack(fill="x", pady=(0, 15))

        btn_frame = ctk.CTkFrame(content, fg_color="transparent")
        btn_frame.pack(fill="x", pady=(0, 15))
        ctk.CTkButton(btn_frame, text="⚡ Hitung Determinan", font=FONT_BUTTON,
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
            self.error_banner.show_error(f"Matriks harus persegi! Ukuran saat ini: {M.rows}×{M.cols}")
            return

        method = self.method_selector.get()

        try:
            if method == "Kofaktor":
                self._det_kofaktor(M)
            elif method == "Reduksi Baris":
                self._det_reduksi(M)
            elif method == "Sarrus (3×3)":
                self._det_sarrus(M)
        except Exception as e:
            self.result_console.insert_error(str(e))

    def _det_kofaktor(self, M):
        """Determinan via ekspansi kofaktor baris pertama."""
        n = M.rows
        self.result_console.insert("Metode: Ekspansi Kofaktor (Baris 1)\n\n", "step")
        self.result_console.insert("Matriks A:\n", "info")
        self.result_console.insert(format_step_matrix(M) + "\n", "matrix")
        self.result_console.insert_separator()

        if n == 1:
            self.result_console.insert_result(f"det(A) = {M[0,0]}")
            return

        if n == 2:
            det = M[0,0]*M[1,1] - M[0,1]*M[1,0]
            self.result_console.insert("\nRumus 2×2:\n", "step")
            self.result_console.insert(f"  det = a₁₁·a₂₂ - a₁₂·a₂₁\n", "info")
            self.result_console.insert(f"  det = ({M[0,0]})·({M[1,1]}) - ({M[0,1]})·({M[1,0]})\n", "info")
            self.result_console.insert(f"  det = {M[0,0]*M[1,1]} - {M[0,1]*M[1,0]}\n", "info")
            self.result_console.insert_result(f"det(A) = {det}")
            return

        # Ekspansi baris pertama
        det = sp.Integer(0)
        self.result_console.insert("\nEkspansi sepanjang baris 1:\n", "step")
        self.result_console.insert(f"  det(A) = Σ (-1)^(1+j) · a₁ⱼ · M₁ⱼ\n\n", "info")

        terms_str = []
        for j in range(n):
            sign = (-1) ** j
            sign_str = "+" if sign > 0 else "-"
            minor_matrix = M.minor_submatrix(0, j)
            minor_det = sp.Matrix(minor_matrix).det()
            cofactor = sign * M[0, j] * minor_det

            self.result_console.insert(f"▶ j = {j+1}:\n", "step")
            self.result_console.insert(f"  Tanda: (-1)^(1+{j+1}) = {sign_str}1\n", "info")
            self.result_console.insert(f"  a₁{j+1} = {M[0,j]}\n", "info")
            self.result_console.insert(f"  Minor M₁{j+1}:\n", "info")
            self.result_console.insert(format_step_matrix(sp.Matrix(minor_matrix)) + "\n", "matrix")
            self.result_console.insert(f"  det(M₁{j+1}) = {minor_det}\n", "info")
            self.result_console.insert(f"  Kofaktor C₁{j+1} = {sign_str}({M[0,j]})({minor_det}) = {cofactor}\n\n", "info")

            det += cofactor
            terms_str.append(f"({cofactor})")

        self.result_console.insert_separator()
        self.result_console.insert(f"\ndet(A) = {' + '.join(terms_str)}\n", "info")
        self.result_console.insert_result(f"det(A) = {det}")

    def _det_reduksi(self, M):
        """Determinan via reduksi baris — menggunakan step engine."""
        self.result_console.insert("Metode: Reduksi Baris (Eliminasi)\n\n", "step")
        self.result_console.insert("Matriks A:\n", "info")
        self.result_console.insert(format_step_matrix(M) + "\n", "matrix")
        self.result_console.insert_separator()

        # Use step engine
        det, steps = determinant_by_elimination(M)

        # Display steps
        for i, step in enumerate(steps[:-1]):  # Last step is the summary
            self.result_console.insert(f"\n▶ Langkah {i+1}: ", "step")
            self.result_console.insert(f"{step.operation}\n", "step")
            if step.description:
                self.result_console.insert(f"  ({step.description})\n", "info")
            self.result_console.insert(format_step_matrix(step.matrix) + "\n", "matrix")

        # Final summary
        if steps:
            last = steps[-1]
            self.result_console.insert_separator()
            self.result_console.insert(f"\nMatriks segitiga atas:\n", "step")
            self.result_console.insert(format_step_matrix(last.matrix) + "\n", "matrix")

            # Show diagonal
            n = M.rows
            diag_vals = [str(last.matrix[i, i]) for i in range(n)]
            self.result_console.insert(f"\nDiagonal: {' × '.join(diag_vals)}\n", "info")

        self.result_console.insert_result(f"det(A) = {det}")

    def _det_sarrus(self, M):
        """Determinan via metode Sarrus (3×3 only)."""
        if M.shape != (3, 3):
            self.error_banner.show_error("Metode Sarrus hanya untuk matriks 3×3!")
            return

        self.result_console.insert("Metode: Sarrus (3×3)\n\n", "step")
        self.result_console.insert("Matriks A:\n", "info")
        self.result_console.insert(format_step_matrix(M) + "\n", "matrix")
        self.result_console.insert_separator()

        a = M
        # Diagonal positif
        pos1 = a[0,0] * a[1,1] * a[2,2]
        pos2 = a[0,1] * a[1,2] * a[2,0]
        pos3 = a[0,2] * a[1,0] * a[2,1]

        # Diagonal negatif
        neg1 = a[0,2] * a[1,1] * a[2,0]
        neg2 = a[0,0] * a[1,2] * a[2,1]
        neg3 = a[0,1] * a[1,0] * a[2,2]

        self.result_console.insert("\n↘ Diagonal Positif (+):\n", "step")
        self.result_console.insert(f"  a₁₁·a₂₂·a₃₃ = ({a[0,0]})·({a[1,1]})·({a[2,2]}) = {pos1}\n", "info")
        self.result_console.insert(f"  a₁₂·a₂₃·a₃₁ = ({a[0,1]})·({a[1,2]})·({a[2,0]}) = {pos2}\n", "info")
        self.result_console.insert(f"  a₁₃·a₂₁·a₃₂ = ({a[0,2]})·({a[1,0]})·({a[2,1]}) = {pos3}\n", "info")
        self.result_console.insert(f"  Jumlah (+) = {pos1 + pos2 + pos3}\n\n", "info")

        self.result_console.insert("↙ Diagonal Negatif (-):\n", "step")
        self.result_console.insert(f"  a₁₃·a₂₂·a₃₁ = ({a[0,2]})·({a[1,1]})·({a[2,0]}) = {neg1}\n", "info")
        self.result_console.insert(f"  a₁₁·a₂₃·a₃₂ = ({a[0,0]})·({a[1,2]})·({a[2,1]}) = {neg2}\n", "info")
        self.result_console.insert(f"  a₁₂·a₂₁·a₃₃ = ({a[0,1]})·({a[1,0]})·({a[2,2]}) = {neg3}\n", "info")
        self.result_console.insert(f"  Jumlah (-) = {neg1 + neg2 + neg3}\n\n", "info")

        det = (pos1 + pos2 + pos3) - (neg1 + neg2 + neg3)
        self.result_console.insert_separator()
        self.result_console.insert(f"\ndet = ({pos1 + pos2 + pos3}) - ({neg1 + neg2 + neg3})\n", "info")
        self.result_console.insert_result(f"det(A) = {det}")
