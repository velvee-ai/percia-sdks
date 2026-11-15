#!/usr/bin/env python3
"""Derive percia/_aresources.py from percia/_resources.py (the sync file is the source of truth)."""

import re
from pathlib import Path

root = Path(__file__).resolve().parent.parent / "percia"
src = (root / "_resources.py").read_text()
src = re.sub(
    r"NOTE: ``_aresources.py``.*?\n",
    "GENERATED from ``_resources.py`` by scripts/make_async_resources.py. Do not edit.\n",
    src,
)
src = src.replace("(sync)", "(async)")
src = re.sub(r"\bPercia\b", "AsyncPercia", src)
src = re.sub(r"^class (\w+):", r"class Async\1:", src, flags=re.M)
src = re.sub(r"^    def (?!__init__)", "    async def ", src, flags=re.M)
src = src.replace("return self._c._call(", "return await self._c._call(")
src = src.replace("return self.update(", "return await self.update(")
src = re.sub(r"= self\.([\w.]+)\(", r"= await self.\1(", src)  # assignments that call a sibling method
(root / "_aresources.py").write_text(src)
