# =============================================================================
# DETERMINAN_PAGE.PY — Halaman Determinan (dengan Step Engine)
# -----------------------------------------------------------------------------
# UI/UX: "Scientific Laboratory" — selaras dengan halaman SPL.
#   • Light Mode  : "Amethyst Haze"  (crisp slate-white + royal lavender)
#   • Dark Mode   : "Cosmic Night"   (deep space + neon lavender)
#
# CATATAN PENTING: Hanya struktur layout, frame, dan parameter tema yang
# diubah. Seluruh logika matematika & metode (Kofaktor, Reduksi Baris,
# Sarrus) beserta data binding tetap 100% utuh & fungsional.
# =============================================================================

import customtkinter as ctk
import sympy as sp
from config import FONT_HEADING, FONT_BODY, FONT_BUTTON, FONT_SMALL
from components.matrix_input import MatrixInputWidget
from components.result_console import ResultConsoleWidget
from components.method_selector import MethodSelector
from components.error_banner import ErrorBanner
from logic.step_engine import determinant_by_elimination, format_step_matrix
from utils.formatter import format_matriks_simple


# ─────────────────────────────────────────────────────────────────────────────
# DUAL-THEME COLOR TOKENS — tuple format (light_color, dark_color)
#   Light : "Amethyst Haze"   |   Dark : "Cosmic Night"
#   (Identik dengan halaman SPL agar suasana desain konsisten.)
# ─────────────────────────────────────────────────────────────────────────────
COLOR_APP_BG         = ("#F8FAFC", "#0B0B14")   # Crisp slate-white / deep space
COLOR_MAIN_CARD      = ("#F1F5F9", "#141423")   # Top & bottom panels
COLOR_WORKSPACE_CARD = ("#FFFFFF", "#1E1E2F")   # Bright workspace / cosmic gray
COLOR_SUB_CARD       = ("#F3E8FF", "#252538")   # Isolated lavender / dark pocket
COLOR_BORDER         = ("#E9D5FF", "#2E2E44")   # Card framing border
COLOR_TEXT_MAIN      = ("#1E3A8A", "#FFFFFF")   # Deep indigo / white
COLOR_TEXT_MUTED     = ("#6B21A8", "#94A3B8")   # Royal purple / slate
COLOR_INPUT_BG       = ("#FFFFFF", "#1A1A26")
COLOR_INPUT_BORDER   = ("#D8B4FE", "#3F3F5C")
COLOR_BUTTON_SUBTLE  = ("#F3E8FF", "#2E2E44")
COLOR_BUTTON_TEXT    = ("#6B21A8", "#A78BFA")
COLOR_ACCENT_CEMENT  = ("#7C3AED", "#A78BFA")   # Big action button glow
COLOR_ACCENT_HOVER   = ("#6D28D9", "#C084FC")


