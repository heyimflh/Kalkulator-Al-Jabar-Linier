# =============================================================================
# SPL_PAGE.PY — Halaman Sistem Persamaan Linear (dengan Step Engine)
# -----------------------------------------------------------------------------
# UI/UX: "Scientific Laboratory" — elevated card system, dual-theme.
#   • Light Mode  : "Amethyst Haze"  (crisp slate-white + royal lavender)
#   • Dark Mode   : "Cosmic Night"   (deep space + neon lavender)
#
# CATATAN PENTING: Hanya struktur layout, frame, dan parameter tema yang
# diubah. Seluruh logika matematika, solver (Gauss, Gauss-Jordan, Matriks
# Balikan), dan data binding tetap 100% utuh & fungsional.
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


# ─────────────────────────────────────────────────────────────────────────────
# DUAL-THEME COLOR TOKENS — tuple format (light_color, dark_color)
#   Light : "Amethyst Haze"   |   Dark : "Cosmic Night"
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


class SPLPage(ctk.CTkFrame):
    """
    Halaman SPL dengan step-by-step engine.
    Metode: Gauss, Gauss-Jordan, Matriks Balikan
    """

    def __init__(self, master, **kwargs):
        # A. Page base — workspace canvas
        super().__init__(master, fg_color=COLOR_APP_BG, **kwargs)
        self._last_mode = ctk.get_appearance_mode()
        self._build_layout()
        # Self-contained watcher → restyle raw tk.Text console on theme toggle.
        self._watch_theme()

    # ─────────────────────────────────────────────
    # STYLE PRESETS (diteruskan ke komponen bersama)
    # ─────────────────────────────────────────────
    def _matrix_style(self, toolbar_cols=3):
        """Style token untuk MatrixInputWidget (cells, selectors, toolbar).

        `toolbar_cols` memungkinkan Matriks A (3 kolom) & Vektor b (2 kolom)
        punya tata-letak toolbar yang rapi sesuai lebar masing-masing kartu.
        """
        return {
            "label_color": COLOR_TEXT_MAIN,
            "muted_color": COLOR_TEXT_MUTED,
            # C. Matrix entry cells — perfectly square, crisp framing
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
            "cell_min": 30,   # cukup utk "-9"/"10" tanpa terpotong
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
            # C. Utility toolbar — modern outlined chip buttons, responsive grid
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
        maupun tak-terpilih:
          • Light: teks ungu tua di atas chip lavender muda (aktif sedikit
            lebih pekat) → selalu kontras.
          • Dark : teks putih di atas chip gelap (aktif violet jenuh) → kontras.
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
    # LAYOUT — Elevated card system
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
            text="⊞   Sistem Persamaan Linear",
            font=FONT_HEADING,
            text_color=COLOR_TEXT_MAIN,
            anchor="w",
        ).pack(fill="x", padx=24, pady=(20, 2))

        ctk.CTkLabel(
            method_card,
            text="Selesaikan Ax = b langkah demi langkah. Pilih metode eliminasi, "
                 "isi matriks, lalu jalankan.",
            font=FONT_SMALL,
            text_color=COLOR_TEXT_MUTED,
            anchor="w",
        ).pack(fill="x", padx=24, pady=(0, 14))

        self.method_selector = MethodSelector(
            method_card,
            options=["Gauss", "Gauss-Jordan", "Matriks Balikan"],
            default="Gauss",
            tooltips={
                "Gauss": "Eliminasi ke bentuk REF + back substitution",
                "Gauss-Jordan": "Eliminasi ke bentuk RREF (solusi langsung terbaca)",
                "Matriks Balikan": "Solusi via x = A⁻¹·b (hanya matriks persegi non-singular)",
            },
            style=self._method_style(),
        )
        self.method_selector.pack(fill="x", padx=24, pady=(0, 20))

        # ════════════════════════════════════════════════════════════════
        # PANEL 2 — SPLIT MATRIX WORKSPACE
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

        # Grid holder: dua sub-card terpisah (tanpa garis pemisah kaku).
        # Bobot 7:3 + minsize → Vektor b selalu dapat porsi lebar yang sehat
        # dan tak pernah terdesak keluar layar, di orde rendah maupun 10×10.
        split = ctk.CTkFrame(workspace_card, fg_color="transparent")
        split.pack(fill="both", expand=True, padx=22, pady=(0, 22))
        split.grid_columnconfigure(0, weight=7, uniform="ws", minsize=320)
        split.grid_columnconfigure(1, weight=3, uniform="ws", minsize=210)
        split.grid_rowconfigure(0, weight=1)

        # ── Left Sub-Card: Matriks A (Koefisien) + dropdown Baris/Kolom ──
        sub_a = ctk.CTkFrame(
            split,
            fg_color=COLOR_SUB_CARD,
            border_width=1,
            border_color=COLOR_BORDER,
            corner_radius=12,
        )
        sub_a.grid(row=0, column=0, sticky="nsew", padx=(0, 12))

        self.matrix_a = MatrixInputWidget(
            sub_a, default_rows=3, default_cols=3,
            label="Matriks A (Koefisien)",
            style=self._matrix_style(toolbar_cols=3),
        )
        self.matrix_a.pack(fill="both", expand=True, padx=16, pady=16)

        # ── Right Sub-Card: Vektor b (Konstanta) ──
        sub_b = ctk.CTkFrame(
            split,
            fg_color=COLOR_SUB_CARD,
            border_width=1,
            border_color=COLOR_BORDER,
            corner_radius=12,
        )
        sub_b.grid(row=0, column=1, sticky="nsew", padx=(12, 0))

        self.matrix_b = MatrixInputWidget(
            sub_b, default_rows=3, default_cols=1,
            label="Vektor b (Konstanta)",
            style=self._matrix_style(toolbar_cols=2),  # toolbar rapi 2 kolom
        )
        self.matrix_b.pack(fill="both", expand=True, padx=16, pady=16)

        # ════════════════════════════════════════════════════════════════
        # PANEL 3 — ACTION (wide, centered)
        # ════════════════════════════════════════════════════════════════
        action_bar = ctk.CTkFrame(content, fg_color="transparent")
        action_bar.pack(fill="x", pady=(0, 18))

        self.calc_button = ctk.CTkButton(
            action_bar, text="⚡   Hitung SPL", font=FONT_BUTTON,
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
            # Posisi-y kartu hasil relatif terhadap tinggi total konten.
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
        # Re-schedule selama widget masih hidup.
        if self.winfo_exists():
            self.after(400, self._watch_theme)

    # =========================================================================
    # ░░  LOGIKA PERHITUNGAN — komputasi berat di BACKGROUND THREAD  ░░
    # Logika solver (Gauss, Gauss-Jordan, Matriks Balikan) tetap utuh; hanya
    # arsitektur threading yang dioptimasi. SELURUH langkah selalu ditampilkan.
    # =========================================================================

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

        self.calc_button.configure(state="disabled", text="⏳  Menghitung...")
        self.result_console.insert("Menghitung...\n", "info")

        import threading
        t = threading.Thread(target=self._run_compute, args=(A, b, method), daemon=True)
        t.start()

    def _run_compute(self, A, b, method):
        """Background thread: selesaikan SPL tanpa menyentuh widget Tk."""
        try:
            from components.result_console import ConsoleBuffer
            buf = ConsoleBuffer()
            error = None
            if method == "Gauss":
                self._solve_gauss(A, b, buf)
            elif method == "Gauss-Jordan":
                self._solve_gauss_jordan(A, b, buf)
            elif method == "Matriks Balikan":
                error = self._solve_inverse(A, b, buf)
            result = {"buffer": buf, "error": error}
        except Exception as e:
            msg = str(e)
            self.after(0, lambda: self._on_compute_error(msg))
            return
        self.after(0, lambda: self._on_compute_done(result))

    def _on_compute_done(self, result):
        """Render hasil ke UI (main thread via self.after)."""
        self.calc_button.configure(state="normal", text="⚡   Hitung SPL")
        self.result_console.clear()
        if result.get("error"):
            self.error_banner.show_error(result["error"])
            return
        result["buffer"].replay(self.result_console)
        self.after(60, self._scroll_to_results)

    def _on_compute_error(self, msg):
        """Tampilkan error (main thread via self.after)."""
        self.calc_button.configure(state="normal", text="⚡   Hitung SPL")
        self.result_console.clear()
        self.result_console.insert_error(msg)
        self.error_banner.show_error(f"Perhitungan gagal: {msg}")

    def _solve_gauss(self, A, b, console):
        """Eliminasi Gauss dengan step-by-step engine."""
        aug = A.row_join(b)
        # Selalu rekam & tampilkan SELURUH langkah, berapa pun ukuran matriks.
        show_steps = True

        console.insert("Metode: Eliminasi Gauss\n\n", "step")
        console.insert("Matriks Augmented [A|b]:\n", "info")
        console.insert(format_step_matrix(aug, augmented_cols=b.cols) + "\n", "matrix")
        console.insert_separator()

        # Solve with step engine
        solution, steps = solve_spl_gauss(A, b, show_steps=show_steps)

        # Display steps
        for i, step in enumerate(steps):
            console.insert(f"\n▶ Langkah {i+1}: ", "step")
            console.insert(f"{step.operation}\n", "step")
            if step.description:
                console.insert(f"  ({step.description})\n", "info")
            console.insert(
                format_step_matrix(step.matrix, augmented_cols=b.cols) + "\n", "matrix"
            )

        # Display solution
        self._display_solution(solution, console)

    def _solve_gauss_jordan(self, A, b, console):
        """Eliminasi Gauss-Jordan dengan step-by-step engine."""
        aug = A.row_join(b)
        # Selalu rekam & tampilkan SELURUH langkah, berapa pun ukuran matriks.
        show_steps = True

        console.insert("Metode: Eliminasi Gauss-Jordan\n\n", "step")
        console.insert("Matriks Augmented [A|b]:\n", "info")
        console.insert(format_step_matrix(aug, augmented_cols=b.cols) + "\n", "matrix")
        console.insert_separator()

        # Solve with step engine
        solution, steps = solve_spl_gauss_jordan(A, b, show_steps=show_steps)

        # Display steps
        for i, step in enumerate(steps):
            console.insert(f"\n▶ Langkah {i+1}: ", "step")
            console.insert(f"{step.operation}\n", "step")
            if step.description:
                console.insert(f"  ({step.description})\n", "info")
            console.insert(
                format_step_matrix(step.matrix, augmented_cols=b.cols) + "\n", "matrix"
            )

        # Display solution
        self._display_solution(solution, console)

    def _solve_inverse(self, A, b, console):
        """Solusi via x = A⁻¹·b.

        Mengembalikan pesan error (str) bila validasi gagal (ditampilkan via
        banner), atau None bila sukses.
        """
        if A.rows != A.cols:
            return "Matriks A harus persegi untuk metode Matriks Balikan"

        det = A.det()
        if det == 0:
            return (
                "Matriks A singular (det = 0), sehingga metode Matriks Balikan "
                "tidak bisa digunakan. Coba gunakan metode Gauss atau Gauss-Jordan."
            )

        console.insert("Metode: x = A⁻¹ · b\n\n", "step")
        console.insert(f"det(A) = {det}\n\n", "info")

        A_inv = A.inv()
        console.insert("A⁻¹:\n", "step")
        console.insert(format_matriks_simple(A_inv) + "\n", "matrix")
        console.insert_separator()

        x = A_inv * b
        console.insert("\nx = A⁻¹·b:\n", "step")
        console.insert(format_matriks_simple(x) + "\n", "matrix")

        # Format solusi
        sol_parts = []
        for i in range(x.rows):
            sol_parts.append(f"x{i+1} = {sp.nsimplify(x[i, 0])}")
        console.insert_result(", ".join(sol_parts))
        return None

    def _display_solution(self, solution, console):
        """Display solution info dari step engine."""
        console.insert_separator()

        if solution["type"] == "unique":
            values = solution["values"]
            sol_parts = [f"x{i+1} = {sp.nsimplify(v)}" for i, v in enumerate(values)]
            console.insert_result("Solusi unik: " + ", ".join(sol_parts))

        elif solution["type"] == "none":
            console.insert(f"\n❌ {solution['message']}\n", "error")

        elif solution["type"] == "infinite":
            console.insert(f"\n∞ {solution['message']}\n", "step")
            # Tampilkan variabel bebas
            if "pivot_cols" in solution:
                n_vars = solution["matrix"].cols - 1
                pivot_cols = solution["pivot_cols"]
                free_vars = [i for i in range(n_vars) if i not in pivot_cols]
                if free_vars:
                    free_str = ", ".join(f"x{i+1}" for i in free_vars)
                    console.insert(f"  Variabel bebas: {free_str}\n", "info")
