from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
path = ROOT / "data" / "learning-outcomes.json"
required = {"ADMISSIBLE_DEVELOPMENT", "MEASURED_CHANGE", "CAPTURE_RISK", "INSUFFICIENT_EVIDENCE", "INADMISSIBLE_TRANSITION"}
ok = path.exists()
if ok:
    data = json.loads(path.read_text(encoding="utf-8"))
    ok = ok and data.get("schema") == "admissible_existence.learning_transition.outcomes.v1"
    ok = ok and data.get("repo") == "learning-transition-governance"
    ok = ok and required.issubset(set(data.get("outcomes", [])))
    ok = ok and data.get("status") == "outcomes_ready"
    ok = ok and data.get("authority") is False
else:
    print("missing: data/learning-outcomes.json")
print("valid: learning transition outcomes" if ok else "learning transition outcomes check failed")
raise SystemExit(0 if ok else 1)
