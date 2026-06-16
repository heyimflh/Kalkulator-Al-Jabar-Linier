# =============================================================================
# DASHBOARD_PAGE.PY — FIATRIX × COSMIC NIGHT Dashboard
# =============================================================================
# Dark theme inspired by tweakcn "Cosmic Night":
#   https://tweakcn.com/editor/theme?theme=cosmic-night
#
# Aesthetic notes (deep slate/purple, soft & luminous):
#   - Soft rounded corners — cards radius 16, buttons/badges radius 8.
#   - Slate-purple surfaces (#1E1E2F card / #2E2E44 border).
#   - Soft violet primary (#A78BFA) with cyan highlight (#22D3EE).
#   - High-contrast text: white headers, slate-400 body copy.
#   - Display font: Inter (fallback Segoe UI / Arial).
#   - Mono font: JetBrains Mono (fallback Consolas / Courier New).
#
# IMPORTANT: This file only re-themes the Dashboard page. Other pages,
# the sidebar, and global config remain untouched.
# =============================================================================

import tkinter.font as tkfont
import customtkinter as ctk

from config import (
    COSMIC_FONT_SANS_CHAIN, COSMIC_FONT_MONO_CHAIN,
    APP_NAME, APP_VERSION,
)


# ─────────────────────────────────────────────
# FONT RESOLUTION
# Pick the first installed font from each chain at runtime.
# ─────────────────────────────────────────────
def _pick_font(chain):
    """Return first available font family from a fallback chain."""
    try:
        installed = {f.lower() for f in tkfont.families()}
        for fam in chain:
            if fam.lower() in installed:
                return fam
    except Exception:
        pass
    return chain[-1]  # last item is the safest fallback


_SANS = _pick_font(COSMIC_FONT_SANS_CHAIN)
_MONO = _pick_font(COSMIC_FONT_MONO_CHAIN)


# ─────────────────────────────────────────────
# Optional font debug. Disabled by default; flip DEBUG_FONTS to True
# (or call _debug_print_fonts() manually) to print the resolved dashboard
# fonts and whether Inter / JetBrains Mono were found.
# ─────────────────────────────────────────────
DEBUG_FONTS = False


def _debug_print_fonts():
    """Print the fonts the dashboard resolved and family availability."""
    try:
        installed = {f.lower() for f in tkfont.families()}
    except Exception as exc:
        print(f"[cosmic-fonts] could not read installed fonts: {exc}")
        return

    print("[cosmic-fonts] sans chain :", COSMIC_FONT_SANS_CHAIN)
    print("[cosmic-fonts] mono chain :", COSMIC_FONT_MONO_CHAIN)
    print("[cosmic-fonts] Inter installed?         ",
          "yes" if "inter" in installed else "no")
    print("[cosmic-fonts] JetBrains Mono installed?",
          "yes" if "jetbrains mono" in installed else "no")
    print(f"[cosmic-fonts] UI sans font  (in use): {_SANS}")
    print(f"[cosmic-fonts] mono/formula  (in use): {_MONO}")


# Cosmic Night typography scale — clean, airy, modern.
# NOTE: seeded at import time (before a Tk root exists, so these fall back to
# the chain tail). They are re-resolved by _resolve_fonts() inside
# DashboardPage.__init__ once a root window is available — only then can
# tkinter report installed families and pick Inter / JetBrains Mono.
F_HERO       = (_SANS, 38, "bold")
F_SECTION    = (_SANS, 19, "bold")
F_CARD_TITLE = (_SANS, 16, "bold")
F_CARD_BODY  = (_SANS, 12)
F_BUTTON     = (_SANS, 12, "bold")
F_BTN_LARGE  = (_SANS, 13, "bold")
F_OVERLINE   = (_SANS, 10, "bold")
F_BADGE      = (_SANS, 10, "bold")
F_META       = (_SANS, 11)
F_BREADCRUMB = (_SANS, 12, "bold")
F_HUGE       = (_SANS, 25, "bold")
F_FORMULA    = (_MONO, 14, "bold")
F_MONO_SM    = (_MONO, 11)
F_MONO_TINY  = (_MONO, 10)


