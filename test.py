#!/usr/bin/env python3
"""Script para ejecutar las pruebas del asistente de voz local."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

import pytest

if __name__ == "__main__":
    exit_code = pytest.main(["-v", "tests/"])
    sys.exit(exit_code)
