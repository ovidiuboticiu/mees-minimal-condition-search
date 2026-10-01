# MEES — Minimal Epistemic Ecology Search

**Minimal-condition search in artificial ecologies, with retained failures and frozen held-out evaluation.**

MEES is a completed research project investigating a bounded question: given an operational target behavior, can a search procedure recover (1) minimal sufficient configurations, (2) functional substitutions, and (3) monotone appearance/disappearance boundaries under a fixed query budget?

## Status

**Completed / archival research release.** The strongest supported claim is deliberately restricted to a bounded **monotone/factorizable minimal-condition** problem class. Broad non-monotone generalization was tested and **not confirmed**.

This repository was reconstructed from the surviving `Experiment_02.zip` project archive. It preserves the frozen algorithm files that remain in that archive, key preregistration/freeze records, final result summaries, negative evidence, publication audits, and provenance documentation.

## Main results

The final frozen METHOD-6 evaluation reports:

| Metric | Result |
|---|---:|
| Mean minimal-set F1 | 0.9669 |
| Mean substitution F1 | 0.9800 |
| Mean boundary MAE | 0.0000 |
| Mean classification F1 | 0.9807 |
| Mean queries | 159.5 / 180 budget |
| Structural advantage vs. strongest tested baseline | 0.1587 |

The final external structural bridge, EXT-3, reports:

| Metric | Result |
|---|---:|
| Mean minimal-set F1 | 0.9800 |
| Pooled substitution precision | 1.0000 |
| Pooled substitution recall | 0.8750 |
| Pooled substitution F1 | 0.9333 |
| Mean queries | 19.1 / 20 budget |

**Guardrail:** EXT-3 is a derived causal-shielding task over externally authored CausaLab topologies. It is **not** a result on the native CausaLab graph/equation-recovery benchmark.

## Retained negative evidence

The repository intentionally retains the failed confirmatory stages:

- METHOD-3 — `FAIL/NOT-CONCORDANT`
- METHOD-4 — `FAIL/NOT-CONCORDANT`
- METHOD-5 — `FAIL/NOT-CONCORDANT`

The historical validation ledger also records EXT-1 and EXT-2 as failed external stages. Those failures are part of the empirical scope definition, not discarded pilot noise.

## What MEES does **not** claim

The frozen release record explicitly rejects claims that:

- MEES is a generally superior causal-discovery algorithm;
- non-monotone MEES generalization is confirmed;
- MEES passed the native CausaLab benchmark;
- the candidate functional invariants are universal laws;
- the overall framework is entirely unprecedented.

See `evidence/MEES_Manuscript_Release_v1.0.json`.

## Repository map

- `code/` — surviving frozen MEES algorithm implementations.
- `protocols/` — surviving preregistration/freeze records for key confirmatory stages.
- `results/method/` — METHOD-3 through METHOD-6 analysis evidence and the final comparison table.
- `results/external/` — EXT-3 analysis, comparison table, and concordance check.
- `evidence/` — historical builder-side validation and publication/release audits.
- `docs/` — AI-assistance disclosure.
- `scripts/` — lightweight evidence checks for this reconstructed repository.
- `PROVENANCE.md` and `REPRODUCIBILITY.md` — what is preserved, what is missing, and what can honestly be verified.

## Verification

Install the minimal Python dependencies if you want to inspect/compile the frozen source:

```bash
pip install -r requirements.txt
```

Check the preserved headline evidence:

```bash
python scripts/check_key_results.py
```

The check validates the retained METHOD-3/4/5 failures, METHOD-6 PASS and headline metrics, EXT-3 PASS and headline metrics, and the CausaLab guardrail.

### Important reproducibility limitation

The surviving source archive contains historical records showing that a fuller reproducibility package passed a builder-side reproduction in August 2026. However, the complete package itself is **not present** in the supplied `Experiment_02.zip`; some generated/hidden inputs and dedicated reproduction scripts referenced by that historical package are absent.

Therefore this reconstructed repository supports **evidence-level verification, provenance checking, frozen-code inspection, and preservation of the reported results**. It does **not** claim that a fresh end-to-end reproduction of METHOD-6 or EXT-3 has been executed from this reconstructed repository.

See `REPRODUCIBILITY.md` and `PROVENANCE.md`.

## Third-party context

The external bridge used CausaLab causal topologies as described in the preserved project evidence. MEES defined its own shielding task and scorer. See `THIRD_PARTY_NOTICES.md`.

## License and citation

This repository is released under the **MIT License**. See `LICENSE` and `LICENSE_STATUS.md`.

Machine-readable citation metadata is provided in `CITATION.cff`. The current archival version is **1.0.0**; see `RELEASE_NOTES_v1.0.0.md`.

## AI assistance disclosure

The surviving project includes an explicit disclosure under `docs/MEES_AI_Disclosure_v0.1.md`.
