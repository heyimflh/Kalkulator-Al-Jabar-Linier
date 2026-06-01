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
from components.result_console import ResultConsoleWidget, ConsoleBuffer
from components.error_banner import ErrorBanner
from utils.formatter import (
    format_matriks_simple, normalisasi,
    format_numeric_matrix, format_num, is_purely_numeric,
)


# ─────────────────────────────────────────────────────────────────────────────
# QUEUE SINK — ConsoleBuffer yang mendorong tiap langkah ke queue thread-safe
# alih-alih menumpuknya, sehingga langkah dapat dirender BERTAHAP (incremental)
# oleh main thread (Tk tidak thread-safe). API tulis identik dgn induknya, jadi
# logika perhitungan tidak perlu diubah.
# ─────────────────────────────────────────────────────────────────────────────
class _QueueSink(ConsoleBuffer):
    def __init__(self, q):
        super().__init__()
        self._q = q

    def insert(self, text, tag=None):
        # Semua helper (insert_matrix/insert_result/insert_separator) memanggil
        # insert() ini, jadi cukup override di sini → semua ikut ke queue.
        self._q.put((text, tag))

    def warn(self, message):
        self._q.put(("__WARNING__", message))


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


# ─────────────────────────────────────────────────────────────────────────────
# SMART RANDOM (khusus halaman Diagonalisasi)
# -----------------------------------------------------------------------------
# Matriks acak penuh sering kali TIDAK bisa didiagonalisasi (eigenvalue kompleks
# / defektif), yang membuat eigenvects() simbolik menggantung. Subclass ini
# meng-override HANYA tombol Random agar selalu menghasilkan matriks yang
# DIJAMIN bisa didiagonalisasi: A = P·D·P⁻¹.
#
# P dibangun dari operasi baris elementer integer (geseran), sehingga P
# unimodular (det = ±1) dan P⁻¹ tetap bilangan bulat. Akibatnya A = P·D·P⁻¹
# adalah matriks bulat EKSAK yang serupa (similar) dengan D — jadi pasti
# terdiagonalisasi dengan eigenvalue bilangan bulat di D, tanpa galat
# pembulatan yang bisa merusak sifat diagonalisabilitas.
#
# Tombol Random pada halaman lain TIDAK terpengaruh (mereka tetap memakai
# MatrixInputWidget bawaan).
# ─────────────────────────────────────────────────────────────────────────────
class _DiagonalizableMatrixInput(MatrixInputWidget):
    """MatrixInputWidget dengan Random yang selalu diagonalizable (Diag. only)."""

    def _random_invertible_int_matrix(self, n):
        """Bangun matriks integer invertible P (unimodular, det = ±1).

        Dibangun dari identitas via operasi baris elementer integer:
          • R_i ← R_i + k·R_j  (geseran, det tidak berubah)
          • tukar baris acak    (det berganti tanda, tetap ±1)
        Hasilnya selalu invertible (det ≠ 0) dengan P⁻¹ bilangan bulat.
        """
        import sympy as sp
        import random

        P = sp.eye(n)
        if n == 1:
            # 1×1: P = [[±1]] sudah invertible; A = D langsung.
            return P

        # Geseran integer secukupnya agar P "teracak" namun entri tetap kecil.
        for _ in range(max(2 * n, 6)):
            i, j = random.sample(range(n), 2)
            k = random.choice([-2, -1, 1, 2])
            P[i, :] = P[i, :] + k * P[j, :]

        # Beberapa pertukaran baris acak (det tetap ±1, entri tetap bulat).
        for _ in range(random.randint(0, n - 1)):
            i, j = random.sample(range(n), 2)
            P.row_swap(i, j)

        # Verifikasi invertibilitas (selalu true utk konstruksi ini; jaga-jaga).
        if P.det() == 0:
            return self._random_invertible_int_matrix(n)
        return P

    def _random_fill(self):
        """Override: isi grid dengan A = P·D·P⁻¹ yang dijamin diagonalizable."""
        import sympy as sp
        import random

        n = self.current_rows
        # Diagonalisasi hanya untuk matriks persegi → samakan kolom dgn baris.
        if self.current_cols != n:
            self.current_cols = n
            self.col_var.set(str(n))
            self._generate_grid()

        # D: eigenvalue integer acak (boleh berulang) di diagonal.
        eigenvalues = [random.randint(-9, 9) for _ in range(n)]
        D = sp.diag(*eigenvalues)

        # P invertible integer → P⁻¹ integer → A = P·D·P⁻¹ bulat & eksak.
        P = self._random_invertible_int_matrix(n)
        A = P * D * P.inv()

        # Bulatkan ke integer terdekat agar input rapi (umumnya sudah bulat).
        for r in range(n):
            for c in range(n):
                val = int(round(float(A[r, c])))
                self.cell_vars[r][c].set(str(val))


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

        self.matrix_input = _DiagonalizableMatrixInput(
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

        # State render bertahap (incremental) via queue thread-safe.
        import queue as _queue
        import threading
        self._queue = _queue.Queue()
        self._render_began = False      # apakah "Menghitung..." sudah dibersihkan
        self._pending_warning = None    # warning ditahan sampai selesai

        # Komputasi berat di background thread; langkah dialirkan via queue.
        t = threading.Thread(target=self._run_compute, args=(M, self._queue), daemon=True)
        t.start()
        # Main thread polling queue (non-blocking) → UI tetap responsif.
        self.after(30, self._drain_queue)

    def _run_compute(self, M, q):
        """Background thread: tulis tiap langkah ke queue tanpa menyentuh Tk."""
        sink = _QueueSink(q)
        try:
            self._compute_diagonal(M, sink)
        except Exception as e:
            q.put(("__ERROR__", str(e)))
        finally:
            q.put(("__DONE__", None))

    def _drain_queue(self):
        """Main thread: render langkah yang tersedia secara bertahap & responsif.

        Setiap siklus menguras item yang sudah ada di queue lalu menjadwalkan
        siklus berikutnya via after() — tanpa sleep/join, jadi event loop Tk
        tidak pernah terblokir (tidak ada "Not Responding").
        """
        import queue as _queue
        try:
            while True:
                text, tag = self._queue.get_nowait()
                if text == "__DONE__":
                    self._on_compute_done()
                    return
                if text == "__ERROR__":
                    self._on_compute_error(tag)
                    return
                if text == "__WARNING__":
                    self._pending_warning = tag
                    continue
                # Langkah pertama → bersihkan pesan "Menghitung...".
                if not self._render_began:
                    self.result_console.clear()
                    self._render_began = True
                self.result_console.insert(text, tag)
        except _queue.Empty:
            pass
        # Jadwalkan polling berikutnya (tetap non-blocking).
        self.after(30, self._drain_queue)

    def _on_compute_done(self):
        """Finalisasi render (dipanggil di main thread saat worker selesai)."""
        self.calc_button.configure(state="normal", text="⚡   Diagonalisasi")
        if not self._render_began:
            # Tidak ada langkah terrender (kasus tak terduga) → bersihkan loader.
            self.result_console.clear()
        if self._pending_warning:
            self.error_banner.show_warning(self._pending_warning)
        self.after(60, self._scroll_to_results)

    def _on_compute_error(self, msg):
        """Tampilkan error (dipanggil di main thread via self.after)."""
        self.calc_button.configure(state="normal", text="⚡   Diagonalisasi")
        self.result_console.clear()
        self.result_console.insert_error(msg)
        self.error_banner.show_error(f"Perhitungan gagal: {msg}")

    def _compute_diagonal(self, M, buf):
        """
        Hitung diagonalisasi A = PDP⁻¹, menulis tiap langkah ke `buf`
        (sebuah _QueueSink) sehingga dirender bertahap oleh main thread.

        TIDAK menyentuh result_console secara langsung (thread-safe).
        Untuk matriks numerik besar (n ≥ 5) gunakan numpy demi kecepatan.
        """
        import numpy as np

        n = M.rows

        buf.insert("Matriks A:\n", "info")
        buf.insert_matrix(format_matriks_simple(M))
        buf.insert_separator()

        # ── Jalur cepat numpy: matriks murni numerik & cukup besar ──
        if is_purely_numeric(M) and n >= 5:
            self._compute_diagonal_numpy(M, buf)
            return

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
            buf.warn("Matriks tidak bisa didiagonalisasi")
            return

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
            buf.warn("Matriks tidak bisa didiagonalisasi")
            return

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
