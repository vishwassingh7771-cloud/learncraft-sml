"""Draws the methodology flowchart used in the final report (Figure 3.1)."""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "figures", "00_methodology_flowchart.png")

fig, ax = plt.subplots(figsize=(8.5, 11))
ax.set_xlim(0, 100)
ax.set_ylim(0, 130)
ax.axis("off")

BLUE, ORANGE, GREEN, GREY, PURPLE = "#DCE8F5", "#FBE3CC", "#D9EEDF", "#EEEEEE", "#E7DDF2"


def box(x, y, w, h, title, body="", color=BLUE, shape="round"):
    style = "round,pad=0.4,rounding_size=1.8" if shape == "round" else "square,pad=0.4"
    ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h, boxstyle=style,
                                fc=color, ec="#333333", lw=1.1))
    if body:
        ax.text(x, y + h * 0.18, title, ha="center", va="center", fontsize=9.5, weight="bold")
        ax.text(x, y - h * 0.18, body, ha="center", va="center", fontsize=7.8, color="#222222")
    else:
        ax.text(x, y, title, ha="center", va="center", fontsize=9.5, weight="bold")


def diamond(x, y, w, h, text):
    ax.add_patch(plt.Polygon([[x, y + h / 2], [x + w / 2, y], [x, y - h / 2], [x - w / 2, y]],
                             fc="#FFF4C2", ec="#333333", lw=1.1))
    ax.text(x, y, text, ha="center", va="center", fontsize=8.3, weight="bold")


def arrow(x1, y1, x2, y2, label=None):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="-|>", color="#333333", lw=1.2))
    if label:
        ax.text((x1 + x2) / 2 + 1, (y1 + y2) / 2, label, fontsize=7.5, color="#555555")


box(50, 124, 46, 7, "Start: CLEAR readability corpus",
    "4,724 passages, teacher-rated BT_easiness", GREY)
arrow(50, 120.3, 50, 116.7)
box(50, 113, 50, 7, "Data cleaning",
    "drop empty / duplicate excerpts  ->  4,723 rows")
arrow(50, 109.3, 50, 105.7)
box(50, 102, 56, 7, "Target definition",
    "regression: BT_easiness   |   classes: Hard / Medium / Easy (tertiles)")
arrow(50, 98.3, 50, 94.7)
box(50, 91, 50, 7, "Stratified train / test split",
    "80% train (3,778)   |   20% test (945), seed 42")
arrow(50, 87.3, 27, 82.7)
arrow(50, 87.3, 73, 82.7)
box(27, 79, 40, 7, "Hand-crafted features (19)",
    "sentence length, syllables, TTR, FRE, FKGL ...", ORANGE)
box(73, 79, 40, 7, "Text vectorisation",
    "TF-IDF word 1-2 grams + char 2-5 grams", ORANGE)
arrow(27, 75.3, 50, 70.7)
arrow(73, 75.3, 50, 70.7)
box(50, 67, 70, 7.5, "Model training with 5-fold cross-validation",
    "Linear, Ridge, Lasso, ElasticNet, KNN, Tree, SVR, RF, GBR, TF-IDF Ridge\n"
    "+ classifiers: LogReg, Naive Bayes, Linear SVM, Random Forest", GREEN)
arrow(50, 63, 50, 59.2)
box(50, 56, 50, 6.5, "Hyper-parameter tuning",
    "GridSearchCV on Ridge alpha, SVR (C, gamma), GBR", GREEN)
arrow(50, 52.5, 50, 48.6)
box(50, 45.5, 60, 6.5, "Evaluation on the untouched test set",
    "RMSE, MAE, R2  |  accuracy, macro-F1  |  paired t-test vs FKGL", GREEN)
arrow(50, 42, 50, 38.6)
diamond(50, 34, 34, 8.5, "Beats FKGL baseline\nsignificantly?")
arrow(67, 34, 79, 34)
ax.text(71, 35.2, "no", fontsize=8)
box(89, 34, 16, 7, "Revise features", "/ parameters", GREY)
ax.plot([89, 89, 87], [37.7, 67, 67], c="#333333", lw=1.2)
arrow(87.5, 67, 85.6, 67)
arrow(50, 29.7, 50, 25.7)
ax.text(51, 27.6, "yes", fontsize=8)
box(50, 22.5, 62, 6.5, "Model export",
    "best pipeline -> joblib   |   Ridge coefficients -> JSON for Node.js", PURPLE)
arrow(50, 19, 50, 15.2)
box(50, 12, 70, 6.5, "LearnCraft app: Gemini writes a module for grade G",
    "ML model scores its difficulty; too hard -> regenerate in simpler language", PURPLE)
arrow(50, 8.5, 50, 5)
box(50, 2.5, 36, 4.5, "End: grade-appropriate module + quiz", "", GREY)

plt.tight_layout()
plt.savefig(OUT, dpi=170, bbox_inches="tight")
print("saved", OUT)
