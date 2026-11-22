"""
Builds the Milestone 3 final report (DOCX) from results/metrics.json and the
figures in results/figures. Formatting follows the lab guidelines:
Times New Roman 12, chapter headings 16 bold, 1.5 line spacing.

    python scripts/generate_final_report.py
"""
import json
import os

import pandas as pd
from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK, WD_LINE_SPACING
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIG = os.path.join(ROOT, "results", "figures")
SHOT = os.path.join(ROOT, "results", "screenshots")
OUT = os.path.join(ROOT, "LearnCraft_AI_Final_Project_Report.docx")
M = json.load(open(os.path.join(ROOT, "results", "metrics.json")))
REG = pd.read_csv(os.path.join(ROOT, "results", "regression_results.csv"))
CLF = pd.read_csv(os.path.join(ROOT, "results", "classification_results.csv"))

TEAM = [("Vishwas Singh", "S25CSEU0018"), ("Yagnesh", "S25CSEU0031"), ("Kushal", "S25CSEU0016")]
FONT = "Times New Roman"


def r(name):
    row = REG[REG.Model == name].iloc[0]
    return row


# ---------------------------------------------------------------- helpers ---
doc = Document()
sec = doc.sections[0]
sec.page_height, sec.page_width = Cm(29.7), Cm(21.0)
sec.left_margin = sec.right_margin = sec.top_margin = sec.bottom_margin = Cm(2.54)


def set_font(style, size, bold=False, italic=False):
    style.font.name = FONT
    style.font.size = Pt(size)
    style.font.bold = bold
    style.font.italic = italic
    style.font.color.rgb = RGBColor(0, 0, 0)
    rpr = style.element.get_or_add_rPr()
    rfonts = rpr.find(qn("w:rFonts"))
    if rfonts is None:
        rfonts = OxmlElement("w:rFonts")
        rpr.append(rfonts)
    for k in ("w:ascii", "w:hAnsi", "w:eastAsia", "w:cs"):
        rfonts.set(qn(k), FONT)
    for k in ("w:asciiTheme", "w:hAnsiTheme", "w:eastAsiaTheme", "w:cstheme"):
        if rfonts.get(qn(k)) is not None:
            del rfonts.attrib[qn(k)]


normal = doc.styles["Normal"]
set_font(normal, 12)
normal.paragraph_format.line_spacing = 1.5
normal.paragraph_format.space_after = Pt(6)
normal.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

for name, size in (("Heading 1", 16), ("Heading 2", 14), ("Heading 3", 12)):
    st = doc.styles[name]
    set_font(st, size, bold=True)
    st.paragraph_format.line_spacing = 1.5
    st.paragraph_format.space_before = Pt(12 if name != "Heading 1" else 0)
    st.paragraph_format.space_after = Pt(6 if name != "Heading 1" else 18)
    st.paragraph_format.keep_with_next = True
    st.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
doc.styles["Heading 1"].paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER

for cname in ("Figure Caption", "Table Caption"):
    st = doc.styles.add_style(cname, 1)
    st.base_style = normal
    set_font(st, 11, italic=False)
    st.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    st.paragraph_format.space_after = Pt(10)
    st.paragraph_format.line_spacing = 1.15
doc.styles["Table Caption"].paragraph_format.keep_with_next = True


def para(text="", bold=False, italic=False, align=None, size=None, space_after=None, style=None):
    p = doc.add_paragraph(style=style)
    if text:
        add_runs(p, text, bold, italic, size)
    if align is not None:
        p.alignment = align
    if space_after is not None:
        p.paragraph_format.space_after = Pt(space_after)
    return p


def add_runs(p, text, bold=False, italic=False, size=None):
    """Very small markup: **bold** segments inside text."""
    parts = text.split("**")
    for i, part in enumerate(parts):
        if not part:
            continue
        run = p.add_run(part)
        run.bold = bold or (i % 2 == 1)
        run.italic = italic
        if size:
            run.font.size = Pt(size)


def bullets(items, numbered=False):
    for it in items:
        p = doc.add_paragraph(style="List Number" if numbered else "List Bullet")
        add_runs(p, it)
        p.paragraph_format.space_after = Pt(3)


def front_title(title, new_page=True):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.page_break_before = new_page
    p.paragraph_format.space_after = Pt(18)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(title)
    run.bold = True
    run.font.size = Pt(16)
    return p


def chapter(title):
    doc.add_heading(title, level=1).paragraph_format.page_break_before = True


def h2(t):
    doc.add_heading(t, level=2)


def h3(t):
    doc.add_heading(t, level=3)


def figure(path, caption, width_cm=15.0):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.keep_with_next = True
    p.paragraph_format.line_spacing = 1.0
    p.add_run().add_picture(path, width=Cm(width_cm))
    doc.add_paragraph(caption, style="Figure Caption")


def figure_pair(p1, p2, caption, w1=7.8, w2=7.8):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.keep_with_next = True
    p.paragraph_format.line_spacing = 1.0
    p.add_run().add_picture(p1, width=Cm(w1))
    p.add_run("  ")
    p.add_run().add_picture(p2, width=Cm(w2))
    doc.add_paragraph(caption, style="Figure Caption")


def shade(cell, hex_fill):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), hex_fill)
    tcPr.append(shd)


def table(caption, header, rows, widths=None, font=10.5, bold_rows=()):
    doc.add_paragraph(caption, style="Table Caption")
    t = doc.add_table(rows=1, cols=len(header))
    t.style = "Table Grid"
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, h in enumerate(header):
        c = t.rows[0].cells[i]
        c.text = ""
        run = c.paragraphs[0].add_run(h)
        run.bold = True
        run.font.size = Pt(font)
        shade(c, "D9E2F3")
    for ri, row in enumerate(rows):
        cells = t.add_row().cells
        for i, v in enumerate(row):
            cells[i].text = ""
            run = cells[i].paragraphs[0].add_run(str(v))
            run.font.size = Pt(font)
            run.bold = ri in bold_rows
    for row in t.rows:
        for i, c in enumerate(row.cells):
            for p in c.paragraphs:
                p.paragraph_format.line_spacing = 1.0
                p.paragraph_format.space_after = Pt(1)
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT if i == 0 else WD_ALIGN_PARAGRAPH.CENTER
            if widths:
                c.width = Cm(widths[i])
    doc.add_paragraph().paragraph_format.space_after = Pt(2)
    return t


def field(paragraph, instr):
    run = paragraph.add_run()
    b = OxmlElement("w:fldChar"); b.set(qn("w:fldCharType"), "begin")
    i = OxmlElement("w:instrText"); i.set(qn("xml:space"), "preserve"); i.text = instr
    s = OxmlElement("w:fldChar"); s.set(qn("w:fldCharType"), "separate")
    t = OxmlElement("w:t"); t.text = "Right-click and choose Update Field."
    e = OxmlElement("w:fldChar"); e.set(qn("w:fldCharType"), "end")
    for el in (b, i, s, t, e):
        run._r.append(el)


