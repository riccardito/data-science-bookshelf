"""Expensive or platform-dependent steps, recorded: replay by default, record on request.

A chapter that calls Claude -- or runs a step whose output can differ between machines, like OCR
-- goes through a ``Recorder``. Every request is keyed by the SHA-256 of its content; the answer
is stored in a JSON file beside the chapter. Replay needs no key, no network and no model, so the
notebook runs in CI exactly as it ran when it was written. ``live=True`` asks for what is missing
and records it.

The Claude call follows the `fedlex-rag` pattern: structured output (a JSON schema), a stated
effort, and ``fallbacks: "default"`` so a safety decline is re-run on the model Anthropic
recommends for it instead of failing. The key comes from ``ANTHROPIC_API_KEY`` or, failing that,
the OS keyring (service ``anthropic``, user ``portfolio``).
"""

from __future__ import annotations

import hashlib
import json
import os
from collections.abc import Callable
from pathlib import Path

MODEL = "claude-opus-5-5"
FALLBACK_BETA = "server-side-fallback-2026-07-01"


class MissingRecording(LookupError):
    """A request with no recorded answer, and nothing live to ask."""


class Refused(RuntimeError):
    """Every model in the fallback chain declined the request."""


def request_key(request: dict) -> str:
    return hashlib.sha256(json.dumps(request, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def api_key() -> str | None:
    key = os.environ.get("ANTHROPIC_API_KEY")
    if key:
        return key
    try:
        import keyring
    except ImportError:
        return None
    return keyring.get_password("anthropic", "portfolio")


def claude_client():
    """An Anthropic client, or a clear error. Needs the ``llm`` extra."""
    import anthropic

    key = api_key()
    if not key:
        raise RuntimeError("no API key: set ANTHROPIC_API_KEY, or store one with "
                           "`python -m keyring set anthropic portfolio`")
    return anthropic.Anthropic(api_key=key)


def call_claude(client, request: dict) -> tuple[dict, dict]:
    """One structured call. Returns (the parsed JSON, metadata: serving model and token usage)."""
    response = client.beta.messages.create(
        model=request["model"],
        max_tokens=16000,
        betas=[FALLBACK_BETA],
        fallbacks="default",
        system=request["system"],
        output_config={"effort": request["effort"],
                       "format": {"type": "json_schema", "schema": request["schema"]}},
        messages=[{"role": "user", "content": request["user"]}],
    )
    if response.stop_reason == "refusal":
        details = getattr(response, "stop_details", None)
        raise Refused(getattr(details, "category", None) or "unknown")
    if response.stop_reason == "max_tokens":
        raise RuntimeError("the response hit max_tokens before the JSON was complete")
    text = next(b.text for b in response.content if b.type == "text")
    usage = response.usage
    return json.loads(text), {"served_by": response.model, "input_tokens": usage.input_tokens,
                              "output_tokens": usage.output_tokens}


class Recorder:
    """Replays recorded answers; with ``live``, computes the misses through ``call`` and records them."""

    def __init__(self, path: Path | str, call: Callable[[object, dict], tuple[object, dict]] | None = None,
                 client=None, live: bool = False, save_every: int = 10):
        self.path = Path(path)
        self.call = call
        self.client = client
        self.live = live
        self.save_every = save_every      # a live run that dies late keeps what it paid for
        self.entries: dict[str, dict] = {}
        if self.path.exists():
            self.entries = json.loads(self.path.read_text(encoding="utf-8")).get("entries", {})
        self.added = 0
        self.used: set[str] = set()

    def ask(self, request: dict):
        key = request_key(request)
        self.used.add(key)
        if key in self.entries:
            return self.entries[key]["output"]
        if not self.live or self.call is None:
            raise MissingRecording(f"no recording for {request.get('task', '?')} request {key[:12]} "
                                   f"in {self.path.name} -- run live to record it")
        output, meta = self.call(self.client, request)
        self.entries[key] = {"task": request.get("task"), **meta, "output": output}
        self.added += 1
        if self.save_every and self.added >= self.save_every:
            self.save()
        return output

    def missing(self, requests) -> list[dict]:
        """The requests that would need a live call -- to count, and to price, before running."""
        return [r for r in requests if request_key(r) not in self.entries]

    def usage(self) -> dict[str, int]:
        """Summed token usage of the recorded entries that carry it."""
        total = {"input_tokens": 0, "output_tokens": 0, "calls": 0}
        for e in self.entries.values():
            if "input_tokens" in e:
                total["input_tokens"] += e["input_tokens"]
                total["output_tokens"] += e["output_tokens"]
                total["calls"] += 1
        return total

    def save(self, prune: bool = False) -> None:
        """Write the store; ``prune`` (after a complete run) drops entries this run never asked for."""
        if prune:
            for key in set(self.entries) - self.used:
                del self.entries[key]
                self.added += 1
        if not self.added:
            return
        body = {"note": "Recorded answers, keyed by the SHA-256 of each request (ds_toolbox.llm).",
                "entries": dict(sorted(self.entries.items()))}
        self.path.parent.mkdir(parents=True, exist_ok=True)
        tmp = self.path.with_suffix(".tmp")
        tmp.write_text(json.dumps(body, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
        tmp.replace(self.path)
        self.added = 0
