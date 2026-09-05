#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "formalism" / "triform-manifest.json"
EXPECTED = ["LTG-P001", "LTG-P002", "LTG-P003", "LTG-P004"]


def validate(data=None):
    data = data or json.loads(MANIFEST.read_text(encoding="utf-8"))
    findings=[]
    if data.get("schema") != "admissible-existence.ltg-triform-manifest/v1": findings.append("schema")
    if data.get("maturity") != "TRIFORM_BOUND_CANDIDATE": findings.append("maturity")
    if data.get("authority_effect") is not False: findings.append("authority_effect")
    if data.get("proof_promotion") is not False: findings.append("proof_promotion")
    if data.get("identity_capture") is not False: findings.append("identity_capture")
    if data.get("predetermined_intellectual_destination") is not False: findings.append("predetermined_destination")
    principles=data.get("principles",[])
    ids=[p.get("id") for p in principles]
    if ids != EXPECTED: findings.append(f"principle_ids:{ids}")
    for p in principles:
        pid=p.get("id","UNKNOWN")
        for key in ("prose","mathematics","code","tests"):
            vals=p.get(key,[])
            if not vals: findings.append(f"empty:{pid}:{key}")
            for rel in vals:
                path=ROOT/rel
                if rel.endswith("/"):
                    if not path.is_dir(): findings.append(f"missing_dir:{pid}:{rel}")
                elif not path.exists(): findings.append(f"missing_file:{pid}:{rel}")
        if not p.get("binding"): findings.append(f"missing_binding:{pid}")
    required_non_auth=("ae_admissibility","execution","publication","release","certification","credential","custody","predetermined_identity")
    non=data.get("non_authority",{})
    for key in required_non_auth:
        if non.get(key) is not False: findings.append(f"non_authority:{key}")
    return findings


def main():
    findings=validate()
    print(json.dumps({"valid":not findings,"principle_count":4,"findings":findings,"authority_effect":False},indent=2,sort_keys=True))
    raise SystemExit(0 if not findings else 1)

if __name__ == "__main__": main()
