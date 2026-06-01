# =============================================================================
# DIAGONAL_PAGE.PY — Halaman Diagonalisasi
# -----------------------------------------------------------------------------
# UI/UX: "Scientific Laboratory" — selaras dengan halaman SPL, Determinan,
# Invers, LU, dan Eigen.
#   • Light Mode  : "Amethyst Haze"  (crisp slate-white + royal lavender)
#   • Dark Mode   : "Cosmic Night"   (deep space + neon lavender)
#
# CATATAN PENTING: Hanya struktur layout, frame, dan parameter tema yang
# diubah. Seluruh logika matematika diagonalisasi (A = PDP⁻¹) beserta data
# binding tetap 100% utuh & fungsional.
# =============================================================================

import customtkinter as ctk
import sympy as sp
from config import FONT_HEADING, FONT_BODY, FONT_BUTTON, FONT_SMALL
from components.matrix_input import MatrixInputWidget
from components.result_console import ResultConsoleWidget
from components.error_banner import ErrorBanner
from utils.formatter import (
    format_matriks_simple, normalisasi,
    format_numeric_matrix, format_num, is_purely_numeric,
)


# ─────────────────────────────────────────────────────────────────────────────
# DUAL-THEME COLOR TOKENS — tuple format (light_color, dark_color)
#   Light : "Amethyst Haze"   |   Dark : "Cosmic Night"
#   (Identik dengan halaman lain agar suasana desain konsisten.)
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


