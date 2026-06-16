# =============================================================================
# APP.PY — FIATRIX Main Application Window
# =============================================================================
# FIATRIX — Linear Algebra Workspace
# Premium desktop application for linear algebra computation.
# =============================================================================

import os
import tkinter as tk
import customtkinter as ctk
from config import (
    WINDOW_DEFAULT, WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT,
    FONT_HEADING, FONT_BODY, FONT_SMALL, MENU_ITEMS, SIDEBAR_WIDTH,
    APP_NAME, APP_SUBTITLE,
)
from components.sidebar import SidebarFrame
from components.status_bar import StatusBar
from components.tooltip import Tooltip
from pages import (
    SPLPage, DeterminanPage, InversPage,
    LUPage, EigenPage, DiagonalPage, SVDPage
)
from pages.dashboard_page import DashboardPage
from components.toast import ToastManager


# Set default appearance
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

# Mapping menu_id → Page class
PAGE_CLASSES = {
    "spl": SPLPage,
    "determinan": DeterminanPage,
    "invers": InversPage,
    "lu": LUPage,
    "eigen": EigenPage,
    "diagonal": DiagonalPage,
    "svd": SVDPage,
}

# Mapping menu_id → display name (untuk status bar)
PAGE_NAMES = {item["id"]: item["label"] for item in MENU_ITEMS}


