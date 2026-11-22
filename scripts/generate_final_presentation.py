"""Builds the Milestone 3 presentation (14 slides) from results/ and figures/.

    python scripts/generate_final_presentation.py
"""
import json
import os

import pandas as pd
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIG = os.path.join(ROOT, "results", "figures")
SHOT = os.path.join(ROOT, "results", "screenshots")
OUT = os.path.join(ROOT, "LearnCraft_AI_Final_Presentation.pptx")
M = json.load(open(os.path.join(ROOT, "results", "metrics.json")))
REG = pd.read_csv(os.path.join(ROOT, "results", "regression_results.csv"))
CLF = pd.read_csv(os.path.join(ROOT, "results", "classification_results.csv"))

NAVY = RGBColor(0x1F, 0x3A, 0x5F)
ACCENT = RGBColor(0xD9, 0x82, 0x2B)
GREY = RGBColor(0x55, 0x55, 0x55)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)

prs = Presentation()
prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
BLANK = prs.slide_layouts[6]
best = REG[REG.Model == "Features + TF-IDF + Ridge (tuned)"].iloc[0]
fk = REG[REG.Model == "FKGL only (linear)"].iloc[0]


def text(slide, x, y, w, h, s, size=18, bold=False, color=GREY, align=PP_ALIGN.LEFT):
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    lines = s if isinstance(s, list) else [s]
    for i, line in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        p.space_after = Pt(8)
        r = p.add_run()
        r.text = line
        r.font.size = Pt(size)
        r.font.bold = bold
        r.font.color.rgb = color
    return tb


def slide(title, number=True):
    s = prs.slides.add_slide(BLANK)
    bar = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, Inches(0.12))
    bar.fill.solid(); bar.fill.fore_color.rgb = ACCENT; bar.line.fill.background()
    text(s, 0.6, 0.35, 12, 0.9, title, 30, True, NAVY)
    if number:
        text(s, 12.2, 6.95, 1, 0.4, str(len(prs.slides._sldIdLst)), 11, color=GREY, align=PP_ALIGN.RIGHT)
        text(s, 0.6, 6.95, 8, 0.4, "LearnCraft AI  |  SML Lab Milestone 3", 11, color=GREY)
    return s


def bullets(s, items, x=0.7, y=1.5, w=6.2, h=5, size=19):
    return text(s, x, y, w, h, ["•  " + i for i in items], size)


def pic(s, path, x, y, w=None, h=None):
    kw = {}
    if w: kw["width"] = Inches(w)
    if h: kw["height"] = Inches(h)
    return s.shapes.add_picture(path, Inches(x), Inches(y), **kw)


# 1 Title
s = prs.slides.add_slide(BLANK)
bg = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
bg.fill.solid(); bg.fill.fore_color.rgb = NAVY; bg.line.fill.background()
text(s, 0.9, 1.6, 11.5, 1.2, "LearnCraft AI", 48, True, WHITE)
text(s, 0.9, 2.6, 11.5, 1.4, "Predicting text readability with statistical machine learning\n"
                             "for a curriculum-adaptive study assistant", 26, False, WHITE)
text(s, 0.9, 4.3, 11.5, 0.5, "Statistical Machine Learning Lab  •  Milestone 3: Final Project", 18, False,
     RGBColor(0xF3, 0xC9, 0x9B))
text(s, 0.9, 5.2, 11.5, 1.2, ["Vishwas Singh (S25CSEU0018)  •  Yagnesh (S25CSEU0031)  •  Kushal (S25CSEU0016)",
                              "Bennett University  •  Under the guidance of [Faculty Name]"], 16, False, WHITE)

# 2 Problem
s = slide("The problem")
bullets(s, ["One textbook, thirty different reading levels in a class",
            "LearnCraft uses Gemini to rewrite a topic for a chosen grade and builds a Bloom's-taxonomy quiz",
            "But “write for Grade 4” is not a guarantee: we need to measure how hard the output really is",
            "Mid-term used the Flesch-Kincaid formula, which only counts sentence length and syllables",
            "Goal: a model that matches human difficulty judgements better and is light enough to run in the app"],
        w=7.2)
