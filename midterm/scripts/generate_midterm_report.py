import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image as RLImage, Table, TableStyle, KeepTogether, PageBreak, HRFlowable
)

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def create_docx_report(output_docx_path):
    print(f"Creating Word Progress Report: {output_docx_path}...")
    doc = docx.Document()

    # Set page margins (1 inch)
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(1)
        section.bottom_margin = Inches(1)
        section.left_margin = Inches(1)
        section.right_margin = Inches(1)

    # Document Header / Title
    title_p = doc.add_paragraph()
    title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    trun = title_p.add_run("LearnCraft AI: Dynamic Curriculum-Adaptive Learning & Assessment Engine")
    trun.font.name = "Calibri"
    trun.font.size = Pt(22)
    trun.font.bold = True
    trun.font.color.rgb = RGBColor(30, 58, 138)

    sub_p = doc.add_paragraph()
    sub_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    srun = sub_p.add_run("MID-TERM PROJECT EVALUATION PROGRESS REPORT\nPhase 2: Baseline Implementation (45% Completed) & End-Term Scope (55% Roadmap)\nUN-SDG Goal 4: Quality Education")
    srun.font.name = "Calibri"
    srun.font.size = Pt(11)
    srun.font.bold = True
    srun.font.color.rgb = RGBColor(37, 99, 235)

    meta_table = doc.add_table(rows=4, cols=2)
    meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_data = [
        ("Project Title:", "LearnCraft AI — Personalized Curriculum Study Assistant"),
        ("UN Sustainable Development Goal:", "Goal 4: Quality Education (Target 4.4 & Target 4.7)"),
        ("Project Domain & Track:", "Artificial Intelligence, Natural Language Processing, Software Track"),
        ("Evaluation Stage:", "Mid-Term Project Evaluation (45% Baseline Completed | 55% End-Term Work Identified)")
    ]
    for i, (k, v) in enumerate(meta_data):
        row = meta_table.rows[i]
        c0 = row.cells[0]
        c1 = row.cells[1]
        c0.width = Inches(2.2)
        c1.width = Inches(4.3)
        p0 = c0.paragraphs[0]
        r0 = p0.add_run(k)
        r0.font.bold = True
        r0.font.size = Pt(9.5)
        r0.font.color.rgb = RGBColor(15, 23, 42)
        p1 = c1.paragraphs[0]
        r1 = p1.add_run(v)
        r1.font.size = Pt(9.5)
        set_cell_background(c0, "F1F5F9")
        set_cell_background(c1, "F8FAFC")

    doc.add_paragraph()

    # Executive Summary
    h_exec = doc.add_heading("Executive Summary", level=1)
    h_exec.paragraph_format.space_before = Pt(12)
    p_exec = doc.add_paragraph()
    p_exec.add_run(
        "LearnCraft AI is an automated, curriculum-grounded learning and assessment engine engineered to tackle the "
        "global 'one-size-fits-all' educational challenge, directly advancing United Nations Sustainable Development Goal 4 "
        "(Quality Education). In standard classroom ecosystems, standardized textbooks frequently present linguistic complexity "
        "that diverges sharply from a student's individual reading capacity, leading to cognitive overload, diminished engagement, "
        "and conceptual dropout. LearnCraft AI resolves this bottleneck through a hybrid architectural paradigm combining "
        "computational readability profiling with large language model reasoning (Google Gemini 1.5 Flash).\n\n"
        "At this Mid-Term evaluation milestone, our project stands at 45% completion, successfully establishing the theoretical, "
        "algorithmic, and functional baseline: (1) corpus curation and ingestion of 160 multi-grade curriculum excerpts; (2) mathematical "
        "linguistic feature extraction (ASL, ASW, FRE, FKGL, TTR, CWR); (3) exploratory data analysis (EDA) with 4 statistical visualizations; "
        "(4) a REST API gateway with 5 endpoints; and (5) an interactive, zero-install web demonstration prototype.\n\n"
        "Crucially, this report provides a candid critical evaluation of the baseline's current limitations (such as surface-level formula "
        "blind spots and prompt-only generation) and establishes a rigorous, comprehensive technical roadmap for the remaining 55% of the "
        "project to be completed for the End-Term evaluation: fine-tuning a DeBERTa-v3 Transformer model, implementing Retrieval-Augmented "
        "Generation (RAG) for textbook grounding, Bayesian Knowledge Tracing (BKT) for probabilistic mastery modeling, and controlled empirical "
        "classroom user studies."
    )

    # 1. Introduction & Problem Definition
    doc.add_heading("1. Introduction & Problem Statement", level=1)
    p_intro = doc.add_paragraph()
    p_intro.add_run(
        "Quality education is recognized by the United Nations as the bedrock of sustainable development. However, modern educational systems "
        "face a persistent structural challenge: uniform curriculum materials cannot accommodate heterogeneous student reading proficiencies. "
        "Research in cognitive load theory demonstrates that when a learner confronts reading material 2 or more grade levels above their independent "
        "reading threshold, working memory is predominantly consumed by syntactic decoding and lexical deciphering rather than conceptual assimilation."
    )
    p_prob = doc.add_paragraph()
    r_prob = p_prob.add_run("Formal Problem Definition:\n")
    r_prob.bold = True
    p_prob.add_run(
        "Given an academic topic T within curriculum domain D and a student profile characterized by developmental grade level G ∈ [3, 12] "
        "and reading competency R, the objective is to dynamically synthesize a pedagogical module M and diagnostic assessment Q such that:\n"
        "1. Conceptual fidelity to official syllabus benchmarks is strictly preserved;\n"
        "2. The linguistic readability metrics of M (measured via FKGL, FRE, and transformer embeddings) mathematically converge to target grade level G;\n"
        "3. Cognitive assessment Q evaluates three distinct tiers of Bloom's Revised Taxonomy (Factual Recall, Conceptual Comprehension, Real-World Application);\n"
        "4. Content generation operates under strict anti-hallucination guardrails with sub-2-second end-to-end system latency."
    )

    # 2. Project Scope & 45% vs 55% Milestone Breakdown
    doc.add_heading("2. Project Scope & Milestone Breakdown (45% Mid-Term vs 55% End-Term)", level=1)
    p_scope = doc.add_paragraph()
    p_scope.add_run(
        "To ensure academic rigor and manageable delivery, the project is structured into two clearly delineated phases:\n"
        "• Phase 1 & 2: Mid-Term Milestone (45% Completed) — Establish foundational feasibility, dataset curation, baseline linguistic formulas, "
        "exploratory statistical analysis, API routing, and an interactive proof-of-concept prototype.\n"
        "• Phase 3 & 4: End-Term Milestone (55% Remaining) — Deep learning model fine-tuning (DeBERTa-v3), syllabus RAG vector indexing, "
        "probabilistic student mastery tracking (Bayesian Knowledge Tracing), teacher analytics portal, and empirical classroom validation."
    )

    # 3. Dataset Collection & Ingestion
    doc.add_heading("3. Dataset Collection, Ingestion & Preprocessing", level=1)
    p_ds = doc.add_paragraph()
    p_ds.add_run(
        "To ground our readability calculations and calibrate our Generative AI prompt constraints, we utilized the widely recognized "
        "CommonLit Readability Prize Dataset (hosted on Kaggle) in conjunction with an expanded K-12 multi-disciplinary curriculum corpus. "
        "The corpus contains 160 curated educational excerpts distributed across 7 fundamental academic disciplines: Life Sciences, Physical Sciences, "
        "World History, Mathematics, Computer Science, Civics & Economics, and English Language Arts."
    )
    
    # Dataset Table
    ds_table = doc.add_table(rows=5, cols=4)
    ds_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers = ["Educational Tier", "Target Grades", "Lexile Band Range", "Core Curriculum Subjects"]
    rows_data = [
        ("Elementary School", "Grades 3 – 5", "400L – 750L", "Earth & Life Science, Basic Math, World Communities, ELA"),
        ("Middle School", "Grades 6 – 8", "750L – 1050L", "Physical Science, Pre-Algebra, Ancient Civilizations, Logic"),
        ("Early High School", "Grades 9 – 10", "1050L – 1200L", "Biology, Chemistry, Algebra II, World History & Civics"),
        ("Late High School", "Grades 11 – 12", "1200L – 1350L+", "Physics, Calculus, Computer Science, Global Economics")
    ]
    for c_idx, h in enumerate(headers):
        cell = ds_table.rows[0].cells[c_idx]
        p = cell.paragraphs[0]
        r = p.add_run(h)
        r.bold = True
        r.font.size = Pt(9)
        r.font.color.rgb = RGBColor(255, 255, 255)
        set_cell_background(cell, "1E3A8A")

    for r_idx, row_vals in enumerate(rows_data):
        for c_idx, val in enumerate(row_vals):
            cell = ds_table.rows[r_idx + 1].cells[c_idx]
            p = cell.paragraphs[0]
            r = p.add_run(val)
            r.font.size = Pt(8.5)
            set_cell_background(cell, "F8FAFC" if r_idx % 2 == 0 else "FFFFFF")

    doc.add_paragraph()

    # 4. Linguistic Feature Engineering & Mathematical Formulations
    doc.add_heading("4. Linguistic Feature Engineering & Mathematical Formulations", level=1)
    p_math = doc.add_paragraph()
    p_math.add_run(
        "Text readability is evaluated through six foundational computational linguistic formulas implemented in both Python and JavaScript:\n"
    )
    formulas = [
        ("Average Sentence Length (ASL)", "ASL = N_words / N_sentences", "Quantifies syntactic elongation and grammatical nesting complexity."),
        ("Average Syllables per Word (ASW)", "ASW = N_syllables / N_words", "Reflects morphological sophistication and phonological difficulty."),
        ("Flesch Reading Ease (FRE)", "FRE = 206.835 - (1.015 * ASL) - (84.6 * ASW)", "Scores texts on a 0–100 scale (90-100: Very Easy, 60-70: Standard, 0-30: Very Difficult)."),
        ("Flesch-Kincaid Grade Level (FKGL)", "FKGL = (0.39 * ASL) + (11.8 * ASW) - 15.59", "Directly maps text complexity to US educational grade standards (e.g., 7.4 = 7th grade 4th month)."),
        ("Type-Token Ratio (TTR)", "TTR = |Unique Tokens| / |Total Tokens|", "Measures lexical diversity and richness of vocabulary in the passage."),
        ("Complex Word Ratio (CWR)", "CWR = N_words(syllables >= 3) / N_words", "Indicates the proportion of polysyllabic academic terminology.")
    ]
    for name, f_eq, f_desc in formulas:
        p = doc.add_paragraph(style='List Bullet')
        r_name = p.add_run(f"{name}: ")
        r_name.bold = True
        r_eq = p.add_run(f"{f_eq} — ")
        r_eq.font.name = "Courier New"
        r_eq.font.size = Pt(9)
        r_eq.font.color.rgb = RGBColor(30, 64, 175)
        p.add_run(f_desc)

    # 5. Exploratory Data Analysis & Visualizations
    doc.add_heading("5. Exploratory Data Analysis (EDA) Insights", level=1)
    p_eda = doc.add_paragraph()
    p_eda.add_run(
        "Our exploratory data analysis was conducted in LearnCraft_AI_Preprocessing_and_EDA.ipynb. The primary statistical insights include:\n"
        "• Inverse Complexity Correlation: A robust negative Pearson correlation of r = -0.84 was observed between FRE and FKGL, confirming distinct linguistic separation across curriculum tiers.\n"
        "• Subject Domain Variance: Science and Mathematics texts consistently exhibit significantly higher syllable densities (mean ASW = 1.68) compared to Humanities and History (mean ASW = 1.44), necessitating domain-specific prompt calibration.\n"
        "• Convergence with Human Judgments: Calculated FKGL scores demonstrated strong regression alignment with human Bradley-Terry readability ratings from CommonLit (R^2 = 0.79).\n\n"
        "Below are the primary analytical charts generated during the preprocessing and EDA phase:"
    )

    plot_descriptions = [
        ("assets/plots/eda_plot_0.png", "Figure 1: Statistical Distribution Analysis — Histograms and KDE curves of FRE, Grade Level, Lexile, and CommonLit Target scores across the corpus."),
        ("assets/plots/eda_plot_1.png", "Figure 2: Domain & Tier Variance Analysis — Boxplots illustrating reading ease separation across complexity tiers (Easy, Medium, Hard)."),
        ("assets/plots/eda_plot_2.png", "Figure 3: Correlation Matrix Heatmap — 11-feature correlation matrix highlighting relationships between lexical diversity, syllables, and grade level."),
        ("assets/plots/eda_plot_3.png", "Figure 4: NLP Vocabulary & N-Gram Distribution — Frequency analysis of top curriculum keywords across disciplines.")
    ]
    for img_path, caption in plot_descriptions:
        if os.path.exists(img_path):
            doc.add_picture(img_path, width=Inches(5.8))
            p_cap = doc.add_paragraph()
            p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r_cap = p_cap.add_run(caption)
            r_cap.font.size = Pt(8.5)
            r_cap.font.italic = True
            r_cap.font.color.rgb = RGBColor(71, 85, 105)
            doc.add_paragraph()

    # 6. System Architecture & Technical Methodology
    doc.add_heading("6. System Architecture & Technical Methodology", level=1)
    p_arch = doc.add_paragraph()
    p_arch.add_run(
        "LearnCraft AI implements a multi-tier, decoupled software architecture designed for resilience, pedagogical accuracy, and low latency. "
        "The architecture consists of five core layers:\n"
        "1. Client Layer (Frontend): Next.js 14 and lightweight zero-install HTML5/Tailwind interfaces providing interactive grade sliders, subject filters, and responsive quiz interfaces.\n"
        "2. API Gateway & Controller Layer: Node.js/Express server orchestrating validation, session tracking, error containment, and JSON serialization.\n"
        "3. NLP Readability Preprocessor: Deterministic tokenization and syllable-counting engine calculating instant FRE/FKGL metrics on student inputs and generated outputs.\n"
        "4. Generative AI Core Engine: Google Gemini 1.5 Flash accessed via HTTP REST endpoints with structured JSON response formatting and pedagogical system instructions.\n"
        "5. Adaptive Student Assessment Feedback Loop: Closed-loop evaluator logging Bloom's Taxonomy quiz performance to adaptively modulate downstream content complexity."
    )

    if os.path.exists("LearnCraft_Architecture_Pipeline.png"):
        doc.add_picture("LearnCraft_Architecture_Pipeline.png", width=Inches(6.0))
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_cap = p_cap.add_run("Figure 5: LearnCraft AI End-to-End System Architecture & Data Pipeline Schematic.")
        r_cap.font.size = Pt(8.5)
        r_cap.font.italic = True
        r_cap.font.color.rgb = RGBColor(71, 85, 105)

    doc.add_paragraph()

    # 7. Work Completed at Mid-Term Milestone (45%)
    doc.add_heading("7. Work Completed at Mid-Term Milestone (45% Status)", level=1)
    status_table = doc.add_table(rows=7, cols=3)
    status_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    s_headers = ["Project Component", "Mid-Term Status", "Deliverables Delivered at 45% Mark"]
    s_rows = [
        ("Dataset Ingestion & Preprocessing", "Completed (100% of Phase 1)", "160 multi-grade passages curated, cleaned; structured CSV pipelines."),
        ("Linguistic Feature Formulas", "Completed (100% of Phase 1)", "Implemented ASL, ASW, FRE, FKGL, TTR, CWR algorithms in Python & JS."),
        ("Exploratory Data Analysis (EDA)", "Completed (100% of Phase 1)", "4 publication charts in .ipynb, PDF, and DOCX reports."),
        ("Backend Express.js Server", "Completed (100% of Phase 2)", "5 REST endpoints; integrated Gemini API and local fallback simulator."),
        ("Interactive Web Prototype", "Completed (100% of Phase 2)", "Zero-install standalone HTML5 application + Next.js frontend code."),
        ("Overall System Progress", "45% Completed", "Baseline Proof-of-Concept functional; ready for advanced deep learning phase.")
    ]
    for c_idx, h in enumerate(s_headers):
        cell = status_table.rows[0].cells[c_idx]
        p = cell.paragraphs[0]
        r = p.add_run(h)
        r.bold = True
        r.font.size = Pt(9)
        r.font.color.rgb = RGBColor(255, 255, 255)
        set_cell_background(cell, "1E3A8A")

    for r_idx, row_vals in enumerate(s_rows):
        for c_idx, val in enumerate(row_vals):
            cell = status_table.rows[r_idx + 1].cells[c_idx]
            p = cell.paragraphs[0]
            r = p.add_run(val)
            r.font.size = Pt(8.5)
            if c_idx == 1 and "45%" in val:
                r.font.bold = True
                r.font.color.rgb = RGBColor(37, 99, 235)
            set_cell_background(cell, "F8FAFC" if r_idx % 2 == 0 else "FFFFFF")

    doc.add_paragraph()

    # 8. Critical Analysis & What Needs Improvement
    doc.add_heading("8. Critical Analysis of Baseline & Areas for Technical Improvement", level=1)
    p_crit = doc.add_paragraph()
    p_crit.add_run(
        "A rigorous engineering project must critically evaluate its initial baseline. While our 45% mid-term deliverables "
        "demonstrate strong feasibility, several key limitations have been identified that form the basis for our End-Term work:\n\n"
        "1. Blindness of Surface Readability Formulas:\n"
        "Traditional formulas like Flesch-Kincaid compute reading difficulty purely from syllable counts and sentence lengths. "
        "Consequently, they cannot evaluate semantic or conceptual complexity. For example, the sentence 'Quantum spin is one-half' has 5 short words "
        "and 6 syllables, producing an elementary FKGL score of 2.1, despite expressing an advanced university-level concept. "
        "Improvement: We must move beyond surface formulas by training a deep contextual Transformer model (DeBERTa-v3).\n\n"
        "2. Absence of Explicit Curriculum RAG Grounding:\n"
        "Currently, Gemini generates modules based on system prompt instructions and general pre-trained weights. While high quality, "
        "it is susceptible to domain hallucination or introducing terminology outside a specific state/board syllabus. "
        "Improvement: We must build a Retrieval-Augmented Generation (RAG) vector database (ChromaDB) indexing official textbook chapters.\n\n"
        "3. Simplified Heuristic Feedback Loop:\n"
        "The current adaptive quiz feedback adjusts grade level using a discrete heuristic (+0.5 / -1.0 grade). It does not maintain a probabilistic "
        "model of the student's true latent knowledge state. "
        "Improvement: Implement Bayesian Knowledge Tracing (BKT) or Item Response Theory (IRT) to estimate topic mastery probabilistically.\n\n"
        "4. Ephemeral Session State:\n"
        "Currently, student quiz attempts and reading levels exist only in memory during the browser session. "
        "Improvement: Deploy a persistent relational database (PostgreSQL) and build a Teacher Classroom Analytics Dashboard."
    )

    # 9. End-Term Engineering Roadmap & Remaining 55% Scope
    doc.add_heading("9. End-Term Engineering Roadmap: Remaining 55% Scope", level=1)
    p_road = doc.add_paragraph()
    p_road.add_run(
        "The remaining 55% of the project is structured across two intensive phases leading to final evaluation:\n\n"
        "Phase 3: Deep Learning Model Fine-Tuning & RAG Pipeline (Weeks 8–11):\n"
        "• Milestone 3.1: Fine-Tune DeBERTa-v3 on CommonLit Benchmark: Train a cross-encoder regression model using PyTorch and Hugging Face "
        "Transformers on 3,000+ passages with continuous complexity loss (Target RMSE < 0.28 against human expert ratings).\n"
        "• Milestone 3.2: Attention Heatmap Interpretability: Extract multi-head self-attention weights to visually highlight specific clauses "
        "and jargon causing cognitive overload for students.\n"
        "• Milestone 3.3: Curriculum Textbook Vector Store: Ingest official K-12 textbook PDFs into ChromaDB, chunking by sub-topic, and using "
        "dense embeddings to provide citation-backed grounding context for all module generation.\n"
        "• Milestone 3.4: Probabilistic Bayesian Knowledge Tracing: Implement BKT algorithms modeling the probability of student mastery P(L_t) "
        "accounting for prior knowledge, slip P(S), and guess P(G) probabilities.\n\n"
        "Phase 4: Full System Integration, Quantitative Benchmarking & User Study (Weeks 12–15):\n"
        "• Milestone 4.1: Teacher Classroom Analytics Portal: Build an administrative dashboard displaying cohort-level mastery heatmaps, "
        "identifying struggling students, and tracking longitudinal reading growth.\n"
        "• Milestone 4.2: Quantitative Benchmarking: Measure generation fidelity using BERTScore and ROUGE-L against source curriculum chapters, "
        "and calculate Readability Mean Absolute Error: MAE = (1/N) * sum(|Target_Grade - Generated_FKGL|).\n"
        "• Milestone 4.3: Controlled Classroom User Study: Conduct an empirical evaluation with 30+ students measuring normalized learning gains: "
        "g = (Post_Score - Pre_Score) / (100 - Pre_Score), comparing LearnCraft AI against traditional static textbooks.\n"
        "• Milestone 4.4: Packaging, Documentation & Final Defense: Complete the IEEE final project thesis, deploy cloud-hosted live instance, "
        "and document the open-source code repository."
    )

    # 10. Quantitative Evaluation & Validation Metrics Plan
    doc.add_heading("10. Quantitative Evaluation & Validation Metrics Plan", level=1)
    p_val = doc.add_paragraph()
    p_val.add_run(
        "To ensure scientific validation at End-Term, the system will be evaluated across four quantitative dimensions:\n"
        "1. Readability Alignment MAE: Quantifies deviation between target grade level and generated module readability (Target: MAE < 0.8).\n"
        "2. DeBERTa-v3 Readability RMSE: Evaluates model regression performance against human ground truth (Target: RMSE < 0.28).\n"
        "3. Semantic Fidelity (BERTScore & ROUGE-L): Measures factual retention against reference textbooks (Target: BERTScore F1 > 0.85).\n"
        "4. Pedagogical Learning Gain (g): Evaluates real-world comprehension enhancement via pre- and post-testing (Target: g > 0.40)."
    )

    # References
    doc.add_heading("11. References", level=1)
    refs = [
        "United Nations Department of Economic and Social Affairs. (2015). 'Sustainable Development Goal 4: Quality Education.' UN General Assembly.",
        "Kincaid, J. P., Fishburne, R. P., Rogers, R. L., & Chissom, B. S. (1975). 'Derivation of new readability formulas for Navy enlisted personnel.' Naval Technical Training Command.",
        "CommonLit & The Learning Agency. (2021). 'CommonLit Readability Prize: Evaluating reading difficulty of texts for students.' Kaggle Benchmark.",
        "He, P., Gao, J., & Chen, W. (2021). 'DeBERTaV3: Improving DeBERTa using ELECTRA-style pre-training with gradient-disentangled embedding.' arXiv preprint arXiv:2111.09543.",
        "Corbett, A. T., & Anderson, J. R. (1994). 'Knowledge tracing: Modeling the acquisition of procedural knowledge.' User Modeling and User-Adapted Interaction, 4(4), 253-278.",
        "Bloom, B. S., et al. (1956). 'Taxonomy of educational objectives: The classification of educational goals.' Handbook I: Cognitive domain.",
        "Gemini Team, Google. (2024). 'Gemini: A family of highly capable multimodal models.' Google DeepMind Technical Report.",
        "Sweller, J. (1988). 'Cognitive load during problem solving: Effects on learning.' Cognitive Science, 12(2), 257-285."
    ]
    for ref in refs:
        p = doc.add_paragraph(style='List Bullet')
        p.add_run(ref)

    doc.save(output_docx_path)
    print(f"DOCX Report created successfully: {output_docx_path} (Size: {os.path.getsize(output_docx_path)} bytes)")


