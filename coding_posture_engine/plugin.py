"""Hermes plugin registration for coding-posture-engine."""
from __future__ import annotations

import json
from typing import Any, Dict, Optional

from coding_posture_engine import PostureEngine, load_default_engine

_ENGINE: Optional[PostureEngine] = None


def _engine() -> PostureEngine:
    global _ENGINE
    if _ENGINE is None:
        _ENGINE = load_default_engine()
    return _ENGINE


def _select_tool(args: Dict[str, Any], **_: Any) -> str:
    prompt = str(args.get("prompt") or "")
    agent = str(args.get("agent") or "hermes")
    previous = args.get("previous_posture")
    result = _engine().select(prompt=prompt, agent=agent, previous_posture=previous)
    return json.dumps(result.to_dict(), ensure_ascii=False, indent=2)


def _render_tool(args: Dict[str, Any], **_: Any) -> str:
    prompt = str(args.get("prompt") or "")
    agent = str(args.get("agent") or "hermes")
    previous = args.get("previous_posture")
    include_task = bool(args.get("include_task", False))
    result = _engine().select(prompt=prompt, agent=agent, previous_posture=previous)
    rendered = _engine().render_prompt(result, task=prompt if include_task else None, agent=agent)
    return json.dumps({"posture": result.to_dict(), "prompt": rendered}, ensure_ascii=False, indent=2)


def pre_llm_call(**kwargs: Any) -> Optional[Dict[str, str]]:
    """Inject a small posture block into Hermes turns that look coding-related.

    The hook contributes ephemeral user-message context, not system prompt text,
    so it preserves prompt caching. Non-coding turns are ignored.
    """
    user_message = str(kwargs.get("user_message") or "")
    if not _engine().looks_coding_related(user_message):
        return None
    result = _engine().select(prompt=user_message, agent="hermes")
    block = _engine().render_prompt(result, task=None, agent="hermes", compact=True)
    return {"context": block}


def slash_command(raw_args: str) -> str:
    raw_args = (raw_args or "").strip()
    if not raw_args or raw_args in {"help", "-h", "--help"}:
        return (
            "Coding posture engine\n\n"
            "Usage:\n"
            "  /posture <task text>          Select posture for task\n"
            "  /posture render <task text>   Render prompt block\n\n"
            "Examples:\n"
            "  /posture fix failing pytest regression\n"
            "  /posture render review auth diff for security\n"
        )
    if raw_args.startswith("render "):
        prompt = raw_args[len("render "):].strip()
        result = _engine().select(prompt=prompt, agent="hermes")
        return _engine().render_prompt(result, task=None, agent="hermes")
    result = _engine().select(prompt=raw_args, agent="hermes")
    return json.dumps(result.to_dict(), ensure_ascii=False, indent=2)


def register(ctx) -> None:
    ctx.register_hook("pre_llm_call", pre_llm_call)
    ctx.register_command(
        "posture",
        handler=slash_command,
        description="Select/render a coding-agent execution posture.",
        args_hint="<task text>",
    )
    ctx.register_tool(
        name="coding_posture_select",
        toolset="coding_posture",
        description="Select a task-aware coding-agent posture.",
        emoji="🧭",
        schema={
            "name": "coding_posture_select",
            "description": "Select a coding-agent execution posture from task text and agent name.",
            "parameters": {
                "type": "object",
                "properties": {
                    "prompt": {"type": "string", "description": "Task/request text."},
                    "agent": {"type": "string", "description": "Agent target: hermes, claude, codex, pi, or generic.", "default": "hermes"},
                    "previous_posture": {"type": "string", "description": "Optional previous posture ID for inertia."}
                },
                "required": ["prompt"]
            }
        },
        handler=lambda args, **kw: _select_tool(args, **kw),
    )
    ctx.register_tool(
        name="coding_posture_render",
        toolset="coding_posture",
        description="Render a concise posture prompt block for coding agents.",
        emoji="🧾",
        schema={
            "name": "coding_posture_render",
            "description": "Render a posture prompt block for Hermes, Claude Code, Codex, Pi, or generic coding agents.",
            "parameters": {
                "type": "object",
                "properties": {
                    "prompt": {"type": "string", "description": "Task/request text."},
                    "agent": {"type": "string", "description": "Agent target: hermes, claude, codex, pi, or generic.", "default": "hermes"},
                    "previous_posture": {"type": "string", "description": "Optional previous posture ID for inertia."},
                    "include_task": {"type": "boolean", "description": "Append the original task after the posture block.", "default": False}
                },
                "required": ["prompt"]
            }
        },
        handler=lambda args, **kw: _render_tool(args, **kw),
    )
