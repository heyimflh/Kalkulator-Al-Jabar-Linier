# =============================================================================
# SIDEBAR.PY — Komponen navigasi sidebar kiri
# =============================================================================

import customtkinter as ctk
from config import (
    FONT_LOGO, FONT_BUTTON, FONT_SMALL,
    SIDEBAR_WIDTH, MENU_ITEMS
)


class SidebarFrame(ctk.CTkFrame):
    """
    Sidebar navigasi kiri dengan:
    - Logo aplikasi
    - Tombol menu (7 fitur)
    - Theme toggle (Dark/Light)
    """

    def __init__(self, master, on_menu_click, on_theme_toggle, **kwargs):
        super().__init__(master, width=SIDEBAR_WIDTH, corner_radius=0, **kwargs)

        self.on_menu_click = on_menu_click
        self.on_theme_toggle = on_theme_toggle
        self.buttons = {}
        self.active_id = None

        # Prevent sidebar from shrinking
        self.grid_propagate(False)
        self.pack_propagate(False)

        self._build_ui()

    def _build_ui(self):
        """Bangun seluruh elemen sidebar."""

        # ─── Logo Section ───
        logo_frame = ctk.CTkFrame(self, fg_color="transparent")
        logo_frame.pack(fill="x", pady=(25, 10))

        ctk.CTkLabel(
            logo_frame,
            text="⊞ ALIN CALC",
            font=FONT_LOGO,
        ).pack(padx=20)

        ctk.CTkLabel(
            logo_frame,
            text="Linear Algebra Dashboard",
            font=FONT_SMALL,
            text_color=("gray50", "gray60"),
        ).pack(padx=20, pady=(2, 0))

        # ─── Separator ───
        ctk.CTkFrame(self, height=1, fg_color=("gray75", "gray30")).pack(
            fill="x", padx=20, pady=(15, 10)
        )

        # ─── Menu Buttons ───
        menu_frame = ctk.CTkFrame(self, fg_color="transparent")
        menu_frame.pack(fill="both", expand=True, padx=10, pady=5)

        for item in MENU_ITEMS:
            btn = ctk.CTkButton(
                menu_frame,
                text=f"  {item['icon']}  {item['label']}",
                font=FONT_BUTTON,
                anchor="w",
                height=42,
                corner_radius=8,
                fg_color="transparent",
                text_color=("gray20", "gray80"),
                hover_color=("gray85", "#1F3A5F"),
                command=lambda mid=item["id"]: self._handle_click(mid),
            )
            btn.pack(fill="x", pady=3)
            self.buttons[item["id"]] = btn

        # ─── Bottom: Theme Toggle ───
        # Separator bawah
        ctk.CTkFrame(self, height=1, fg_color=("gray75", "gray30")).pack(
            fill="x", side="bottom", padx=20, pady=(0, 10)
        )

        bottom_frame = ctk.CTkFrame(self, fg_color="transparent")
        bottom_frame.pack(fill="x", side="bottom", padx=20, pady=(10, 20))

        self.theme_label = ctk.CTkLabel(
            bottom_frame,
            text="🌙 Dark Mode",
            font=FONT_SMALL,
        )
        self.theme_label.pack(side="left")

        self.theme_switch = ctk.CTkSwitch(
            bottom_frame,
            text="",
            width=40,
            command=self._toggle_theme,
            onvalue=1,
            offvalue=0,
        )
        self.theme_switch.pack(side="right")
        self.theme_switch.select()  # Default: dark mode ON

    def _handle_click(self, menu_id):
        """Handle klik tombol menu."""
        self.set_active(menu_id)
        self.on_menu_click(menu_id)

    def set_active(self, menu_id):
        """Set tombol aktif dengan visual highlight."""
        # Reset semua
        for btn in self.buttons.values():
            btn.configure(
                fg_color="transparent",
                text_color=("gray20", "gray80"),
            )

        # Highlight aktif
        if menu_id in self.buttons:
            self.buttons[menu_id].configure(
                fg_color=("gray80", "#0F3460"),
                text_color=("gray10", "#ECF0F1"),
            )
            self.active_id = menu_id

    def _toggle_theme(self):
        """Toggle dark/light mode."""
        if self.theme_switch.get() == 1:
            self.theme_label.configure(text="🌙 Dark Mode")
            self.on_theme_toggle("dark")
        else:
            self.theme_label.configure(text="☀️ Light Mode")
            self.on_theme_toggle("light")
