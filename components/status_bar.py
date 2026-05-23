# =============================================================================
# STATUS_BAR.PY — Status bar di bagian bawah window
# =============================================================================

import customtkinter as ctk
from config import FONT_SMALL


class StatusBar(ctk.CTkFrame):
    """
    Status bar di bawah window yang menampilkan:
    - Info halaman aktif (kiri)
    - Shortcut hints (tengah)
    - Status terakhir (kanan)
    """

    def __init__(self, master, **kwargs):
        super().__init__(master, height=30, corner_radius=0, **kwargs)
        self.pack_propagate(False)

        # Left: page info
        self.left_label = ctk.CTkLabel(
            self, text="", font=FONT_SMALL,
            text_color=("gray50", "gray60"),
        )
        self.left_label.pack(side="left", padx=15)

        # Right: status
        self.right_label = ctk.CTkLabel(
            self, text="", font=FONT_SMALL,
            text_color=("gray50", "gray60"),
        )
        self.right_label.pack(side="right", padx=15)

        # Center: shortcuts hint
        self.center_label = ctk.CTkLabel(
            self,
            text="Ctrl+1~7: Navigasi  │  Ctrl+Enter: Hitung  │  Ctrl+L: Clear",
            font=("Segoe UI", 10),
            text_color=("gray60", "gray50"),
        )
        self.center_label.pack(expand=True)

    def set_page(self, page_name):
        """Update info halaman aktif."""
        self.left_label.configure(text=f"📍 {page_name}")

    def set_status(self, message, status_type="info"):
        """Update status message (kanan)."""
        colors = {
            "info": ("gray50", "gray60"),
            "success": ("#059669", "#2ECC71"),
            "error": ("#DC2626", "#E74C3C"),
        }
        color = colors.get(status_type, colors["info"])
        self.right_label.configure(text=message, text_color=color)

        # Auto-clear after 5 seconds
        if status_type != "info":
            self.after(5000, lambda: self.right_label.configure(
                text="", text_color=("gray50", "gray60")
            ))

    def clear_status(self):
        """Clear status message."""
        self.right_label.configure(text="", text_color=("gray50", "gray60"))