class DiagonalPage(ctk.CTkFrame):
    """
    Halaman Diagonalisasi: A = PDP⁻¹
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

    # ─────────────────────────────────────────────
    # LAYOUT — Elevated card system (selaras halaman lain)
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
        # PANEL 1 — HEADER / INFO CARD
        # (Diagonalisasi satu alur perhitungan, jadi tanpa segmented button.)
        # ════════════════════════════════════════════════════════════════
        info_card = ctk.CTkFrame(
            content,
            fg_color=COLOR_MAIN_CARD,
            border_width=1,
            border_color=COLOR_BORDER,
            corner_radius=16,
        )
        info_card.pack(fill="x", pady=(0, 18))

        ctk.CTkLabel(
            info_card,
            text="⋱   Diagonalisasi",
            font=FONT_HEADING,
            text_color=COLOR_TEXT_MAIN,
            anchor="w",
        ).pack(fill="x", padx=24, pady=(20, 2))

        ctk.CTkLabel(
            info_card,
            text="Faktorkan A = P·D·P⁻¹.  P = matriks eigenvector,  "
                 "D = matriks diagonal eigenvalue. Isi matriks persegi, lalu jalankan.",
            font=FONT_SMALL,
            text_color=COLOR_TEXT_MUTED,
            anchor="w",
            justify="left",
        ).pack(fill="x", padx=24, pady=(0, 20))

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

        # Holder agar konsisten dgn halaman lain (grid di dalam workspace).
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
            action_bar, text="⚡   Diagonalisasi", font=FONT_BUTTON,
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
    # Logika matematika diagonalisasi (A = PDP⁻¹) tetap utuh; hanya
    # arsitektur (threading) & verifikasi yang dioptimasi agar UI tak freeze.
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

        # Disable tombol + tampilkan loading (ringan, di main thread).
        self.calc_button.configure(state="disabled", text="⏳  Menghitung...")
        self.result_console.insert("Menghitung...\n", "info")

        # Jalankan komputasi berat di background thread → UI tetap responsif.
        import threading
        t = threading.Thread(target=self._run_compute, args=(M,), daemon=True)
        t.start()

    def _run_compute(self, M):
        """Background thread: hitung diagonalisasi tanpa menyentuh widget Tk."""
        try:
            result = self._compute_diagonal(M)
        except Exception as e:
            msg = str(e)
            self.after(0, lambda: self._on_compute_error(msg))
            return
        self.after(0, lambda: self._on_compute_done(result))

    def _on_compute_done(self, result):
        """Render hasil ke UI (dipanggil di main thread via self.after)."""
        self.calc_button.configure(state="normal", text="⚡   Diagonalisasi")
        self.result_console.clear()
        result["buffer"].replay(self.result_console)
        if result.get("warning"):
            self.error_banner.show_warning(result["warning"])
        self.after(60, self._scroll_to_results)

    def _on_compute_error(self, msg):
        """Tampilkan error (dipanggil di main thread via self.after)."""
        self.calc_button.configure(state="normal", text="⚡   Diagonalisasi")
        self.result_console.clear()
        self.result_console.insert_error(msg)
        self.error_banner.show_error(f"Perhitungan gagal: {msg}")

    def _compute_diagonal(self, M):
        """
        Hitung diagonalisasi A = PDP⁻¹.

        Mengembalikan dict {"buffer": ConsoleBuffer, "warning": str|None}.
        TIDAK menyentuh result_console secara langsung (thread-safe).
        Untuk matriks numerik besar (n ≥ 5) gunakan numpy demi kecepatan.
        """
        import numpy as np
        from components.result_console import ConsoleBuffer

        buf = ConsoleBuffer()
        n = M.rows

        buf.insert("Matriks A:\n", "info")
        buf.insert_matrix(format_matriks_simple(M))
        buf.insert_separator()

        # ── Jalur cepat numpy: matriks murni numerik & cukup besar ──
        if is_purely_numeric(M) and n >= 5:
            return self._compute_diagonal_numpy(M, buf)

        # ── Jalur SymPy simbolik (exact) untuk matriks kecil / simbolik ──
        eigen_data = M.eigenvects()
        total_vects = sum(len(v[2]) for v in eigen_data)

        if total_vects < n:
            buf.insert("\n", None)
            buf.insert("❌ Matriks TIDAK bisa didiagonalisasi\n\n", "error")
            buf.insert(f"Alasan: Hanya ditemukan {total_vects} eigenvector independen,\n", "info")
            buf.insert(f"tetapi dibutuhkan {n} eigenvector untuk matriks {n}×{n}.\n\n", "info")

            buf.insert("Detail eigenvalues:\n", "step")
            for val, mult, vects in eigen_data:
                geo_mult = len(vects)
                status = "✓" if geo_mult == mult else "✗"
                buf.insert(
                    f"  λ = {val}: aljabar={mult}, geometri={geo_mult} {status}\n", "info"
                )
            return {"buffer": buf, "warning": "Matriks tidak bisa didiagonalisasi"}

        # Build P and D
        P_cols = []
        D_vals = []

        buf.insert("\nEigenvectors (kolom P):\n", "step")
        col_idx = 1
        for val, mult, vects in eigen_data:
            for v in vects:
                normalized = normalisasi(v)
                P_cols.append(normalized)
                D_vals.append(val)
                buf.insert(f"  p{col_idx} = {tuple(normalized)}  (λ = {val})\n", "info")
                col_idx += 1

        # Construct matrices
        P = sp.Matrix.hstack(*[sp.Matrix(v) for v in P_cols])
        D = sp.diag(*D_vals)
        P_inv = P.inv()

        buf.insert_separator()

        buf.insert("\nMatriks P (eigenvectors):\n", "step")
        buf.insert_matrix(format_matriks_simple(P))

        buf.insert("\nMatriks D (diagonal eigenvalues):\n", "step")
        buf.insert_matrix(format_matriks_simple(D))

        buf.insert("\nMatriks P⁻¹:\n", "step")
        buf.insert_matrix(format_matriks_simple(P_inv))

        # Verifikasi (numpy allclose — jauh lebih cepat dari sp.simplify)
        buf.insert_separator()
        buf.insert("\nVerifikasi A = P·D·P⁻¹:\n", "step")
        product = P * D * P_inv
        buf.insert_matrix(format_matriks_simple(product))

        diff = product - M
        try:
            verified = np.allclose(
                np.array(diff.tolist(), dtype=float),
                np.zeros((n, n)),
                atol=1e-6,
            )
        except (TypeError, ValueError):
            # Simbolik/kompleks: fallback ke norm (tetap lebih ringan dari simplify)
            verified = (diff.norm() < 1e-6)

        if verified:
            buf.insert_result("A = P·D·P⁻¹ ✓ (Terverifikasi)")
        else:
            buf.insert_result("Diagonalisasi selesai")

        return {"buffer": buf, "warning": None}

    def _compute_diagonal_numpy(self, M, buf):
        """Jalur cepat diagonalisasi numerik via numpy (matriks besar)."""
        import numpy as np

        M_np = np.array(M.tolist(), dtype=float)
        eigenvalues, eigenvectors = np.linalg.eig(M_np)
        n = M.rows

        buf.insert("Pendekatan numerik (numpy) untuk matriks besar.\n", "info")

        # Cek diagonalizability: butuh n eigenvector independen → rank P = n.
        rank_P = np.linalg.matrix_rank(eigenvectors)
        if rank_P < n:
            buf.insert("\n", None)
            buf.insert("❌ Matriks TIDAK bisa didiagonalisasi\n\n", "error")
            buf.insert(f"Alasan: Hanya ditemukan {rank_P} eigenvector independen,\n", "info")
            buf.insert(f"tetapi dibutuhkan {n} eigenvector untuk matriks {n}×{n}.\n", "info")
            return {"buffer": buf, "warning": "Matriks tidak bisa didiagonalisasi"}

        P = eigenvectors
        D = np.diag(eigenvalues)
        P_inv = np.linalg.inv(P)

        buf.insert("\nEigenvalues (diagonal D):\n", "step")
        for i, val in enumerate(eigenvalues):
            buf.insert(f"  λ{i+1} = {format_num(val)}\n", "info")

        buf.insert_separator()
        buf.insert("\nMatriks P (eigenvectors, ternormalisasi numpy):\n", "step")
        buf.insert_matrix(format_numeric_matrix(P))

        buf.insert("\nMatriks D (diagonal eigenvalues):\n", "step")
        buf.insert_matrix(format_numeric_matrix(D))

        buf.insert("\nMatriks P⁻¹:\n", "step")
        buf.insert_matrix(format_numeric_matrix(P_inv))

        # Verifikasi numerik
        buf.insert_separator()
        buf.insert("\nVerifikasi A = P·D·P⁻¹:\n", "step")
        product = P @ D @ P_inv
        buf.insert_matrix(format_numeric_matrix(product))

        if np.allclose(product, M_np, atol=1e-6):
            buf.insert_result("A = P·D·P⁻¹ ✓ (Terverifikasi)")
        else:
            buf.insert_result("Diagonalisasi selesai")

        return {"buffer": buf, "warning": None}
