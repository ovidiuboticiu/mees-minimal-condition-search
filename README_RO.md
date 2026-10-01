# MEES — Minimal Epistemic Ecology Search

Acesta este release-ul arhival al proiectului MEES, reconstruit din arhiva supraviețuitoare `Experiment_02.zip`.

## Ce a fost demonstrat

Rezultatul final susținut este restrâns la o clasă **monotonă/factorizabilă** de probleme de căutare a condițiilor minime. METHOD-6 a trecut evaluarea held-out înghețată, iar EXT-3 a trecut un task structural derivat construit peste topologii CausaLab.

## Ce nu a fost demonstrat

- generalizare non-monotonă;
- superioritate generală în causal discovery;
- performanță pe benchmarkul nativ CausaLab;
- universalitatea invariantelor candidate.

Eșecurile METHOD-3, METHOD-4 și METHOD-5 sunt păstrate intenționat și fac parte din delimitarea domeniului de valabilitate.

## Verificare

```bash
python scripts/check_key_results.py
```

## Limitare importantă de reproducibilitate

Arhiva primită conține manifestul și raportul de validare al unui pachet reproducibil mai complet pregătit în august 2026, dar nu conține pachetul respectiv integral. Din acest motiv, repository-ul actual nu pretinde o rerulare end-to-end nouă din toate inputurile originale; el oferă verificare a dovezilor conservate, proveniență, cod înghețat și rezultate brute disponibile.

Pentru detalii, consultați `README.md` și `REPRODUCIBILITY.md`.