def _resolve_fonts():
    """Re-resolve the Cosmic Night font chains and rebuild the type scale.

    Must be called after a Tk root window exists (e.g. from
    DashboardPage.__init__). Before a root exists, tkinter.font.families()
    raises and _pick_font() falls back to the chain tail; calling this once
    the root is live lets the dashboard actually select Inter / JetBrains
    Mono when they are installed.
    """
    global _SANS, _MONO
    global F_HERO, F_SECTION, F_CARD_TITLE, F_CARD_BODY, F_BUTTON, F_BTN_LARGE
    global F_OVERLINE, F_BADGE, F_META, F_BREADCRUMB, F_HUGE
    global F_FORMULA, F_MONO_SM, F_MONO_TINY

    _SANS = _pick_font(COSMIC_FONT_SANS_CHAIN)
    _MONO = _pick_font(COSMIC_FONT_MONO_CHAIN)

    F_HERO       = (_SANS, 38, "bold")
    F_SECTION    = (_SANS, 19, "bold")
    F_CARD_TITLE = (_SANS, 16, "bold")
    F_CARD_BODY  = (_SANS, 12)
    F_BUTTON     = (_SANS, 12, "bold")
    F_BTN_LARGE  = (_SANS, 13, "bold")
    F_OVERLINE   = (_SANS, 10, "bold")
    F_BADGE      = (_SANS, 10, "bold")
    F_META       = (_SANS, 11)
    F_BREADCRUMB = (_SANS, 12, "bold")
    F_HUGE       = (_SANS, 25, "bold")
    F_FORMULA    = (_MONO, 14, "bold")
    F_MONO_SM    = (_MONO, 11)
    F_MONO_TINY  = (_MONO, 10)

    return _SANS, _MONO


# ═════════════════════════════════════════════════════════════════════════════
# GLOBAL DESIGN TOKENS — DUAL THEME
#   Light = "Amethyst Haze"  (soft lavender-tinted academic light theme)
#   Dark  = "Cosmic Night"   (deep space dark with neon lavender highlights)
#
# Every token is a CustomTkinter (light_color, dark_color) tuple, so calling
# ctk.set_appearance_mode("Light"/"Dark") restyles the whole dashboard with no
# rebuild. This is the single source of truth — tweak here, restyle everywhere.
# ═════════════════════════════════════════════════════════════════════════════
#                          (  light  ,   dark   )
COLOR_MAIN_BG          = ("#F5F3FF", "#0B0B14")  # app / dashboard background
COLOR_CARD_BG          = ("#EFE9FE", "#1E1E2F")  # card / panel surface
COLOR_CARD_BORDER      = ("#DDBBFF", "#2E2E44")  # subtle border framing
COLOR_TEXT_PRIMARY     = ("#2E1065", "#FFFFFF")  # headers, titles, logo text
COLOR_TEXT_MUTED       = ("#5B21B6", "#94A3B8")  # descriptions, secondary labels
COLOR_ACCENT_PRIMARY   = ("#7C3AED", "#A78BFA")  # primary buttons / key accents
COLOR_ACCENT_HOVER     = ("#6D28D9", "#C084FC")  # primary button hover (stable)

# ── Derived / supporting tuples (kept consistent with the two palettes) ──
COLOR_ON_ACCENT        = ("#FFFFFF", "#1E1E2F")  # text on a filled accent button
COLOR_TEXT_DIM         = ("#7E6BA8", "#7E7EA8")  # faint hints, code comments
COLOR_INSET_BG         = ("#F3EEFD", "#13131F")  # code/formula inset surface
COLOR_ACCENT_SURFACE   = ("#E5DBFA", "#303060")  # icon-box / quick-button fill
COLOR_SECONDARY_BG     = ("#E5DBFA", "#2D2B55")  # chips / badges fill
COLOR_SECONDARY_TEXT   = ("#5B21B6", "#C4C2FF")  # chips / badges text
COLOR_GLOW_HOVER       = ("#E0D4FB", "#2E2A4D")  # outline / ghost button hover glow

# ── Per-feature accent colors (vivid in dark, deepened for light legibility) ──
ACC_VIOLET = COLOR_ACCENT_PRIMARY
ACC_CYAN   = ("#0891B2", "#22D3EE")
ACC_BLUE   = ("#2563EB", "#64B5F6")
ACC_TEAL   = ("#0D9488", "#4DB6AC")
ACC_PINK   = ("#DB2777", "#FF79C6")
ACC_INDIGO = ("#4F46E5", "#7986CB")
ACC_ROSE   = ("#E11D48", "#FF5470")

