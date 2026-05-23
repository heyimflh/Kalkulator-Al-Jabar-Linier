# =============================================================================
# TOOLTIP.PY — Tooltip widget yang muncul saat hover
# =============================================================================

import customtkinter as ctk


class Tooltip:
    """
    Tooltip yang muncul saat mouse hover di atas widget.
    Muncul setelah delay 500ms, hilang saat mouse keluar.
    
    Usage:
        btn = ctk.CTkButton(...)
        Tooltip(btn, "Penjelasan tombol ini")
    """

    def __init__(self, widget, text, delay=500):
        self.widget = widget
        self.text = text
        self.delay = delay
        self._after_id = None
        self._tooltip_window = None

        widget.bind("<Enter>", self._on_enter)
        widget.bind("<Leave>", self._on_leave)
        widget.bind("<ButtonPress>", self._on_leave)

    def _on_enter(self, event=None):
        """Schedule tooltip appearance."""
        self._cancel()
        self._after_id = self.widget.after(self.delay, self._show)

    def _on_leave(self, event=None):
        """Cancel and hide tooltip."""
        self._cancel()
        self._hide()

    def _cancel(self):
        if self._after_id:
            self.widget.after_cancel(self._after_id)
            self._after_id = None

    def _show(self):
        """Display the tooltip."""
        if self._tooltip_window:
            return

        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 5

        self._tooltip_window = tw = ctk.CTkToplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        tw.attributes("-topmost", True)

        # Tooltip frame
        frame = ctk.CTkFrame(
            tw,
            corner_radius=6,
            fg_color=("gray90", "#2C3E50"),
            border_width=1,
            border_color=("gray70", "#34495E"),
        )
        frame.pack()

        label = ctk.CTkLabel(
            frame,
            text=self.text,
            font=("Segoe UI", 11),
            text_color=("gray20", "#ECF0F1"),
            wraplength=250,
        )
        label.pack(padx=10, pady=6)

    def _hide(self):
        """Hide the tooltip."""
        if self._tooltip_window:
            self._tooltip_window.destroy()
            self._tooltip_window = None

    def update_text(self, new_text):
        """Update tooltip text."""
        self.text = new_text
