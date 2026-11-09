from __future__ import annotations

import inspect

from percia import _aresources, _resources


def test_async_resources_mirror_sync_resources():
    for name, sync_cls in inspect.getmembers(_resources, inspect.isclass):
        if sync_cls.__module__ != _resources.__name__:
            continue
        async_cls = getattr(_aresources, "Async" + name)
        s = {n for n, f in inspect.getmembers(sync_cls, inspect.isfunction) if not n.startswith("_")}
        a = {n for n, f in inspect.getmembers(async_cls, inspect.isfunction) if not n.startswith("_")}
        assert s == a, name
        for n in a:
            assert inspect.iscoroutinefunction(getattr(async_cls, n)), f"{name}.{n}"


def test_async_file_is_up_to_date():
    import re
    from pathlib import Path

    root = Path(_resources.__file__).parent
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
    src = src.replace("return self._c._call(", "return await self._c._call(").replace(
        "return self.update(", "return await self.update("
    )
    squash = lambda t: re.sub(r"[\s,()]+", "", t)  # noqa: E731 - ignore formatter differences
    assert squash(src) == squash((root / "_aresources.py").read_text()), (
        "run: python scripts/make_async_resources.py && ruff format percia"
    )
