"""Test bootstrap: resolve hermes-agent imports and the plugin module.

The plugin imports ``tools.registry`` (and optionally ``hermes_cli.config``)
from a hermes-agent checkout. Point HERMES_AGENT_REPO at one (defaults to
``~/.hermes/hermes-agent``).
"""

import os
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parent

_hermes_agent = Path(
    os.environ.get("HERMES_AGENT_REPO", Path.home() / ".hermes" / "hermes-agent")
).expanduser()

# hermes-agent first (tools/, hermes_cli/), then this repo (backsearch_tools).
for p in (str(_hermes_agent), str(_REPO_ROOT)):
    if p not in sys.path:
        sys.path.insert(0, p)

collect_ignore = ["__init__.py", "backsearch_tools.py"]
