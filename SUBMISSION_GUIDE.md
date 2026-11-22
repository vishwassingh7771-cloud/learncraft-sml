# Milestone 3 submission guide

What goes in each field of the Google Form, plus a script for the demo video.

## Form answers

| Q | Field | What to submit |
|---|-------|----------------|
| 6 | GitHub repository link (public) | The repo URL (code, dataset, README, report and slides are all in it) |
| 7 | Project report & technical documentation | `LearnCraft_AI_Final_Project_Report.pdf` (1.3 MB, under the 10 MB limit) |
| 8 | Project PPT (10–20 slides) | `LearnCraft_AI_Final_Presentation.pptx` (14 slides, 1.3 MB) |
| 9 | Demo video link (must be open) | Upload the recording to YouTube (Unlisted) or Google Drive ("Anyone with the link can view"), then paste the link |

Before uploading the report:
- [x] Faculty name (Deepti Shakya) is on the title page, certificate and slide 1.
- [ ] Sign the declaration table.
- [ ] Run your plagiarism check. Everything is written from scratch; only the references are standard text.

## Demo video script (about 5 minutes)

Record the screen with OBS, the Xbox Game Bar (`Win + Alt + R`) or Loom. Each person can present one part.

**0:00–0:40 Intro (Vishwas).** Team names and project title. The problem: one textbook, many reading
levels. LearnCraft rewrites topics for a grade with Gemini, and our ML model checks the result is
actually readable for that grade.

**0:40–1:40 Data and method (Yagnesh).** Show `dataset/clear_corpus.csv` and slide 5 (the flowchart).
Explain the CLEAR corpus (4,723 teacher-rated passages), the 19 features in `ml/features.py`, and TF-IDF.
Mention 5-fold CV, GridSearchCV, and the single held-out test set.

**1:40–2:50 Results (Kushal).** Run `python ml/train.py` (or show its last lines if time is short).
Open `results/figures/04_model_comparison.png`: RMSE 0.936 for Flesch-Kincaid against 0.675 for the best
model, with p ≈ 2.6e-6 on the paired t-test. Show the confusion matrix (63.3%) and the PCA/K-Means plot.

**2:50–4:30 Live app (Vishwas).**
1. Double-click `start_demo.bat`.
2. In the *Readability Inspector*, show the default photosynthesis paragraph: ML class **Easy**.
3. Paste a hard paragraph, for example:
   "Epigenetic mechanisms modulate gene expression without altering the underlying nucleotide sequence.
   DNA methylation and post-translational histone modifications dynamically regulate chromatin
   architecture, thereby governing transcriptional accessibility during cellular differentiation..."
   (repeat it to pass 80 words). Show that it switches to **Hard**.
4. Choose Grade 4 and click *Synthesize Learning Module*. In the backend console or the network response,
   show `adaptiveCheck`: the first draft was rated too hard, so the server asked for a simpler rewrite.
5. Generate the Bloom's taxonomy quiz and answer it to show the feedback banner.

**4:30–5:00 Wrap-up (Yagnesh).** Limitations (short texts, approximate grade mapping) and future work
(DistilBERT, Indian textbook data, a classroom study).