def page_number_footer(section, fmt="decimal", start=None):
    pgNumType = OxmlElement("w:pgNumType")
    pgNumType.set(qn("w:fmt"), fmt)
    if start is not None:
        pgNumType.set(qn("w:start"), str(start))
    section._sectPr.append(pgNumType)
    footer = section.footer
    footer.is_linked_to_previous = False
    p = footer.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    for run in list(p.runs):
        run._r.getparent().remove(run._r)
    field(p, "PAGE")


f2 = lambda x: f"{x:.3f}"

# ------------------------------------------------------------- title page ---
for _ in range(2):
    para()
para("A PROJECT REPORT ON", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, size=14, space_after=6)
para("LearnCraft AI: Predicting Text Readability with Statistical Machine Learning "
     "for a Curriculum-Adaptive Study Assistant",
     bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, size=18, space_after=18)
para("Submitted in partial fulfilment of the requirements of the course", align=WD_ALIGN_PARAGRAPH.CENTER,
     space_after=0)
para("Statistical Machine Learning (SML) Lab — Milestone 3: Final Project Submission", bold=True,
     align=WD_ALIGN_PARAGRAPH.CENTER, space_after=24)
para("Submitted by", italic=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=4)
tt = doc.add_table(rows=1, cols=2)
tt.alignment = WD_TABLE_ALIGNMENT.CENTER
tt.rows[0].cells[0].text, tt.rows[0].cells[1].text = "Name", "Enrolment No."
for n, roll in TEAM:
    c = tt.add_row().cells
    c[0].text, c[1].text = n, roll
for i, row in enumerate(tt.rows):
    for c in row.cells:
        c.width = Cm(6)
        for p in c.paragraphs:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for run in p.runs:
                run.bold = i == 0
para(space_after=18)
para("Under the guidance of", italic=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=0)
para("Ms. Deepti Shakya", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=36)
para("Department of Computer Science & Engineering", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=0)
para("School of Computer Science Engineering & Technology", align=WD_ALIGN_PARAGRAPH.CENTER, space_after=0)
para("Bennett University, Greater Noida", align=WD_ALIGN_PARAGRAPH.CENTER, space_after=0)
para("November 2026", align=WD_ALIGN_PARAGRAPH.CENTER)

# Front matter section (roman numerals)
front = doc.add_section(WD_SECTION.NEW_PAGE)
page_number_footer(front, "lowerRoman", 1)

front_title("DECLARATION", new_page=False)
para("We hereby declare that the project report titled “LearnCraft AI: Predicting Text Readability with "
     "Statistical Machine Learning for a Curriculum-Adaptive Study Assistant” is a record of work carried out "
     "by us as part of the Statistical Machine Learning Lab. The code, experiments and analysis presented here "
     "are our own. Wherever we have used published data, formulas or ideas, the source has been cited in the "
     "references. This work has not been submitted elsewhere for any other degree or course.")
para()
dt = doc.add_table(rows=1, cols=3)
for i, h in enumerate(("Name", "Enrolment No.", "Signature")):
    dt.rows[0].cells[i].text = h
for n, roll in TEAM:
    c = dt.add_row().cells
    c[0].text, c[1].text, c[2].text = n, roll, ""
dt.style = "Table Grid"
para("Date: ____________          Place: Greater Noida", align=WD_ALIGN_PARAGRAPH.LEFT)

front_title("CERTIFICATE", new_page=False).paragraph_format.space_before = Pt(18)
para("This is to certify that the project titled “LearnCraft AI: Predicting Text Readability with Statistical "
     "Machine Learning for a Curriculum-Adaptive Study Assistant”, submitted by Vishwas Singh (S25CSEU0018), "
     "Yagnesh (S25CSEU0031) and Kushal (S25CSEU0016), is a bona fide record of the work done by them under my "
     "supervision as part of the Statistical Machine Learning Lab during the academic year 2026–27.")
para()
para("______________________________", align=WD_ALIGN_PARAGRAPH.RIGHT, space_after=0)
para("Ms. Deepti Shakya", bold=True, align=WD_ALIGN_PARAGRAPH.RIGHT, space_after=0)
para("Statistical Machine Learning Lab", align=WD_ALIGN_PARAGRAPH.RIGHT, space_after=0)
para("Bennett University", align=WD_ALIGN_PARAGRAPH.RIGHT)

front_title("ACKNOWLEDGEMENT")
para("We would like to thank our faculty in the Statistical Machine Learning Lab for the feedback we received "
     "at the mid-term review. Their comments pushed us to stop relying on hand-picked example passages and to "
     "test our ideas on a proper, human-labelled dataset, which ended up shaping most of this final phase.")
para("We are also grateful to CommonLit and to Scott Crossley and his co-authors for releasing the CLEAR corpus "
     "openly. Without teacher-rated passages at this scale, a fair comparison between machine learning models "
     "and the old readability formulas would not have been possible for a student project.")
para("Finally, we thank our classmates and friends for their patience while we argued over feature lists and "
     "re-ran the same experiments more times than we would like to admit.")
para("Vishwas Singh, Yagnesh, Kushal", italic=True, align=WD_ALIGN_PARAGRAPH.RIGHT)

front_title("ABSTRACT")
best = r("Features + TF-IDF + Ridge (tuned)")
fk = r("FKGL only (linear)")
para("Students in the same class often read at very different levels, but they are handed the same textbook. "
     "LearnCraft AI is a study assistant that rewrites a syllabus topic for a chosen grade using a large language "
     "model (Google Gemini) and then generates a short quiz. The weak point of our mid-term prototype was the "
     "step that checks whether the generated text is actually easy enough: it used the Flesch-Kincaid formula, "
     "which only looks at sentence length and syllable counts.")
para(f"In this final milestone we replaced that check with a statistical machine learning model. We trained "
     f"and compared models on the CommonLit Ease of Readability (CLEAR) corpus, which contains "
     f"{M['data']['rows_clean']:,} passages with difficulty scores derived from teacher judgements. We extracted 19 "
     f"linguistic features and TF-IDF word and character n-grams, and evaluated eleven regression models, five "
     f"classifiers and two unsupervised methods with 5-fold cross-validation and a held-out test set. A tuned "
     f"Ridge regression on TF-IDF plus hand-crafted features gave the best result (test RMSE {best.RMSE:.3f}, "
     f"R² {best.R2:.2f}), against RMSE {fk.RMSE:.3f} and R² {fk.R2:.2f} for a regression on the Flesch-Kincaid "
     f"grade alone. A paired t-test over the cross-validation folds confirms the difference is significant "
     f"(p < 0.001). For three-way classification into Hard, Medium and Easy, logistic regression reached "
     f"{CLF['Accuracy'].max()*100:.1f}% accuracy, where chance is 33%.")