class DeterminanPage(ctk.CTkFrame):
    """
    Halaman Determinan dengan step-by-step engine.
    Metode: Kofaktor, Reduksi Baris, Sarrus (3×3)
    """

    def __init__(self, master, **kwargs):
        # Page base — workspace canvas
        super().__init__(master, fg_color=COLOR_APP_BG, **kwargs)
        self._last_mode = ctk.get_appearance_mode()
        self._build_layout()
        # Self-contained watcher → restyle raw tk.Text console on theme toggle.
        self._watch_theme()

    # ─────────────────────────────────────────────
    # STYLE PRESETS (diteruskan ke komponen bersama)
    # ─────────────────────────────────────────────
    def _matrix_style(self):
        """Style token untuk MatrixInputWidget (cells, selectors, toolbar)."""
        return {
            "label_color": COLOR_TEXT_MAIN,
            "muted_color": COLOR_TEXT_MUTED,
            # Matrix entry cells — perfectly square, crisp framing
            "cell_fg": COLOR_INPUT_BG,
            "cell_text": COLOR_TEXT_MAIN,
            "cell_border": COLOR_INPUT_BORDER,
            "cell_border_focus": COLOR_ACCENT_CEMENT,
            "cell_radius": 6,
            "cell_width": 46,
            "cell_height": 46,
            # Sel + font menyusut otomatis agar muat di lebar kartu
            # (anti-clipping horizontal pd orde besar 10×10), tetap persegi.
            "adaptive_cells": True,
            "cell_min": 30,
            # Dimension selectors (Baris/Kolom) — stacked so they never clip
            "selector_fg": COLOR_INPUT_BG,
            "selector_button": COLOR_ACCENT_CEMENT,
            "selector_button_hover": COLOR_ACCENT_HOVER,
            "selector_text": COLOR_TEXT_MAIN,
            "selector_width": 58,
            "header_stack": True,
            # Grid tumbuh dinamis: tanpa kotak scroll internal → tidak ada
            # konflik nested-scroll & tidak ada clipping utk orde besar (10×10).
            "grid_scroll": False,
            # Utility toolbar — modern outlined chip buttons, responsive wrap
            "util_fg": COLOR_BUTTON_SUBTLE,
            "util_hover": COLOR_BORDER,
            "util_text": COLOR_BUTTON_TEXT,
            "util_border": COLOR_BUTTON_TEXT,   # visible outline (both themes)
            "util_border_width": 1,
            "toolbar_wrap": True,
            "toolbar_cols": 3,
        }

    def _method_style(self):
        """Style token untuk MethodSelector (segmented button).

        CTkSegmentedButton hanya punya SATU text_color per tema, sehingga
        warna chip dipilih agar SATU warna teks terbaca baik di chip terpilih
        maupun tak-terpilih (light: ungu tua di lavender; dark: putih di gelap).
        """
        return {
            "label_color": COLOR_TEXT_MAIN,
            "muted_color": COLOR_TEXT_MUTED,
            "seg_fg": COLOR_SUB_CARD,                          # gap / track
            "seg_selected": ("#C4B5FD", "#7C3AED"),            # chip aktif
            "seg_selected_hover": ("#DDD6FE", "#8B5CF6"),
            "seg_unselected": ("#F3E8FF", "#252538"),          # chip idle
            "seg_unselected_hover": ("#E9D5FF", "#2E2E44"),
            "seg_text": ("#5B21B6", "#FFFFFF"),                # 1 warna / tema
        }

    # ─────────────────────────────────────────────
    # LAYOUT — Elevated card system (selaras SPL)
    # ─────────────────────────────────────────────
    def _build_layout(self):
        # Scroll surface keeps the app background visible behind the cards.
        content = ctk.CTkScrollableFrame(self, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=26, pady=22)
        self._scroll_frame = content   # disimpan utk auto-scroll ke hasil

        # Inline error banner (di atas semua card)
        self.error_banner = ErrorBanner(content)
        self.error_banner.pack(fill="x", pady=(0, 6))

        # ════════════════════════════════════════════════════════════════
        # PANEL 1 — METHOD SELECTION CARD
        # ════════════════════════════════════════════════════════════════
        method_card = ctk.CTkFrame(
            content,
            fg_color=COLOR_MAIN_CARD,
            border_width=1,
            border_color=COLOR_BORDER,
            corner_radius=16,
        )
        method_card.pack(fill="x", pady=(0, 18))

        ctk.CTkLabel(
            method_card,
            text="⊡   Determinan",
            font=FONT_HEADING,
            text_color=COLOR_TEXT_MAIN,
            anchor="w",
        ).pack(fill="x", padx=24, pady=(20, 2))

        ctk.CTkLabel(
            method_card,
            text="Hitung det(A) langkah demi langkah. Pilih metode, "
                 "isi matriks persegi, lalu jalankan.",
            font=FONT_SMALL,
            text_color=COLOR_TEXT_MUTED,
            anchor="w",
        ).pack(fill="x", padx=24, pady=(0, 14))

        self.method_selector = MethodSelector(
            method_card,
            options=["Kofaktor", "Reduksi Baris", "Sarrus (3×3)"],
            default="Kofaktor",
            tooltips={
                "Kofaktor": "Ekspansi kofaktor sepanjang baris pertama",
                "Reduksi Baris": "Eliminasi ke segitiga atas (step-by-step)",
                "Sarrus (3×3)": "Metode Sarrus — hanya untuk matriks 3×3",
            },
            style=self._method_style(),
        )
        self.method_selector.pack(fill="x", padx=24, pady=(0, 20))

        # ════════════════════════════════════════════════════════════════
        # PANEL 2 — MATRIX WORKSPACE (satu sub-card untuk matriks n×n)
        # ════════════════════════════════════════════════════════════════
        workspace_card = ctk.CTkFrame(
            content,
            fg_color=COLOR_WORKSPACE_CARD,
            border_width=1,
            border_color=COLOR_BORDER,
            corner_radius=16,
        )
        workspace_card.pack(fill="x", pady=(0, 18))

        ctk.CTkLabel(
            workspace_card,
            text="🧮   Workspace Matriks",
            font=FONT_BODY,
            text_color=COLOR_TEXT_MAIN,
            anchor="w",
        ).pack(fill="x", padx=22, pady=(18, 12))

        # Holder agar konsisten dgn SPL (grid container di dalam workspace).
        holder = ctk.CTkFrame(workspace_card, fg_color="transparent")
        holder.pack(fill="both", expand=True, padx=22, pady=(0, 22))
        holder.grid_columnconfigure(0, weight=1)
        holder.grid_rowconfigure(0, weight=1)

        # Sub-Card: Matriks A (persegi n×n)
        sub_a = ctk.CTkFrame(
            holder,
            fg_color=COLOR_SUB_CARD,
            border_width=1,
            border_color=COLOR_BORDER,
            corner_radius=12,
        )
        sub_a.grid(row=0, column=0, sticky="nsew")

        self.matrix_input = MatrixInputWidget(
            sub_a, default_rows=3, default_cols=3,
            label="Matriks A (n×n)", style=self._matrix_style(),
        )
        self.matrix_input.pack(fill="both", expand=True, padx=16, pady=16)

        # ════════════════════════════════════════════════════════════════
        # PANEL 3 — ACTION (wide, centered)
        # ════════════════════════════════════════════════════════════════
        action_bar = ctk.CTkFrame(content, fg_color="transparent")
        action_bar.pack(fill="x", pady=(0, 18))

        self.calc_button = ctk.CTkButton(
            action_bar, text="⚡   Hitung Determinan", font=FONT_BUTTON,
            width=420, height=50, corner_radius=12,
            fg_color=COLOR_ACCENT_CEMENT, hover_color=COLOR_ACCENT_HOVER,
            command=self._on_calculate,
        )
        self.calc_button.pack(anchor="center", pady=(0, 4))

        ctk.CTkLabel(
            action_bar, text="Pintasan: Ctrl+Enter", font=("Segoe UI", 10),
            text_color=COLOR_TEXT_MUTED,
        ).pack(anchor="center")

        # ════════════════════════════════════════════════════════════════
        # PANEL 4 — PREMIUM OUTPUT TERMINAL
        # ════════════════════════════════════════════════════════════════
        result_card = ctk.CTkFrame(
            content,
            fg_color=COLOR_MAIN_CARD,
            border_width=1,
            border_color=COLOR_BORDER,
            corner_radius=16,
        )
        result_card.pack(fill="both", expand=True, pady=(0, 4))
        self._result_card = result_card   # target auto-scroll

        self.result_console = ResultConsoleWidget(result_card, fg_color="transparent")
        self.result_console.pack(fill="both", expand=True, padx=25, pady=25)

    # ─────────────────────────────────────────────
    # AUTO-SCROLL KE HASIL (UX: user tak perlu scroll manual)
    # ─────────────────────────────────────────────
    def _scroll_to_results(self):
        """Geser scrollable frame agar kartu hasil terlihat penuh."""
        try:
            canvas = self._scroll_frame._parent_canvas
            self.update_idletasks()
            card_y = self._result_card.winfo_y()
            total = canvas.bbox("all")
            if not total:
                return
            total_h = total[3] - total[1]
            if total_h <= 0:
                return
            frac = max(0.0, min(1.0, card_y / total_h))
            canvas.yview_moveto(frac)
        except Exception:
            pass  # canvas belum siap / widget destroyed

    # ─────────────────────────────────────────────
    # THEME WATCHER (self-contained, tidak menyentuh app.py)
    # ─────────────────────────────────────────────
    def _watch_theme(self):
        """Pantau perubahan appearance mode → restyle console tk.Text."""
        try:
            mode = ctk.get_appearance_mode()
            if mode != self._last_mode:
                self._last_mode = mode
                self.result_console.update_theme()
        except Exception:
            return  # widget sudah destroyed
        if self.winfo_exists():
            self.after(400, self._watch_theme)

    # =========================================================================
    # ░░  LOGIKA PERHITUNGAN — TIDAK DIUBAH (data binding & metode utuh)  ░░
    # =========================================================================

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

        # UX: arahkan tampilan ke hasil setelah konten ter-render.
        self.after(60, self._scroll_to_results)

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
