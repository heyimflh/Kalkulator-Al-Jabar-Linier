# =============================================================================
# MAIN.PY — Entry Point
# =============================================================================
# AXIOM — Linear Algebra Workspace
# Premium desktop calculator for linear algebra computation.
# =============================================================================

import sys
import os

# Ensure project directory is in path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import ModernAlinApp


def main():
    """Launch AXIOM application."""
    app = ModernAlinApp()
    app.mainloop()


if __name__ == "__main__":
    main()