para("A lighter Ridge model on the 19 features was exported as plain coefficients and runs inside the Node.js "
     "backend and the browser demo. The server now scores each generated module and, if it is too hard for the "
     "student's grade, asks Gemini once for a simpler version. The report also discusses where the models fail, "
     "mainly on very short inputs and on the middle difficulty band.")
para("**Keywords:** readability assessment, ridge regression, TF-IDF, gradient boosting, cross-validation, "
     "CLEAR corpus, SDG 4, adaptive learning", align=WD_ALIGN_PARAGRAPH.LEFT)

front_title("TABLE OF CONTENTS")
field(doc.add_paragraph(), r'TOC \o "1-2" \h \z \u')
front_title("LIST OF FIGURES")
field(doc.add_paragraph(), r'TOC \h \z \t "Figure Caption,1"')
front_title("LIST OF TABLES", new_page=False)
field(doc.add_paragraph(), r'TOC \h \z \t "Table Caption,1"')

# Main body section (arabic numerals)
body = doc.add_section(WD_SECTION.NEW_PAGE)
page_number_footer(body, "decimal", 1)

# =============================================================== CHAPTER 1 ===
doc.add_heading("CHAPTER 1: INTRODUCTION", level=1)
h2("1.1 Background")
para("Anyone who has tutored a younger sibling knows the problem: the textbook explains the idea correctly, but "
     "in words the reader cannot get through. A Grade 7 science chapter written at a Grade 10 reading level "
     "does not teach much science to a student who reads at Grade 5. Cognitive load theory gives a name to "
     "this. When too much working memory goes into decoding sentences, little is left for understanding the "
     "concept (Sweller, 1988).")
para("Large language models now make it cheap to rewrite the same topic at different levels. That was the idea "
     "behind LearnCraft AI, which we started in the earlier milestones of this lab. A student picks a grade, a "
     "subject and a topic; the system asks Gemini for a learning module written for that grade, followed by a "
     "three-question quiz arranged by Bloom's taxonomy. The project is aligned with UN Sustainable Development "
     "Goal 4 (Quality Education), especially the target of inclusive and equitable learning for every student.")
para("There is a catch, though. Asking a language model to “write for Grade 4” does not guarantee that it will. "
     "Generated text drifts towards textbook vocabulary and long sentences, and the mid-term version had no "
     "reliable way to notice. So the system needs an independent way of measuring how "
     "hard a passage is. That measurement is a statistical learning problem, and it is the focus of this report.")

h2("1.2 Problem Statement")
para("Given a passage of English text, estimate how difficult it is for a school student to read, on a "
     "continuous scale and as a coarse class (Hard, Medium or Easy). The estimate should agree with human "
     "judgements of difficulty better than the classical readability formulas do. It also has to be cheap "
     "enough to run inside the web application every time Gemini produces a module, so that text which is too "
     "hard for the chosen grade can be caught and regenerated.")

h2("1.3 Objectives")
bullets([
    "Replace the synthetic 160-passage dataset used at mid-term with a real, human-labelled readability corpus "
    "and prepare it for modelling.",
    "Engineer interpretable linguistic features and text representations (TF-IDF) for each passage.",
    "Train and compare a range of supervised regression and classification models using cross-validation, "
    "tune the strongest ones, and test whether they beat the Flesch-Kincaid baseline in a statistically "
    "meaningful way.",
    "Use unsupervised methods (PCA and K-Means) to check whether difficulty shows up as natural structure in "
    "the feature space.",
    "Deploy a trained model inside the LearnCraft backend and demo page, and use it to drive the adaptive "
    "regeneration loop.",
], numbered=True)

h2("1.4 What Changed Since the Mid-Term Review")
para("At mid-term our dataset had 160 rows, but on closer inspection it was built from only 15 template "
     "passages repeated with random grade and subject labels. Any model trained on it would simply memorise "
     "those 15 texts, so we dropped it. We also scaled back one promise from the mid-term roadmap: fine-tuning "
     "a DeBERTa transformer. It would have needed GPU time we did not have, and it would also have taken the "
     "project away from the statistical learning methods this lab is about. We discuss transformers briefly as "
     "future work in Chapter 6.")

# =============================================================== CHAPTER 2 ===
chapter("CHAPTER 2: LITERATURE REVIEW")
h2("2.1 Classical Readability Formulas")
para("Readability research goes back almost a century. The best-known formulas came out of the 1940s to 1970s: "
     "Flesch Reading Ease (Flesch, 1948), the Dale-Chall formula, which counts words missing from a list of "
     "familiar words (Dale & Chall, 1948), and the Flesch-Kincaid Grade Level, developed for US Navy training "
     "manuals (Kincaid et al., 1975). All of them are linear equations in two or three surface counts, "
     "typically average sentence length plus average syllables per word or the share of unfamiliar words.")
para("They are popular because anyone can compute them, and word processors still report them. But they "
     "have well-known blind spots. A sentence of short, rare words (“The tort was moot.”) scores as easy. "
     "Narrative passages with lots of dialogue score as easier than they really are for a child, and the "
     "weights were fitted decades ago on small samples of adult readers.")

h2("2.2 Machine-Learning Approaches")
para("Starting in the mid-2000s, researchers began to treat readability as a supervised learning problem. "
     "Schwarm and Ostendorf (2005) combined language-model features with a support vector machine to classify "
     "Weekly Reader articles by grade. Feng et al. (2010) compared a large set of features, from part-of-speech "
     "counts to discourse features, and found that simple lexical and syntactic features carry much of the "
     "signal. Vajjala and Meurers (2012) added measures from second-language acquisition research, such as "
     "lexical richness and syntactic complexity, and got large accuracy gains on the WeeBit corpus. "
     "Collins-Thompson (2014) gives a useful survey of this period.")
para("More recently, neural models have taken the lead on benchmarks. Martinc et al. (2021) compared "
     "supervised neural approaches including BERT and hierarchical attention networks across several "
     "readability datasets. In the 2021 CommonLit Readability Prize on Kaggle, the top solutions were ensembles "
     "of large transformer models. These models are accurate but expensive to train and serve, and much "
     "harder to explain to a teacher.")

h2("2.3 The CLEAR Corpus")
para("Crossley et al. (2023) released the CommonLit Ease of Readability (CLEAR) corpus, which grew out of the "
     "same effort as the Kaggle competition. It contains about 4,700 excerpts of 140 to 200 words from "
     "literary and informational texts written over roughly 250 years, aimed at Grades 3 to 12. Instead of "
     "grade labels assigned by publishers, each excerpt has a “BT easiness” score. Teachers were shown pairs of "
     "passages and asked which one was easier, and a Bradley-Terry model turned those comparisons into a "
     "single continuous score. Higher scores mean easier text. The corpus also includes the values of several "
     "classical formulas, which makes it a natural benchmark for our question.")