class ModernAlinApp(ctk.CTk):
    """
    FIATRIX — Linear Algebra Workspace
    Main application window with premium dashboard and feature pages.
    """

    def __init__(self):
        super().__init__()

        # ─── Window Config ───
        self.title(f"{APP_NAME} — {APP_SUBTITLE}")
        self.geometry(WINDOW_DEFAULT)
        self.minsize(WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT)
        self._setup_app_icon()

        # ─── State ───
        self.pages = {}
        self.current_page = None
        self.current_page_id = None
        self._sidebar_collapsed = False

        # ─── Layout Grid ───
        self.grid_columnconfigure(0, weight=0)  # Sidebar fixed
        self.grid_columnconfigure(1, weight=1)  # Content expandable
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)     # Status bar

        # ─── Build ───
        self._build_sidebar()
        self._build_content_area()
        self._build_status_bar()
        self._build_pages()
        self._build_dashboard()
        self._show_dashboard()
        self._setup_shortcuts()
        self._setup_responsive()
        
        # Toast global notification layer
        self.toast_manager = ToastManager(self)

    def show_toast(self, message=None, toast_type="error", title=None, description=None, duration=None):
        if not hasattr(self, "toast_manager"):
            return None

        return self.toast_manager.show(
            message=message,
            toast_type=toast_type,
            title=title,
            description=description,
            duration=duration,
        )

    def _setup_app_icon(self):
        """Pasang logo aplikasi tanpa mengganggu startup jika asset belum tersedia."""
        try:
            icon_path = os.path.join("assets", "fiatrix-icon.ico")
            if os.path.exists(icon_path):
                self.iconbitmap(icon_path)
                return
        except Exception:
            pass

        try:
            png_path = os.path.join("assets", "fiatrix-logo.png")
            if os.path.exists(png_path):
                icon = tk.PhotoImage(file=png_path)
                self.iconphoto(True, icon)
                self._app_icon_ref = icon
        except Exception:
            pass

    # ─────────────────────────────────────────────
    # BUILD
    # ─────────────────────────────────────────────

    def _build_sidebar(self):
        """Build sidebar navigation."""
        self.sidebar = SidebarFrame(
            self,
            on_menu_click=self._on_menu_click,
            on_theme_toggle=self._on_theme_toggle,
        )
        self.sidebar.grid(row=0, column=0, rowspan=2, sticky="nsew")

    def _build_content_area(self):
        """Build content container."""
        self.content_container = ctk.CTkFrame(
            self,
            corner_radius=0,
            fg_color=("gray97", "#030303"),
        )
        self.content_container.grid(row=0, column=1, padx=0, pady=0, sticky="nsew")
        self.content_container.grid_columnconfigure(0, weight=1)
        self.content_container.grid_rowconfigure(0, weight=1)

    def _build_status_bar(self):
        """Build status bar at the bottom."""
        self.status_bar = StatusBar(self)
        self.status_bar.grid(row=1, column=1, padx=0, pady=0, sticky="ew")

    def _build_pages(self):
        """Build all feature page frames."""
        for item in MENU_ITEMS:
            page_id = item["id"]
            if page_id in PAGE_CLASSES:
                page = PAGE_CLASSES[page_id](self.content_container)
            else:
                page = self._create_placeholder_page(page_id, item["label"], item["icon"])
            self.pages[page_id] = page

    def _build_dashboard(self):
        """Build the premium FIATRIX dashboard page."""
        self.dashboard = DashboardPage(
            self.content_container,
            on_navigate=self._dashboard_navigate,
        )

    def _create_placeholder_page(self, page_id, label, icon):
        """Fallback placeholder for missing pages."""
        frame = ctk.CTkFrame(self.content_container, fg_color="transparent")
        header = ctk.CTkFrame(frame, fg_color="transparent")
        header.pack(fill="x", padx=30, pady=(25, 15))
        ctk.CTkLabel(header, text=f"{icon}  {label}", font=FONT_HEADING, anchor="w").pack(side="left")
        ctk.CTkFrame(frame, height=1, fg_color=("gray75", "gray30")).pack(fill="x", padx=30, pady=(0, 20))
        ctk.CTkLabel(frame, text=f"Halaman {label}\n\nSegera hadir.",
                     font=FONT_BODY, text_color=("gray50", "gray60"), justify="center").pack(expand=True)
        return frame

    # ─────────────────────────────────────────────
    # DASHBOARD
    # ─────────────────────────────────────────────

    def _show_dashboard(self):
        """Show the FIATRIX dashboard."""
        self.dashboard.grid(row=0, column=0, sticky="nsew")
        self.status_bar.set_page("Dashboard")

    def _dashboard_navigate(self, page_id):
        """Handle navigation from dashboard cards/buttons."""
        self.sidebar.set_active(page_id)
        self._on_menu_click(page_id)

    # ─────────────────────────────────────────────
    # NAVIGATION
    # ─────────────────────────────────────────────

    def _on_menu_click(self, menu_id):
        """Switch page based on menu click."""
        # Hide dashboard
        if self.dashboard.winfo_ismapped():
            self.dashboard.grid_forget()

        # Hide current page
        if self.current_page and self.current_page.winfo_ismapped():
            self.current_page.grid_forget()

        # Show selected page
        if menu_id in self.pages:
            page = self.pages[menu_id]
            page.grid(row=0, column=0, sticky="nsew")
            self.current_page = page
            self.current_page_id = menu_id

            # Update status bar
            self.status_bar.set_page(PAGE_NAMES.get(menu_id, menu_id))

    def _on_theme_toggle(self, mode):
        """Handle theme switch."""
        ctk.set_appearance_mode("Dark" if mode == "dark" else "Light")
        self.status_bar.set_status(
            f"Tema: {'Dark' if mode == 'dark' else 'Light'} Mode", "info"
        )

    # ─────────────────────────────────────────────
    # KEYBOARD SHORTCUTS
    # ─────────────────────────────────────────────

    def _setup_shortcuts(self):
        """Setup all keyboard shortcuts."""
        # Ctrl+1 to Ctrl+7: menu navigation
        for i, item in enumerate(MENU_ITEMS):
            self.bind(
                f"<Control-Key-{i + 1}>",
                lambda e, mid=item["id"]: self._shortcut_nav(mid)
            )

        # Ctrl+L: Clear input on active page
        self.bind("<Control-l>", self._shortcut_clear)
        self.bind("<Control-L>", self._shortcut_clear)

        # Ctrl+Shift+C: Copy result to clipboard
        self.bind("<Control-Shift-C>", self._shortcut_copy)
        self.bind("<Control-Shift-c>", self._shortcut_copy)

        # Escape: back to dashboard
        self.bind("<Escape>", self._shortcut_home)

        # Ctrl+Enter: Calculate SPL on active page
        self.bind_all("<Control-Return>", self._shortcut_calculate, add="+")
        self.bind_all("<Control-KP_Enter>", self._shortcut_calculate, add="+")

    def _shortcut_nav(self, menu_id):
        """Navigate via keyboard shortcut."""
        self.sidebar.set_active(menu_id)
        self._on_menu_click(menu_id)

    def _shortcut_clear(self, event=None):
        """Clear input on active page."""
        if self.current_page and hasattr(self.current_page, 'matrix_input'):
            self.current_page.matrix_input._clear_all()
            self.status_bar.set_status("Input cleared", "info")
        if self.current_page and hasattr(self.current_page, 'matrix_a'):
            self.current_page.matrix_a._clear_all()
            if hasattr(self.current_page, 'matrix_b'):
                self.current_page.matrix_b._clear_all()
            self.status_bar.set_status("Input cleared", "info")

    def _shortcut_calculate(self, event=None):
        """Trigger calculation on the active page (SPL)."""
        try:
            if not self.current_page or not self.current_page.winfo_ismapped():
                return None
            
            # Check if calc_button is enabled
            if hasattr(self.current_page, 'calc_button') and hasattr(self.current_page, '_on_calculate'):
                if str(self.current_page.calc_button.cget("state")) != "disabled":
                    self.current_page._on_calculate()
                    return "break"
        except Exception:
            pass
        return None

    def _shortcut_copy(self, event=None):
        """Copy result from result console."""
        if self.current_page and hasattr(self.current_page, 'result_console'):
            content = self.current_page.result_console.get_content()
            if content:
                self.clipboard_clear()
                self.clipboard_append(content)
                self.status_bar.set_status("✓ Hasil disalin ke clipboard", "success")

    def _shortcut_home(self, event=None):
        """Return to dashboard."""
        if self.current_page and self.current_page.winfo_ismapped():
            self.current_page.grid_forget()
        self.current_page = None
        self.current_page_id = None
        self.sidebar.set_active(None)

        if not self.dashboard.winfo_ismapped():
            self._show_dashboard()

    # ─────────────────────────────────────────────
    # RESPONSIVE SIDEBAR
    # ─────────────────────────────────────────────

    def _setup_responsive(self):
        """Setup responsive behavior — sidebar collapse on small window."""
        self.bind("<Configure>", self._on_resize)
        self._last_width = self.winfo_width()

    def _on_resize(self, event):
        """Handle window resize — collapse/expand sidebar."""
        if event.widget != self:
            return

        width = event.width

        if abs(width - self._last_width) < 50:
            return
        self._last_width = width

        if width < 1000 and not self._sidebar_collapsed:
            self._collapse_sidebar()
        elif width >= 1000 and self._sidebar_collapsed:
            self._expand_sidebar()

    def _collapse_sidebar(self):
        """Collapse sidebar to icon-only mode."""
        self._sidebar_collapsed = True
        self.sidebar.configure(width=60)
        for menu_id, btn in self.sidebar.buttons.items():
            item = next((i for i in MENU_ITEMS if i["id"] == menu_id), None)
            if item:
                btn.configure(text=f" {item['icon']} ")

    def _expand_sidebar(self):
        """Expand sidebar to full mode."""
        self._sidebar_collapsed = False
        self.sidebar.configure(width=SIDEBAR_WIDTH)
        for menu_id, btn in self.sidebar.buttons.items():
            item = next((i for i in MENU_ITEMS if i["id"] == menu_id), None)
            if item:
                btn.configure(text=f"  {item['icon']}  {item['label']}")
