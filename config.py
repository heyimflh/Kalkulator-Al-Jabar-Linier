# =============================================================================
# CONFIG.PY — Konstanta warna, font, dan konfigurasi aplikasi
# =============================================================================

# ─────────────────────────────────────────────
# DARK THEME — "Deep Space"
# ─────────────────────────────────────────────
DARK = {
    "bg_main": "#1A1A2E",
    "bg_sidebar": "#16213E",
    "bg_card": "#0F3460",
    "bg_input": "#1E2A3A",
    "accent_primary": "#E94560",
    "accent_secondary": "#533483",
    "accent_success": "#2D8A4E",
    "accent_error": "#E74C3C",
    "text_primary": "#ECF0F1",
    "text_secondary": "#95A5A6",
    "border_focus": "#3498DB",
    "border_default": "#2C3E50",
    "hover_bg": "#1F3A5F",
    "active_indicator": "#E94560",
}

# ─────────────────────────────────────────────
# LIGHT THEME — "Clean Slate"
# ─────────────────────────────────────────────
LIGHT = {
    "bg_main": "#F8F9FA",
    "bg_sidebar": "#FFFFFF",
    "bg_card": "#FFFFFF",
    "bg_input": "#F1F3F5",
    "accent_primary": "#2563EB",
    "accent_secondary": "#7C3AED",
    "accent_success": "#059669",
    "accent_error": "#DC2626",
    "text_primary": "#1F2937",
    "text_secondary": "#6B7280",
    "border_focus": "#2563EB",
    "border_default": "#E5E7EB",
    "hover_bg": "#EEF2FF",
    "active_indicator": "#2563EB",
}

# ─────────────────────────────────────────────
# FONTS (System fonts dengan fallback)
# ─────────────────────────────────────────────
FONT_LOGO = ("Segoe UI", 22, "bold")
FONT_HEADING = ("Segoe UI", 18, "bold")
FONT_SUBHEADING = ("Segoe UI", 14, "bold")
FONT_BODY = ("Segoe UI", 13)
FONT_BUTTON = ("Segoe UI", 13, "bold")
FONT_MATRIX_CELL = ("Consolas", 14)
FONT_CONSOLE = ("Consolas", 12)
FONT_SMALL = ("Segoe UI", 11)

# ─────────────────────────────────────────────
# LAYOUT
# ─────────────────────────────────────────────
SIDEBAR_WIDTH = 220
WINDOW_MIN_WIDTH = 900
WINDOW_MIN_HEIGHT = 600
WINDOW_DEFAULT = "1200x750"
MATRIX_CELL_WIDTH = 60
MATRIX_CELL_HEIGHT = 35
MAX_MATRIX_DIM = 10

# ─────────────────────────────────────────────
# MENU ITEMS
# ─────────────────────────────────────────────
MENU_ITEMS = [
    {"id": "spl", "label": "SPL", "icon": "⊞"},
    {"id": "determinan", "label": "Determinan", "icon": "⊡"},
    {"id": "invers", "label": "Invers", "icon": "⊟"},
    {"id": "lu", "label": "Dekomposisi LU", "icon": "△"},
    {"id": "eigen", "label": "Eigen", "icon": "λ"},
    {"id": "diagonal", "label": "Diagonalisasi", "icon": "⋱"},
    {"id": "svd", "label": "SVD", "icon": "Σ"},
]
