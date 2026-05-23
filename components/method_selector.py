# =============================================================================
# METHOD_SELECTOR.PY — Segmented Button untuk pemilihan metode
# =============================================================================

import customtkinter as ctk
from config import FONT_BODY, FONT_SMALL


class MethodSelector(ctk.CTkFrame):
    """
    Widget pemilihan metode menggunakan CTkSegmentedButton.
    Menggantikan radio button pop-up dari kode lama.
    
    Usage:
        selector = MethodSelector(parent, 
            label="Metode:",
            options=["Gauss", "Gauss-Jordan", "Matriks Balikan"],
            default="Gauss",
            tooltips={"Gauss": "Eliminasi ke bentuk REF", ...}
        )
        selected = selector.get()
    """

    def __init__(self, master, label="Metode:", options=None,
                 default=None, tooltips=None, on_change=None, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)

        self.options = options or ["Option 1", "Option 2"]
        self.tooltips = tooltips or {}
        self.on_change = on_change
        self._selected = ctk.StringVar(value=default or self.options[0])

        self._build_ui()

    def _build_ui(self):
        """Bangun label dan segmented button."""

        # Label
        ctk.CTkLabel(
            self, text="Metode:", font=FONT_BODY
        ).pack(anchor="w", pady=(0, 8))

        # Segmented Button
        self.seg_button = ctk.CTkSegmentedButton(
            self,
            values=self.options,
            variable=self._selected,
            font=FONT_SMALL,
            height=36,
            corner_radius=8,
            command=self._on_select,
        )
        self.seg_button.pack(fill="x")

        # Tooltip/description label (shows description of selected method)
        self.desc_label = ctk.CTkLabel(
            self,
            text=self._get_tooltip(self._selected.get()),
            font=FONT_SMALL,
            text_color=("gray50", "gray60"),
            anchor="w",
        )
        self.desc_label.pack(anchor="w", pady=(5, 0))

    def _on_select(self, value):
        """Handle selection change."""
        self._selected.set(value)
        # Update tooltip
        self.desc_label.configure(text=self._get_tooltip(value))
        # Callback
        if self.on_change:
            self.on_change(value)

    def _get_tooltip(self, value):
        """Get tooltip text for a method."""
        return self.tooltips.get(value, "")

    # ─────────────────────────────────────────────
    # PUBLIC API
    # ─────────────────────────────────────────────

    def get(self):
        """Return currently selected method string."""
        return self._selected.get()

    def set(self, value):
        """Set selected method programmatically."""
        if value in self.options:
            self._selected.set(value)
            self.seg_button.set(value)
            self.desc_label.configure(text=self._get_tooltip(value))

    def set_options(self, options, default=None, tooltips=None):
        """Update available options."""
        self.options = options
        if tooltips:
            self.tooltips = tooltips
        self.seg_button.configure(values=options)
        if default:
            self.set(default)
        elif options:
            self.set(options[0])
