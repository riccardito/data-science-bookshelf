import json
import types

import pytest

from ds_toolbox import llm


def test_replay_record_and_prune(tmp_path):
    path = tmp_path / "rec.json"
    calls = []

    def fake(client, request):
        calls.append(request["x"])
        return {"answer": request["x"] * 2}, {"input_tokens": 10, "output_tokens": 3}

    rec = llm.Recorder(path, call=fake, live=True)
    assert rec.ask({"task": "t", "x": 2}) == {"answer": 4}
    assert rec.ask({"task": "t", "x": 2}) == {"answer": 4}
    assert calls == [2]
    rec.ask({"task": "t", "x": 5})
    rec.save()
    assert rec.usage() == {"input_tokens": 20, "output_tokens": 6, "calls": 2}

    replay = llm.Recorder(path)
    assert replay.ask({"task": "t", "x": 5}) == {"answer": 10}
    assert replay.missing([{"task": "t", "x": 5}, {"task": "t", "x": 9}]) == [{"task": "t", "x": 9}]
    with pytest.raises(llm.MissingRecording, match="run live"):
        replay.ask({"task": "t", "x": 9})
    replay.save(prune=True)                       # only x=5 was asked for this run
    assert len(json.loads(path.read_text(encoding="utf-8"))["entries"]) == 1


def test_key_ignores_dict_order():
    assert llm.request_key({"a": 1, "b": 2}) == llm.request_key({"b": 2, "a": 1})


def test_api_key_from_env(monkeypatch):
    monkeypatch.setenv("ANTHROPIC_API_KEY", "k")
    assert llm.api_key() == "k"


def _response(stop="end_turn", text='{"ok": true}'):
    return types.SimpleNamespace(
        stop_reason=stop, model="claude-opus-5-5", stop_details=types.SimpleNamespace(category="x"),
        content=[types.SimpleNamespace(type="thinking"), types.SimpleNamespace(type="text", text=text)],
        usage=types.SimpleNamespace(input_tokens=7, output_tokens=2))


class _Client:
    def __init__(self, response):
        self.sent = None
        outer = self

        class Messages:
            def create(self, **kw):
                outer.sent = kw
                return response

        self.beta = types.SimpleNamespace(messages=Messages())


REQ = {"model": llm.MODEL, "effort": "low", "system": "s", "user": "u", "schema": {"type": "object"}}


def test_call_claude_sends_the_structured_request():
    client = _Client(_response())
    out, meta = llm.call_claude(client, REQ)
    assert out == {"ok": True} and meta["served_by"] == "claude-opus-5-5" and meta["input_tokens"] == 7
    assert client.sent["fallbacks"] == "default" and client.sent["betas"] == [llm.FALLBACK_BETA]
    assert client.sent["output_config"]["format"]["type"] == "json_schema"


def test_call_claude_refusal_and_truncation():
    with pytest.raises(llm.Refused, match="x"):
        llm.call_claude(_Client(_response(stop="refusal")), REQ)
    with pytest.raises(RuntimeError, match="max_tokens"):
        llm.call_claude(_Client(_response(stop="max_tokens")), REQ)


def test_a_live_run_saves_as_it_goes(tmp_path):
    path = tmp_path / "rec.json"
    rec = llm.Recorder(path, call=lambda c, r: ({"v": r["x"]}, {}), live=True, save_every=3)
    for x in range(3):
        rec.ask({"x": x})
    assert len(json.loads(path.read_text(encoding="utf-8"))["entries"]) == 3   # written before save()
