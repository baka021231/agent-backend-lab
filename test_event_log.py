from event_log import build_search_event, event_to_json, append_event
import json
from pathlib import Path
from tempfile import TemporaryDirectory

with TemporaryDirectory() as temp_dir:
    log_path = Path(temp_dir) / "logs" / "events.jsonl"
    res = event_to_json(build_search_event("python agent", [("python.md", 4)], 12.5))

    append_event(str(log_path), build_search_event("python agent", [("python.md", 4)], 12.5))
    append_event(str(log_path), build_search_event("中文查询", [("python.md", 4)], 12.5))
    lines = log_path.read_text(encoding="utf-8").splitlines()
    events = [json.loads(line) for line in lines]

    assert len(events) == 2
    assert events[0]["query"] == "python agent"
    assert events[1]["query"] == "中文查询"

    assert events[0]["results"] == [
        {"filename": "python.md", "score": 4}
    ]
    assert events[0]["elapsed_ms"] == 12.5

    assert events[1]["results"] == [
        {"filename": "python.md", "score": 4}
    ]
    assert events[1]["elapsed_ms"] == 12.5