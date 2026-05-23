# =============================================================================
# APP.PY — Main Application Window (Fase 5: Polish & UX)
# =============================================================================

import customtkinter as ctk
from config import (
    WINDOW_DEFAULT, WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT,
    FONT_HEADING, FONT_BODY, FONT_SMALL, MENU_ITEMS, SIDEBAR_WIDTH
)
from components.sidebar import SidebarFrame
from components.status_bar import StatusBar
from components.tooltip import Tooltip
from pages import (
    SPLPage, DeterminanPage, InversPage,
    LUPage, EigenPage, DiagonalPage, SVDPage
)


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
    Main application — Single-Window Dashboard.
    Fase 5: Responsive sidebar, status bar, enhanced shortcuts, polish.
    """

    def __init__(self):
        super().__init__()

        # ─── Window Config ───
        self.title("Linear Algebra Dashboard Pro")
        self.geometry(WINDOW_DEFAULT)
        self.minsize(WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT)

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
        self._show_welcome()
        self._setup_shortcuts()
        self._setup_responsive()

    # ─────────────────────────────────────────────
    # BUILD
    # ─────────────────────────────────────────────

    def _build_sidebar(self):
        """Buat sidebar navigation."""
        self.sidebar = SidebarFrame(
            self,
            on_menu_click=self._on_menu_click,
            on_theme_toggle=self._on_theme_toggle,
        )
        self.sidebar.grid(row=0, column=0, rowspan=2, sticky="nsew")

    def _build_content_area(self):
        """Buat container content area."""
        self.content_container = ctk.CTkFrame(self, corner_radius=15)
        self.content_container.grid(row=0, column=1, padx=(0, 15), pady=(15, 5), sticky="nsew")
        self.content_container.grid_columnconfigure(0, weight=1)
        self.content_container.grid_rowconfigure(0, weight=1)

    def _build_status_bar(self):
        """Buat status bar di bawah."""
        self.status_bar = StatusBar(self)
        self.status_bar.grid(row=1, column=1, padx=(0, 15), pady=(0, 5), sticky="ew")

    def _build_pages(self):
        """Buat semua page frames."""
        for item in MENU_ITEMS:
            page_id = item["id"]
            if page_id in PAGE_CLASSES:
                page = PAGE_CLASSES[page_id](self.content_container)
            else:
                page = self._create_placeholder_page(page_id, item["label"], item["icon"])
            self.pages[page_id] = page

    def _create_placeholder_page(self, page_id, label, icon):
        """Fallback placeholder."""
        frame = ctk.CTkFrame(self.content_container, fg_color="transparent")
        header = ctk.CTkFrame(frame, fg_color="transparent")
        header.pack(fill="x", padx=30, pady=(25, 15))
        ctk.CTkLabel(header, text=f"{icon}  {label}", font=FONT_HEADING, anchor="w").pack(side="left")
        ctk.CTkFrame(frame, height=1, fg_color=("gray75", "gray30")).pack(fill="x", padx=30, pady=(0, 20))
        ctk.CTkLabel(frame, text=f"Halaman {label}\n\nSegera hadir.",
                     font=FONT_BODY, text_color=("gray50", "gray60"), justify="center").pack(expand=True)
        return frame

    # ─────────────────────────────────────────────
    # WELCOME PAGE
    # ─────────────────────────────────────────────

    def _show_welcome(self):
        """Tampilkan welcome/dashboard page."""
        self.welcome_frame = ctk.CTkFrame(self.content_container, fg_color="transparent")
        self.welcome_frame.grid(row=0, column=0, sticky="nsew")

        # Center content
        center = ctk.CTkFrame(self.welcome_frame, fg_color="transparent")
        center.place(relx=0.5, rely=0.38, anchor="center")

        ctk.CTkLabel(center, text="⊞", font=("Segoe UI", 64)).pack()
        ctk.CTkLabel(center, text="Linear Algebra Dashboard",
                     font=("Segoe UI", 28, "bold")).pack(pady=(10, 5))
        ctk.CTkLabel(center, text="Pilih menu di sidebar untuk memulai perhitungan",
                     font=FONT_BODY, text_color=("gray50", "gray60")).pack()

        # Feature cards
        cards = ctk.CTkFrame(self.welcome_frame, fg_color="transparent")
        cards.place(relx=0.5, rely=0.65, anchor="center")

        features = [
            ("7 Fitur", "SPL, Det, Invers,\nLU, Eigen, Diag, SVD"),
            ("Step-by-Step", "Lihat proses\nperhitungan detail"),
            ("Dark / Light", "Tema yang nyaman\ndi mata"),
        ]

        for i, (title, desc) in enumerate(features):
            card = ctk.CTkFrame(cards, corner_radius=12, width=180, height=100)
            card.grid(row=0, column=i, padx=10, pady=10)
            card.grid_propagate(False)
            ctk.CTkLabel(card, text=title, font=("Segoe UI", 14, "bold")).pack(pady=(18, 3))
            ctk.CTkLabel(card, text=desc, font=FONT_SMALL, text_color=("gray50", "gray60")).pack()

        # Shortcut hints di bawah cards
        hints = ctk.CTkFrame(self.welcome_frame, fg_color="transparent")
        hints.place(relx=0.5, rely=0.88, anchor="center")
        ctk.CTkLabel(
            hints,
            text="💡 Tips: Gunakan Ctrl+1~7 untuk navigasi cepat, Ctrl+Enter untuk hitung",
            font=("Segoe UI", 11),
            text_color=("gray50", "gray55"),
        ).pack()

    # ─────────────────────────────────────────────
    # NAVIGATION
    # ─────────────────────────────────────────────

    def _on_menu_click(self, menu_id):
        """Switch halaman berdasarkan menu yang diklik."""
        # Hide welcome
        if hasattr(self, "welcome_frame") and self.welcome_frame.winfo_ismapped():
            self.welcome_frame.grid_forget()

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
    # KEYBOARD SHORTCUTS (Enhanced)
    # ─────────────────────────────────────────────

    def _setup_shortcuts(self):
        """Setup semua keyboard shortcuts."""
        # Ctrl+1 s/d Ctrl+7: navigasi menu
        for i, item in enumerate(MENU_ITEMS):
            self.bind(
                f"<Control-Key-{i + 1}>",
                lambda e, mid=item["id"]: self._shortcut_nav(mid)
            )

        # Ctrl+L: Clear input pada halaman aktif
        self.bind("<Control-l>", self._shortcut_clear)
        self.bind("<Control-L>", self._shortcut_clear)

        # Ctrl+Shift+C: Copy hasil ke clipboard
        self.bind("<Control-Shift-C>", self._shortcut_copy)
        self.bind("<Control-Shift-c>", self._shortcut_copy)

        # Escape: kembali ke welcome
        self.bind("<Escape>", self._shortcut_home)

    def _shortcut_nav(self, menu_id):
        """Navigate via keyboard shortcut."""
        self.sidebar.set_active(menu_id)
        self._on_menu_click(menu_id)

    def _shortcut_clear(self, event=None):
        """Clear input pada halaman aktif."""
        if self.current_page and hasattr(self.current_page, 'matrix_input'):
            self.current_page.matrix_input._clear_all()
            self.status_bar.set_status("Input cleared", "info")
        # Juga clear untuk SPL page yang punya matrix_a
        if self.current_page and hasattr(self.current_page, 'matrix_a'):
            self.current_page.matrix_a._clear_all()
            if hasattr(self.current_page, 'matrix_b'):
                self.current_page.matrix_b._clear_all()
            self.status_bar.set_status("Input cleared", "info")

    def _shortcut_copy(self, event=None):
        """Copy hasil dari result console."""
        if self.current_page and hasattr(self.current_page, 'result_console'):
            content = self.current_page.result_console.get_content()
            if content:
                self.clipboard_clear()
                self.clipboard_append(content)
                self.status_bar.set_status("✓ Hasil disalin ke clipboard", "success")

    def _shortcut_home(self, event=None):
        """Kembali ke welcome page."""
        if self.current_page and self.current_page.winfo_ismapped():
            self.current_page.grid_forget()
        self.current_page = None
        self.current_page_id = None
        self.sidebar.set_active(None)

        if hasattr(self, "welcome_frame"):
            self.welcome_frame.grid(row=0, column=0, sticky="nsew")
        self.status_bar.set_page("Dashboard")

    # ─────────────────────────────────────────────
    # RESPONSIVE SIDEBAR
    # ─────────────────────────────────────────────

    def _setup_responsive(self):
        """Setup responsive behavior — sidebar collapse pada window kecil."""
        self.bind("<Configure>", self._on_resize)
        self._last_width = self.winfo_width()

    def _on_resize(self, event):
        """Handle window resize — collapse/expand sidebar."""
        # Only respond to root window resize events
        if event.widget != self:
            return

        width = event.width

        # Debounce: hanya proses jika perubahan signifikan
        if abs(width - self._last_width) < 50:
            return
        self._last_width = width

        # Collapse sidebar jika window < 1000px
        if width < 1000 and not self._sidebar_collapsed:
            self._collapse_sidebar()
        elif width >= 1000 and self._sidebar_collapsed:
            self._expand_sidebar()

    def _collapse_sidebar(self):
        """Collapse sidebar ke icon-only mode."""
        self._sidebar_collapsed = True
        self.sidebar.configure(width=60)
        # Hide text labels, show only icons
        for menu_id, btn in self.sidebar.buttons.items():
            item = next((i for i in MENU_ITEMS if i["id"] == menu_id), None)
            if item:
                btn.configure(text=f" {item['icon']} ")

        # Hide subtitle and theme label
        if hasattr(self.sidebar, 'subtitle_label'):
            pass  # Will be handled by sidebar internal state

    def _expand_sidebar(self):
        """Expand sidebar ke full mode."""
        self._sidebar_collapsed = False
        self.sidebar.configure(width=SIDEBAR_WIDTH)
        # Restore full text
        for menu_id, btn in self.sidebar.buttons.items():
            item = next((i for i in MENU_ITEMS if i["id"] == menu_id), None)
            if item:
                btn.configure(text=f"  {item['icon']}  {item['label']}")
