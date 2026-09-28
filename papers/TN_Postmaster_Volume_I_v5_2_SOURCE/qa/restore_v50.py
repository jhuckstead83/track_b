#!/usr/bin/env python3
"""Restore the untouched v5.0 source tree using shared unchanged figures."""
from pathlib import Path
import shutil,sys
ROOT=Path(__file__).resolve().parents[1]
if len(sys.argv)!=2:
    raise SystemExit('Usage: python qa/restore_v50.py NEW_DESTINATION')
dest=Path(sys.argv[1]).expanduser().resolve()
if dest.exists(): raise SystemExit('Destination must not already exist.')
shutil.copytree(ROOT/'provenance/v5_0',dest)
shutil.copytree(ROOT/'figures',dest/'figures')
print(dest)
