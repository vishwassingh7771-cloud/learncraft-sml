# Dataset

| File | What it is |
|------|------------|
| `clear_corpus.csv` | The CommonLit Ease of Readability (CLEAR) corpus, trimmed to the columns we use (4,724 rows). |
| `clear_features.csv` | Output of `ml/train.py`: our 19 hand-crafted features per passage plus the target and class. |

**Source:** https://github.com/scrosseye/CLEAR-Corpus (file `CLEAR_corpus_final.xlsx`).

**Licence:** CC BY-NC-SA 4.0. The data is redistributed here unchanged except for dropping columns,
for non-commercial academic use, with attribution:

> Crossley, S. A., Heintz, A., Choi, J. S., Batchelor, J., Karimi, M., & Malatinszky, A. (2023).
> A large-scaled corpus for assessing text readability. *Behavior Research Methods, 55*, 491–507.

Key columns: `Excerpt` (passage text), `BT_easiness` (target, higher = easier), `s.e.` (standard error),
`Categ` (Lit / Info).
