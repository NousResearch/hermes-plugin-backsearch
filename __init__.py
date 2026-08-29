"""BackSearch plugin — point-in-time web search + fetch.

Registers two tools into the ``backsearch`` toolset:

- ``backsearch`` — search a frozen news archive as of a date
- ``backfetch``  — fetch a page's text as archived on or before a date

Backed by BackSearch from General Reasoning (https://www.gr.inc), served at
https://search.openreward.ai and billed against an OpenReward prepaid
balance. Both tools gate on ``OPENREWARD_API_KEY`` via ``check_fn`` — when
the key is absent the tools stay registered but never reach the model
schema, so the plugin costs zero model-tool footprint without a credential.

Install into ``~/.hermes/plugins/backsearch`` and enable with
``hermes plugins enable backsearch`` (see README).
"""

from __future__ import annotations

try:  # loaded as a package by the hermes plugin loader
    from .backsearch_tools import (
        BACKFETCH_SCHEMA,
        BACKSEARCH_SCHEMA,
        check_backsearch_available,
        handle_backfetch,
        handle_backsearch,
    )
except ImportError:  # imported flat (tests put the repo root on sys.path)
    from backsearch_tools import (
        BACKFETCH_SCHEMA,
        BACKSEARCH_SCHEMA,
        check_backsearch_available,
        handle_backfetch,
        handle_backsearch,
    )

_TOOLS = (
    ("backsearch", BACKSEARCH_SCHEMA, handle_backsearch, "🕰️"),
    ("backfetch", BACKFETCH_SCHEMA, handle_backfetch, "📰"),
)


def register(ctx) -> None:
    """Register the BackSearch tools. Called once by the plugin loader."""
    for name, schema, handler, emoji in _TOOLS:
        ctx.register_tool(
            name=name,
            toolset="backsearch",
            schema=schema,
            handler=handler,
            check_fn=check_backsearch_available,
            requires_env=["OPENREWARD_API_KEY"],
            emoji=emoji,
        )
