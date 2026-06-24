"""Directory-plugin entrypoint for Hermes.

Hermes directory installs load this repository-root module and call `register(ctx)`.
"""
from coding_posture_engine.plugin import register

__all__ = ["register"]
