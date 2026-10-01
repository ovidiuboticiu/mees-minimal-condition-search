#!/usr/bin/env python3
"""Verify headline MEES results from preserved analysis JSON files."""
from pathlib import Path
import json, math, sys
ROOT = Path(__file__).resolve().parents[1]

def load(rel):
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))

def close(a,b,tol=1e-12):
    return math.isclose(float(a), float(b), rel_tol=0.0, abs_tol=tol)

checks=[]
def expect(label, cond):
    checks.append((label,bool(cond)))

for name in ("3","4","5"):
    d=load(f"results/method/MEES-METHOD-{name}_HELDOUT_analysis.json")
    expect(f"METHOD-{name} retained failure", d.get("overall_verdict") == "FAIL/NOT-CONCORDANT")

d=load("results/method/MEES-METHOD-6_HELDOUT_analysis.json")
m=d["MonotoneMEES_v1.1"]
expect("METHOD-6 PASS", d.get("overall_verdict") == "PASS")
expect("METHOD-6 minimal-set F1", close(m["mean_minimal_set_F1"],0.9669108669108668))
expect("METHOD-6 substitution F1", close(m["mean_substitution_F1"],0.98))
expect("METHOD-6 boundary MAE", close(m["mean_boundary_MAE"],0.0))
expect("METHOD-6 mean queries", close(m["mean_queries"],159.5))
expect("METHOD-6 structural advantage", close(d["structural_advantage"],0.15870976849237706))

e=load("results/external/MEES-EXT-3_analysis.json")
expect("EXT-3 PASS", e.get("overall_verdict") == "PASS")
expect("EXT-3 minimal-set F1", close(e["MEES_mean_minimal_set_F1"],0.98))
expect("EXT-3 substitution precision", close(e["MEES_pooled_substitution_precision"],1.0))
expect("EXT-3 substitution recall", close(e["MEES_pooled_substitution_recall"],0.875))
expect("EXT-3 substitution F1", close(e["MEES_pooled_substitution_F1"],0.9333333333333333))
expect("EXT-3 mean queries", close(e["MEES_mean_queries"],19.1))
expect("EXT-3 guardrail present", "not native CausaLab" in e.get("guardrail", ""))

failed=[label for label,ok in checks if not ok]
for label,ok in checks:
    print(("PASS" if ok else "FAIL") + " - " + label)
print()
print(f"{len(checks)-len(failed)}/{len(checks)} checks passed")
sys.exit(1 if failed else 0)