h2("2.4 Research Gap and Our Position")
para("Most published work either stops at feature engineering with simple models or jumps straight to "
     "transformers. For a tool like LearnCraft we need something in between: a model clearly better than "
     "Flesch-Kincaid, but small enough to run in JavaScript with no GPU and simple enough that we can explain "
     "its decisions. We also wanted a careful comparison of the classical statistical learners taught in this "
     "lab on the same split of a real dataset, with a significance test rather than a single accuracy number. "
     "Table 2.1 summarises where our work sits.")
table("Table 2.1: Summary of related work",
      ["Work", "Data", "Method", "Takeaway for us"],
      [["Flesch (1948); Kincaid et al. (1975)", "Small adult samples", "Linear formula", "Our baseline"],
       ["Schwarm & Ostendorf (2005)", "Weekly Reader", "SVM + LM features", "ML beats formulas"],
       ["Feng et al. (2010)", "Weekly Reader", "Many feature sets", "Lexical features carry most signal"],
       ["Vajjala & Meurers (2012)", "WeeBit", "SLA-inspired features", "Lexical richness helps"],
       ["Martinc et al. (2021)", "Several corpora", "BERT, HAN", "Accurate but heavy"],
       ["Crossley et al. (2023)", "CLEAR, 4.7k", "Formula comparison", "Dataset we use"],
       ["This project", "CLEAR, 4.7k", "11 regressors + 5 classifiers", "Light model for deployment"]],
      widths=[4.3, 2.8, 3.5, 4.4], font=10)

# =============================================================== CHAPTER 3 ===
chapter("CHAPTER 3: DATASET AND PROPOSED METHODOLOGY")
h2("3.1 Overview of the Methodology")
para("Figure 3.1 shows the full pipeline. In short, we cleaned the CLEAR corpus, defined a regression target "
     "and a three-class target, split the data once into training and test sets, built two kinds of input "
     "representation, trained and cross-validated a set of models, tuned the best few, and evaluated "
     "everything on a test set the models had never seen. The model that went into the app was then exported "
     "and connected to the Gemini generation step.")
figure(os.path.join(FIG, "00_methodology_flowchart.png"), "Figure 3.1: Flowchart of the proposed methodology",
       width_cm=10.5)

h2("3.2 Dataset Description")
d = M["data"]
para(f"We downloaded the CLEAR corpus from its public GitHub repository (released under CC BY-NC-SA 4.0) and "
     f"kept the columns we needed. The raw file has {d['rows_raw']:,} rows. One excerpt appeared twice, so "
     f"after removing duplicates and empty text we were left with {d['rows_clean']:,} passages: "
     f"{d['lit']:,} literary and {d['info']:,} informational. We used four fields: the excerpt text, the "
     f"BT_easiness target, its standard error, and the genre (Lit or Info). The formula scores that come "
     f"with the corpus were used only to sanity-check our own feature code.")
ts = d["target_stats"]
para(f"The target ranges from {ts['min']:.2f} to {ts['max']:.2f}, with mean {ts['mean']:.2f} and standard "
     f"deviation {ts['std']:.2f}. Its distribution is close to normal with a slightly longer tail on the hard "
     f"side (Figure 3.2). Informational texts are clearly harder on average than literary ones, which is "
     f"something any model will have to deal with.")
figure(os.path.join(FIG, "01_target_distribution.png"),
       "Figure 3.2: Distribution of BT_easiness (left) and easiness by genre (right)",
       width_cm=14)

h2("3.3 Target Definition")
para(f"For regression, the target is BT_easiness as given. For classification, we split the passages into "
     f"three equal-sized groups by the tertiles of BT_easiness: **Hard** (below {d['tertile_cuts'][0]:.2f}), "
     f"**Medium** (between {d['tertile_cuts'][0]:.2f} and {d['tertile_cuts'][1]:.2f}) and **Easy** (above "
     f"{d['tertile_cuts'][1]:.2f}). Equal-sized classes keep accuracy meaningful, since chance is exactly one "
     f"in three. In the app we map these classes loosely to high-school, middle-school and elementary reading "
     f"bands. The mapping is approximate, because the corpus does not attach a grade to each passage.")

h2("3.4 Train/Test Split and Validation")
para(f"We made a single stratified 80/20 split with a fixed random seed of 42: {M['split']['train']:,} passages "
     f"for training and {M['split']['test']:,} for testing. Stratifying on the difficulty class means the test "
     f"set has the same mix of hard and easy texts as the training set. All model selection and tuning used "
     f"5-fold cross-validation inside the training set only. The test set was used once, at the end, to report "
     f"final numbers. This matters because with 16 regression variants it would be easy to fool ourselves by "
     f"repeatedly peeking at test scores.")

h2("3.5 Feature Engineering")
para("We wrote our own feature extractor instead of using the formula columns shipped with the corpus. That "
     "way exactly the same code (ported line by line to JavaScript) can run in the app on new text. Table 3.1 "
     "lists the 19 features. Syllables are counted with a simple vowel-group rule. It is not perfect "
     "(it counts “queue” as two syllables, for example), but it is fast and gives identical results in Python "
     "and JavaScript.")
table("Table 3.1: Hand-crafted linguistic features",
      ["Group", "Features", "Intuition"],
      [["Length", "words, sentences, paragraphs", "Passage size and layout"],
       ["Sentence", "average, SD and max sentence length", "Long, uneven sentences are harder"],
       ["Word", "avg word length, avg syllables, % words > 6 letters, % words with 3+ syllables, "
                "% one-syllable words", "Long words are usually rarer words"],
       ["Vocabulary", "type-token ratio, root TTR, % very common words", "Lexical variety and familiarity"],
       ["Punctuation", "commas per sentence, ; and : per sentence, quote density", "Clause nesting; dialogue"],
       ["Formulas", "Flesch Reading Ease, Flesch-Kincaid Grade", "Classical baselines as features"]],
      widths=[2.6, 7.2, 5.2], font=10)
para("The two formula features are computed as:")
para("FRE = 206.835 − 1.015 × (words / sentences) − 84.6 × (syllables / words)", align=WD_ALIGN_PARAGRAPH.CENTER)
para("FKGL = 0.39 × (words / sentences) + 11.8 × (syllables / words) − 15.59", align=WD_ALIGN_PARAGRAPH.CENTER)
para("For the text-based models we also used TF-IDF vectors: word unigrams and bigrams (minimum document "
     "frequency 2, up to 40,000 terms, sublinear term frequency) and, separately, character 2- to 5-grams "
     "within word boundaries (up to 60,000 terms). TF-IDF lets the model learn directly that words like "
     "“moreover” or “photosynthesis” signal harder text, which no syllable count can capture. In the combined "
     "model the 19 features are standardised, scaled by 0.35 so they do not swamp the sparse TF-IDF columns, "
     "and stacked next to the word vectors.")

