from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, Iterator, List

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from percia import (  # noqa: E402
    AsyncPercia,
    Percia,
    _retry,  # noqa: E402
)

from .mock_server import MockPercia  # noqa: E402

KEY = "pk_live_test"


@pytest.fixture
def server() -> MockPercia:
    return MockPercia()


@pytest.fixture
def sleeps(monkeypatch: pytest.MonkeyPatch) -> List[float]:
    """Record the backoff sleeps instead of sleeping (sync and async)."""
    recorded: List[float] = []

    async def fake_asleep(seconds: float) -> None:
        recorded.append(seconds)

    monkeypatch.setattr(_retry, "_sleep", recorded.append)
    monkeypatch.setattr(_retry, "_asleep", fake_asleep)
    return recorded


@pytest.fixture
def client(server: MockPercia, sleeps: List[float]) -> Iterator[Percia]:
    c = Percia(api_key=KEY, base_url="http://mock.test", transport=server.transport())
    yield c
    c.close()


@pytest.fixture
async def aclient(server: MockPercia, sleeps: List[float]) -> Any:
    c = AsyncPercia(api_key=KEY, base_url="http://mock.test", transport=server.transport())
    yield c
    await c.aclose()
