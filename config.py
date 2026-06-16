# =============================================================================
# CONFIG.PY — FIATRIX Theme, Font, and Layout Configuration
# =============================================================================
# FIATRIX — Linear Algebra Workspace
# Darkmatter Neon aesthetic: ultra-dark, violet primary, cyan secondary.
# =============================================================================

# ─────────────────────────────────────────────
# DARK THEME — "Darkmatter"
# ─────────────────────────────────────────────
DARK = {
    "bg_main": "#030303",
    "bg_sidebar": "#070707",
    "bg_card": "#0B0B0F",
    "bg_card_glass": "#111118",
    "bg_input": "#111118",
    "accent_primary": "#8B5CF6",
    "accent_secondary": "#06B6D4",
    "accent_success": "#22C55E",
    "accent_warning": "#F59E0B",
    "accent_error": "#F43F5E",
    "text_primary": "#FAFAFA",
    "text_secondary": "#A1A1AA",
    "text_muted": "#71717A",
    "border_focus": "#A78BFA",
    "border_default": "#27272A",
    "hover_bg": "#18181F",
    "active_indicator": "#8B5CF6",
}

# ─────────────────────────────────────────────
# LIGHT THEME — "Clean Slate" (preserved)
# ─────────────────────────────────────────────
LIGHT = {
    "bg_main": "#F8F9FA",
    "bg_sidebar": "#FFFFFF",
    "bg_card": "#FFFFFF",
    "bg_card_glass": "#F1F5F9",
    "bg_input": "#F1F3F5",
    "accent_primary": "#7C3AED",
    "accent_secondary": "#0891B2",
    "accent_success": "#059669",
    "accent_warning": "#D97706",
    "accent_error": "#DC2626",
    "text_primary": "#1F2937",
    "text_secondary": "#6B7280",
    "text_muted": "#9CA3AF",
    "border_focus": "#7C3AED",
    "border_default": "#E5E7EB",
    "hover_bg": "#F5F3FF",
    "active_indicator": "#7C3AED",
}

# ─────────────────────────────────────────────
# DASHBOARD THEME — Darkmatter Neon
# ─────────────────────────────────────────────
DASHBOARD_DARK = {
    "bg": "#030303",
    "hero_bg": "#0B0B0F",
    "hero_border": "#27272A",
    "card_bg": "#0A0A0F",
    "card_border": "#27272A",
    "card_hover": "#18181F",
    "stat_bg": "#070707",
    "accent_violet": "#8B5CF6",
    "accent_cyan": "#06B6D4",
    "accent_green": "#22C55E",
    "accent_amber": "#F59E0B",
    "accent_rose": "#F43F5E",
    "text_white": "#FAFAFA",
    "text_gray": "#A1A1AA",
    "text_muted": "#71717A",
    "border": "#27272A",
    "border_hover": "#8B5CF6",
    "glow_violet": "#7C3AED",
    "glow_cyan": "#0891B2",
}

DASHBOARD_LIGHT = {
    "bg": "#FAFAFA",
    "hero_bg": "#FFFFFF",
    "hero_border": "#E5E7EB",
    "card_bg": "#FFFFFF",
    "card_border": "#E5E7EB",
    "card_hover": "#F5F3FF",
    "stat_bg": "#F9FAFB",
    "accent_violet": "#7C3AED",
    "accent_cyan": "#0891B2",
    "accent_green": "#059669",
    "accent_amber": "#D97706",
    "accent_rose": "#DC2626",
    "text_white": "#1F2937",
    "text_gray": "#6B7280",
    "text_muted": "#9CA3AF",
    "border": "#E5E7EB",
    "border_hover": "#7C3AED",
    "glow_violet": "#7C3AED",
    "glow_cyan": "#0891B2",
}

# ─────────────────────────────────────────────
# DASHBOARD THEME — DOOM 64 (tweakcn)
# Source: https://tweakcn.com/editor/theme?theme=doom-64
# Aesthetic: Gothic / brutalist 90s shooter — sharp corners,
# blood red primary, toxic green secondary, sky blue accent,
# amber destructive, deep charcoal blacks.
# ─────────────────────────────────────────────
DASHBOARD_DOOM64 = {
    # Surfaces
    "bg":            "#1a1a1a",   # background
    "panel":         "#2a2a2a",   # card / popover
    "deep":          "#141414",   # sidebar / deepest
    "muted":         "#252525",   # muted surface
    "input":         "#4a4a4a",   # input / chip bg
    # Text
    "fg":            "#e0e0e0",   # foreground
    "fg_muted":      "#a0a0a0",   # muted-foreground
    "fg_dim":        "#6e6e6e",   # extra dim / inactive
    "fg_on_red":     "#ffffff",   # primary-foreground
    "fg_on_green":   "#000000",   # secondary-foreground
    "fg_on_blue":    "#000000",   # accent-foreground
    "fg_on_amber":   "#000000",   # destructive-foreground
    # Brand colors (chart palette of doom-64)
    "red":           "#e53935",   # primary — blood red
    "red_hover":     "#c62828",
    "green":         "#689f38",   # secondary — toxic green
    "green_hover":   "#558b2f",
    "blue":          "#64b5f6",   # accent — sky blue
    "blue_hover":    "#42a5f5",
    "amber":         "#ffa000",   # destructive — amber
    "amber_hover":   "#ff8f00",
    "earth":         "#a1887f",   # chart-5 — earth / dust
    # Lines
    "border":        "#4a4a4a",
    "border_strong": "#5a5a5a",
}

