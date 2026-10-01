# Reproducibility status

## What is directly preserved here

The reconstructed repository contains the surviving frozen implementations, key pre-specified protocols, result summaries for the final methodological sequence, EXT-3 external-bridge evidence, and the historical builder-side validation report.

Repository-level checks added during reconstruction verify the frozen PASS/FAIL verdicts and headline metrics and allow syntax checking of the surviving Python source files.

## What cannot be honestly claimed from the surviving archive

The source archive does not contain every file named in its historical `package_manifest.json`. Missing examples include the full METHOD-6 held-out-world snapshot and several dedicated reproduction scripts from the earlier package.

The historical `BUILD_VALIDATION_REPORT.json` records a builder-side `REPRODUCTION_PASS` from 2026-08-09, but that report is preserved here as historical evidence. It is **not** presented as a reproduction newly executed from this reconstructed repository.

## Verification commands

```bash
python scripts/check_key_results.py
python -m py_compile code/*.py
```

A successful run verifies the preserved public reconstruction only. It does not restore absent historical inputs.
