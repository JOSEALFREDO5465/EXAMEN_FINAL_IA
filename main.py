#!/usr/bin/env python3
import os
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
if BASE not in sys.path:
    sys.path.insert(0, BASE)

from agent.cli import main

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nHasta luego.")
        sys.exit(0)
    except EOFError:
        print("\nHasta luego.")
        sys.exit(0)
