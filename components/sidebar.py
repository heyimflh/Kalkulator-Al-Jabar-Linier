# =============================================================================
# SIDEBAR.PY — AXIOM Premium Navigation Rail
# =============================================================================
# Darkmatter aesthetic sidebar with strong brand, premium active states,
# and bottom utility card.
# =============================================================================

import customtkinter as ctk
from config import (
    FONT_NAV_ITEM, FONT_NAV_LABEL, FONT_SMALL,
    SIDEBAR_WIDTH, MENU_ITEMS,
    APP_NAME, APP_SUBTITLE, DARK,
)


class SidebarFrame(ctk.CTkFrame):
    """
    AXIOM premium navigation rail.
    - Strong brand area with diamond icon
    - Menu items with violet left-bar active indicator
    - Bottom utility card with status + theme toggle
    """

    def __init__(self, master, on_menu_click, on_theme_toggle, **kwargs):
        super().__init__(
            master, width=SIDEBAR_WIDTH, corner_radius=0,
            fg_color=("gray98", "#070707"),
            **kwargs,
        )

        self.on_menu_click = on_menu_click
        self.on_theme_toggle = on_theme_toggle
        self.buttons = {}
        self.active_id = None
        self._indicators = {}

        self.grid_propagate(False)
        self.pack_propagate(False)

        self._build()

    def _build(self):
        """Construct sidebar."""

        # ═══════════════════════════════════════
        # BRAND AREA
        # ═══════════════════════════════════════
        brand_area = ctk.CTkFrame(self, fg_color="transparent")
        brand_area.pack(fill="x", padx=20, pady=(28, 0))

        # Logo row: diamond + AXIOM
        logo_row = ctk.CTkFrame(brand_area, fg_color="transparent")
        logo_row.pack(anchor="w")

        # Diamond icon with subtle glow bg
        diamond_bg = ctk.CTkFrame(
            logo_row,
            fg_color=("gray92", "#14101F"),
            corner_radius=10,
            width=36, height=36,
        )
        diamond_bg.pack(side="left", padx=(0, 10))
        diamond_bg.pack_propagate(False)
        ctk.CTkLabel(
            diamond_bg, text="◇",
            font=("Segoe UI", 18),
            text_color=("#7C3AED", "#A78BFA"),
        ).place(relx=0.5, rely=0.5, anchor="center")

        # Brand name
        ctk.CTkLabel(
            logo_row, text=APP_NAME,
            font=("Segoe UI", 20, "bold"),
            text_color=("gray10", "#FAFAFA"),
        ).pack(side="left")

        # Subtitle
        ctk.CTkLabel(
            brand_area, text=APP_SUBTITLE,
            font=("Segoe UI", 12),
            text_color=("gray45", "#94A3B8"),
        ).pack(anchor="w", pady=(6, 0))

        # ═══════════════════════════════════════
        # DIVIDER
        # ═══════════════════════════════════════
        ctk.CTkFrame(
            self, height=1,
            fg_color=("gray88", "#1F1F23"),
        ).pack(fill="x", padx=20, pady=(20, 14))

        # ═══════════════════════════════════════
        # SECTION LABEL
        # ═══════════════════════════════════════
        ctk.CTkLabel(
            self, text="  W O R K S P A C E",
            font=FONT_NAV_LABEL,
            text_color=("gray55", "#52525B"),
        ).pack(anchor="w", padx=20, pady=(0, 8))

        # ═══════════════════════════════════════
        # MENU ITEMS
        # ═══════════════════════════════════════
        menu_frame = ctk.CTkFrame(self, fg_color="transparent")
        menu_frame.pack(fill="both", expand=True, padx=10, pady=0)

        for item in MENU_ITEMS:
            # Row container
            row = ctk.CTkFrame(menu_frame, fg_color="transparent", height=44)
            row.pack(fill="x", pady=2)
            row.pack_propagate(False)

            # Left accent indicator (3px bar)
            indicator = ctk.CTkFrame(
                row, width=3, height=24,
                corner_radius=2, fg_color="transparent",
            )
            indicator.place(x=0, rely=0.5, anchor="w")
            self._indicators[item["id"]] = indicator

            # Menu button
            btn = ctk.CTkButton(
                row,
                text=f"  {item['icon']}   {item['label']}",
                font=FONT_NAV_ITEM,
                anchor="w",
                height=40,
                corner_radius=12,
                fg_color="transparent",
                text_color=("gray35", "#A1A1AA"),
                hover_color=("gray92", "#141418"),
                command=lambda mid=item["id"]: self._handle_click(mid),
            )
            btn.pack(fill="x", padx=(8, 6), expand=True)
            self.buttons[item["id"]] = btn

        # ═══════════════════════════════════════
        # BOTTOM UTILITY CARD
        # ═══════════════════════════════════════
        # Divider above bottom
        ctk.CTkFrame(
            self, height=1,
            fg_color=("gray88", "#1F1F23"),
        ).pack(fill="x", side="bottom", padx=20, pady=(0, 12))

        # Utility card
        util_card = ctk.CTkFrame(
            self,
            fg_color=("gray95", "#0B0B0F"),
            corner_radius=12,
            border_width=1,
            border_color=("gray88", "#27272A"),
        )
        util_card.pack(fill="x", side="bottom", padx=14, pady=(0, 18))

        util_inner = ctk.CTkFrame(util_card, fg_color="transparent")
        util_inner.pack(fill="x", padx=14, pady=12)

        # Status row
        status_row = ctk.CTkFrame(util_inner, fg_color="transparent")
        status_row.pack(fill="x", pady=(0, 8))

        ctk.CTkLabel(
            status_row, text="●",
            font=("Segoe UI", 8),
            text_color=("#059669", "#22C55E"),
        ).pack(side="left", padx=(0, 6))

        ctk.CTkLabel(
            status_row, text="Ready",
            font=("Segoe UI", 11, "bold"),
            text_color=("gray30", "#A1A1AA"),
        ).pack(side="left")

        ctk.CTkLabel(
            status_row, text="v1.0",
            font=("Segoe UI", 9),
            text_color=("gray55", "#52525B"),
        ).pack(side="right")

        # Theme toggle row
        theme_row = ctk.CTkFrame(util_inner, fg_color="transparent")
        theme_row.pack(fill="x")

        self.theme_label = ctk.CTkLabel(
            theme_row, text="Dark Mode",
            font=("Segoe UI", 11),
            text_color=("gray40", "#A1A1AA"),
        )
        self.theme_label.pack(side="left")

        self.theme_switch = ctk.CTkSwitch(
            theme_row, text="", width=40,
            command=self._toggle_theme,
            onvalue=1, offvalue=0,
            progress_color=("#7C3AED", "#8B5CF6"),
            button_color=("#FFFFFF", "#FAFAFA"),
            button_hover_color=("#F3F4F6", "#E4E4E7"),
        )
        self.theme_switch.pack(side="right")
        self.theme_switch.select()

    # ─── Handlers ───

    def _handle_click(self, menu_id):
        """Handle menu click."""
        self.set_active(menu_id)
        self.on_menu_click(menu_id)

    def set_active(self, menu_id):
        """Set active menu with violet indicator + highlight."""
        # Reset all
        for mid, btn in self.buttons.items():
            btn.configure(
                fg_color="transparent",
                text_color=("gray35", "#A1A1AA"),
            )
            if mid in self._indicators:
                self._indicators[mid].configure(fg_color="transparent")

        # Activate
        if menu_id and menu_id in self.buttons:
            self.buttons[menu_id].configure(
                fg_color=("gray92", "#14101F"),
                text_color=("gray10", "#FAFAFA"),
            )
            if menu_id in self._indicators:
                self._indicators[menu_id].configure(
                    fg_color=("#7C3AED", "#8B5CF6")
                )
            self.active_id = menu_id
        else:
            self.active_id = None

    def _toggle_theme(self):
        """Toggle dark/light."""
        if self.theme_switch.get() == 1:
            self.theme_label.configure(text="Dark Mode")
            self.on_theme_toggle("dark")
        else:
            self.theme_label.configure(text="Light Mode")
            self.on_theme_toggle("light")