CORNER_RADIUS_CARD = 16      # all main frames / cards
CORNER_RADIUS_BTN  = 8       # all buttons / badges / small interactive elements

# Internal radius aliases (kept so existing call sites stay readable).
R_CARD  = CORNER_RADIUS_CARD
R_INNER = max(CORNER_RADIUS_CARD - 4, 8)
R_PILL  = CORNER_RADIUS_BTN
R_BTN   = CORNER_RADIUS_BTN


# ═════════════════════════════════════════════════════════════════════════════
# DASHBOARD PAGE
# ═════════════════════════════════════════════════════════════════════════════
class DashboardPage(ctk.CTkScrollableFrame):
    """
    FIATRIX Dashboard — dual theme.
    Light = "Amethyst Haze" (soft lavender academic look),
    Dark  = "Cosmic Night" (deep space with neon lavender highlights).
    Switches live via ctk.set_appearance_mode("Light"/"Dark").
    """

    def __init__(self, master, on_navigate=None, **kwargs):
        super().__init__(
            master,
            fg_color=COLOR_MAIN_BG,
            corner_radius=0,
            **kwargs,
        )
        self.on_navigate = on_navigate
        # Resolve fonts now that a Tk root window exists, so the dashboard
        # can actually pick Inter / JetBrains Mono when installed (the
        # module-level seed values fall back because they run at import time).
        _resolve_fonts()
        if DEBUG_FONTS:
            _debug_print_fonts()
        self._build()

    # ─────────────────────────────────────────
    def _build(self):
        self.grid_columnconfigure(0, weight=1)
        r = 0
        self._build_header(r);     r += 1
        self._build_hero(r);       r += 1
        self._build_bento(r);      r += 1
        self._build_quickstart(r); r += 1
        self._build_footer(r)

    # ═════════════════════════════════════════════════════════════════════════
    # 1. COMMAND HEADER — top breadcrumb + status badges
    # ═════════════════════════════════════════════════════════════════════════
    def _build_header(self, row):
        bar = ctk.CTkFrame(self, fg_color="transparent")
        bar.grid(row=row, column=0, sticky="ew", padx=28, pady=(22, 6))
        bar.grid_columnconfigure(1, weight=1)

        # Left — brand breadcrumb
        left = ctk.CTkFrame(bar, fg_color="transparent")
        left.grid(row=0, column=0, sticky="w")

        ctk.CTkLabel(
            left, text=f"✦ {APP_NAME}",
            font=F_BREADCRUMB,
            text_color=COLOR_ACCENT_PRIMARY,
        ).pack(side="left")

        ctk.CTkLabel(
            left, text="  /  Dashboard",
            font=F_BREADCRUMB,
            text_color=COLOR_TEXT_MUTED,
        ).pack(side="left")

        # Right — status pills
        right = ctk.CTkFrame(bar, fg_color="transparent")
        right.grid(row=0, column=2, sticky="e")

        # "Ready" status pill — soft violet-tinted
        ready = ctk.CTkFrame(
            right, fg_color=COLOR_SECONDARY_BG,
            corner_radius=R_PILL, border_width=0,
        )
        ready.pack(side="left", padx=(0, 8))
        dot = ctk.CTkFrame(
            ready, width=8, height=8, corner_radius=4,
            fg_color=ACC_CYAN,
        )
        dot.pack(side="left", padx=(10, 6), pady=6)
        ctk.CTkLabel(
            ready, text="Ready  ",
            font=F_BADGE,
            text_color=COLOR_SECONDARY_TEXT,
        ).pack(side="left", pady=4)

        # Version chip
        ver = ctk.CTkFrame(
            right, fg_color=COLOR_CARD_BG,
            corner_radius=R_PILL, border_width=1,
            border_color=COLOR_CARD_BORDER,
        )
        ver.pack(side="left")
        ctk.CTkLabel(
            ver, text=f"  {APP_VERSION}  ",
            font=F_BADGE,
            text_color=COLOR_TEXT_MUTED,
        ).pack(padx=4, pady=4)

    # ═════════════════════════════════════════════════════════════════════════
    # 2. HERO — title + CTA on left, formula terminal on right
    # ═════════════════════════════════════════════════════════════════════════
    def _build_hero(self, row):
        hero = ctk.CTkFrame(
            self,
            fg_color=COLOR_CARD_BG,
            corner_radius=R_CARD,
            border_width=1,
            border_color=COLOR_CARD_BORDER,
        )
        hero.grid(row=row, column=0, sticky="ew", padx=28, pady=(8, 14))
        hero.grid_columnconfigure(0, weight=5)
        hero.grid_columnconfigure(1, weight=3)

        # ─── LEFT ───
        left = ctk.CTkFrame(hero, fg_color="transparent")
        left.grid(row=0, column=0, sticky="nsew", padx=(38, 18), pady=36)

        ctk.CTkLabel(
            left, text="LINEAR ALGEBRA WORKSPACE",
            font=F_OVERLINE,
            text_color=COLOR_ACCENT_PRIMARY,
        ).pack(anchor="w")

        ctk.CTkLabel(
            left, text="Jelajahi dunia\nmatriks & ruang vektor.",
            font=F_HERO,
            text_color=COLOR_TEXT_PRIMARY,
            justify="left",
        ).pack(anchor="w", pady=(8, 12))

        ctk.CTkLabel(
            left,
            text=("Selesaikan SPL, operasi matriks, eigen, diagonalisasi,\n"
                  "dan SVD dalam satu workspace berbasis Python."),
            font=F_CARD_BODY,
            text_color=COLOR_TEXT_MUTED,
            justify="left",
        ).pack(anchor="w", pady=(0, 16))

        # Tech stack chips — soft pills (radius = button radius)
        chips = ctk.CTkFrame(left, fg_color="transparent")
        chips.pack(anchor="w", pady=(0, 20))
        for tech in ("Python", "SymPy", "NumPy", "CTk"):
            chip = ctk.CTkFrame(
                chips, fg_color=COLOR_SECONDARY_BG,
                corner_radius=R_BTN, border_width=0,
            )
            chip.pack(side="left", padx=(0, 6))
            ctk.CTkLabel(
                chip, text=f" {tech} ",
                font=F_BADGE,
                text_color=COLOR_SECONDARY_TEXT,
            ).pack(padx=6, pady=4)

        # CTA buttons — primary violet, secondary outline
        cta = ctk.CTkFrame(left, fg_color="transparent")
        cta.pack(anchor="w")

        ctk.CTkButton(
            cta, text="Mulai dari SPL  →",
            font=F_BTN_LARGE,
            fg_color=COLOR_ACCENT_PRIMARY,
            text_color=COLOR_ON_ACCENT,
            hover_color=COLOR_ACCENT_HOVER,
            corner_radius=R_BTN, height=44, width=190,
            border_width=0,
            command=lambda: self._nav("spl"),
        ).pack(side="left", padx=(0, 10))

        ctk.CTkButton(
            cta, text="Eksplor Fitur",
            font=F_BTN_LARGE,
            fg_color="transparent",
            text_color=COLOR_ACCENT_PRIMARY,
            hover_color=COLOR_GLOW_HOVER,
            corner_radius=R_BTN, height=44, width=160,
            border_width=1,
            border_color=COLOR_ACCENT_PRIMARY,
            command=lambda: self._nav("eigen"),
        ).pack(side="left")

        # ─── RIGHT — formula terminal (code simulation) ───
        term = ctk.CTkFrame(
            hero,
            fg_color=COLOR_INSET_BG,
            corner_radius=R_INNER,
            border_width=1,
            border_color=COLOR_CARD_BORDER,
        )
        term.grid(row=0, column=1, sticky="nsew", padx=(0, 34), pady=34)

        # Terminal chrome
        chrome = ctk.CTkFrame(term, fg_color="transparent")
        chrome.pack(fill="x", padx=20, pady=(16, 0))

        dots = ctk.CTkFrame(chrome, fg_color="transparent")
        dots.pack(side="left")
        
        traffic_colors = [
            ("#FF5F57", "#FF5F57"),
            ("#FFBD2E", "#FFBD2E"),
            ("#28C840", "#28C840"),
        ]
        
        for color in traffic_colors:
            dot = ctk.CTkFrame(
                dots, width=11, height=11,
                corner_radius=999, fg_color=color,
            )
            dot.pack(side="left", padx=(0, 7))
            dot.pack_propagate(False)

        ctk.CTkLabel(
            chrome, text="fiatrix.py",
            font=F_MONO_SM,
            text_color=COLOR_TEXT_DIM,
        ).pack(side="right")

        ctk.CTkFrame(
            term, height=1, fg_color=COLOR_CARD_BORDER,
        ).pack(fill="x", padx=20, pady=(12, 0))

        # Code body — generous internal padding so text never touches borders.
        # Each line uses a (light, dark) tuple so the "syntax" stays legible
        # on the Amethyst inset surface in light mode and the deep inset dark.
        body = ctk.CTkFrame(term, fg_color="transparent")
        body.pack(fill="both", expand=True, padx=20, pady=20)

        formulas = [
            ("# linear system",          COLOR_TEXT_DIM,       False),
            ("Ax = b",                   COLOR_ACCENT_PRIMARY, True),
            (None, None, None),
            ("# diagonalization",        COLOR_TEXT_DIM,       False),
            ("A = P D P^-1",             ACC_BLUE,             True),
            (None, None, None),
            ("# singular value decomp.", COLOR_TEXT_DIM,       False),
            ("A = U S V^T",              ACC_CYAN,             True),
            (None, None, None),
            ("det(A)   A^-1   lambda",   ACC_PINK,             True),
        ]
        for text, color, is_formula in formulas:
            if text is None:
                ctk.CTkFrame(body, height=6, fg_color="transparent").pack()
                continue
            ctk.CTkLabel(
                body, text=text,
                font=F_FORMULA if is_formula else F_MONO_SM,
                text_color=color,
                anchor="w",
            ).pack(anchor="w", pady=2)

    # ═════════════════════════════════════════════════════════════════════════
    # 3. BENTO FEATURE GRID
    # ═════════════════════════════════════════════════════════════════════════
    def _build_bento(self, row):
        wrap = ctk.CTkFrame(self, fg_color="transparent")
        wrap.grid(row=row, column=0, sticky="ew", padx=28, pady=(0, 8))

        # Section header
        header = ctk.CTkFrame(wrap, fg_color="transparent")
        header.pack(fill="x", pady=(2, 10))
        ctk.CTkLabel(
            header, text="FITUR",
            font=F_OVERLINE,
            text_color=COLOR_ACCENT_PRIMARY,
        ).pack(anchor="w")
        ctk.CTkLabel(
            header, text="Fitur Utama",
            font=F_SECTION,
            text_color=COLOR_TEXT_PRIMARY,
        ).pack(anchor="w", pady=(2, 0))

        # Top row: SPL (wide) | Det | Inv
        top = ctk.CTkFrame(wrap, fg_color="transparent")
        top.pack(fill="x")
        top.grid_columnconfigure(0, weight=4)
        top.grid_columnconfigure(1, weight=3)
        top.grid_columnconfigure(2, weight=3)

        self._build_spl_card(top, 0, 0)
        self._build_core_card(
            top, 0, 1,
            nav_id="determinan", icon="det(A)",
            title="Determinan", badge="Exact",
            desc=("Hitung determinan matriks persegi\n"
                  "via ekspansi kofaktor."),
            accent=ACC_BLUE,
        )
        self._build_core_card(
            top, 0, 2,
            nav_id="invers", icon="A⁻¹",
            title="Invers Matriks", badge="Non-Singular",
            desc=("Cek dan hitung invers matriks\n"
                  "menggunakan eliminasi Gauss-Jordan."),
            accent=ACC_TEAL,
        )

        # Bottom row: 4 advanced cards
        bot = ctk.CTkFrame(wrap, fg_color="transparent")
        bot.pack(fill="x", pady=(8, 0))
        for i in range(4):
            bot.grid_columnconfigure(i, weight=1)

        advanced = [
            ("lu",       "L·U",   "Dekomposisi LU",
             "Faktorkan matriks menjadi\nP, L, dan U triangular.",
             "P · L · U", ACC_INDIGO),
            ("eigen",    "λ",     "Eigen System",
             "Polynomial karakteristik,\neigenvalue, eigenvector.",
             "λ", COLOR_ACCENT_PRIMARY),
            ("diagonal", "PDP⁻¹", "Diagonalisasi",
             "Cek apakah matriks dapat\ndidiagonalisasi: A = PDP⁻¹.",
             "PDP⁻¹", ACC_BLUE),
            ("svd",      "UΣVᵀ",  "SVD",
             "Dekomposisi Singular Value:\nA = UΣVᵀ.",
             "UΣVᵀ", ACC_PINK),
        ]
        for i, args in enumerate(advanced):
            self._build_adv_card(bot, 0, i, *args)

        # Insight strip
        self._build_insight(wrap)

    # ─── SPL — dominant card ───
    def _build_spl_card(self, parent, r, c):
        card = ctk.CTkFrame(
            parent,
            fg_color=COLOR_CARD_BG,
            corner_radius=R_CARD,
            border_width=1,
            border_color=COLOR_CARD_BORDER,
        )
        card.grid(row=r, column=c, sticky="nsew", padx=(0, 6), pady=0)

        # Symmetric inner padding; button carries the bottom pad (see below).
        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(padx=22, pady=(22, 0), fill="both", expand=True)

        # Top row: icon + badge
        top = ctk.CTkFrame(inner, fg_color="transparent")
        top.pack(fill="x")

        icon_box = ctk.CTkFrame(
            top, fg_color=COLOR_ACCENT_PRIMARY,
            corner_radius=R_INNER, width=52, height=52,
        )
        icon_box.pack(side="left")
        icon_box.pack_propagate(False)
        ctk.CTkLabel(
            icon_box, text="Ax=b",
            font=(_MONO, 14, "bold"),
            text_color=COLOR_ON_ACCENT,
        ).place(relx=0.5, rely=0.5, anchor="center")

        badge = ctk.CTkFrame(
            top, fg_color=COLOR_SECONDARY_BG,
            corner_radius=R_BTN, border_width=0,
        )
        badge.pack(side="right")
        ctk.CTkLabel(
            badge, text=" Gauss · Jordan · Inverse ",
            font=F_BADGE,
            text_color=COLOR_SECONDARY_TEXT,
        ).pack(padx=8, pady=5)

        ctk.CTkLabel(
            inner, text="SPL Solver",
            font=F_HUGE,
            text_color=COLOR_TEXT_PRIMARY,
        ).pack(anchor="w", pady=(20, 6))

        ctk.CTkLabel(
            inner,
            text=("Selesaikan sistem persamaan linear dengan\n"
                  "metode Gauss, Gauss-Jordan, atau Matriks Balikan."),
            font=F_CARD_BODY,
            text_color=COLOR_TEXT_MUTED,
            justify="left",
        ).pack(anchor="w", pady=(0, 10))

        formula = ctk.CTkFrame(
            inner, fg_color=COLOR_INSET_BG,
            corner_radius=R_INNER,
            border_width=1, border_color=COLOR_CARD_BORDER,
        )
        formula.pack(anchor="w", pady=(0, 18))
        ctk.CTkLabel(
            formula, text="  Ax = b   →   x = A⁻¹b  ",
            font=F_FORMULA,
            text_color=COLOR_ACCENT_PRIMARY,
        ).pack(padx=14, pady=10)

        ctk.CTkButton(
            inner, text="Buka SPL Solver  →",
            font=F_BUTTON,
            fg_color=COLOR_ACCENT_PRIMARY,
            text_color=COLOR_ON_ACCENT,
            hover_color=COLOR_ACCENT_HOVER,
            corner_radius=R_BTN, height=40, width=200,
            border_width=0,
            command=lambda: self._nav("spl"),
        ).pack(anchor="w", pady=(0, 22))

    # ─── Medium core card (Det / Invers) ───
    def _build_core_card(self, parent, r, c, nav_id, icon, title,
                         badge, desc, accent):
        card = ctk.CTkFrame(
            parent,
            fg_color=COLOR_CARD_BG,
            corner_radius=R_CARD,
            border_width=1,
            border_color=COLOR_CARD_BORDER,
        )
        card.grid(row=r, column=c, sticky="nsew", padx=6, pady=0)

        # Top padding lives on the inner frame; the bottom padding is carried
        # by the "Buka →" button so it stays symmetrical with the top (20/20)
        # and never sits flush against the card's bottom edge.
        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(padx=20, pady=(20, 0), fill="both", expand=True)

        icon_box = ctk.CTkFrame(
            inner, fg_color=COLOR_ACCENT_SURFACE,
            corner_radius=R_INNER, width=44, height=44,
            border_width=0,
        )
        icon_box.pack(anchor="w")
        icon_box.pack_propagate(False)
        ctk.CTkLabel(
            icon_box, text=icon,
            font=(_MONO, 11, "bold"),
            text_color=accent,
        ).place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(
            inner, text=title,
            font=F_CARD_TITLE,
            text_color=COLOR_TEXT_PRIMARY,
        ).pack(anchor="w", pady=(14, 5))

        ctk.CTkLabel(
            inner, text=desc,
            font=F_CARD_BODY,
            text_color=COLOR_TEXT_MUTED,
            justify="left",
        ).pack(anchor="w", pady=(0, 12))

        bg = ctk.CTkFrame(
            inner, fg_color=COLOR_SECONDARY_BG,
            corner_radius=R_BTN, border_width=0,
        )
        bg.pack(anchor="w", pady=(0, 14))
        ctk.CTkLabel(
            bg, text=f" {badge} ",
            font=F_BADGE,
            text_color=COLOR_SECONDARY_TEXT,
        ).pack(padx=8, pady=4)

        ctk.CTkButton(
            inner, text="Buka  →",
            font=F_BUTTON,
            fg_color="transparent",
            text_color=accent,
            border_width=1,
            border_color=COLOR_CARD_BORDER,
            hover_color=COLOR_GLOW_HOVER,
            corner_radius=R_BTN, height=34, width=110,
            command=lambda: self._nav(nav_id),
        ).pack(anchor="w", pady=(10, 20))

    # ─── Compact advanced card ───
    def _build_adv_card(self, parent, r, c, nav_id, icon, title, desc,
                        badge, accent):
        card = ctk.CTkFrame(
            parent,
            fg_color=COLOR_CARD_BG,
            corner_radius=R_CARD,
            border_width=1,
            border_color=COLOR_CARD_BORDER,
        )
        card.grid(row=r, column=c, sticky="nsew", padx=4, pady=0)

        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(padx=16, pady=(16, 0), fill="both", expand=True)

        top = ctk.CTkFrame(inner, fg_color="transparent")
        top.pack(fill="x")

        icon_box = ctk.CTkFrame(
            top, fg_color=COLOR_ACCENT_SURFACE,
            corner_radius=R_INNER, width=36, height=36,
            border_width=0,
        )
        icon_box.pack(side="left")
        icon_box.pack_propagate(False)
        ctk.CTkLabel(
            icon_box, text=icon,
            font=(_MONO, 10, "bold"),
            text_color=accent,
        ).place(relx=0.5, rely=0.5, anchor="center")

        bg = ctk.CTkFrame(
            top, fg_color=COLOR_SECONDARY_BG,
            corner_radius=R_BTN, border_width=0,
        )
        bg.pack(side="right")
        ctk.CTkLabel(
            bg, text=f" {badge} ",
            font=F_MONO_TINY,
            text_color=COLOR_SECONDARY_TEXT,
        ).pack(padx=5, pady=3)

        ctk.CTkLabel(
            inner, text=title,
            font=(_SANS, 13, "bold"),
            text_color=COLOR_TEXT_PRIMARY,
        ).pack(anchor="w", pady=(12, 4))

        ctk.CTkLabel(
            inner, text=desc,
            font=(_SANS, 11),
            text_color=COLOR_TEXT_MUTED,
            justify="left",
        ).pack(anchor="w", pady=(0, 12))

        ctk.CTkButton(
            inner, text="Buka  →",
            font=F_BUTTON,
            fg_color="transparent",
            text_color=accent,
            border_width=1,
            border_color=COLOR_CARD_BORDER,
            hover_color=COLOR_GLOW_HOVER,
            corner_radius=R_BTN, height=30, width=90,
            command=lambda: self._nav(nav_id),
        ).pack(anchor="w", pady=(8, 16))

    # ─── Insight metric strip ───
    def _build_insight(self, parent):
        strip = ctk.CTkFrame(
            parent,
            fg_color=COLOR_CARD_BG,
            corner_radius=R_CARD,
            border_width=1,
            border_color=COLOR_CARD_BORDER,
        )
        strip.pack(fill="x", pady=(10, 0))

        inner = ctk.CTkFrame(strip, fg_color="transparent")
        inner.pack(fill="x", padx=24, pady=18)

        items = [
            ("07", "Fitur Utama",        COLOR_ACCENT_PRIMARY),
            ("03", "Metode SPL",         ACC_BLUE),
            ("∞",  "Step-by-Step",       ACC_CYAN),
            ("◆",  "Exact & Numerical",  ACC_PINK),
        ]
        for i, (val, label, color) in enumerate(items):
            cell = ctk.CTkFrame(inner, fg_color="transparent")
            cell.pack(side="left", expand=True)

            ctk.CTkLabel(
                cell, text=val,
                font=(_SANS, 24, "bold"),
                text_color=color,
            ).pack(side="left", padx=(0, 10))

            ctk.CTkLabel(
                cell, text=label,
                font=F_BADGE,
                text_color=COLOR_TEXT_MUTED,
            ).pack(side="left")

            if i < len(items) - 1:
                ctk.CTkFrame(
                    inner, width=1, height=24,
                    fg_color=COLOR_CARD_BORDER,
                    corner_radius=0,
                ).pack(side="left", padx=14)

    # ═════════════════════════════════════════════════════════════════════════
    # 4. QUICK START STRIP
    # ═════════════════════════════════════════════════════════════════════════
    def _build_quickstart(self, row):
        strip = ctk.CTkFrame(
            self,
            fg_color=COLOR_CARD_BG,
            corner_radius=R_CARD,
            border_width=1,
            border_color=COLOR_CARD_BORDER,
        )
        strip.grid(row=row, column=0, sticky="ew", padx=28, pady=(8, 10))

        inner = ctk.CTkFrame(strip, fg_color="transparent")
        inner.pack(fill="x", padx=24, pady=18)

        left = ctk.CTkFrame(inner, fg_color="transparent")
        left.pack(side="left")

        ctk.CTkLabel(
            left, text="QUICK ACCESS",
            font=F_OVERLINE,
            text_color=COLOR_ACCENT_PRIMARY,
        ).pack(anchor="w")
        ctk.CTkLabel(
            left, text="Mulai Cepat",
            font=F_CARD_TITLE,
            text_color=COLOR_TEXT_PRIMARY,
        ).pack(anchor="w", pady=(2, 2))
        ctk.CTkLabel(
            left,
            text="Pilih fitur untuk langsung memulai perhitungan.",
            font=F_META,
            text_color=COLOR_TEXT_MUTED,
        ).pack(anchor="w")

        # Right — quick action buttons. Background + border adapt to the
        # lavender palette in light mode via the dual tuples below.
        btns = ctk.CTkFrame(inner, fg_color="transparent")
        btns.pack(side="right")

        actions = [
            ("⊞  SPL",   "spl",        COLOR_ACCENT_PRIMARY),
            ("⊡  Det",   "determinan", ACC_BLUE),
            ("⊟  Inv",   "invers",     ACC_TEAL),
            ("λ  Eigen", "eigen",      ACC_PINK),
        ]
        for label, nav_id, color in actions:
            ctk.CTkButton(
                btns, text=label,
                font=F_BUTTON,
                fg_color=COLOR_ACCENT_SURFACE,
                text_color=color,
                hover_color=COLOR_GLOW_HOVER,
                border_width=1,
                border_color=COLOR_CARD_BORDER,
                corner_radius=R_BTN, height=36, width=92,
                command=lambda nid=nav_id: self._nav(nid),
            ).pack(side="left", padx=3)

    # ═════════════════════════════════════════════════════════════════════════
    # 5. FOOTER
    # ═════════════════════════════════════════════════════════════════════════
    def _build_footer(self, row):
        footer = ctk.CTkFrame(self, fg_color="transparent")
        footer.grid(row=row, column=0, sticky="ew", padx=28, pady=(4, 24))

        ctk.CTkFrame(
            footer, height=1, fg_color=COLOR_CARD_BORDER,
            corner_radius=0,
        ).pack(fill="x", pady=(0, 12))

        ctk.CTkLabel(
            footer,
            text=("Ctrl+1–7 Navigasi   ·   Ctrl+Enter Hitung   ·   "
                  "Ctrl+L Clear   ·   Esc Kembali"),
            font=F_BADGE,
            text_color=COLOR_TEXT_DIM,
        ).pack(anchor="center")

    # ═════════════════════════════════════════════════════════════════════════
    # NAVIGATION
    # ═════════════════════════════════════════════════════════════════════════
    def _nav(self, page_id):
        if self.on_navigate:
            self.on_navigate(page_id)
