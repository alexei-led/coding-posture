"""Pip entrypoint shim for Hermes plugin discovery."""
from __future__ import annotations

from .plugin import register

__all__ = ["register"]
