#!/usr/bin/env python3
"""Regenerate python/percia/_generated from ../spec/openapi.json with openapi-python-client.

Deterministic: the spec is pre-processed in memory (see `fix_spec`), generated into a temp dir, ruff-formatted,
and copied over percia/_generated. Run from anywhere: `python3 python/scripts/generate.py`
(uses python/.venv when present, otherwise whatever `openapi-python-client` is on PATH).
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
PY = HERE.parent
SPEC = PY.parent / "spec" / "openapi.json"
TARGET = PY / "percia" / "_generated"
VENV_BIN = PY / ".venv" / "bin"


def fix_spec(node):
    """openapi-python-client rejects `items: false` (a JSON Schema 2020-12 tuple with prefixItems).
    The zone points are [x, y] number pairs: turn them into a plain array of numbers (minItems/maxItems stay)."""
    if isinstance(node, dict):
        if node.get("items") is False and isinstance(node.get("prefixItems"), list) and node["prefixItems"]:
            node = dict(node)
            node["items"] = {k: v for k, v in node["prefixItems"][0].items()}
            del node["prefixItems"]
        return {k: fix_spec(v) for k, v in node.items()}
    if isinstance(node, list):
        return [fix_spec(v) for v in node]
    return node


def tool(name: str) -> str:
    p = VENV_BIN / name
    return str(p) if p.exists() else name


def main() -> int:
    spec = fix_spec(json.loads(SPEC.read_text()))
    with tempfile.TemporaryDirectory() as tmp:
        tmpd = Path(tmp)
        (tmpd / "openapi.json").write_text(json.dumps(spec, indent=2, sort_keys=True))
        out = tmpd / "out"
        out.mkdir()
        subprocess.run(
            [
                tool("openapi-python-client"),
                "generate",
                "--path",
                str(tmpd / "openapi.json"),
                "--config",
                str(HERE / "generator-config.yml"),
                "--meta",
                "none",
                "--output-path",
                str(out / "percia_generated"),
                "--overwrite",
            ],
            check=True,
            cwd=tmp,
        )
        pkg = out / "percia_generated"
        if not pkg.exists():
            print("generator produced no package", file=sys.stderr)
            return 1
        if TARGET.exists():
            shutil.rmtree(TARGET)
        shutil.copytree(pkg, TARGET)
    # The generated code only uses relative imports; assert that so a generator upgrade cannot silently break the move.
    bad = [str(p) for p in TARGET.rglob("*.py") if "percia_generated" in p.read_text()]
    if bad:
        print("absolute self-imports found:", bad[:5], file=sys.stderr)
        return 1
    subprocess.run([tool("ruff"), "format", "--config", str(PY / "pyproject.toml"), str(TARGET)], check=False)
    n = sum(1 for _ in TARGET.rglob("*.py"))
    print(f"generated {n} files into {TARGET.relative_to(PY.parent)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
