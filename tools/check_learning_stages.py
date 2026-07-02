from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
path = ROOT / "data" / "learning-stages.json"
required = {"Exposure", "Attention", "Interpretation", "Model Formation", "Action or Expression", "Feedback", "Revision", "Responsibility"}
ok = path.exists()
if ok:
    data = json.loads(path.read_text(encoding="utf-8"))
    ok = ok and data.get("schema") == "admissible_existence.learning_transition.stages.v1"
    ok = ok and data.get("repo") == "learning-transition-governance"
    ok = ok and required.issubset(set(data.get("stages", [])))
    ok = ok and data.get("status") == "stages_ready"
    ok = ok and data.get("authority") is False
else:
    print("missing: data/learning-stages.json")
print("valid: learning transition stages" if ok else "learning transition stages check failed")
raise SystemExit(0 if ok else 1)
