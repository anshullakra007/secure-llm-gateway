import logging
import json
import os
from datetime import datetime
from fastapi import Request

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

logger = logging.getLogger("security_audit")
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler(os.path.join(LOG_DIR, "security_audit.log"))
file_handler.setFormatter(logging.Formatter('%(message)s'))
logger.addHandler(file_handler)

def log_security_event(request: Request, event_type: str, details: dict):
    """
    Logs a security event in structured JSON format.
    """
    client_ip = request.client.host if request.client else "unknown"
    log_entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "client_ip": client_ip,
        "event_type": event_type,
        "details": details
    }
    logger.info(json.dumps(log_entry))
