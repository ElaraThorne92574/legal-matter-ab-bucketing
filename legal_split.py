import hashlib

from infrai import infrai


def bucket(matter_id, experiment="legal-intake-v1"):
    """Return a stable 0..99 bucket for one matter and experiment."""
    digest = hashlib.sha256(f"{experiment}:{matter_id}".encode("utf-8")).hexdigest()
    return int(digest[:8], 16) % 100


def assign_matter(matter, default_value="control"):
    """Choose a treatment and expose the three workflow state transitions."""
    flag = infrai.flags.get_value("legal-intake-v1")
    configured = flag.get("value") if isinstance(flag, dict) else None
    treatment = configured or default_value
    if bucket(matter["matter_id"]) >= 50:
        treatment = "control"
    return {
        "matter_id": matter["matter_id"],
        "treatment": treatment,
        "matter_intake": "received",
        "signed_document_delivery": "queued",
        "deadline_follow_up": "scheduled",
    }

