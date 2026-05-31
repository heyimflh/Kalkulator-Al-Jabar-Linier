# =============================================================================
# MATRIX_INPUT.PY — Dynamic Matrix Grid Input Widget
# =============================================================================

import customtkinter as ctk
import re
from config import (
    FONT_BODY, FONT_MATRIX_CELL, FONT_SMALL, FONT_BUTTON,
    MATRIX_CELL_WIDTH, MATRIX_CELL_HEIGHT, MAX_MATRIX_DIM
)


class MatrixInputWidget(ctk.CTkFrame):
    """
    Widget input matriks dinamis dengan:
    - Dimension selector (baris x kolom)
    - Grid cells (CTkEntry) yang di-generate otomatis
    - Validasi real-time per cell
    - Tab & Arrow key navigation
    - Quick actions: Clear, Random, Identity, Paste
    """

    # Default visual style — preserves the original look so existing pages
    # (eigen, determinan, dll.) yang tidak mengirim `style` tetap sama.
    DEFAULT_STYLE = {
        "label_color": None,                          # None → theme default
        "muted_color": ("gray50", "gray60"),
        "cell_fg": None,                              # None → CTkEntry default
        "cell_text": None,
        "cell_border": ("gray60", "#2C3E50"),
        "cell_border_focus": ("#2563EB", "#3498DB"),
        "cell_border_error": ("#DC2626", "#E74C3C"),
        "cell_width": MATRIX_CELL_WIDTH,
        "cell_height": MATRIX_CELL_HEIGHT,
        "cell_radius": 4,
        "selector_fg": None,
        "selector_button": None,
        "selector_button_hover": None,
        "selector_text": None,
        "selector_width": 60,
        # When True, the Baris/Kolom selectors wrap onto their own row below
        # the label (prevents truncation inside narrow cards). Default keeps
        # the original single-row layout so existing pages are unaffected.
        "header_stack": False,
        # Grid container behavior:
        #   • "grid_scroll" False → grid tumbuh dinamis (tanpa kotak scroll
        #     internal), jadi sel orde berapa pun tampil penuh & hanya
        #     halaman induk yang menggulir. Mencegah nested-scroll & clipping.
        #   • "grid_height" hanya dipakai saat grid_scroll=True (legacy).
        "grid_scroll": True,
        "grid_height": 200,
        # When True, cells shrink to fit the container width (staying square)
        # so any order renders fully without horizontal clipping, and grow
        # back up to cell_width when there's room. Off by default (legacy).
        "adaptive_cells": False,
        "cell_min": 26,
        "util_fg": ("gray80", "#2C3E50"),
        "util_hover": ("gray70", "#34495E"),
        "util_text": ("gray20", "gray80"),
        "util_border": None,
        "util_border_width": 0,
        # When True, the utility buttons wrap into a responsive grid instead
        # of a single overflowing row. Off by default (legacy pages unchanged).
        "toolbar_wrap": False,
        "toolbar_cols": 3,
    }

    def __init__(self, master, default_rows=3, default_cols=3,
                 show_augmented=False, label="Matriks", style=None, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)

        # Merge optional style overrides with defaults (backward compatible).
        self.style = {**self.DEFAULT_STYLE, **(style or {})}

        self.label_text = label
        self.show_augmented = show_augmented  # Untuk SPL: matriks A | b
        self.cells = []       # 2D list of CTkEntry
        self.cell_vars = []   # 2D list of StringVar
        self.current_rows = default_rows
        self.current_cols = default_cols

        self._build_ui()
        self._generate_grid()

    # ─────────────────────────────────────────────
    # BUILD UI
    # ─────────────────────────────────────────────

    def _build_ui(self):
        """Bangun header (label + dimension selector) dan area grid."""

        s = self.style

        # Optional kwargs for OptionMenu styling (only pass if provided so we
        # don't override the theme default with None).
        sel_kwargs = {}
        if s.get("selector_fg"):
            sel_kwargs["fg_color"] = s["selector_fg"]
        if s.get("selector_button"):
            sel_kwargs["button_color"] = s["selector_button"]
        if s.get("selector_button_hover"):
            sel_kwargs["button_hover_color"] = s["selector_button_hover"]
        if s.get("selector_text"):
            sel_kwargs["text_color"] = s["selector_text"]

        label_kwargs = {}
        if s.get("label_color"):
            label_kwargs["text_color"] = s["label_color"]

        muted_kwargs = {"text_color": s["muted_color"]} if s.get("muted_color") else {}

        sel_width = s.get("selector_width") or 60

        # ─── Header: Label + Dimension Selectors ───
        # Two layouts:
        #   • header_stack=False (default): single horizontal row (legacy look)
        #   • header_stack=True: label on top, "Baris/Kolom" wrap to a 2nd row
        #     so they never truncate inside a narrow card.
        if s.get("header_stack"):
            header = ctk.CTkFrame(self, fg_color="transparent")
            header.pack(fill="x", pady=(0, 10))

            ctk.CTkLabel(
                header, text=self.label_text, font=FONT_BODY, anchor="w",
                **label_kwargs
            ).pack(fill="x", pady=(0, 6))

            dim_row = ctk.CTkFrame(header, fg_color="transparent")
            dim_row.pack(fill="x")
            row_parent = col_parent = dim_row
        else:
            header = ctk.CTkFrame(self, fg_color="transparent")
            header.pack(fill="x", pady=(0, 10))

            ctk.CTkLabel(
                header, text=self.label_text, font=FONT_BODY, **label_kwargs
            ).pack(side="left", padx=(0, 15))
            row_parent = col_parent = header

        # Row selector
        ctk.CTkLabel(row_parent, text="Baris:", font=FONT_SMALL, **muted_kwargs).pack(side="left", padx=(0, 5))
        self.row_var = ctk.StringVar(value=str(self.current_rows))
        self.row_menu = ctk.CTkOptionMenu(
            row_parent,
            values=[str(i) for i in range(1, MAX_MATRIX_DIM + 1)],
            variable=self.row_var,
            width=sel_width,
            height=28,
            font=FONT_SMALL,
            command=self._on_dimension_change,
            **sel_kwargs,
        )
        self.row_menu.pack(side="left", padx=(0, 10))

        # Col selector
        ctk.CTkLabel(col_parent, text="Kolom:", font=FONT_SMALL, **muted_kwargs).pack(side="left", padx=(0, 5))
        self.col_var = ctk.StringVar(value=str(self.current_cols))
        self.col_menu = ctk.CTkOptionMenu(
            col_parent,
            values=[str(i) for i in range(1, MAX_MATRIX_DIM + 1)],
            variable=self.col_var,
            width=sel_width,
            height=28,
            font=FONT_SMALL,
            command=self._on_dimension_change,
            **sel_kwargs,
        )
        self.col_menu.pack(side="left")

        # ─── Grid Container ───
        if s.get("grid_scroll", True):
            # Legacy: internal scroll box with fixed height.
            self.grid_container = ctk.CTkScrollableFrame(
                self, fg_color="transparent", height=s.get("grid_height", 200)
            )
            self.grid_container.pack(fill="both", expand=True, pady=(0, 10))
        else:
            # Dynamic: plain frame that grows with content, so any order
            # renders fully and only the parent page scrolls (no nested-scroll
            # conflict, no clipping for large matrices like 10×10).
            self.grid_container = ctk.CTkFrame(self, fg_color="transparent")
            self.grid_container.pack(fill="both", expand=True, pady=(0, 10))

        # ─── Quick Actions Bar ───
        actions = ctk.CTkFrame(self, fg_color="transparent")
        actions.pack(fill="x")

        btn_style = {
            "font": FONT_SMALL,
            "height": 30,
            "corner_radius": 6,
            "fg_color": s["util_fg"],
            "hover_color": s["util_hover"],
            "text_color": s["util_text"],
        }
        if s.get("util_border"):
            btn_style["border_color"] = s["util_border"]
            btn_style["border_width"] = s.get("util_border_width", 1)

        buttons = [
            ("Clear", self._clear_all),
            ("Random", self._random_fill),
            ("Identity", self._identity_fill),
            ("Transpose", self._transpose),
            ("Paste", self._paste_from_clipboard),
        ]

        if s.get("toolbar_wrap"):
            # Responsive grid: buttons stretch to fill the card width and wrap
            # to a second row, so nothing gets clipped inside narrow cards.
            ncols = s.get("toolbar_cols", 3)
            for i in range(ncols):
                actions.grid_columnconfigure(i, weight=1, uniform="util")
            for idx, (text, cmd) in enumerate(buttons):
                r, c = divmod(idx, ncols)
                ctk.CTkButton(
                    actions, text=text, command=cmd, **btn_style
                ).grid(row=r, column=c, sticky="ew", padx=2, pady=2)
        else:
            widths = {"Clear": 70, "Random": 80, "Identity": 80, "Transpose": 90, "Paste": 70}
            for idx, (text, cmd) in enumerate(buttons):
                pad = (0, 5) if idx < len(buttons) - 1 else (0, 0)
                ctk.CTkButton(
                    actions, text=text, width=widths[text], command=cmd, **btn_style
                ).pack(side="left", padx=pad)

    # ─────────────────────────────────────────────
    # GRID GENERATION
    # ─────────────────────────────────────────────

    def _generate_grid(self):
        """Generate matrix grid berdasarkan dimensi saat ini."""
        s = self.style
        # Clear existing grid
        for widget in self.grid_container.winfo_children():
            widget.destroy()
        self.cells = []
        self.cell_vars = []

        rows = self.current_rows
        cols = self.current_cols

        adaptive = s.get("adaptive_cells")

        # Inner frame for grid layout. For adaptive sizing it fills the width
        # so cells can distribute evenly; otherwise it hugs content (legacy).
        grid_frame = ctk.CTkFrame(self.grid_container, fg_color="transparent")
        if adaptive:
            grid_frame.pack(fill="x", expand=True)
        else:
            grid_frame.pack(anchor="w")
        self._grid_frame = grid_frame

        base_w = s["cell_width"]
        base_h = s["cell_height"]

        for r in range(rows):
            row_cells = []
            row_vars = []
            for c in range(cols):
                var = ctk.StringVar(value="0")
                entry_kwargs = {
                    "textvariable": var,
                    "width": base_w,
                    "height": base_h,
                    "font": FONT_MATRIX_CELL,
                    "justify": "center",
                    "corner_radius": s["cell_radius"],
                    "border_width": 1,
                    "border_color": s["cell_border"],
                }
                if s.get("cell_fg"):
                    entry_kwargs["fg_color"] = s["cell_fg"]
                if s.get("cell_text"):
                    entry_kwargs["text_color"] = s["cell_text"]

                entry = ctk.CTkEntry(grid_frame, **entry_kwargs)
                if adaptive:
                    entry.grid(row=r, column=c, padx=2, pady=2, sticky="nsew")
                else:
                    entry.grid(row=r, column=c, padx=2, pady=2)

                # Bind events
                entry.bind("<FocusIn>", lambda e, ent=entry: self._on_focus_in(ent))
                entry.bind("<FocusOut>", lambda e, ent=entry, v=var: self._on_focus_out(ent, v))
                entry.bind("<Tab>", lambda e, row=r, col=c: self._tab_next(row, col))
                entry.bind("<Shift-Tab>", lambda e, row=r, col=c: self._tab_prev(row, col))
                entry.bind("<Up>", lambda e, row=r, col=c: self._arrow_nav(row - 1, col))
                entry.bind("<Down>", lambda e, row=r, col=c: self._arrow_nav(row + 1, col))
                entry.bind("<Left>", lambda e, row=r, col=c, ent=entry: self._arrow_left(ent, row, col))
                entry.bind("<Right>", lambda e, row=r, col=c, ent=entry: self._arrow_right(ent, row, col))

                row_cells.append(entry)
                row_vars.append(var)

            self.cells.append(row_cells)
            self.cell_vars.append(row_vars)

        if adaptive:
            # Equal-weight columns so cells distribute & shrink to fit width.
            for c in range(cols):
                grid_frame.grid_columnconfigure(c, weight=1, uniform="mcell")
            # Recompute square cell size whenever the container is resized.
            self.grid_container.bind("<Configure>", self._relayout_cells)
            self.after(0, self._relayout_cells)

    def _font_for_cell(self, size):
        """Pilih ukuran font yang proporsional dgn ukuran sel agar angka
        (mis. '-3', '10') tetap terbaca penuh & tak pernah terpotong."""
        fam = FONT_MATRIX_CELL[0]
        if size >= 44:
            fs = 14
        elif size >= 38:
            fs = 13
        elif size >= 32:
            fs = 12
        elif size >= 28:
            fs = 11
        else:
            fs = 10
        return (fam, fs)

    def _relayout_cells(self, event=None):
        """Adaptive sizing: shrink/grow square cells + skala font agar muat
        di lebar container tanpa clipping, untuk orde rendah maupun tinggi."""
        s = self.style
        if not s.get("adaptive_cells") or not self.cells:
            return
        cols = self.current_cols
        if cols <= 0:
            return
        avail = self.grid_container.winfo_width()
        if avail <= 1:
            return  # belum ter-render
        # Kurangi padding antar sel (4px per sel) + sedikit margin aman.
        per_cell = int((avail - cols * 4 - 6) / cols)
        size = max(s.get("cell_min", 26), min(s["cell_width"], per_cell))
        cell_font = self._font_for_cell(size)
        # Terapkan ukuran persegi + font yang sama ke semua sel.
        for row in self.cells:
            for entry in row:
                try:
                    entry.configure(width=size, height=size, font=cell_font)
                except Exception:
                    pass

    def _on_dimension_change(self, _=None):
        """Rebuild grid saat dimensi berubah."""
        new_rows = int(self.row_var.get())
        new_cols = int(self.col_var.get())

        # Simpan data lama
        old_data = self.get_values_raw()

        self.current_rows = new_rows
        self.current_cols = new_cols
        self._generate_grid()

        # Restore data yang masih muat
        for r in range(min(len(old_data), new_rows)):
            for c in range(min(len(old_data[r]), new_cols)):
                self.cell_vars[r][c].set(old_data[r][c])

    # ─────────────────────────────────────────────
    # VALIDATION
    # ─────────────────────────────────────────────

    def _validate_cell(self, value):
        """
        Validasi input cell. Terima:
        - Integer: 1, -3, 0
        - Desimal: 1.5, -0.33
        - Pecahan: 1/3, -2/5
        - Kosong (akan jadi 0)
        """
        if value.strip() == "" or value.strip() == "-":
            return True
        pattern = r'^-?\d+(/\d+)?(\.\d*)?$'
        return bool(re.match(pattern, value.strip()))

    def _on_focus_in(self, entry):
        """Highlight cell saat focus."""
        entry.configure(border_color=self.style["cell_border_focus"])
        # Select all text
        entry.select_range(0, "end")

    def _on_focus_out(self, entry, var):
        """Validasi dan reset border saat focus keluar."""
        value = var.get().strip()
        if value == "" or value == "-":
            var.set("0")

        if self._validate_cell(var.get()):
            entry.configure(border_color=self.style["cell_border"])
        else:
            entry.configure(border_color=self.style["cell_border_error"])

    # ─────────────────────────────────────────────
    # NAVIGATION
    # ─────────────────────────────────────────────

    def _tab_next(self, row, col):
        """Tab → next cell (kiri ke kanan, atas ke bawah)."""
        col += 1
        if col >= self.current_cols:
            col = 0
            row += 1
        if row < self.current_rows:
            self.cells[row][col].focus_set()
        return "break"

    def _tab_prev(self, row, col):
        """Shift+Tab → previous cell."""
        col -= 1
        if col < 0:
            col = self.current_cols - 1
            row -= 1
        if row >= 0:
            self.cells[row][col].focus_set()
        return "break"

    def _arrow_nav(self, row, col):
        """Arrow up/down navigation."""
        if 0 <= row < self.current_rows and 0 <= col < self.current_cols:
            self.cells[row][col].focus_set()
        return "break"

    def _arrow_left(self, entry, row, col):
        """Arrow left — pindah cell jika cursor di posisi 0."""
        if entry.index("insert") == 0:
            if col > 0:
                self.cells[row][col - 1].focus_set()
            return "break"

    def _arrow_right(self, entry, row, col):
        """Arrow right — pindah cell jika cursor di akhir."""
        if entry.index("insert") == len(entry.get()):
            if col < self.current_cols - 1:
                self.cells[row][col + 1].focus_set()
            return "break"

    # ─────────────────────────────────────────────
    # QUICK ACTIONS
    # ─────────────────────────────────────────────

    def _clear_all(self):
        """Reset semua cell ke 0."""
        for r in range(self.current_rows):
            for c in range(self.current_cols):
                self.cell_vars[r][c].set("0")

    def _random_fill(self):
        """Isi matriks dengan angka random -9 s/d 9."""
        import random
        for r in range(self.current_rows):
            for c in range(self.current_cols):
                self.cell_vars[r][c].set(str(random.randint(-9, 9)))

    def _identity_fill(self):
        """Isi dengan matriks identitas."""
        for r in range(self.current_rows):
            for c in range(self.current_cols):
                self.cell_vars[r][c].set("1" if r == c else "0")

    def _transpose(self):
        """Transpose matriks yang sudah diinput."""
        data = self.get_values_raw()
        rows = self.current_rows
        cols = self.current_cols

        # Transpose data
        transposed = []
        for c in range(cols):
            new_row = []
            for r in range(rows):
                new_row.append(data[r][c])
            transposed.append(new_row)

        # Update dimensions (swap rows/cols)
        self.current_rows = cols
        self.current_cols = rows
        self.row_var.set(str(self.current_rows))
        self.col_var.set(str(self.current_cols))
        self._generate_grid()

        # Fill transposed data
        for r in range(self.current_rows):
            for c in range(self.current_cols):
                self.cell_vars[r][c].set(transposed[r][c])

    def _paste_from_clipboard(self):
        """Paste matriks dari clipboard (tab/space separated)."""
        try:
            clipboard = self.clipboard_get()
            lines = clipboard.strip().split("\n")
            for r, line in enumerate(lines):
                if r >= self.current_rows:
                    break
                # Support tab-separated (Excel) dan space-separated
                values = re.split(r'[\t\s]+', line.strip())
                for c, val in enumerate(values):
                    if c >= self.current_cols:
                        break
                    if self._validate_cell(val):
                        self.cell_vars[r][c].set(val)
        except Exception:
            pass  # Clipboard kosong atau format tidak valid

    # ─────────────────────────────────────────────
    # PUBLIC API
    # ─────────────────────────────────────────────

    def get_values_raw(self):
        """Return 2D list of string values."""
        result = []
        for r in range(self.current_rows):
            row = []
            for c in range(self.current_cols):
                row.append(self.cell_vars[r][c].get())
            result.append(row)
        return result

    def get_matrix(self):
        """
        Return sympy Matrix dari input.
        Raises ValueError jika ada cell invalid.
        """
        import sympy as sp
        data = []
        for r in range(self.current_rows):
            row = []
            for c in range(self.current_cols):
                val = self.cell_vars[r][c].get().strip()
                if val == "" or val == "-":
                    val = "0"
                try:
                    row.append(sp.Rational(val))
                except (ValueError, TypeError):
                    raise ValueError(
                        f"Input tidak valid di baris {r+1}, kolom {c+1}: '{val}'"
                    )
            data.append(row)
        return sp.Matrix(data)

    def set_matrix(self, matrix):
        """Set grid dari sympy Matrix atau 2D list."""
        import sympy as sp
        if isinstance(matrix, sp.Matrix):
            rows, cols = matrix.shape
            data = matrix.tolist()
        else:
            data = matrix
            rows = len(data)
            cols = len(data[0]) if data else 0

        # Update dimensi jika perlu
        if rows != self.current_rows or cols != self.current_cols:
            self.current_rows = min(rows, MAX_MATRIX_DIM)
            self.current_cols = min(cols, MAX_MATRIX_DIM)
            self.row_var.set(str(self.current_rows))
            self.col_var.set(str(self.current_cols))
            self._generate_grid()

        # Fill values
        for r in range(self.current_rows):
            for c in range(self.current_cols):
                val = str(data[r][c]) if r < rows and c < cols else "0"
                self.cell_vars[r][c].set(val)

    def get_dimensions(self):
        """Return (rows, cols) tuple."""
        return (self.current_rows, self.current_cols)

    def set_dimensions(self, rows, cols):
        """Set dimensi matriks secara programmatic."""
        self.current_rows = min(rows, MAX_MATRIX_DIM)
        self.current_cols = min(cols, MAX_MATRIX_DIM)
        self.row_var.set(str(self.current_rows))
        self.col_var.set(str(self.current_cols))
        self._generate_grid()