# Doom 64 font stack (CTk uses single family — pages do runtime
# fallback detection via tkinter.font.families()).
DOOM64_FONT_SANS_CHAIN = ("Oxanium", "Bahnschrift", "Eurostile", "Segoe UI")
DOOM64_FONT_MONO_CHAIN = ("Source Code Pro", "JetBrains Mono", "Cascadia Mono", "Consolas")
DOOM64_RADIUS = 0   # brutalist sharp corners

# ─────────────────────────────────────────────
# DASHBOARD THEME — COSMIC NIGHT (tweakcn)
# Source: https://tweakcn.com/editor/theme?theme=cosmic-night
# Aesthetic: deep midnight-violet surfaces, soft rounded cards,
# luminous lavender primary, cool indigo/blue/teal/pink chart accents.
# Converted from the theme's OKLCH dark-mode tokens to hex.
# ─────────────────────────────────────────────
DASHBOARD_COSMIC = {
    # Surfaces
    "bg":            "#0F0F1A",   # background — deep cosmic midnight
    "panel":         "#1A1A2E",   # card / popover / sidebar
    "deep":          "#13131F",   # deepest inset (terminal, formula well)
    "muted":         "#222244",   # muted surface
    "secondary":     "#2D2B55",   # secondary surface
    "accent":        "#303060",   # accent surface / hover
    "input":         "#303052",   # input / chip bg
    # Text
    "fg":            "#E2E2F5",   # foreground
    "fg_muted":      "#A0A0C0",   # muted-foreground
    "fg_dim":        "#7E7EA8",   # extra dim / inactive
    "fg_secondary":  "#C4C2FF",   # secondary-foreground (lavender)
    "fg_on_primary": "#0F0F1A",   # text on violet primary
    "fg_on_rose":    "#FFFFFF",   # destructive-foreground
    # Brand colors (chart palette of cosmic-night)
    "violet":        "#A48FFF",   # primary — luminous lavender
    "violet_hover":  "#B8A8FF",
    "violet_dim":    "#8B72F0",
    "indigo":        "#7986CB",   # chart-2
    "indigo_hover":  "#8C98D6",
    "blue":          "#64B5F6",   # chart-3 — sky blue
    "blue_hover":    "#7FC2F8",
    "teal":          "#4DB6AC",   # chart-4
    "teal_hover":    "#63C2B9",
    "pink":          "#FF79C6",   # chart-5
    "pink_hover":    "#FF93D2",
    "rose":          "#FF5470",   # destructive
    "rose_hover":    "#FF6E85",
    # Lines
    "border":        "#303052",
    "border_strong": "#3D3D66",
    "border_glow":   "#A48FFF",   # focus / hover glow (primary)
}

# Cosmic Night font stack — Inter sans + JetBrains Mono.
# Pages do runtime fallback detection via tkinter.font.families().
COSMIC_FONT_SANS_CHAIN = ("Inter", "Segoe UI", "Arial")
COSMIC_FONT_MONO_CHAIN = ("JetBrains Mono", "Consolas", "Courier New")
COSMIC_RADIUS = 12   # soft rounded corners (radius 0.5rem ≈ 8–12px)

# ─────────────────────────────────────────────
# BRANDING
# ─────────────────────────────────────────────
APP_NAME = "FIATRIX"
APP_SUBTITLE = "Linear Algebra Workspace"
APP_VERSION = "v1.0"
APP_DESCRIPTION = "Matrix computation, equation solving, eigen analysis, and SVD."

# ─────────────────────────────────────────────
# TYPOGRAPHY SCALE
# Optimized for readability on desktop displays.
# Primary: Segoe UI Variable / Segoe UI (Windows)
# Mono: Cascadia Mono / Consolas (Windows)
# ─────────────────────────────────────────────
_UI = "Segoe UI"
_MONO = "Cascadia Mono"

FONT_LOGO = (_UI, 22, "bold")
FONT_HEADING = (_UI, 18, "bold")
FONT_SUBHEADING = (_UI, 14, "bold")
FONT_BODY = (_UI, 13)
FONT_BUTTON = (_UI, 13, "bold")
FONT_MATRIX_CELL = ("Consolas", 14)
FONT_CONSOLE = ("Consolas", 12)
FONT_SMALL = (_UI, 11)

# Dashboard-specific typography
FONT_HERO_TITLE = (_UI, 36, "bold")
FONT_SECTION_TITLE = (_UI, 20, "bold")
FONT_CARD_TITLE = (_UI, 16, "bold")
FONT_CARD_BODY = (_UI, 12)
FONT_BADGE = (_UI, 10, "bold")
FONT_MONO_FORMULA = (_MONO, 14, "bold")
FONT_MONO_SMALL = (_MONO, 11)
FONT_NAV_ITEM = (_UI, 13, "bold")
FONT_NAV_LABEL = (_UI, 9, "bold")
FONT_STATUS = (_UI, 11)

# ─────────────────────────────────────────────
# LAYOUT
# ─────────────────────────────────────────────
SIDEBAR_WIDTH = 230
WINDOW_MIN_WIDTH = 900
WINDOW_MIN_HEIGHT = 600
WINDOW_DEFAULT = "1320x820"
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
