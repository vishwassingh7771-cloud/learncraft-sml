"""Draws the final (Milestone 3) system architecture diagram used in the report."""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "figures", "00_system_architecture.png")

fig, ax = plt.subplots(figsize=(11, 6.2))
ax.set_xlim(0, 110)
ax.set_ylim(4, 60)
ax.axis("off")


def layer(x, y, w, h, title, lines, color):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.3,rounding_size=1.2",
                                fc=color, ec="#333333", lw=1.1))
    ax.text(x + w / 2, y + h - 2.2, title, ha="center", va="center", fontsize=10, weight="bold")
    for i, line in enumerate(lines):
        ax.text(x + 1.5, y + h - 5.6 - i * 2.9, "• " + line, ha="left", va="center", fontsize=8.2)


def arrow(x1, y1, x2, y2, text=None, dy=1.2):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1), arrowprops=dict(arrowstyle="-|>", lw=1.3, color="#333333"))
    if text:
        ax.text((x1 + x2) / 2, (y1 + y2) / 2 + dy, text, ha="center", fontsize=7.6, color="#444444")


layer(1, 32, 24, 26, "1. Client layer", ["index.html (zero-install)", "Next.js 14 page", "grade / subject / topic",
                                         "readability inspector", "quiz console"], "#DCE8F5")
layer(29, 32, 24, 26, "2. API layer (Express)", ["/api/generate-module", "/api/generate-quiz",
                                                  "/api/analyze-reading-level", "/api/curriculum-topics",
                                                  "/api/health"], "#E7DDF2")
layer(57, 32, 24, 26, "3. Readability engine", ["19 hand-crafted features", "Flesch / FKGL / Lexile",
                                                 "Ridge model (JSON)", "difficulty class + band",
                                                 "low-confidence flag"], "#D9EEDF")
layer(85, 32, 24, 26, "4. Generative AI", ["Google Gemini API", "grade-aware prompt",
                                            "module + Bloom quiz", "offline simulator",
                                            "when no API key"], "#FBE3CC")
layer(29, 6, 52, 18, "5. Offline ML training (Python, scikit-learn)",
      ["CLEAR corpus: 4,723 passages", "features + TF-IDF, 5-fold CV, GridSearchCV",
       "11 regressors, 5 classifiers, PCA, K-Means", "exports models/ridge_features.json + joblib"],
      "#EEEEEE")

arrow(25, 45, 29, 45)
arrow(53, 45, 57, 45)
arrow(81, 49, 85, 49, "prompt")
arrow(85, 41, 81, 41, "draft text", dy=-2.6)
arrow(69, 24.5, 69, 31.5, "trained model")
ax.text(97, 22, "Adaptive loop: if the draft is too hard\nfor the chosen grade, the server asks\n"
        "Gemini once more for simpler text.",
        ha="center", va="center", fontsize=7.6, color="#B5403A",
        bbox=dict(boxstyle="round,pad=0.4", fc="white", ec="#B5403A", lw=0.8))
ax.text(13, 29.5, "module + quiz + scores returned to the student", ha="center", fontsize=7.4, color="#444444")
plt.tight_layout()
plt.savefig(OUT, dpi=170, bbox_inches="tight")
print("saved", OUT)
