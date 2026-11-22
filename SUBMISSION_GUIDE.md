# Milestone 3 submission guide

What goes in each field of the Google Form, plus a script for the demo video.

## Form answers

| Q | Field | What to submit |
|---|-------|----------------|
| 6 | GitHub repository link (public) | The repo URL (code, dataset, README, report and slides are all in it) |
| 7 | Project report & technical documentation | `LearnCraft_AI_Final_Project_Report.pdf` (1.3 MB, under the 10 MB limit) |
| 8 | Project PPT (10–20 slides) | `LearnCraft_AI_Final_Presentation.pptx` (15 slides) |
| 9 | Demo video link (must be open) | Upload the recording to YouTube (Unlisted) or Google Drive ("Anyone with the link can view"), then paste the link |

Before uploading the report:
- [x] Faculty name (Ms. Deepti Shakya) is on the title page, certificate and slide 1.
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
1. Double-click `start_demo.bat`. The pill at the top right should say **Connected · Gemini AI**.
2. **Learn a topic** tab: click grade **5**, then the **Water cycle** chip. Point out the three steps at the
   top and the green box saying "Good fit for Grade 5". If it also says the first draft was rewritten, that
   is the adaptive loop in action.
3. Click **Read aloud** for a few seconds, then stop it.
4. Answer the quiz with one wrong answer on purpose. Show that **Check my answers** stays locked until all
   three are answered. Then show the explanations and the suggested next step.
5. Click grade **3**, choose **Ohm's law** and press **Create my lesson**. If it is rated too hard, click
   **Make it simpler**.
6. **Check any text** tab: click **Easy sample** (Easy, good fit), then **Hard sample** with grade 6 selected
   ("Might be hard for Grade 6" plus tips). Open **Details for teachers** to show the ML score next to
   Flesch-Kincaid.

**4:30–5:00 Wrap-up (Yagnesh).** Limitations (short texts, approximate grade mapping) and future work
(DistilBERT, Indian textbook data, a classroom study).
