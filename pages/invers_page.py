# =============================================================================
# INVERS_PAGE.PY — Halaman Invers Matriks (dengan Step Engine)
# -----------------------------------------------------------------------------
# UI/UX: "Scientific Laboratory" — selaras dengan halaman SPL & Determinan.
#   • Light Mode  : "Amethyst Haze"  (crisp slate-white + royal lavender)
#   • Dark Mode   : "Cosmic Night"   (deep space + neon lavender)
#
# CATATAN PENTING: Hanya struktur layout, frame, dan parameter tema yang
# diubah. Seluruh logika matematika & metode (Adjugate, Gauss-Jordan,
# Built-in) beserta data binding tetap 100% utuh & fungsional.
# =============================================================================

import customtkinter as ctk
import sympy as sp
from config import FONT_HEADING, FONT_BODY, FONT_BUTTON, FONT_SMALL
from components.matrix_input import MatrixInputWidget
from components.result_console import ResultConsoleWidget
from components.method_selector import MethodSelector
from components.error_banner import ErrorBanner
from logic.step_engine import gauss_jordan_inverse, format_step_matrix
from utils.formatter import format_matriks_simple


# ─────────────────────────────────────────────────────────────────────────────
# DUAL-THEME COLOR TOKENS — tuple format (light_color, dark_color)
#   Light : "Amethyst Haze"   |   Dark : "Cosmic Night"
#   (Identik dengan halaman SPL & Determinan agar suasana desain konsisten.)
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


