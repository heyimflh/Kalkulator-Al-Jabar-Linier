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

    def __init__(self, master, default_rows=3, default_cols=3,
                 show_augmented=False, label="Matriks", **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)

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

        # ─── Header Row: Label + Dimension Selectors ───
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", pady=(0, 10))

        ctk.CTkLabel(
            header, text=self.label_text, font=FONT_BODY
        ).pack(side="left", padx=(0, 15))

        # Row selector
        ctk.CTkLabel(header, text="Baris:", font=FONT_SMALL).pack(side="left", padx=(0, 5))
        self.row_var = ctk.StringVar(value=str(self.current_rows))
        self.row_menu = ctk.CTkOptionMenu(
            header,
            values=[str(i) for i in range(1, MAX_MATRIX_DIM + 1)],
            variable=self.row_var,
            width=60,
            height=28,
            font=FONT_SMALL,
            command=self._on_dimension_change,
        )
        self.row_menu.pack(side="left", padx=(0, 10))

        # Col selector
        ctk.CTkLabel(header, text="Kolom:", font=FONT_SMALL).pack(side="left", padx=(0, 5))
        self.col_var = ctk.StringVar(value=str(self.current_cols))
        self.col_menu = ctk.CTkOptionMenu(
            header,
            values=[str(i) for i in range(1, MAX_MATRIX_DIM + 1)],
            variable=self.col_var,
            width=60,
            height=28,
            font=FONT_SMALL,
            command=self._on_dimension_change,
        )
        self.col_menu.pack(side="left")

        # ─── Grid Container (scrollable for large matrices) ───
        self.grid_container = ctk.CTkScrollableFrame(
            self, fg_color="transparent", height=200
        )
        self.grid_container.pack(fill="both", expand=True, pady=(0, 10))

        # ─── Quick Actions Bar ───
        actions = ctk.CTkFrame(self, fg_color="transparent")
        actions.pack(fill="x")

        btn_style = {
            "font": FONT_SMALL,
            "height": 30,
            "corner_radius": 6,
            "fg_color": ("gray80", "#2C3E50"),
            "hover_color": ("gray70", "#34495E"),
            "text_color": ("gray20", "gray80"),
        }

        ctk.CTkButton(
            actions, text="Clear", width=70, command=self._clear_all, **btn_style
        ).pack(side="left", padx=(0, 5))

        ctk.CTkButton(
            actions, text="Random", width=80, command=self._random_fill, **btn_style
        ).pack(side="left", padx=(0, 5))

        ctk.CTkButton(
            actions, text="Identity", width=80, command=self._identity_fill, **btn_style
        ).pack(side="left", padx=(0, 5))

        ctk.CTkButton(
            actions, text="Transpose", width=90, command=self._transpose, **btn_style
        ).pack(side="left", padx=(0, 5))

        ctk.CTkButton(
            actions, text="Paste", width=70, command=self._paste_from_clipboard, **btn_style
        ).pack(side="left")

    # ─────────────────────────────────────────────
    # GRID GENERATION
    # ─────────────────────────────────────────────

    def _generate_grid(self):
        """Generate matrix grid berdasarkan dimensi saat ini."""
        # Clear existing grid
        for widget in self.grid_container.winfo_children():
            widget.destroy()
        self.cells = []
        self.cell_vars = []

        rows = self.current_rows
        cols = self.current_cols

        # Inner frame for grid layout
        grid_frame = ctk.CTkFrame(self.grid_container, fg_color="transparent")
        grid_frame.pack(anchor="w")

        for r in range(rows):
            row_cells = []
            row_vars = []
            for c in range(cols):
                var = ctk.StringVar(value="0")
                entry = ctk.CTkEntry(
                    grid_frame,
                    textvariable=var,
                    width=MATRIX_CELL_WIDTH,
                    height=MATRIX_CELL_HEIGHT,
                    font=FONT_MATRIX_CELL,
                    justify="center",
                    corner_radius=4,
                    border_width=1,
                )
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
        entry.configure(border_color=("#2563EB", "#3498DB"))
        # Select all text
        entry.select_range(0, "end")

    def _on_focus_out(self, entry, var):
        """Validasi dan reset border saat focus keluar."""
        value = var.get().strip()
        if value == "" or value == "-":
            var.set("0")

        if self._validate_cell(var.get()):
            entry.configure(border_color=("gray60", "#2C3E50"))
        else:
            entry.configure(border_color=("#DC2626", "#E74C3C"))

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
