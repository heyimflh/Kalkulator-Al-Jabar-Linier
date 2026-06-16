# =============================================================================
# MAIN.PY — Entry Point
# =============================================================================
# FIATRIX — Linear Algebra Workspace
# Premium desktop calculator for linear algebra computation.
# =============================================================================

import sys
import os

# Ensure project directory is in path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import ModernAlinApp


def main():
    """Launch FIATRIX application."""
    app = ModernAlinApp()
    app.mainloop()


if __name__ == "__main__":
    main()
