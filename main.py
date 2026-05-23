# =============================================================================
# MAIN.PY — Entry Point Aplikasi
# =============================================================================
# Linear Algebra Dashboard Pro
# Kalkulator Aljabar Linear Modern dengan CustomTkinter
# =============================================================================

import sys
import os

# Pastikan directory project ada di path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import ModernAlinApp


def main():
    """Launch the application."""
    app = ModernAlinApp()
    app.mainloop()


if __name__ == "__main__":
    main()