h2("3.6 Models and Hyper-parameter Tuning")
para("We picked models that cover the main families from the course: linear models with and without "
     "regularisation (Ridge adds an L2 penalty α‖w‖² that shrinks correlated coefficients; Hoerl & Kennard, "
     "1970), instance-based learning, kernels, single trees and tree ensembles (Breiman, 2001; Friedman, 2001). "
     "Table 3.2 lists them. The three most promising were tuned with GridSearchCV and 5-fold cross-validation "
     "over the grids in the last column.")
table("Table 3.2: Models compared and tuning grids",
      ["Family", "Models (settings)", "Grid searched"],
      [["Baselines", "Training mean; linear regression on FKGL only", "—"],
       ["Linear", "Linear Regression, Ridge (α=1), Lasso (α=0.01), Elastic Net (α=0.01, l1=0.5)", "—"],
       ["Instance / kernel", "KNN (k=15, distance-weighted); SVR with RBF kernel",
        "SVR: C {0.3,1,3}, γ {scale,0.02,0.05}, ε {0.1,0.3}"],
       ["Trees", "Decision Tree (depth 6); Random Forest (400 trees); Gradient Boosting (400 trees, lr 0.05)",
        "GBR: trees {300,600}, lr {0.03,0.06}, depth {2,3,4}"],
       ["Text", "Ridge on TF-IDF words; on TF-IDF characters; on words + 19 features",
        "Ridge α {0.5,1,1.5,3,6}"],
       ["Classifiers", "Logistic Regression, Random Forest, Multinomial NB, Linear SVM, LogReg on words + features",
        "—"],
       ["Unsupervised", "PCA (2 components); K-Means (k=3), compared using the adjusted Rand index", "—"]],
      widths=[2.6, 7.6, 5.4], font=9.5)

h2("3.7 Evaluation Metrics and Statistical Test")
para("For regression we report root mean squared error (RMSE), mean absolute error (MAE) and the coefficient "
     "of determination R². RMSE is in the same units as BT_easiness and punishes large errors more, which "
     "suits our use case: one badly misjudged module matters more than many slightly off ones. For "
     "classification we report accuracy and macro-averaged F1, along with a confusion matrix. To check whether "
     "the improvement over Flesch-Kincaid is real and not luck of the split, we ran a paired t-test on the "
     "five per-fold RMSE values of the two models. We know this test is somewhat optimistic because the folds "
     "share training data (Dietterich, 1998), so we read it together with the size of the gap rather than "
     "on its own.")

# =============================================================== CHAPTER 4 ===
chapter("CHAPTER 4: IMPLEMENTATION")
h2("4.1 System Architecture")
para("Figure 4.1 shows how the pieces fit together. The offline training part is pure Python. The live "
     "system is a Node.js/Express server with two front ends: a zero-install HTML page (open index.html) and "
     "a Next.js page. The readability engine sits between the API and Gemini, so that every generated module "
     "is scored before it reaches the student.")
figure(os.path.join(FIG, "00_system_architecture.png"), "Figure 4.1: LearnCraft AI system architecture (final version)", width_cm=14)

h2("4.2 Tools and Environment")
para("The machine learning work uses Python 3.11 with scikit-learn 1.9, SciPy, NumPy and pandas, and the plots "
     "use Matplotlib and Seaborn. The application runs on Node.js with Express 4, with a standalone HTML/Tailwind "
     "page and a Next.js 14 page as front ends. Text generation uses the Google Gemini API, with a built-in "
     "simulator when no API key is set. Code is versioned with Git and hosted on GitHub.")

h2("4.3 Code Structure")
table("Table 4.1: Main files in the repository",
      ["Path", "Purpose"],
      [["ml/features.py", "The 19-feature extractor and small sklearn helpers"],
       ["ml/train.py", "Loads data, trains all models, writes metrics, figures and model files"],
       ["ml/check_js_parity.js", "Checks the JavaScript port against Python predictions"],
       ["shared/readability_ml.js", "Feature extractor + Ridge predictor for Node and the browser"],
       ["models/ridge_features.json", "Exported scaler means, scales and Ridge coefficients"],
       ["models/best_regressor.joblib", "Best TF-IDF + features pipeline (Python)"],
       ["backend/server.js", "REST API, Gemini calls and the adaptive regeneration loop"],
       ["index.html, frontend/", "User interfaces"],
       ["results/", "metrics.json, result tables, all figures"]], widths=[5.5, 9.5], font=10)

h2("4.4 Training Pipeline")
para("Running python ml/train.py from the project root reproduces every number in this report in about six "
     "minutes on a laptop. Each model is wrapped in a scikit-learn Pipeline, so scaling and TF-IDF fitting "
     "happen inside each cross-validation fold rather than on the whole training set. That avoids a subtle "
     "kind of leakage, where the vocabulary or the feature means would otherwise include information from the "
     "validation fold. The script writes results/metrics.json, two CSV result tables and ten figures.")

h2("4.5 Deploying the Model in JavaScript")
para("The most accurate model uses a 40,000-term vocabulary, which is awkward to ship to a browser. For "
     "the app we therefore exported a smaller model: standardisation followed by Ridge regression on the 19 "
     "features. It is just 19 means, 19 scales, 19 coefficients and an intercept, stored in a JSON file. The "
     "prediction is")
para("ŷ = b + Σⱼ wⱼ (xⱼ − μⱼ) / σⱼ", align=WD_ALIGN_PARAGRAPH.CENTER)
para("which takes a few lines of JavaScript. The risky part is making sure the JavaScript features are "
     "exactly the same as the Python ones. A regular expression that splits sentences slightly differently "
     "would silently shift every prediction. We wrote ml/check_js_parity.js, which runs 25 random corpus "
     "passages through both implementations. The largest difference was about 5 × 10⁻¹¹, which is just "
     "floating-point noise.")

h2("4.6 Adaptive Regeneration Loop")
para("When a student requests a module, the server sends a grade-aware prompt to Gemini and scores the "
     "reply with the exported model. Grades 3–5 accept only Easy text, Grades 6–8 accept Easy or Medium, "
     "and Grades 9–12 accept anything. If the first draft falls outside that range, the server sends one more "
     "request telling Gemini how the draft was rated and asking for shorter sentences and everyday words. "
     "The response includes an adaptiveCheck object recording what happened, so the decision is visible to "
     "the user. We limited this to one retry to keep response time and API cost under control.")
para("We also added a “low confidence” flag. CLEAR passages are 140–200 words long, and when we pasted in "
     "a single sentence the model gave odd answers. Root type-token ratio, for example, depends strongly on "
     "length. Below 80 words the app still shows a prediction but warns that it is unreliable.")

