"""Core selection and rendering logic for coding-posture-engine.

The engine is intentionally dependency-free so it can run inside Hermes plugins,
standalone CLI wrappers, and tests without dragging in yet another ecosystem.
Entropy already has enough package managers.
"""
from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
import re
from typing import Any, Dict, List, Optional

_WORD_RE = re.compile(r"[a-zA-Z0-9_./-]+")


@dataclass(frozen=True)
class PostureResult:
    posture: Dict[str, Any]
    score: float
    reason: str
    warnings: List[str]
    agent: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.posture["id"],
            "label": self.posture.get("label", self.posture["id"]),
            "description": self.posture.get("description", ""),
            "score": round(self.score, 3),
            "reason": self.reason,
            "warnings": list(self.warnings),
            "axes": self.posture.get("axes", {}),
            "rules": self.posture.get("rules", []),
            "agent": self.agent,
        }


class PostureEngine:
    def __init__(self, catalog: Dict[str, Any]) -> None:
        self.catalog = catalog
        self.postures = catalog.get("postures", [])
        if not self.postures:
            raise ValueError("posture catalog is empty")

    def looks_coding_related(self, text: str) -> bool:
        t = text.lower()
        signals = [
            "code", "repo", "git", "test", "pytest", "npm", "build", "ci", "bug", "fix",
            "diff", "pr", "pull request", "refactor", "function", "class", "api", "deploy",
            "python", "typescript", "javascript", "go", "docker", "kubernetes", "terraform",
        ]
        return any(s in t for s in signals)

    def select(self, prompt: str, agent: str = "generic", previous_posture: Optional[str] = None) -> PostureResult:
        text = (prompt or "").lower()
        tokens = set(_WORD_RE.findall(text))
        best: Optional[tuple[float, Dict[str, Any], List[str]]] = None
        for posture in self.postures:
            score = 0.0
            hits: List[str] = []
            for trig in posture.get("triggers", []):
                trig_l = trig.lower()
                if " " in trig_l:
                    if trig_l in text:
                        score += 2.0
                        hits.append(trig)
                elif trig_l in tokens or trig_l in text:
                    score += 1.2
                    hits.append(trig)
            if previous_posture and posture.get("id") == previous_posture:
                score += 0.35
                hits.append("inertia")
            score += self._risk_bonus(text, posture)
            if best is None or score > best[0]:
                best = (score, posture, hits)
        assert best is not None
        score, posture, hits = best
        if score <= 0:
            posture = self._by_id("forensic-debugger") or self.postures[0]
            hits = ["default: coding task with no stronger signal"]
            score = 0.1
        warnings = self._warnings(text, posture)
        reason = ", ".join(hits[:6]) if hits else "default selection"
        return PostureResult(posture=posture, score=score, reason=reason, warnings=warnings, agent=agent)

    def render_prompt(self, result: PostureResult, task: Optional[str] = None, agent: str = "generic", compact: bool = False) -> str:
        d = result.to_dict()
        header = f"Coding posture: {d['id']} — {d['label']}"
        lines = [header, f"Reason: {d['reason']}"]
        if d["warnings"]:
            lines.append("Risk warnings: " + "; ".join(d["warnings"]))
        rules = d["rules"][:3 if compact else 6]
        lines.append("Rules:")
        lines.extend(f"- {rule}" for rule in rules)
        if agent in {"claude", "claude-code"}:
            lines.append("Claude Code adapter: keep edits scoped, use its native planning/checking, and report concrete commands run.")
        elif agent in {"codex", "openai", "openai-codex"}:
            lines.append("Codex adapter: prefer repository-grounded edits and include test output in the final summary.")
        elif agent == "pi":
            lines.append("Pi adapter: generic prompt-injection mode; if Pi cannot edit files directly, return a patch/plan instead of pretending.")
        if task:
            lines.extend(["", "Task:", task])
        return "\n".join(lines)

    def _risk_bonus(self, text: str, posture: Dict[str, Any]) -> float:
        risk = self.catalog.get("risk_patterns", {})
        high_risk = any(p in text for p in risk.get("high_risk_paths", []))
        destructive = any(w in text for w in risk.get("destructive_words", []))
        pid = posture.get("id")
        if (high_risk or destructive) and pid in {"entropy-auditor", "cautious-migrator"}:
            return 3.0
        if destructive and pid == "surgical-fixer":
            return -1.0
        return 0.0

    def _warnings(self, text: str, posture: Dict[str, Any]) -> List[str]:
        risk = self.catalog.get("risk_patterns", {})
        warnings: List[str] = []
        if any(p in text for p in risk.get("high_risk_paths", [])):
            warnings.append("high-risk path/domain detected; keep risk tolerance low")
        if any(w in text for w in risk.get("destructive_words", [])):
            warnings.append("destructive wording detected; require explicit scope and rollback")
        if posture.get("id") == "prototype-goblin" and warnings:
            warnings.append("prototype posture must stay isolated from production paths")
        return warnings

    def _by_id(self, posture_id: str) -> Optional[Dict[str, Any]]:
        for posture in self.postures:
            if posture.get("id") == posture_id:
                return posture
        return None


def load_default_engine() -> PostureEngine:
    path = Path(__file__).with_name("postures.json")
    return PostureEngine(json.loads(path.read_text(encoding="utf-8")))
