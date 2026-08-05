# -*- coding: utf-8 -*-
import sys
sys.dont_write_bytecode = True

import os
from pathlib import Path

# Ensure scripts/ is importable
scripts_dir = Path(__file__).parent.parent / "scripts"
sys.path.insert(0, str(scripts_dir))