h2("4.7 User Interface")
para("The mid-term interface was built to show off features, and it read like it: labels such as “Pedagogical "
     "Scaffolding Tier” and metric cards that were not computed from the lesson at all. For the final version we "
     "rebuilt it around what a student actually does. The page has two tabs. **Learn a topic** walks through three "
     "numbered steps (choose, read, test) with large grade buttons, topic suggestions and a plain choice of "
     "Simpler, Normal or Challenge (Figure 4.2). Every lesson carries a reading-level check from our model, phrased "
     "as “good fit for Grade 5” rather than a raw score, plus a read-aloud button for weaker readers. The quiz "
     "only unlocks once all questions are answered. Its result leads to a real next step: a simpler lesson after a "
     "low score, or the next grade after a perfect one (Figure 4.4). **Check any text** lets a teacher paste any "
     "passage and see the verdict update while typing, with a Hard-to-Easy meter, concrete tips and the raw "
     "numbers tucked away under “Details for teachers” (Figure 4.3). The page also works offline with hand-written "
     "sample lessons, and it says clearly which mode it is in.")
figure(os.path.join(SHOT, "app_home.png"), "Figure 4.2: Learn tab with an AI-written Grade 5 lesson; the first "
       "draft was rated too hard and rewritten", width_cm=11.5)
figure(os.path.join(SHOT, "app_inspector.png"), "Figure 4.3: Check-any-text tab rating a dense passage against "
       "Grade 6", width_cm=12)
figure(os.path.join(SHOT, "app_quiz_result.png"), "Figure 4.4: Graded quiz with explanations and the suggested "
       "next step", width_cm=7)

# =============================================================== CHAPTER 5 ===
chapter("CHAPTER 5: RESULTS AND DISCUSSION")
h2("5.1 Exploratory Analysis of Features")
cor = M["feature_correlations"]
para(f"Before training anything, we looked at how each feature relates to the target (Figure 5.1). The "
     f"strongest single correlate is Flesch Reading Ease (r = {cor['flesch_reading_ease']:.2f}), followed by the "
     f"Flesch-Kincaid grade (r = {cor['flesch_kincaid_grade']:.2f}) and the share of long words "
     f"(r = {cor['pct_long_words']:.2f}). So the old formulas are not useless. They capture real signal, but "
     f"with |r| around 0.5 they explain only about a quarter of the variance. One surprise was quote density "
     f"(r = {cor['quote_density']:.2f}): passages with lots of dialogue tend to be easier, which makes sense for "
     f"children's fiction.")
para("The right half of Figure 5.1 shows that many features are strongly correlated with each other. Average syllables, word "
     "length and the share of long words all measure roughly the same thing. This multicollinearity is the "
     "main reason we expected Ridge to behave better than plain least squares, and it also means the "
     "individual coefficients should not be read too literally.")
figure_pair(os.path.join(FIG, "02_feature_correlations.png"), os.path.join(FIG, "03_feature_heatmap.png"),
            "Figure 5.1: Correlation of each feature with BT_easiness (left) and between features (right)",
            w1=7.9, w2=7.3)

h2("5.2 Regression Results")
para("Table 5.1 gives the full comparison. CV RMSE is the mean over five folds on the training set; the other "
     "three columns are on the held-out test set.")
rows, bold = [], []
for i, row in REG.iterrows():
    cv = "—" if pd.isna(row["CV RMSE"]) else f"{row['CV RMSE']:.3f}"
    rows.append([row.Model, "Text" if row.Input == "Raw text" else ("Both" if row.Input == "Both" else "Features"),
                 cv, f2(row.RMSE), f2(row.MAE), f"{row.R2:.3f}"])
    if row.Model == "Features + TF-IDF + Ridge (tuned)":
        bold.append(i)
table("Table 5.1: Regression results (lower RMSE/MAE and higher R² are better)",
      ["Model", "Input", "CV RMSE", "Test RMSE", "Test MAE", "Test R²"], rows,
      widths=[5.8, 1.7, 1.8, 1.9, 1.9, 1.8], font=9.5, bold_rows=bold)
figure(os.path.join(FIG, "04_model_comparison.png"), "Figure 5.2: Test RMSE of all regression models",
       width_cm=9.5)
mb = r("Mean baseline")
para(f"A few things stand out. First, every model beats the Flesch-Kincaid baseline (RMSE {fk.RMSE:.3f}), and "
     f"the mean baseline ({mb.RMSE:.3f}) shows what “no information” looks like. Second, among models that only "
     f"see the 19 features, the non-linear ones (SVR, random forest, gradient boosting) sit around 0.81–0.82, "
     f"while the linear models sit around 0.85. There is some non-linearity, but not much. The four linear "
     f"variants are practically tied, which tells us regularisation is not doing much on 19 features and "
     f"3,778 rows. The decision tree is the weakest learned model, as expected from a single tree with high "
     f"variance.")
para(f"Third, and most important, switching to the raw text through TF-IDF makes a much bigger difference "
     f"than switching between learners. Word n-grams alone reach {r('TF-IDF words + Ridge').RMSE:.3f}, "
     f"character n-grams {r('TF-IDF chars + Ridge').RMSE:.3f}, and combining word n-grams with our features "
     f"gives {r('Features + TF-IDF + Ridge').RMSE:.3f}. After tuning, this drops to {best.RMSE:.3f} with "
     f"R² = {best.R2:.3f}. Character n-grams doing well was a nice surprise. They pick up suffixes like "
     f"“-tion” and “-ous” that mark academic vocabulary, even for words that never appeared in training.")
para(f"We also tried a simple weighted average of the tuned text model and tuned gradient boosting. It came "
     f"out at {r('Ensemble (0.6 text Ridge + 0.4 GBR)').RMSE:.3f}, slightly worse than the text model on its "
     f"own. The boosting model makes errors that are too similar to the text model's and is clearly weaker, "
     f"so averaging just pulls the better model down. We report it anyway because it is a useful negative "
     f"result.")

h2("5.3 Hyper-parameter Tuning")
tu = M["tuning"]
para(f"For the combined Ridge model, cross-validated RMSE kept improving as α went down, with the best value "
     f"at α = {tu['Features + TF-IDF + Ridge']['best_params']['m__alpha']} (CV RMSE "
     f"{tu['Features + TF-IDF + Ridge']['grid']['0.5']:.3f} at α = 0.5 against "
     f"{tu['Features + TF-IDF + Ridge']['grid']['6.0']:.3f} at α = 6). Smaller α means less "
     f"shrinkage, so with this much data the model can afford to trust the vocabulary more. The best SVR used "
     f"C = {tu['SVR (RBF)']['best_params']['m__C']}, γ = {tu['SVR (RBF)']['best_params']['m__gamma']}, and the "
     f"best gradient boosting used {tu['Gradient Boosting']['best_params']['n_estimators']} trees of depth "
     f"{tu['Gradient Boosting']['best_params']['max_depth']} with learning rate "
     f"{tu['Gradient Boosting']['best_params']['learning_rate']}. Tuning improved SVR and boosting only "
     f"marginally (about 0.004 RMSE), which suggests the 19 features are the limit there, not the settings.")

