import json
from datetime import datetime, timezone
from pathlib import Path

def build_search_event(
        query:str, 
        results:list[tuple[str, int]],
        elapsed_ms:float
) -> dict:
    # TODO:返回事件字典
    event = {}
    event["timestamp"] = datetime.now(timezone.utc).isoformat()
    event["query"] = query
    event["results"] = [
    {"filename": filename, "score": score}
    for filename, score in results
]
    event["elapsed_ms"] = elapsed_ms
    return event

def event_to_json(event:dict) -> str:
    # TODO: 使用json.dumps转成字符串
    return json.dumps(event, ensure_ascii=False)

def append_event(log_path:str, event:dict) -> None:
    path = Path(log_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as file:
        file.write(event_to_json(event) + '\n')
