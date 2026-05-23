# =============================================================================
# ERROR_BANNER.PY — Inline error/warning/success banner
# =============================================================================

import customtkinter as ctk
from config import FONT_BODY, FONT_SMALL


class ErrorBanner(ctk.CTkFrame):
    """
    Inline banner untuk menampilkan error, warning, atau success message.
    Menggantikan messagebox pop-up dari kode lama.
    
    Features:
    - Auto-dismiss setelah timeout (default 5 detik)
    - Tiga tipe: error (merah), warning (kuning), success (hijau)
    - Bisa dismiss manual via tombol ×
    - Animasi fade-in (opsional)
    """

    # Color schemes per type
    STYLES = {
        "error": {
            "fg_color": ("#FEE2E2", "#3B1010"),
            "border_color": ("#EF4444", "#E74C3C"),
            "text_color": ("#991B1B", "#FCA5A5"),
            "icon": "⚠️",
        },
        "warning": {
            "fg_color": ("#FEF3C7", "#3B2F08"),
            "border_color": ("#F59E0B", "#D97706"),
            "text_color": ("#92400E", "#FCD34D"),
            "icon": "⚡",
        },
        "success": {
            "fg_color": ("#D1FAE5", "#082F1A"),
            "border_color": ("#10B981", "#059669"),
            "text_color": ("#065F46", "#6EE7B7"),
            "icon": "✅",
        },
        "info": {
            "fg_color": ("#DBEAFE", "#0C1929"),
            "border_color": ("#3B82F6", "#2563EB"),
            "text_color": ("#1E40AF", "#93C5FD"),
            "icon": "ℹ️",
        },
    }

    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", height=0, **kwargs)

        self._after_id = None
        self._is_visible = False
        self.inner_frame = None

    def show(self, message, banner_type="error", auto_dismiss=5000):
        """
        Tampilkan banner.
        
        Args:
            message: Teks pesan
            banner_type: 'error', 'warning', 'success', 'info'
            auto_dismiss: ms sebelum auto-hide (0 = no auto-dismiss)
        """
        # Cancel previous auto-dismiss
        if self._after_id:
            self.after_cancel(self._after_id)
            self._after_id = None

        # Remove existing banner
        if self.inner_frame:
            self.inner_frame.destroy()

        style = self.STYLES.get(banner_type, self.STYLES["error"])

        # Build banner
        self.inner_frame = ctk.CTkFrame(
            self,
            fg_color=style["fg_color"],
            border_color=style["border_color"],
            border_width=1,
            corner_radius=8,
            height=45,
        )
        self.inner_frame.pack(fill="x", pady=(0, 10))
        self.inner_frame.pack_propagate(False)

        # Content
        content = ctk.CTkFrame(self.inner_frame, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=12, pady=8)

        # Icon + Message
        ctk.CTkLabel(
            content,
            text=f"{style['icon']}  {message}",
            font=FONT_SMALL,
            text_color=style["text_color"],
            anchor="w",
        ).pack(side="left", fill="x", expand=True)

        # Dismiss button
        dismiss_btn = ctk.CTkButton(
            content,
            text="×",
            width=24,
            height=24,
            corner_radius=4,
            fg_color="transparent",
            hover_color=style["border_color"],
            text_color=style["text_color"],
            font=("Segoe UI", 14, "bold"),
            command=self.hide,
        )
        dismiss_btn.pack(side="right")

        self._is_visible = True

        # Auto-dismiss
        if auto_dismiss > 0:
            self._after_id = self.after(auto_dismiss, self.hide)

    def hide(self):
        """Sembunyikan banner."""
        if self._after_id:
            self.after_cancel(self._after_id)
            self._after_id = None

        if self.inner_frame:
            self.inner_frame.destroy()
            self.inner_frame = None

        self._is_visible = False

    def show_error(self, message, auto_dismiss=5000):
        """Shortcut untuk error banner."""
        self.show(message, "error", auto_dismiss)

    def show_warning(self, message, auto_dismiss=5000):
        """Shortcut untuk warning banner."""
        self.show(message, "warning", auto_dismiss)

    def show_success(self, message, auto_dismiss=3000):
        """Shortcut untuk success banner."""
        self.show(message, "success", auto_dismiss)

    def show_info(self, message, auto_dismiss=4000):
        """Shortcut untuk info banner."""
        self.show(message, "info", auto_dismiss)

    @property
    def is_visible(self):
        return self._is_visible