h2("5.4 Is the Improvement Significant?")
tt_ = M["ttest_text_vs_fkgl"]
para(f"Across the five folds, the combined text model had RMSE between {min(tt_['fold_rmse_text']):.3f} and "
     f"{max(tt_['fold_rmse_text']):.3f}, while the Flesch-Kincaid baseline was between "
     f"{min(tt_['fold_rmse_fkgl']):.3f} and {max(tt_['fold_rmse_fkgl']):.3f}. The model won on every fold. "
     f"The paired t-test gives t = {tt_['t']:.1f} with p = {tt_['p']:.1e}. Gradient boosting on features "
     f"alone is also significantly better than the baseline (t = {M['ttest_gbr_vs_fkgl']['t']:.1f}, "
     f"p = {M['ttest_gbr_vs_fkgl']['p']:.1e}). Given the caveat about overlapping training folds, we would "
     f"not lean on the exact p-value, but a gap of more than 0.2 RMSE on every single fold is not luck.")

h2("5.5 Residual and Error Analysis")
res_ = M["residuals"]
para(f"Figure 5.3 plots predicted against actual easiness for the best model on the test set. The residuals "
     f"have mean {res_['mean']:.3f} and standard deviation {res_['sd']:.3f}, so the model is not biased overall. "
     f"A Shapiro-Wilk test on 500 residuals (p = {res_['shapiro_p_sample500']:.2f}) does not reject normality. "
     f"The scatter does show regression to the mean: the easiest passages are predicted as somewhat harder "
     f"than they are and the hardest as somewhat easier. This is typical for regularised linear models.")
figure(os.path.join(FIG, "05_pred_vs_actual.png"),
       "Figure 5.3: Predicted vs actual easiness (left) and residual distribution (right), best model",
       width_cm=10)
eg = M["error_by_genre"]
para(f"Broken down by genre, the error is a little higher on informational texts (RMSE {eg['Info']:.3f}) than "
     f"on literature ({eg['Lit']:.3f}). We read the eight test passages with the largest errors. Six were "
     f"rated harder by teachers than by the model. They include a dense 2013 passage on visual perception, "
     f"a story containing whole sentences in a non-English language, and four texts written between 1884 "
     f"and 1929 with old-fashioned phrasing that our features do not capture. The other two went the "
     f"opposite way: two modern children's stories that the model judged too hard, apparently because unfamiliar "
     f"names and food words (for example sorghum and cassava) look like rare vocabulary to TF-IDF.")
para("To see what the feature-based models rely on, we computed permutation importance for the tuned "
     "gradient boosting model (Figure 5.4, left). Flesch Reading Ease is by far the most important feature, followed "
     "by the share of long words and the variation in sentence length. The last one is interesting: texts that "
     "mix very long and very short sentences are rated harder, independent of the average length.")

h2("5.6 Learning Curve")
lc = M["learning_curve"]
para(f"The right half of Figure 5.4 shows how the best model improves with more data. Validation RMSE falls from "
     f"{lc['val'][0]:.3f} with {lc['sizes'][0]} passages to {lc['val'][-1]:.3f} with {lc['sizes'][-1]:,}, and is "
     f"still going down at the end. Training RMSE stays around {lc['train'][-1]:.2f}, so there is a clear gap "
     f"between the two curves. With a 40,000-term vocabulary the model can fit the training set closely. The "
     f"still-falling validation curve suggests more labelled passages would help more than a fancier model.")
figure_pair(os.path.join(FIG, "06_permutation_importance.png"), os.path.join(FIG, "07_learning_curve.png"),
            "Figure 5.4: Permutation importance for gradient boosting (left) and learning curve of the best "
            "model (right)", w1=6.3, w2=6.8)

h2("5.7 Classification Results")
para("Table 5.2 shows the three-class results. Chance accuracy is 33.3% because the classes are balanced.")
table("Table 5.2: Classification results on the test set (Hard / Medium / Easy)",
      ["Model", "Accuracy", "Macro F1"],
      [[row.Model, f"{row.Accuracy*100:.1f}%", f"{row['Macro F1']:.3f}"] for _, row in CLF.iterrows()],
      widths=[8.5, 3, 3])
bc = M["best_classifier"]
rep = bc["report"]
para(f"The pattern matches the regression results: text-based models beat feature-only ones, and the best "
     f"model combines both ({CLF['Accuracy'].max()*100:.1f}% accuracy). The confusion matrix (Figure 5.5) shows "
     f"where the errors are. Hard and Easy are recognised reasonably well (F1 {rep['Hard']['f1-score']:.2f} and "
     f"{rep['Easy']['f1-score']:.2f}), but Medium only reaches F1 {rep['Medium']['f1-score']:.2f}. That is "
     f"expected, since the Medium class borders both others and the cut-offs are arbitrary points on a "
     f"continuous scale. Hard passages are confused with Easy ones only rarely ({bc['confusion_matrix'][0][2]} "
     f"of 315), which is the mistake that would hurt a student most.")
figure(os.path.join(FIG, "09_confusion_matrix.png"), "Figure 5.5: Confusion matrix of the best classifier",
       width_cm=6.3)

h2("5.8 Unsupervised View: PCA and K-Means")
pc = M["pca"]
para(f"Finally, we asked whether difficulty is the main source of variation in the features, using no labels "
     f"at all. The first two principal components explain {pc['explained_variance'][0]*100:.0f}% and "
     f"{pc['explained_variance'][1]*100:.0f}% of the variance. Colouring the PCA plot by true class (Figure 5.6, "
     f"left) shows a gradient from hard to easy along the first component, but with heavy overlap. K-Means with "
     f"three clusters finds groups that agree with the difficulty classes only weakly (adjusted Rand index "
     f"{pc['kmeans_ari_vs_difficulty']:.2f}). They agree more with genre (ARI 0.23): one cluster is 92% "
     f"informational text, and another is mostly fiction with many short paragraphs and a lot of dialogue. Difficulty is real in the feature space, but it is not the dominant structure, which is "
     f"why supervision is needed.")
figure(os.path.join(FIG, "10_pca_kmeans.png"), "Figure 5.6: PCA projection coloured by true class (left) and by "
                                               "K-Means cluster (right)", width_cm=11)