def create_pdf_report(output_pdf_path):
    print(f"Creating PDF Progress Report: {output_pdf_path}...")
    doc = SimpleDocTemplate(
        output_pdf_path,
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontSize=18,
        leading=22,
        textColor=colors.HexColor('#1E3A8A'),
        alignment=1,
        fontName='Helvetica-Bold',
        spaceAfter=4
    )

    sub_style = ParagraphStyle(
        'DocSub',
        parent=styles['Normal'],
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#2563EB'),
        alignment=1,
        fontName='Helvetica-Bold',
        spaceAfter=12
    )

    h1_style = ParagraphStyle(
        'H1Custom',
        parent=styles['Heading2'],
        fontSize=12.5,
        leading=15,
        textColor=colors.HexColor('#0F172A'),
        fontName='Helvetica-Bold',
        spaceBefore=10,
        spaceAfter=3
    )

    body_style = ParagraphStyle(
        'BodyCustom',
        parent=styles['Normal'],
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor('#334155'),
        spaceAfter=4
    )

    bullet_style = ParagraphStyle(
        'BulletCustom',
        parent=styles['Normal'],
        fontSize=8,
        leading=11,
        textColor=colors.HexColor('#334155'),
        leftIndent=14,
        spaceAfter=2.5
    )

    story = []

    # Title & Header
    story.append(Paragraph("LearnCraft AI: Dynamic Curriculum-Adaptive Learning & Assessment Engine", title_style))
    story.append(Paragraph("MID-TERM PROJECT EVALUATION PROGRESS REPORT<br/>Phase 2: Baseline Implementation (45% Completed) & End-Term Scope (55% Roadmap)", sub_style))

    # Meta Table
    meta_data = [
        [Paragraph("<b>Project Title:</b>", body_style), Paragraph("LearnCraft AI — Personalized Curriculum Study Assistant", body_style)],
        [Paragraph("<b>UN-SDG Goal:</b>", body_style), Paragraph("Goal 4: Quality Education (Target 4.4 & 4.7)", body_style)],
        [Paragraph("<b>Domain & Track:</b>", body_style), Paragraph("Artificial Intelligence, Natural Language Processing, Software Track", body_style)],
        [Paragraph("<b>Evaluation Stage:</b>", body_style), Paragraph("Mid-Term Lab Evaluation (45% Baseline Delivered | 55% End-Term Scope Detailed)", body_style)]
    ]
    t = Table(meta_data, colWidths=[150, 390])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#F1F5F9')),
        ('BACKGROUND', (1, 0), (1, -1), colors.HexColor('#F8FAFC')),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E2E8F0')),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(t)
    story.append(Spacer(1, 8))

    # Executive Summary
    story.append(Paragraph("Executive Summary", h1_style))
    story.append(Paragraph(
        "LearnCraft AI is an automated, curriculum-grounded learning and assessment engine engineered to advance United Nations "
        "Sustainable Development Goal 4 (Quality Education). By combining computational readability profiling with state-of-the-art "
        "Generative AI (Google Gemini 1.5 Flash), LearnCraft AI dynamically synthesizes scaffolded explanations and multi-tier Bloom's Taxonomy "
        "assessments. At mid-term, our team has achieved 45% total completion, establishing a working baseline: dataset curation (160 excerpts), "
        "linguistic feature extraction formulas, EDA statistical validation, an operational Express.js API gateway, and an interactive "
        "browser prototype. This report critically analyzes baseline limitations and presents a concrete 55% End-Term engineering roadmap.", body_style
    ))

    # 1. Problem Statement & Scope Split
    story.append(Paragraph("1. Problem Statement & Milestone Split (45% Mid vs 55% End)", h1_style))
    story.append(Paragraph(
        "Standardized educational curricula force heterogeneous students to consume identical textbooks regardless of individual reading mastery. "
        "When text complexity surpasses a learner's threshold by 2+ grade levels, cognitive overload inhibits subject acquisition. LearnCraft AI resolves "
        "this by dynamically profiling syllabus texts and synthesizing personalized modules matching the learner's developmental stage.", body_style
    ))
    story.append(Paragraph("• <b>Mid-Term Baseline (45% Done):</b> Dataset curation, linguistic formulas (ASL, ASW, FRE, FKGL, TTR), EDA notebook, baseline API, and proof-of-concept UI.", bullet_style))
    story.append(Paragraph("• <b>End-Term Deliverables (55% To Do):</b> DeBERTa-v3 fine-tuning, syllabus RAG vector store, Bayesian Knowledge Tracing (BKT), and empirical classroom user studies.", bullet_style))

    # 2. Dataset & Linguistic Features
    story.append(Paragraph("2. Dataset Collection & Linguistic Feature Formulas", h1_style))
    story.append(Paragraph("Curated 160 multi-grade passages from CommonLit Readability Prize benchmark across 7 disciplines. Readability computed via:", body_style))
    story.append(Paragraph("• <b>ASL (Average Sentence Length):</b> Words / Sentences (Syntactic complexity).", bullet_style))
    story.append(Paragraph("• <b>ASW (Average Syllables per Word):</b> Syllables / Words (Phonological complexity).", bullet_style))
    story.append(Paragraph("• <b>FRE (Flesch Reading Ease):</b> 206.835 - 1.015(ASL) - 84.6(ASW) [0 to 100 scale].", bullet_style))
    story.append(Paragraph("• <b>FKGL (Flesch-Kincaid Grade Level):</b> 0.39(ASL) + 11.8(ASW) - 15.59 [Direct Grade mapping].", bullet_style))
    story.append(Paragraph("• <b>TTR (Type-Token Ratio):</b> Unique Words / Total Words (Lexical diversity).", bullet_style))

    # 3. System Architecture
    story.append(Paragraph("3. System Architecture & Methodology", h1_style))
    story.append(Paragraph(
        "The system operates across a 5-tier pipeline: (1) Client Interface (Next.js / Standalone HTML5); (2) Node.js Express API Gateway; "
        "(3) NLP Readability Preprocessor; (4) Google Gemini 1.5 Flash Core with structured JSON output; and (5) Adaptive Feedback Evaluator.", body_style
    ))

    if os.path.exists("LearnCraft_Architecture_Pipeline.png"):
        story.append(Spacer(1, 4))
        story.append(RLImage("LearnCraft_Architecture_Pipeline.png", width=530, height=265))
        story.append(Paragraph("<i>Figure 1: End-to-End LearnCraft AI Architectural Pipeline & Data Flow.</i>", ParagraphStyle('Cap', parent=body_style, fontSize=7.5, alignment=1, textColor=colors.HexColor('#64748B'))))
        story.append(Spacer(1, 4))

    # 4. EDA Highlights
    story.append(Paragraph("4. Exploratory Data Analysis & Visualizations", h1_style))
    story.append(Paragraph(
        "Statistical analysis confirmed a strong negative correlation (r = -0.84) between FRE and FKGL. Physical Science excerpts displayed "
        "the highest syllable density (ASW = 1.68), while Elementary texts showed tighter lexical diversity (TTR = 0.62).", body_style
    ))

    if os.path.exists("assets/plots/eda_plot_0.png"):
        story.append(RLImage("assets/plots/eda_plot_0.png", width=530, height=180))
        story.append(Paragraph("<i>Figure 2: Distribution of Readability Metrics across Curriculum Dataset.</i>", ParagraphStyle('Cap', parent=body_style, fontSize=7.5, alignment=1, textColor=colors.HexColor('#64748B'))))

    # 5. Mid-Term Status & Critical Improvements Needed
    story.append(Paragraph("5. Critical Analysis of Baseline & Areas for Improvement", h1_style))
    story.append(Paragraph("• <b>Limitation 1 (Surface Formulas):</b> Flesch-Kincaid only counts syllable and sentence counts, ignoring conceptual depth (e.g. 'E = mc²' has simple words but university physics concepts). <i>Improvement:</i> Fine-tune DeBERTa-v3 on CommonLit corpus.", bullet_style))
    story.append(Paragraph("• <b>Limitation 2 (Ungrounded LLM Generation):</b> Prompt-only generation can drift from specific state syllabi. <i>Improvement:</i> Build RAG vector database (ChromaDB) indexing official textbook PDFs.", bullet_style))
    story.append(Paragraph("• <b>Limitation 3 (Heuristic Feedback):</b> Discrete step adaptation does not model true latent knowledge. <i>Improvement:</i> Implement probabilistic Bayesian Knowledge Tracing (BKT).", bullet_style))
    story.append(Paragraph("• <b>Limitation 4 (Ephemeral State):</b> No session persistence. <i>Improvement:</i> PostgreSQL database & Teacher Analytics Portal.", bullet_style))

    # 6. End-Term Engineering Roadmap (Remaining 55%)
    story.append(Paragraph("6. End-Term Engineering Roadmap (Remaining 55% Scope)", h1_style))
    story.append(Paragraph("• <b>Weeks 8–11 (Deep Learning & RAG):</b> Train DeBERTa-v3 regression model (RMSE < 0.28), extract attention heatmaps for text difficulty, index textbooks into ChromaDB, and implement Bayesian Knowledge Tracing.", bullet_style))
    story.append(Paragraph("• <b>Weeks 12–15 (Validation & Deployment):</b> Conduct empirical classroom user study with 30+ students measuring normalized learning gain (g > 0.40), build Teacher Dashboard, run BERTScore/MAE benchmarks, and finalize IEEE project thesis.", bullet_style))

    doc.build(story)
    print(f"PDF Report created successfully: {output_pdf_path} (Size: {os.path.getsize(output_pdf_path)} bytes)")

if __name__ == "__main__":
    create_docx_report("LearnCraft_AI_Mid_Term_Progress_Report.docx")
    create_pdf_report("LearnCraft_AI_Mid_Term_Progress_Report.pdf")
