# =============================================================================
# STATUS_BAR.PY — AXIOM Status Bar (Polished)
# =============================================================================
# Clean, minimal status bar with proper contrast and spacing.
# =============================================================================

import customtkinter as ctk
from config import FONT_STATUS


class StatusBar(ctk.CTkFrame):
    """
    Minimal status bar: page indicator (left), shortcuts (center), status (right).
    """

    def __init__(self, master, **kwargs):
        super().__init__(
            master, height=32, corner_radius=0,
            fg_color=("gray97", "#070707"),
            **kwargs,
        )
        self.pack_propagate(False)

        # Left: page info
        self.left_label = ctk.CTkLabel(
            self, text="", font=FONT_STATUS,
            text_color=("gray45", "#71717A"),
        )
        self.left_label.pack(side="left", padx=16)

        # Right: status message
        self.right_label = ctk.CTkLabel(
            self, text="", font=FONT_STATUS,
            text_color=("gray45", "#71717A"),
        )
        self.right_label.pack(side="right", padx=16)

        # Center: shortcuts
        self.center_label = ctk.CTkLabel(
            self,
            text="Ctrl+1–7 Navigasi   ·   Ctrl+Enter Hitung   ·   Ctrl+L Clear",
            font=("Segoe UI", 10),
            text_color=("gray55", "#3F3F46"),
        )
        self.center_label.pack(expand=True)

    def set_page(self, page_name):
        """Update active page indicator."""
        self.left_label.configure(text=f"◈ {page_name}")

    def set_status(self, message, status_type="info"):
        """Update status message."""
        colors = {
            "info": ("gray45", "#71717A"),
            "success": ("#059669", "#22C55E"),
            "error": ("#DC2626", "#F43F5E"),
        }
        color = colors.get(status_type, colors["info"])
        self.right_label.configure(text=message, text_color=color)

        if status_type != "info":
            self.after(5000, lambda: self.right_label.configure(
                text="", text_color=("gray45", "#71717A")
            ))

    def clear_status(self):
        """Clear status message."""
        self.right_label.configure(text="", text_color=("gray45", "#71717A"))
