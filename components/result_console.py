# =============================================================================
# RESULT_CONSOLE.PY — Output area dengan syntax highlighting & copy
# =============================================================================

import customtkinter as ctk
import tkinter as tk
from config import FONT_CONSOLE, FONT_SMALL, FONT_BODY


class ResultConsoleWidget(ctk.CTkFrame):
    """
    Widget output hasil perhitungan dengan:
    - Header (judul + tombol Copy/Clear)
    - Scrollable text area dengan font monospace
    - Syntax highlighting via tags (step=biru, result=hijau, error=merah)
    - Auto-scroll ke bawah setelah insert
    """

    def __init__(self, master, title="Hasil Perhitungan", **kwargs):
        super().__init__(master, corner_radius=10, **kwargs)

        self.title_text = title

        # Terminal display state (font scaling + wrap toggle).
        self._font_family = FONT_CONSOLE[0]
        self._font_size = FONT_CONSOLE[1]
        self._min_font = 9
        self._max_font = 16
        self._wrap = "none"   # "none" → horizontal scroll for long expressions

        self._build_ui()

    def _build_ui(self):
        """Bangun header dan text area."""

        # ─── Header ───
        header = ctk.CTkFrame(self, fg_color="transparent", height=40)
        header.pack(fill="x", padx=15, pady=(12, 5))
        header.pack_propagate(False)

        ctk.CTkLabel(
            header,
            text=f"📋 {self.title_text}",
            font=FONT_BODY,
        ).pack(side="left")

        # Action buttons (right side)
        btn_style = {
            "font": FONT_SMALL,
            "height": 28,
            "width": 70,
            "corner_radius": 6,
            "fg_color": ("gray80", "#2C3E50"),
            "hover_color": ("gray70", "#34495E"),
            "text_color": ("gray20", "gray80"),
        }
        # Compact square style for terminal utility controls (-, +, wrap).
        util_style = {
            "font": FONT_SMALL,
            "height": 28,
            "width": 30,
            "corner_radius": 6,
            "fg_color": ("gray80", "#2C3E50"),
            "hover_color": ("gray70", "#34495E"),
            "text_color": ("gray20", "gray80"),
        }

        ctk.CTkButton(
            header, text="Clear", command=self.clear, **btn_style
        ).pack(side="right", padx=(5, 0))

        ctk.CTkButton(
            header, text="Copy", command=self._copy_to_clipboard, **btn_style
        ).pack(side="right", padx=(5, 0))

        ctk.CTkButton(
            header, text="LaTeX", command=self._copy_latex, **btn_style
        ).pack(side="right", padx=(5, 0))

        # ─── Terminal utility cluster: font −/+ & wrap toggle ───
        # Dipisahkan visual dari tombol aksi dengan sedikit jarak.
        self.wrap_btn = ctk.CTkButton(
            header, text="↩ Wrap", command=self._toggle_wrap, **{**util_style, "width": 64}
        )
        self.wrap_btn.pack(side="right", padx=(5, 12))

        ctk.CTkButton(
            header, text="A+", command=lambda: self._adjust_font(+1), **util_style
        ).pack(side="right", padx=(5, 0))

        ctk.CTkButton(
            header, text="A−", command=lambda: self._adjust_font(-1), **util_style
        ).pack(side="right", padx=(5, 0))

        # ─── Separator ───
        ctk.CTkFrame(self, height=1, fg_color=("gray75", "gray30")).pack(
            fill="x", padx=15, pady=(0, 5)
        )

        # ─── Text Area (tkinter Text for tag support) ───
        # Grid layout agar scrollbar vertikal & horizontal terintegrasi rapi
        # tanpa saling menimpa, dan tombol aksi di header tetap bersih.
        text_frame = ctk.CTkFrame(self, fg_color="transparent")
        text_frame.pack(fill="both", expand=True, padx=15, pady=(0, 12))
        text_frame.grid_rowconfigure(0, weight=1)
        text_frame.grid_columnconfigure(0, weight=1)

        self.textbox = tk.Text(
            text_frame,
            wrap=self._wrap,
            font=(self._font_family, self._font_size),
            relief="flat",
            padx=20,
            pady=20,
            state="disabled",
            cursor="arrow",
            borderwidth=0,
            highlightthickness=0,
        )
        self.textbox.grid(row=0, column=0, sticky="nsew")

        # Vertical scrollbar
        self.scrollbar_y = ctk.CTkScrollbar(text_frame, command=self.textbox.yview)
        self.scrollbar_y.grid(row=0, column=1, sticky="ns")

        # Horizontal scrollbar — untuk ekspresi panjang (CRootOf, polinom, dll.)
        self.scrollbar_x = ctk.CTkScrollbar(
            text_frame, orientation="horizontal", command=self.textbox.xview
        )
        self.scrollbar_x.grid(row=1, column=0, sticky="ew")

        self.textbox.configure(
            yscrollcommand=self.scrollbar_y.set,
            xscrollcommand=self.scrollbar_x.set,
        )
        self._sync_hscroll_visibility()

        # ─── Isolate mouse-wheel scrolling ───
        # CTkScrollableFrame binds <MouseWheel> at the "all" bindtag level, so
        # tanpa ini scroll di area hasil ikut menggeser seluruh halaman.
        # Handler ini menggulir HANYA textbox lalu "break" agar event tidak
        # naik ke page scroller.
        self.textbox.bind("<MouseWheel>", self._on_mousewheel)       # Windows / macOS
        self.textbox.bind("<Button-4>", self._on_mousewheel)         # Linux up
        self.textbox.bind("<Button-5>", self._on_mousewheel)         # Linux down
        # Shift+wheel → horizontal scroll (nyaman utk ekspresi panjang).
        self.textbox.bind("<Shift-MouseWheel>", self._on_shift_mousewheel)
        self.textbox.bind("<Shift-Button-4>", self._on_shift_mousewheel)
        self.textbox.bind("<Shift-Button-5>", self._on_shift_mousewheel)

        # ─── Configure Tags (syntax highlighting) ───
        self._setup_tags()

        # ─── Apply theme colors ───
        self._apply_theme()

    def _setup_tags(self):
        """Setup text tags untuk syntax highlighting (font mengikuti ukuran)."""
        fam, fs = self._font_family, self._font_size
        self.textbox.tag_configure("step", foreground="#3498DB", font=(fam, fs, "bold"))
        self.textbox.tag_configure("result", foreground="#2ECC71", font=(fam, fs, "bold"))
        self.textbox.tag_configure("error", foreground="#E74C3C", font=(fam, fs, "bold"))
        self.textbox.tag_configure("matrix", foreground="#ECF0F1")
        self.textbox.tag_configure("separator", foreground="#7F8C8D")
        self.textbox.tag_configure("info", foreground="#95A5A6")

    def _apply_theme(self):
        """Apply warna berdasarkan current appearance mode.

        Penting: kedua cabang HARUS men-set ulang SEMUA tag. Sebelumnya
        cabang Dark hanya set bg/fg, sehingga setelah toggle Light→Dark
        warna tag (matrix/info/separator) tertinggal di nilai light-mode
        (abu-abu gelap) dan tak terlihat di atas background gelap.

        Terminal "lab report": bg ("#F8FAFC", "#151522"), teks high-contrast
        ("#1E1B4B", "#E2E8F0"). Aksen hijau "result" dipertahankan bersih.
        """
        mode = ctk.get_appearance_mode()
        if mode == "Dark":
            # Cosmic Night — code-workspace dark fill, teks terang & jelas.
            self.textbox.configure(bg="#151522", fg="#E2E8F0", insertbackground="#E2E8F0")
            self.textbox.tag_configure("step", foreground="#A78BFA")       # lavender
            self.textbox.tag_configure("result", foreground="#4ADE80")     # green accent
            self.textbox.tag_configure("error", foreground="#FB7185")      # rose terang
            self.textbox.tag_configure("matrix", foreground="#E2E8F0")     # near-white (angka jelas)
            self.textbox.tag_configure("separator", foreground="#64748B")  # slate
            self.textbox.tag_configure("info", foreground="#A5B4CF")       # muted terang
        else:
            # Amethyst Haze — lab-report light fill, teks indigo gelap.
            self.textbox.configure(bg="#F8FAFC", fg="#1E1B4B", insertbackground="#1E1B4B")
            self.textbox.tag_configure("step", foreground="#7C3AED")       # violet
            self.textbox.tag_configure("result", foreground="#059669")     # green accent
            self.textbox.tag_configure("error", foreground="#DC2626")
            self.textbox.tag_configure("matrix", foreground="#1E293B")     # deep slate (angka jelas)
            self.textbox.tag_configure("separator", foreground="#9CA3AF")
            self.textbox.tag_configure("info", foreground="#6B21A8")       # royal purple

    # ─────────────────────────────────────────────
    # SCROLL ISOLATION
    # ─────────────────────────────────────────────

    def _on_mousewheel(self, event):
        """Gulir hanya textbox; cegah event naik ke page scroller.

        Mengembalikan "break" agar binding <MouseWheel> milik
        CTkScrollableFrame (level "all") tidak ikut tereksekusi.
        """
        # Tentukan arah & jumlah unit (lintas platform).
        if getattr(event, "num", None) == 4:          # Linux scroll up
            delta = -3
        elif getattr(event, "num", None) == 5:        # Linux scroll down
            delta = 3
        else:                                          # Windows / macOS
            delta = -1 * int(event.delta / 120) * 3
            if delta == 0:
                delta = -1 if event.delta > 0 else 1
        self.textbox.yview_scroll(delta, "units")
        return "break"

    def _on_shift_mousewheel(self, event):
        """Shift+wheel → scroll horizontal (untuk ekspresi panjang)."""
        if getattr(event, "num", None) == 4:
            delta = -3
        elif getattr(event, "num", None) == 5:
            delta = 3
        else:
            delta = -1 * int(event.delta / 120) * 3
            if delta == 0:
                delta = -1 if event.delta > 0 else 1
        self.textbox.xview_scroll(delta, "units")
        return "break"

    # ─────────────────────────────────────────────
    # TERMINAL CONTROLS — font scaling & wrap toggle
    # ─────────────────────────────────────────────

    def _adjust_font(self, delta):
        """Perbesar/perkecil font textbox (clamp 9–16pt) + sinkron tag font."""
        new_size = max(self._min_font, min(self._max_font, self._font_size + delta))
        if new_size == self._font_size:
            return
        self._font_size = new_size
        self.textbox.configure(font=(self._font_family, self._font_size))
        # Tag step/result/error pakai bold → ikut diskalakan ulang.
        self._setup_tags()
        self._apply_theme()
        self._sync_hscroll_visibility()

    def _toggle_wrap(self):
        """Toggle antara wrap='none' (scroll horizontal) & 'word' (lipat baris)."""
        if self._wrap == "none":
            self._wrap = "word"
            self.wrap_btn.configure(text="↩ Wrap: On")
        else:
            self._wrap = "none"
            self.wrap_btn.configure(text="↩ Wrap")
        self.textbox.configure(wrap=self._wrap)
        self._sync_hscroll_visibility()

    def _sync_hscroll_visibility(self):
        """Sembunyikan scrollbar horizontal saat wrap aktif (tak diperlukan)."""
        try:
            if self._wrap == "none":
                self.scrollbar_x.grid()
            else:
                self.scrollbar_x.grid_remove()
        except Exception:
            pass

    # ─────────────────────────────────────────────
    # PUBLIC API
    # ─────────────────────────────────────────────

    def clear(self):
        """Clear semua output."""
        self.textbox.configure(state="normal")
        self.textbox.delete("1.0", "end")
        self.textbox.configure(state="disabled")

    def insert(self, text, tag=None):
        """
        Insert text ke console.
        tag: 'step', 'result', 'error', 'matrix', 'separator', 'info', atau None
        """
        self.textbox.configure(state="normal")
        if tag:
            self.textbox.insert("end", text, tag)
        else:
            self.textbox.insert("end", text)
        self.textbox.configure(state="disabled")
        # Auto-scroll ke bawah
        self.textbox.see("end")

    def insert_step(self, step_num, description):
        """Insert langkah perhitungan."""
        self.insert(f"\n▶ Langkah {step_num}: ", "step")
        self.insert(f"{description}\n", "step")

    def insert_matrix(self, matrix_str):
        """Insert matriks (formatted string)."""
        self.insert(f"{matrix_str}\n", "matrix")

    def insert_result(self, text):
        """Insert hasil akhir (hijau)."""
        self.insert("\n" + "═" * 45 + "\n", "separator")
        self.insert(f"✅ {text}\n", "result")

    def insert_error(self, text):
        """Insert pesan error (merah)."""
        self.insert(f"\n⚠️ {text}\n", "error")

    def insert_info(self, text):
        """Insert info tambahan (abu-abu)."""
        self.insert(f"{text}\n", "info")

    def insert_separator(self):
        """Insert garis pemisah."""
        self.insert("\n" + "─" * 45 + "\n", "separator")

    def get_content(self):
        """Return seluruh konten sebagai plain text."""
        return self.textbox.get("1.0", "end").strip()

    def set_loading(self, is_loading=True):
        """Tampilkan/sembunyikan loading indicator."""
        if is_loading:
            self.clear()
            self.insert("⏳ Menghitung...\n", "info")
        # Jika False, caller akan clear dan insert hasil

    # ─────────────────────────────────────────────
    # COPY FUNCTIONS
    # ─────────────────────────────────────────────

    def _copy_to_clipboard(self):
        """Copy seluruh output sebagai plain text."""
        content = self.get_content()
        if content:
            self.clipboard_clear()
            self.clipboard_append(content)
            self._flash_feedback("✓ Copied!")

    def _copy_latex(self):
        """Copy matriks terakhir dalam format LaTeX."""
        content = self.get_content()
        if content:
            latex = self._convert_to_latex(content)
            self.clipboard_clear()
            self.clipboard_append(latex)
            self._flash_feedback("✓ LaTeX copied!")

    def _convert_to_latex(self, text):
        """Convert output text ke format LaTeX (best effort)."""
        import re
        lines = text.split("\n")
        latex_parts = []
        matrix_lines = []
        in_matrix = False

        for line in lines:
            # Detect matrix rows (lines starting with [ or containing │)
            stripped = line.strip()
            if stripped.startswith("[") and stripped.endswith("]"):
                # Extract numbers from matrix row
                inner = stripped[1:-1]
                # Remove augmented separator
                inner = inner.replace("│", "&")
                # Split by whitespace
                vals = re.split(r'\s+', inner.strip())
                vals = [v for v in vals if v and v != "&"]
                matrix_lines.append(" & ".join(vals))
                in_matrix = True
            elif stripped.startswith("┌") or stripped.startswith("└"):
                continue
            elif stripped.startswith("│"):
                inner = stripped[1:-1] if stripped.endswith("│") else stripped[1:]
                vals = re.split(r'\s+', inner.strip())
                vals = [v for v in vals if v]
                matrix_lines.append(" & ".join(vals))
                in_matrix = True
            else:
                if in_matrix and matrix_lines:
                    latex_parts.append(
                        "\\begin{bmatrix}\n"
                        + " \\\\\n".join(matrix_lines)
                        + "\n\\end{bmatrix}"
                    )
                    matrix_lines = []
                    in_matrix = False
                if stripped:
                    latex_parts.append(stripped)

        # Flush remaining matrix
        if matrix_lines:
            latex_parts.append(
                "\\begin{bmatrix}\n"
                + " \\\\\n".join(matrix_lines)
                + "\n\\end{bmatrix}"
            )

        return "\n\n".join(latex_parts)

    def _flash_feedback(self, message):
        """Brief visual feedback setelah copy — flash pada header."""
        # Store original text
        if not hasattr(self, '_header_label'):
            # Find the header label
            for widget in self.winfo_children():
                if isinstance(widget, ctk.CTkFrame):
                    for child in widget.winfo_children():
                        if isinstance(child, ctk.CTkLabel):
                            self._header_label = child
                            self._original_text = child.cget("text")
                            break
                    break

        if hasattr(self, '_header_label'):
            self._header_label.configure(text=f"📋 {message}", text_color=("#059669", "#2ECC71"))
            self.after(2000, lambda: self._header_label.configure(
                text=f"📋 {self.title_text}",
                text_color=ctk.ThemeManager.theme["CTkLabel"]["text_color"]
            ))

    # ─────────────────────────────────────────────
    # THEME UPDATE
    # ─────────────────────────────────────────────

    def update_theme(self):
        """Re-apply theme saat mode berubah."""
        self._apply_theme()