pic(s, os.path.join(SHOT, "app_inspector.png"), 8.6, 1.4, h=5.2)

# 3 Objectives / SDG
s = slide("Objectives and SDG 4 link")
bullets(s, ["Replace the synthetic mid-term data (only 15 unique passages) with a real labelled corpus",
            "Engineer interpretable linguistic features plus TF-IDF text features",
            "Compare 11 regressors and 5 classifiers with 5-fold CV and a held-out test set",
            "Test significance against the Flesch-Kincaid baseline",
            "Deploy the model inside the backend to drive an adaptive “too hard? simplify” loop",
            "SDG 4 (Quality Education): inclusive learning material for every reading level"], w=12)

# 4 Dataset
d = M["data"]
s = slide("Dataset: CommonLit CLEAR corpus")
bullets(s, [f"{d['rows_clean']:,} passages (140–200 words), Grades 3–12",
            f"{d['lit']:,} literature  •  {d['info']:,} informational",
            "Target: BT_easiness from teachers' pairwise comparisons (higher = easier)",
            f"Classes by tertile: Hard < {d['tertile_cuts'][0]:.2f} < Medium < {d['tertile_cuts'][1]:.2f} < Easy",
            "Stratified 80/20 split: 3,778 train / 945 test, seed 42",
            "Public release, CC BY-NC-SA 4.0 (Crossley et al., 2023)"], w=5.6, size=18)
pic(s, os.path.join(FIG, "01_target_distribution.png"), 6.4, 1.6, w=6.6)

# 5 Methodology flowchart
s = slide("Proposed methodology")
pic(s, os.path.join(FIG, "00_methodology_flowchart.png"), 0.6, 1.2, h=5.7)
bullets(s, ["Clean → define targets → split once",
            "Two representations: 19 hand-crafted features and TF-IDF word + character n-grams",
            "5-fold CV for every model, GridSearchCV for the top three",
            "Test set touched once at the end",
            "Export → Node.js backend → adaptive regeneration"], x=5.6, y=1.6, w=7.2, size=18)

# 6 Features
s = slide("Feature engineering")
bullets(s, ["Sentence: average / SD / max length",
            "Word: length, syllables, % long words, % 3+ syllable words, % one-syllable words",
            "Vocabulary: type-token ratio, root TTR, % very common words",
            "Punctuation: commas, ; and :, quote density",
            "Formulas: Flesch Reading Ease, Flesch-Kincaid Grade",
            "Same code ported to JavaScript; parity test max |diff| ≈ 5×10⁻¹¹"], w=5.8, size=17)
pic(s, os.path.join(FIG, "02_feature_correlations.png"), 6.7, 1.3, w=6.2)

# 7 Models
s = slide("Models compared")
rows = [("Baselines", "Mean, linear regression on FKGL"),
        ("Linear", "OLS, Ridge, Lasso, Elastic Net"),
        ("Instance / kernel", "KNN (k=15), SVR (RBF)"),
        ("Trees", "Decision Tree, Random Forest, Gradient Boosting"),
        ("Text", "Ridge on TF-IDF words, characters, words + features"),
        ("Classifiers", "Logistic Regression, RF, Naive Bayes, Linear SVM"),
        ("Unsupervised", "PCA, K-Means (k = 3)")]
tbl = s.shapes.add_table(len(rows) + 1, 2, Inches(0.8), Inches(1.5), Inches(11.7), Inches(4.6)).table
tbl.columns[0].width, tbl.columns[1].width = Inches(3.2), Inches(8.5)
for j, h in enumerate(("Family", "Models")):
    tbl.cell(0, j).text = h
for i, (a, b) in enumerate(rows, 1):
    tbl.cell(i, 0).text, tbl.cell(i, 1).text = a, b
for i in range(len(rows) + 1):
    for j in range(2):
        for p in tbl.cell(i, j).text_frame.paragraphs:
            for r in p.runs:
                r.font.size = Pt(17)