h2("5.9 Deployed Model and Limitations")
dl = M["deployed_light_model"]
para(f"The light Ridge model that runs in the app scored test RMSE {dl['RMSE']:.3f} and R² {dl['R2']:.3f}: worse "
     f"than the best text model ({best.RMSE:.3f}) but clearly better than Flesch-Kincaid ({fk.RMSE:.3f}), and it "
     f"runs in microseconds with no dependencies, which we think is the right trade-off for a classroom tool. For "
     f"context, the winning transformer ensembles in the CommonLit competition reached RMSE around 0.45 on a "
     f"related target, so deep models still have headroom.")
para("The work has clear limitations. The model is trained on 140–200-word passages and is unreliable on single "
     "sentences, which the app flags. The Hard/Medium/Easy to grade-band mapping is approximate, because CLEAR "
     "gives no grade per passage, and the heuristic syllable counter makes our Flesch values differ slightly from "
     "the corpus. The adaptive loop has been tested with the simulator and a few live Gemini requests (one Grade 5 "
     "lesson was rewritten after its first draft was rated too hard), but not with real students. Finally, the "
     "corpus is mostly US/UK English, so Indian or translated textbook passages may behave differently.")

# =============================================================== CHAPTER 6 ===
chapter("CHAPTER 6: CONCLUSION AND FUTURE SCOPE")
h2("6.1 Conclusion")
para(f"We set out to give LearnCraft AI a better way of judging whether the text it generates is easy enough "
     f"for the student it is meant for. Using {M['data']['rows_clean']:,} teacher-rated passages from the CLEAR "
     f"corpus, we compared sixteen regression set-ups and five classifiers under the same cross-validation and "
     f"test protocol. The best model, a tuned Ridge regression on TF-IDF n-grams plus 19 linguistic features, "
     f"reduced RMSE from {fk.RMSE:.3f} (Flesch-Kincaid) to {best.RMSE:.3f} and raised R² from {fk.R2:.2f} to "
     f"{best.R2:.2f}. The gain held on every cross-validation fold.")
para("Probably the most useful lesson for us was that representation mattered more than the choice of "
     "learner. Swapping a linear model for gradient boosting on the same 19 features bought about 0.03 RMSE, "
     "while letting the model see the actual words bought more than 0.13. We also learned to be suspicious "
     "of our own data: the mid-term dataset looked fine in the EDA plots, and only when we checked for "
     "duplicate passages did we notice it had just 15 unique texts.")
para("On the engineering side, the exported Ridge model now runs inside the backend and the browser. It "
     "scores every generated module and triggers one simplification retry when a module is too hard for the "
     "chosen grade, turning the “adaptive” part of the project from a claim into a working feature.")

h2("6.2 Future Scope")
bullets([
    "Fine-tune a small transformer (for example DistilBERT) on CLEAR and serve it next to the Ridge model, "
    "using the Ridge model as a fast first check.",
    "Add a list of words by school grade (age-of-acquisition norms) as features, which should help with "
    "archaic and technical words.",
    "Collect ratings from teachers in Indian schools on NCERT-style passages, to check how well the model "
    "transfers.",
    "Use quiz scores to estimate each student's reading level over time and feed that back into the target "
    "difficulty, instead of relying on the grade the student selects.",
    "Run a small classroom study measuring whether ML-checked modules actually improve quiz scores compared "
    "with unchecked ones.",
])

# ============================================================== REFERENCES ===
chapter("REFERENCES")
refs = [
    "Breiman, L. (2001). Random forests. Machine Learning, 45(1), 5–32.",
    "Collins-Thompson, K. (2014). Computational assessment of text readability: A survey of current and future "
    "research. ITL – International Journal of Applied Linguistics, 165(2), 97–135.",
    "Crossley, S. A., Heintz, A., Choi, J. S., Batchelor, J., Karimi, M., & Malatinszky, A. (2023). A "
    "large-scaled corpus for assessing text readability. Behavior Research Methods, 55, 491–507.",
    "Crossley, S. A., Heintz, A., Choi, J., Batchelor, J., & Karimi, M. (2021). The CommonLit Ease of "
    "Readability (CLEAR) corpus. Proceedings of the 14th International Conference on Educational Data Mining.",
    "Dale, E., & Chall, J. S. (1948). A formula for predicting readability. Educational Research Bulletin, "
    "27(1), 11–28.",
    "Dietterich, T. G. (1998). Approximate statistical tests for comparing supervised classification learning "
    "algorithms. Neural Computation, 10(7), 1895–1923.",
    "Feng, L., Jansche, M., Huenerfauth, M., & Elhadad, N. (2010). A comparison of features for automatic "
    "readability assessment. Proceedings of COLING 2010: Posters, 276–284.",
    "Flesch, R. (1948). A new readability yardstick. Journal of Applied Psychology, 32(3), 221–233.",
    "Friedman, J. H. (2001). Greedy function approximation: A gradient boosting machine. Annals of Statistics, "
    "29(5), 1189–1232.",
    "Hastie, T., Tibshirani, R., & Friedman, J. (2009). The Elements of Statistical Learning (2nd ed.). "
    "Springer.",
    "Hoerl, A. E., & Kennard, R. W. (1970). Ridge regression: Biased estimation for nonorthogonal problems. "
    "Technometrics, 12(1), 55–67.",
    "Kincaid, J. P., Fishburne, R. P., Rogers, R. L., & Chissom, B. S. (1975). Derivation of new readability "
    "formulas for Navy enlisted personnel (Research Branch Report 8-75). Naval Technical Training Command.",
    "Martinc, M., Pollak, S., & Robnik-Šikonja, M. (2021). Supervised and unsupervised neural approaches to "
    "text readability. Computational Linguistics, 47(1), 141–179.",
    "Pedregosa, F., et al. (2011). Scikit-learn: Machine learning in Python. Journal of Machine Learning "
    "Research, 12, 2825–2830.",
    "Schwarm, S. E., & Ostendorf, M. (2005). Reading level assessment using support vector machines and "
    "statistical language models. Proceedings of the 43rd Annual Meeting of the ACL, 523–530.",
    "Sweller, J. (1988). Cognitive load during problem solving: Effects on learning. Cognitive Science, 12(2), "
    "257–285.",
    "United Nations. (2015). Transforming our world: The 2030 Agenda for Sustainable Development "
    "(A/RES/70/1).",
    "Vajjala, S., & Meurers, D. (2012). On improving the accuracy of readability classification using insights "
    "from second language acquisition. Proceedings of the 7th Workshop on Building Educational Applications "
    "Using NLP, 163–173.",
]
for i, ref in enumerate(refs, 1):
    p = para(f"[{i}] {ref}", align=WD_ALIGN_PARAGRAPH.LEFT, space_after=4)
    p.paragraph_format.left_indent = Cm(0.9)
    p.paragraph_format.first_line_indent = Cm(-0.9)
    p.paragraph_format.line_spacing = 1.0

doc.save(OUT)
print("saved", OUT)
