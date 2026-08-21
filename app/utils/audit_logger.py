import json
import logging
from datetime import datetime, timezone
from pathlib import Path


_LOG_PATH = Path(__file__).resolve().parents[2] / "logs" / "audit.log"
_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

_audit_logger = logging.getLogger("construction_audit")
_audit_logger.setLevel(logging.INFO)
_audit_logger.propagate = False
if not _audit_logger.handlers:
	_handler = logging.FileHandler(_LOG_PATH, encoding="utf-8")
	_handler.setFormatter(logging.Formatter("%(message)s"))
	_audit_logger.addHandler(_handler)


def log_audit_event(action: str,actor_id: int,site_id: int,target_user_id: int | None = None,details: dict | None = None,) -> None:
	event = {
		"timestamp": datetime.now(timezone.utc).isoformat(),
		"action": action,
		"actor_id": actor_id,
		"site_id": site_id,
	}
	if target_user_id is not None:
		event["target_user_id"] = target_user_id
	if details:
		event["details"] = details
	_audit_logger.info(json.dumps(event, ensure_ascii=False))