# 8 Regression results
s = slide("Regression results (held-out test set)")
pic(s, os.path.join(FIG, "04_model_comparison.png"), 0.4, 1.2, w=7.6)
text(s, 8.3, 1.6, 4.7, 5, [f"Best: Features + TF-IDF + Ridge (tuned)",
                           f"RMSE {best.RMSE:.3f}  •  R² {best.R2:.2f}",
                           f"FKGL baseline: RMSE {fk.RMSE:.3f}  •  R² {fk.R2:.2f}",
                           "Text representation mattered more than the learner: features-only models plateau "
                           "around 0.81–0.85",
                           "Ensemble with boosting was slightly worse (0.700), a useful negative result"], 17)

# 9 Significance + residuals
tt = M["ttest_text_vs_fkgl"]
s = slide("Is it really better? Significance and errors")
pic(s, os.path.join(FIG, "05_pred_vs_actual.png"), 0.5, 1.4, w=7.6)
text(s, 8.4, 1.5, 4.5, 5, [f"Paired t-test on 5 CV folds vs FKGL: t = {tt['t']:.1f}, p = {tt['p']:.1e}",
                           "Model won on every fold by > 0.2 RMSE",
                           f"Residual mean {M['residuals']['mean']:.3f}, SD {M['residuals']['sd']:.3f}",
                           "Worst errors: 1880s–1920s prose with old-fashioned phrasing; modern children's "
                           "stories with unfamiliar names"], 17)

# 10 Tuning + learning curve + importance
s = slide("Tuning, feature importance and learning curve")
pic(s, os.path.join(FIG, "06_permutation_importance.png"), 0.4, 1.3, w=6.2)
pic(s, os.path.join(FIG, "07_learning_curve.png"), 6.8, 1.3, w=6.1)
text(s, 6.9, 5.4, 6, 1.4, ["Best Ridge α = 0.5; validation RMSE still falling at 3,000 passages, "
                           "so more labelled data would help"], 16)

# 11 Classification
s = slide("Classification: Hard / Medium / Easy")
pic(s, os.path.join(FIG, "09_confusion_matrix.png"), 7.4, 1.4, h=4.7)
lines = [f"{r.Model}: {r.Accuracy*100:.1f}%" for _, r in CLF.iterrows()]
text(s, 0.7, 1.5, 7, 5, ["Accuracy (chance = 33%)"] + ["•  " + l for l in lines] +
     ["Medium is hardest (F1 0.49); Hard↔Easy confusions are rare (18 of 315)"], 17)

# 12 Unsupervised
s = slide("Unsupervised view: PCA and K-Means")
pic(s, os.path.join(FIG, "10_pca_kmeans.png"), 0.6, 1.3, w=12.1)
text(s, 0.7, 6.15, 12, 0.8, f"Clusters match difficulty weakly (ARI {M['pca']['kmeans_ari_vs_difficulty']:.2f}) "
                            "and genre more (ARI 0.23), so supervision is needed", 16)

# 13 Deployment
s = slide("Deployment and the adaptive loop")
pic(s, os.path.join(FIG, "00_system_architecture.png"), 0.4, 1.3, w=7.6)
bullets(s, ["Light Ridge model on 19 features exported as JSON (test RMSE "
            f"{M['deployed_light_model']['RMSE']:.3f}, still far better than FKGL)",
            "Runs in Node.js and in the browser, no Python needed",
            "Grades 3–5 accept Easy text, 6–8 Easy/Medium, 9–12 any",
            "Too hard → server asks Gemini once more for simpler wording",
            "< 80 words → low-confidence flag"], x=8.2, y=1.4, w=4.8, size=16)

# 14 Conclusion
s = slide("Conclusion and future work")
bullets(s, [f"RMSE {fk.RMSE:.3f} → {best.RMSE:.3f} and R² {fk.R2:.2f} → {best.R2:.2f} over Flesch-Kincaid on "
            "real teacher-rated data",
            "Lesson: representation > choice of learner; check your data for duplicates",
            "The adaptive loop now actually works inside the app",
            "Next: DistilBERT alongside Ridge, grade-level word lists, Indian textbook passages, a classroom study",
            "Code, data and README: GitHub (link in the submission form)"], w=12, size=19)
text(s, 0.7, 6.2, 12, 0.6, "Thank you  •  Questions?", 22, True, NAVY)

prs.save(OUT)
print("saved", OUT, "slides:", len(prs.slides._sldIdLst))
