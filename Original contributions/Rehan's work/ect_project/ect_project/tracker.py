# tracker.py
# Purpose: Track email campaign metrics (sent, failed, etc.).
import os
import json
from config import LOG_DIR

def get_metrics():
    """Read logs and calculate email campaign metrics."""
    sent_count = 0
    failed_count = 0
    log_file = os.path.join(LOG_DIR, "email_logs.log")
    
    if not os.path.exists(log_file):
        return {"sent": 0, "failed": 0, "details": []}
    
    details = []
    with open(log_file, "r") as f:
        for line in f:
            if "Email sent to" in line:
                sent_count += 1
                details.append(line.strip())
            elif "Failed to send email to" in line:
                failed_count += 1
                details.append(line.strip())
    
    return {
        "sent": sent_count,
        "failed": failed_count,
        "details": details
    }

def save_metrics():
    """Save metrics to a JSON file."""
    metrics = get_metrics()
    with open(os.path.join(LOG_DIR, "metrics.json"), "w") as f:
        json.dump(metrics, f, indent=4)
    return metrics