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

        # Buttons (right side)
        btn_style = {
            "font": FONT_SMALL,
            "height": 28,
            "width": 70,
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
        ).pack(side="right")

        # ─── Separator ───
        ctk.CTkFrame(self, height=1, fg_color=("gray75", "gray30")).pack(
            fill="x", padx=15, pady=(0, 5)
        )

        # ─── Text Area (using tkinter Text for tag support) ───
        text_frame = ctk.CTkFrame(self, fg_color="transparent")
        text_frame.pack(fill="both", expand=True, padx=15, pady=(0, 12))

        self.textbox = tk.Text(
            text_frame,
            wrap="none",
            font=FONT_CONSOLE,
            relief="flat",
            padx=10,
            pady=10,
            state="disabled",
            cursor="arrow",
        )
        self.textbox.pack(fill="both", expand=True, side="left")

        # Scrollbar
        scrollbar_y = ctk.CTkScrollbar(text_frame, command=self.textbox.yview)
        scrollbar_y.pack(fill="y", side="right")
        self.textbox.configure(yscrollcommand=scrollbar_y.set)

        # ─── Configure Tags (syntax highlighting) ───
        self._setup_tags()

        # ─── Apply theme colors ───
        self._apply_theme()

    def _setup_tags(self):
        """Setup text tags untuk syntax highlighting."""
        self.textbox.tag_configure("step", foreground="#3498DB", font=(FONT_CONSOLE[0], FONT_CONSOLE[1], "bold"))
        self.textbox.tag_configure("result", foreground="#2ECC71", font=(FONT_CONSOLE[0], FONT_CONSOLE[1], "bold"))
        self.textbox.tag_configure("error", foreground="#E74C3C", font=(FONT_CONSOLE[0], FONT_CONSOLE[1], "bold"))
        self.textbox.tag_configure("matrix", foreground="#ECF0F1")
        self.textbox.tag_configure("separator", foreground="#7F8C8D")
        self.textbox.tag_configure("info", foreground="#95A5A6")

    def _apply_theme(self):
        """Apply warna berdasarkan current appearance mode."""
        mode = ctk.get_appearance_mode()
        if mode == "Dark":
            self.textbox.configure(bg="#1A1A2E", fg="#ECF0F1", insertbackground="#ECF0F1")
        else:
            self.textbox.configure(bg="#FFFFFF", fg="#1F2937", insertbackground="#1F2937")
            # Override tag colors for light mode
            self.textbox.tag_configure("step", foreground="#2563EB")
            self.textbox.tag_configure("result", foreground="#059669")
            self.textbox.tag_configure("error", foreground="#DC2626")
            self.textbox.tag_configure("matrix", foreground="#1F2937")
            self.textbox.tag_configure("separator", foreground="#9CA3AF")
            self.textbox.tag_configure("info", foreground="#6B7280")

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
