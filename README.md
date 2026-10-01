# MEES — Minimal Epistemic Ecology Search

**Minimal-condition search in artificial ecologies, with retained failures and frozen held-out evaluation.**

MEES is a completed research project investigating a bounded question: given an operational target behavior, can a search procedure recover (1) minimal sufficient configurations, (2) functional substitutions, and (3) monotone appearance/disappearance boundaries under a fixed query budget?

## Status

**Completed / archival research release.** The strongest supported claim is deliberately restricted to a bounded **monotone/factorizable minimal-condition** problem class. Broad non-monotone generalization was tested and **not confirmed**.

This repository is reconstructed from the surviving `Experiment_02.zip` project archive. It preserves the frozen code, protocols, key results, negative evidence, claim-boundary documents, release-candidate manuscript, and publication audit available in that archive.

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

The repository intentionally keeps failed confirmatory stages:

- METHOD-3 — `FAIL/NOT-CONCORDANT`
- METHOD-4 — `FAIL/NOT-CONCORDANT`
- METHOD-5 — `FAIL/NOT-CONCORDANT`
- EXT-1 and EXT-2 are recorded in the historical evidence ledgers as failed external stages.

Those failures are part of the empirical scope definition, not discarded pilot noise.

## What MEES does **not** claim

This repository does **not** support claims that:

- MEES is a generally superior causal-discovery algorithm;
- non-monotone MEES generalization is confirmed;
- MEES passed the native CausaLab benchmark;
- the candidate functional invariants are universal laws;
- the individual algorithmic components are unprecedented.

See `evidence/MEES_Manuscript_Release_v1.0.json` and the manuscript for the frozen claim boundary.

## Repository map

- `code/` — surviving frozen MEES implementations.
- `protocols/` — surviving pre-specified/hash-frozen protocols for key confirmatory stages.
- `results/method/` — METHOD-1 through METHOD-6 evidence used to establish the final scope.
- `results/external/` — surviving EXT-3 external-bridge results and concordance check.
- `evidence/` — checkpoints, ledgers, claim freezes, validation report, and editorial red-team audit.
- `figures/` — surviving final-result figures from the source archive.
- `manuscript/` — release-candidate manuscript and PDF preserved as historical artifacts.
- `archive/` — provenance index plus the historical reproducibility-package manifest.
- `scripts/` — repository-level integrity and evidence checks added during public reconstruction.

## Verification

From the repository root:

```bash
python scripts/check_key_results.py
python scripts/verify_repository.py
```

The first command checks the frozen verdicts and headline metrics against the preserved JSON evidence. The second checks SHA-256 hashes for all files listed in `MANIFEST_SHA256.json`.

### Important reproducibility limitation

The surviving source archive contains `package_manifest.json` and an August 2026 build report for an earlier full reproducibility package, but it does **not** contain that complete package itself. In particular, some world snapshots and reproduction scripts named in the historical manifest are absent from `Experiment_02.zip`.

Therefore this reconstructed repository supports **evidence-level verification, provenance checking, code inspection, and preservation of the frozen results**, but it does **not** claim a fresh end-to-end reproduction of METHOD-6/EXT-3 from all original hidden/generated inputs. See `REPRODUCIBILITY.md`.

## Manuscript

The release-candidate manuscript is preserved under `manuscript/`. Its Markdown references two figure assets that are not present in the surviving archive; the preserved PDF is the more complete historical rendering.

## Third-party context

The external bridge used CausaLab causal topologies as described in the project evidence. MEES's shielding task and scorer were separately defined. See `THIRD_PARTY_NOTICES.md` and the manuscript for the distinction.

## License status

No open-source/content license has been selected in the surviving project record. The repository is made available for inspection and archival transparency; see `LICENSE_STATUS.md` before reusing code, data, text, or figures.

## AI assistance disclosure

The surviving project includes an explicit AI-assistance disclosure under `docs/MEES_AI_Disclosure_v0.1.md`.
