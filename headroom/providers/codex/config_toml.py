"""Parse Codex ``config.toml`` with the syntax Codex itself accepts."""

from __future__ import annotations

import sys
from typing import Any, cast

import tomlkit
from tomlkit.exceptions import TOMLKitError

if sys.version_info >= (3, 11):
    import tomllib
else:  # pragma: no cover - exercised only on Python 3.10
    import tomli as tomllib  # type: ignore[no-redef]


def loads_codex_config(content: str) -> dict[str, Any]:
    """Parse Codex config text, falling back to ``tomlkit`` for TOML 1.1 syntax.

    Codex accepts TOML 1.1, where an inline table may span several lines and
    end with a trailing comma (#4378). ``tomllib`` before Python 3.15 only
    implements TOML 1.0 and rejects that, so retry with ``tomlkit`` (0.15+),
    which parses it. Text neither parser accepts raises the original
    ``tomllib.TOMLDecodeError``, so callers keep their existing error handling.
    """
    try:
        return cast("dict[str, Any]", tomllib.loads(content))
    except tomllib.TOMLDecodeError as exc:
        try:
            return tomlkit.parse(content).unwrap()
        except TOMLKitError:
            raise exc from None