class InversPage(ctk.CTkFrame):
    """
    Halaman Invers dengan step-by-step engine.
    Metode: Adjugate, Gauss-Jordan, Built-in
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
    def _matrix_style(self, toolbar_cols=3):
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
            # Utility toolbar — modern outlined chip buttons, responsive grid
            "util_fg": COLOR_BUTTON_SUBTLE,
            "util_hover": COLOR_BORDER,
            "util_text": COLOR_BUTTON_TEXT,
            "util_border": COLOR_BUTTON_TEXT,   # visible outline (both themes)
            "util_border_width": 1,
            "toolbar_wrap": True,
            "toolbar_cols": toolbar_cols,
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
    # LAYOUT — Elevated card system (selaras SPL/Determinan)
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
            text="⊟   Invers Matriks",
            font=FONT_HEADING,
            text_color=COLOR_TEXT_MAIN,
            anchor="w",
        ).pack(fill="x", padx=24, pady=(20, 2))

        ctk.CTkLabel(
            method_card,
            text="Hitung A⁻¹ langkah demi langkah. Pilih metode, "
                 "isi matriks persegi non-singular, lalu jalankan.",
            font=FONT_SMALL,
            text_color=COLOR_TEXT_MUTED,
            anchor="w",
        ).pack(fill="x", padx=24, pady=(0, 14))

        self.method_selector = MethodSelector(
            method_card,
            options=["Adjugate", "Gauss-Jordan", "Built-in"],
            default="Gauss-Jordan",
            tooltips={
                "Adjugate": "A⁻¹ = (1/det(A)) × adj(A) — tampilkan kofaktor",
                "Gauss-Jordan": "[A|I] → [I|A⁻¹] — step-by-step eliminasi",
                "Built-in": "Langsung hitung + verifikasi A·A⁻¹ = I",
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

        # Holder agar konsisten dgn SPL/Determinan (grid di dalam workspace).
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
            label="Matriks A (n×n)", style=self._matrix_style(toolbar_cols=3),
        )
        self.matrix_input.pack(fill="both", expand=True, padx=16, pady=16)

        # ════════════════════════════════════════════════════════════════
        # PANEL 3 — ACTION (wide, centered)
        # ════════════════════════════════════════════════════════════════
        action_bar = ctk.CTkFrame(content, fg_color="transparent")
        action_bar.pack(fill="x", pady=(0, 18))

        self.calc_button = ctk.CTkButton(
            action_bar, text="⚡   Hitung Invers", font=FONT_BUTTON,
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
    # ░░  LOGIKA PERHITUNGAN — komputasi berat di BACKGROUND THREAD  ░░
    # Logika metode (Adjugate, Gauss-Jordan, Built-in) tetap utuh; hanya
    # arsitektur threading & step-recording (skip utk n>6) yang dioptimasi.
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
            self.error_banner.show_error(f"Matriks harus persegi! Ukuran: {M.rows}×{M.cols}")
            return

        method = self.method_selector.get()

        # det() bisa berat utk matriks besar → hitung di background thread.
        self.calc_button.configure(state="disabled", text="⏳  Menghitung...")
        self.result_console.insert("Menghitung...\n", "info")

        import threading
        t = threading.Thread(target=self._run_compute, args=(M, method), daemon=True)
        t.start()

    def _run_compute(self, M, method):
        """Background thread: hitung invers tanpa menyentuh widget Tk."""
        try:
            det = M.det()
            if det == 0:
                self.after(0, lambda: self._on_singular())
                return

            from components.result_console import ConsoleBuffer
            buf = ConsoleBuffer()
            if method == "Adjugate":
                self._inv_adjugate(M, det, buf)
            elif method == "Gauss-Jordan":
                self._inv_gauss_jordan(M, buf)
            elif method == "Built-in":
                self._inv_builtin(M, det, buf)
            result = {"buffer": buf}
        except Exception as e:
            msg = str(e)
            self.after(0, lambda: self._on_compute_error(msg))
            return
        self.after(0, lambda: self._on_compute_done(result))

    def _on_compute_done(self, result):
        """Render hasil ke UI (main thread via self.after)."""
        self.calc_button.configure(state="normal", text="⚡   Hitung Invers")
        self.result_console.clear()
        result["buffer"].replay(self.result_console)
        self.after(60, self._scroll_to_results)

    def _on_compute_error(self, msg):
        """Tampilkan error (main thread via self.after)."""
        self.calc_button.configure(state="normal", text="⚡   Hitung Invers")
        self.result_console.clear()
        self.result_console.insert_error(msg)
        self.error_banner.show_error(f"Perhitungan gagal: {msg}")

    def _on_singular(self):
        """Matriks singular (det = 0) — kembalikan tombol & tampilkan error."""
        self.calc_button.configure(state="normal", text="⚡   Hitung Invers")
        self.result_console.clear()
        self.error_banner.show_error("Matriks singular (det = 0), invers tidak ada")

    def _inv_adjugate(self, M, det, console):
        """Invers via adjugate: A⁻¹ = (1/det) × adj(A)."""
        n = M.rows
        console.insert("Metode: Adjugate\n", "step")
        console.insert("A⁻¹ = (1/det(A)) × adj(A)\n\n", "info")

        # Determinan
        console.insert(f"det(A) = {det}\n\n", "info")

        # Matriks Kofaktor (step-by-step untuk matriks kecil)
        if n <= 4:
            console.insert("Matriks Kofaktor C:\n", "step")
            console.insert("  Cᵢⱼ = (-1)^(i+j) × det(Mᵢⱼ)\n\n", "info")

            cof = sp.zeros(n)
            for i in range(n):
                for j in range(n):
                    minor = M.minor_submatrix(i, j)
                    minor_det = sp.Matrix(minor).det()
                    sign = (-1) ** (i + j)
                    cof[i, j] = sign * minor_det

            console.insert(format_step_matrix(cof) + "\n", "matrix")
        else:
            cof = M.cofactor_matrix()
            console.insert("Matriks Kofaktor:\n", "step")
            console.insert(format_step_matrix(cof) + "\n", "matrix")

        # Adjugate = transpose kofaktor
        adj = cof.T
        console.insert("\nAdj(A) = Cᵀ (transpose kofaktor):\n", "step")
        console.insert(format_step_matrix(adj) + "\n", "matrix")

        # Invers
        inv = adj / det
        console.insert_separator()
        console.insert(f"\nA⁻¹ = (1/{det}) × Adj(A):\n", "step")
        console.insert(format_step_matrix(inv) + "\n", "matrix")
        console.insert_result("Invers berhasil dihitung via Adjugate")

    def _inv_gauss_jordan(self, M, console):
        """Invers via Gauss-Jordan [A|I] → [I|A⁻¹] — step-by-step."""
        n = M.rows
        I = sp.eye(n)
        aug = M.row_join(I)

        # Matriks besar (n>6): skip step recording demi performa & kepraktisan.
        show_steps = (n <= 6)

        console.insert("Metode: Gauss-Jordan\n", "step")
        console.insert("Augmentasi [A | I]:\n\n", "info")
        console.insert(format_step_matrix(aug, augmented_cols=n) + "\n", "matrix")
        console.insert_separator()

        # Use step engine
        inverse, steps = gauss_jordan_inverse(M, show_steps=show_steps)

        if not show_steps:
            console.insert(
                f"\n(Matriks {n}×{n} besar — langkah eliminasi disembunyikan "
                "demi performa. Menampilkan hasil akhir.)\n", "info"
            )

        # Display steps
        for i, step in enumerate(steps):
            console.insert(f"\n▶ Langkah {i+1}: ", "step")
            console.insert(f"{step.operation}\n", "step")
            if step.description:
                console.insert(f"  ({step.description})\n", "info")
            console.insert(format_step_matrix(step.matrix, augmented_cols=n) + "\n", "matrix")

        # Final result
        console.insert_separator()
        console.insert(f"\nHasil [I | A⁻¹] → A⁻¹:\n", "step")
        console.insert(format_step_matrix(inverse) + "\n", "matrix")

        # Verifikasi
        console.insert(f"\nVerifikasi A × A⁻¹:\n", "info")
        product = M * inverse
        console.insert(format_step_matrix(product) + "\n", "matrix")
        console.insert_result("Invers berhasil dihitung via Gauss-Jordan ✓")

    def _inv_builtin(self, M, det, console):
        """Invers via built-in sympy + verifikasi."""
        console.insert("Metode: Built-in (sympy)\n\n", "step")
        console.insert(f"det(A) = {det}\n\n", "info")

        inv = M.inv()
        console.insert("A⁻¹:\n", "step")
        console.insert(format_step_matrix(inv) + "\n", "matrix")

        # Verifikasi
        console.insert_separator()
        console.insert("\nVerifikasi A × A⁻¹ = I:\n", "step")
        product = M * inv
        console.insert(format_step_matrix(product) + "\n", "matrix")

        is_identity = (product == sp.eye(M.rows))
        if is_identity:
            console.insert_result("A × A⁻¹ = I ✓ (Terverifikasi)")
        else:
            console.insert_result("Invers berhasil dihitung")
