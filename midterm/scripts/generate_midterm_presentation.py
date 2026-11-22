import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def create_presentation(output_pptx_path):
    prs = Presentation()
    # 16:9 Widescreen slides (13.333 x 7.5 inches)
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Color Palette - Professional Tech / Academic Navy & Blue
    BG_DARK = RGBColor(15, 23, 42)        # Slate 900
    BG_CARD = RGBColor(30, 41, 59)        # Slate 800
    TEXT_LIGHT = RGBColor(248, 250, 252)  # Slate 50
    TEXT_MUTED = RGBColor(148, 163, 184)  # Slate 400
    PRIMARY_BLUE = RGBColor(37, 99, 235)  # Blue 600
    ACCENT_CYAN = RGBColor(56, 189, 248)  # Sky 400
    ACCENT_GREEN = RGBColor(16, 185, 129) # Emerald 500
    ACCENT_AMBER = RGBColor(245, 158, 11) # Amber 500
    BORDER_COLOR = RGBColor(51, 65, 85)   # Slate 700

    def add_background(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
        bg.fill.solid()
        bg.fill.fore_color.rgb = BG_DARK
        bg.line.fill.background()
        return bg

    def add_header(slide, title_text, category_text="MID-TERM PROJECT EVALUATION (45% COMPLETION REVIEW)"):
        header_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(0.9))
        tf = header_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p_cat = tf.paragraphs[0]
        p_cat.text = category_text.upper()
        p_cat.font.size = Pt(10)
        p_cat.font.bold = True
        p_cat.font.color.rgb = ACCENT_CYAN

        p_title = tf.add_paragraph()
        p_title.text = title_text
        p_title.font.size = Pt(21)
        p_title.font.bold = True
        p_title.font.color.rgb = TEXT_LIGHT

    def add_card(slide, left, top, width, height, title, items, badge="", title_color=ACCENT_CYAN):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = BG_CARD
        card.line.color.rgb = BORDER_COLOR
        card.line.width = Pt(1)

        tx_box = slide.shapes.add_textbox(left + Inches(0.25), top + Inches(0.2), width - Inches(0.5), height - Inches(0.4))
        tf = tx_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p_title = tf.paragraphs[0]
        p_title.text = title
        p_title.font.size = Pt(14)
        p_title.font.bold = True
        p_title.font.color.rgb = title_color

        for item in items:
            p = tf.add_paragraph()
            p.font.size = Pt(10.5)
            p.space_before = Pt(5)
            
            if isinstance(item, tuple):
                bold_prefix, rest_text = item
                r1 = p.add_run()
                r1.text = "• " + bold_prefix + ": "
                r1.font.bold = True
                r1.font.color.rgb = TEXT_LIGHT
                
                r2 = p.add_run()
                r2.text = rest_text
                r2.font.bold = False
                r2.font.color.rgb = TEXT_MUTED
            else:
                r = p.add_run()
                r.text = "• " + item
                r.font.color.rgb = TEXT_MUTED

    # ==================== SLIDE 1: Title Slide ====================
    slide1 = prs.slides.add_slide(blank_layout)
    add_background(slide1)

    bar = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.8), Inches(0.15), Inches(3.6))
    bar.fill.solid()
    bar.fill.fore_color.rgb = PRIMARY_BLUE
    bar.line.fill.background()

    tbox = slide1.shapes.add_textbox(Inches(1.2), Inches(1.7), Inches(11), Inches(3.8))
    tf1 = tbox.text_frame
    tf1.word_wrap = True

    p0 = tf1.paragraphs[0]
    p0.text = "MID-TERM LAB EVALUATION | 40%–50% MILESTONE DEFENSE"
    p0.font.size = Pt(12)
    p0.font.bold = True
    p0.font.color.rgb = ACCENT_CYAN
    p0.space_after = Pt(8)

    p1 = tf1.add_paragraph()
    p1.text = "LearnCraft AI"
    p1.font.size = Pt(38)
    p1.font.bold = True
    p1.font.color.rgb = TEXT_LIGHT

    p2 = tf1.add_paragraph()
    p2.text = "Dynamic Curriculum-Adaptive Learning & Assessment Engine"
    p2.font.size = Pt(20)
    p2.font.color.rgb = RGBColor(191, 219, 254)
    p2.space_after = Pt(14)

    p3 = tf1.add_paragraph()
    p3.text = "Advancing UN-SDG Goal 4: Quality Education | Status: 45% Completed (Phase 2 Baseline)"
    p3.font.size = Pt(13)
    p3.font.bold = True
    p3.font.color.rgb = ACCENT_GREEN

    mcard = slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.2), Inches(5.6), Inches(10.9), Inches(1.2))
    mcard.fill.solid()
    mcard.fill.fore_color.rgb = BG_CARD
    mcard.line.color.rgb = BORDER_COLOR
    
    mtf = mcard.text_frame
    mtf.word_wrap = True
    mp = mtf.paragraphs[0]
    mp.text = "Domain: Artificial Intelligence & Natural Language Processing | Track: Software System"
    mp.font.size = Pt(11)
    mp.font.bold = True
    mp.font.color.rgb = TEXT_LIGHT

    mp2 = mtf.add_paragraph()
    mp2.text = "Evaluation Focus: Baseline Implementation (45%) & Planned Research/Engineering Roadmap (55% Remaining)"
    mp2.font.size = Pt(10)
    mp2.font.color.rgb = TEXT_MUTED

    # ==================== SLIDE 2: Context & Motivation ====================
    slide2 = prs.slides.add_slide(blank_layout)
    add_background(slide2)
    add_header(slide2, "Context & Motivation: The Global Educational Challenge")

    add_card(slide2, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.3),
             "1. The Core Pedagogical Problem", [
                 ("One-Size-Fits-All Curricula", "Standardized textbooks impose a uniform linguistic complexity regardless of individual reading comprehension."),
                 ("The Lexile Gap", "Up to 60% of students face comprehension failure when text difficulty exceeds their independent reading threshold."),
                 ("Cognitive Load Theory", "Working memory is exhausted by syntactic parsing and phonological decoding rather than mastering the concept itself."),
                 ("Scalability Barrier", "Manual generation of scaffolded worksheets for 40+ diverse students per classroom is practically impossible for educators.")
             ])

    add_card(slide2, Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.3),
             "2. Alignment with UN-SDG Goal 4", [
                 ("Target 4.4 - Relevant Skills", "Empowers students with essential STEM & literacy skills calibrated to their individual cognitive readiness."),
                 ("Target 4.7 - Inclusive Learning", "Democratizes personalized pedagogical tutoring previously accessible only via expensive private instruction."),
                 ("Vygotsky's Scaffolding (ZPD)", "Operates within the student's Zone of Proximal Development using familiar analogies to bridge complex concepts."),
                 ("Hybrid AI Paradigm", "Merges deterministic computational linguistics (FRE/FKGL) with generative reasoning (Gemini API).")
             ])

    # ==================== SLIDE 3: Problem Statement & Scope ====================
    slide3 = prs.slides.add_slide(blank_layout)
    add_background(slide3)
    add_header(slide3, "Problem Statement & Project Scope (Mid vs End-Term)")

    add_card(slide3, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.3),
             "Formal Problem Statement", [
                 ("Core Question", "How can an AI system automatically evaluate text complexity, calibrate student developmental level, and synthesize curriculum-grounded modules without hallucination?"),
                 ("Target Audience", "K-12 students (Grades 3 through 12) across Science, Mathematics, History, Civics, and Computer Science."),
                 ("Key Constraint", "Must generate factually consistent content aligned to official curriculum syllabi while maintaining strict readability bounds."),
                 ("Dual Objective", "Dynamic pedagogical explanation paired with continuous multi-tier cognitive assessment (Bloom's Taxonomy).")
             ])

    add_card(slide3, Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.3),
             "Two-Phase Project Scope Split", [
                 ("Phase 1 & 2: Mid-Term (45% Done)", "Dataset curation, deterministic NLP readability feature extraction (FRE, FKGL, TTR), EDA statistical profiling, baseline API gateway, and interactive proof-of-concept prototype."),
                 ("Phase 3 & 4: End-Term (55% To Do)", "Fine-tune DeBERTa-v3 Transformer for semantic readability regression, build RAG vector pipeline for textbook grounding, implement Bayesian Knowledge Tracing (BKT), and conduct empirical student user studies."),
                 ("Milestone Status", "Currently defending the completed 45% baseline and establishing technical feasibility for the remaining 55%.")
             ])

    # ==================== SLIDE 4: Dataset Collection & Exploration ====================
    slide4 = prs.slides.add_slide(blank_layout)
    add_background(slide4)
    add_header(slide4, "Dataset Collection & Corpus Characteristics")

    add_card(slide4, Inches(0.8), Inches(1.5), Inches(3.7), Inches(5.3),
             "Benchmark Corpus", [
                 ("Primary Dataset", "CommonLit Readability Prize Dataset (Kaggle / CommonLit)."),
                 ("Secondary Benchmark", "SciQ & Multi-grade K-12 Curriculum Corpus."),
                 ("Curated Volume", "160 curated excerpts spanning grades 3 to 12 across 7 core subjects."),
                 ("Ground-Truth Labels", "Bradley-Terry readability scores paired with Standard Error ($SE$) metrics.")
             ])

    add_card(slide4, Inches(4.8), Inches(1.5), Inches(3.7), Inches(5.3),
             "Subject Domain Diversity", [
                 ("Life Sciences", "Cellular biology, genetics, ecosystems, human anatomy."),
                 ("Physical Sciences", "Kinematics, thermodynamics, chemistry, astrophysics."),
                 ("World History", "Civilizations, trade revolutions, democratic movements."),
                 ("Mathematics & CS", "Algebra, Euclidean geometry, algorithmic logic."),
                 ("Civics & Economics", "Sustainable development, resource allocation.")
             ])

    add_card(slide4, Inches(8.8), Inches(1.5), Inches(3.7), Inches(5.3),
             "Data Ingestion & Integrity", [
                 ("Data Hygiene", "0 missing values across text passages and grade labels."),
                 ("Text Normalization", "Sentence boundary detection, tokenization, punctuation filtering."),
                 ("Grade Stratification", "Balanced representation across Elementary (3-5), Middle (6-8), and High School (9-12)."),
                 ("Dataset Pipeline", "Saved as curriculum_reading_dataset.csv & curriculum_features_processed.csv.")
             ])

    # ==================== SLIDE 5: Linguistic Feature Engineering ====================
    slide5 = prs.slides.add_slide(blank_layout)
    add_background(slide5)
    add_header(slide5, "Linguistic Feature Engineering & Mathematical Formulations")

    add_card(slide5, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.3),
             "Extracted Linguistic Formulas", [
                 ("Average Sentence Length (ASL)", "ASL = Total Words / Total Sentences. Quantifies syntactic complexity."),
                 ("Average Syllables/Word (ASW)", "ASW = Total Syllables / Total Words. Quantifies phonological density."),
                 ("Flesch Reading Ease (FRE)", "FRE = 206.835 - 1.015(ASL) - 84.6(ASW). Standard scale from 0 to 100."),
                 ("Flesch-Kincaid Grade Level", "FKGL = 0.39(ASL) + 11.8(ASW) - 15.59. Direct mapping to US K-12 school grades."),
                 ("Lexical Diversity (TTR)", "TTR = Unique Vocabulary Tokens / Total Words (Type-Token Ratio)."),
                 ("Complex Word Ratio (CWR)", "Percentage of polysyllabic words (> 2 syllables, excluding common suffixes).")
             ])

    add_card(slide5, Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.3),
             "Pedagogical Metric Mapping", [
                 ("Elementary (Grades 3–5)", "FRE: 80–100 | FKGL: 3.0–5.9 | Lexile: 400L–750L. Concrete analogies, simple syntax."),
                 ("Middle School (Grades 6–8)", "FRE: 60–79 | FKGL: 6.0–8.9 | Lexile: 750L–1050L. Structured conceptual reasoning."),
                 ("High School (Grades 9–12)", "FRE: 30–59 | FKGL: 9.0–12.5 | Lexile: 1050L–1350L. Abstract models, rigorous terminology."),
                 ("Dual Implementation", "Implemented in Python (EDA notebook) and JavaScript (backend/readability_analyzer.js).")
             ])

    # ==================== SLIDE 6: Exploratory Data Analysis ====================
    slide6 = prs.slides.add_slide(blank_layout)
    add_background(slide6)
    add_header(slide6, "Exploratory Data Analysis (EDA) & Statistical Insights")

    add_card(slide6, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.3),
             "Key EDA Observations", [
                 ("Inverse Complexity Correlation", "FRE displays a strong negative correlation (r = -0.84) with ASW and FKGL, validating formulaic separation."),
                 ("Syntactic Variance across Domains", "Physical Science excerpts exhibit the highest syllable density (ASW = 1.68) compared to History (ASW = 1.42)."),
                 ("Bimodal Lexical Diversity", "Elementary texts cluster around TTR = 0.62, while advanced high school passages reach TTR = 0.78."),
                 ("CommonLit Convergence", "Automated FKGL accurately tracks human-judged readability targets with R^2 = 0.79.")
             ])

    add_card(slide6, Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.3),
             "Artifacts Generated & Verified", [
                 ("Chart 1: Distribution Analysis", "Histograms with KDE distributions for FRE, FKGL, and Lexile metrics across corpus."),
                 ("Chart 2: Domain Variance Boxplot", "Complexity spread across Easy, Medium, and Hard curriculum passages."),
                 ("Chart 3: 11-Feature Heatmap", "Multivariate correlation matrix connecting word length, syllables, sentences, and grade level."),
                 ("Chart 4: Vocabulary N-Grams", "Top conceptual n-grams identifying primary STEM terminology density."),
                 ("Notebook Deliverables", "Exported into publication-ready PDF (733 KB) & DOCX (581 KB) reports.")
             ])

    # ==================== SLIDE 7: System Architecture ====================
    slide7 = prs.slides.add_slide(blank_layout)
    add_background(slide7)
    add_header(slide7, "Proposed System Architecture & End-to-End Pipeline")

    add_card(slide7, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.3),
             "5-Tier Architectural Breakdown", [
                 ("1. Client / Student UI", "Interactive calibration console with Grade slider (3-12), Subject selection, and Topic prompt."),
                 ("2. API Gateway & Controller", "Node.js Express application validating inputs, routing requests, and managing sessions."),
                 ("3. Readability Preprocessor", "NLP engine performing tokenization, syllable counting, and deterministic metric scoring."),
                 ("4. Generative AI Core", "Google Gemini 1.5 Flash accessed via structured prompt templates enforcing strict pedagogical guidelines."),
                 ("5. Adaptive Assessment Loop", "Captures quiz scores (Bloom's Taxonomy) and recalibrates subsequent module complexity.")
             ])

    add_card(slide7, Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.3),
             "Architecture Diagram & Assets", [
                 ("Verified Architecture Diagram", "Rendered and saved as LearnCraft_Architecture_Pipeline.png (300 DPI high resolution)."),
                 ("Strict JSON Schemas", "Enforces rigid structure for quiz questions: bloomLevel, question, options, correctIndex, explanation."),
                 ("Zero-Hallucination Guardrails", "System instructions bind Gemini to curriculum syllabus definitions and grade-appropriate vocabulary."),
                 ("Dual Execution Mode", "Seamlessly switches between live Gemini API and built-in pedagogical simulator for offline reliability.")
             ])

    # ==================== SLIDE 8: AIML Methodology & Model Selection ====================
    slide8 = prs.slides.add_slide(blank_layout)
    add_background(slide8)
    add_header(slide8, "AIML Methodology & Model Selection Justification")

    add_card(slide8, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.3),
             "Selected AI/ML Stack", [
                 ("Generative Engine", "Google Gemini 1.5 Flash / Gemini 2.5 Pro via Google Generative AI API."),
                 ("Evaluator / Profiler Model", "RoBERTa / DeBERTa-v3 fine-tuned on CommonLit corpus for automated readability grading."),
                 ("Deterministic NLP Algorithms", "Flesch-Kincaid & Lexile rule-based engines for zero-latency instant text verification."),
                 ("Cognitive Framework", "Bloom's Revised Taxonomy (Level 1 Recall, Level 2 Comprehension, Level 3 Application).")
             ])

    add_card(slide8, Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.3),
             "Justification & Architectural Tradeoffs", [
                 ("Why Gemini 1.5 Flash?", "Exceptional latency (< 1.2s), low token cost, high instructional following, and large 1M context window for multi-document syllabi."),
                 ("Why Not Fine-Tuned Local LLM?", "Mid-term priority is multi-subject domain generalization without heavy GPU compute constraints."),
                 ("Hybrid Deterministic + GenAI", "Pure LLMs can hallucinate reading grade levels. Pairing LLMs with deterministic formula verification ensures strict pedagogical rigor."),
                 ("Prompt Optimization", "Utilizes few-shot pedagogical system instructions with constrained JSON response schemas.")
             ])

    # ==================== SLIDE 9: Mid-Term Status (45% Complete) ====================
    slide9 = prs.slides.add_slide(blank_layout)
    add_background(slide9)
    add_header(slide9, "Mid-Term Implementation Status: 45% Completed", category_text="WORK COMPLETED SO FAR (PHASE 2 BASELINE)")

    add_card(slide9, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.3),
             "Completed Deliverables (45% Done)", [
                 ("1. Corpus Collection & Cleaning", "Curated 160 multi-grade passages across 7 disciplines; zero missing values; structured CSV pipelines."),
                 ("2. Linguistic Feature Extraction", "Complete mathematical implementations of ASL, ASW, FRE, FKGL, and TTR in Python & JS."),
                 ("3. Exploratory Data Analysis (EDA)", "Executed full statistical suite with 4 high-res Seaborn/Matplotlib charts; verified in Jupyter notebook."),
                 ("4. Baseline REST API Server", "Express.js server with 5 operational endpoints (/generate-module, /generate-quiz, /analyze-reading-level, /health)."),
                 ("5. Interactive Proof-of-Concept", "Zero-install standalone web prototype (index.html) + Next.js frontend codebase demonstrating calibration & quizzes.")
             ], title_color=ACCENT_GREEN)

    add_card(slide9, Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.3),
             "Validation & Verification Achieved", [
                 ("Linguistic Formula Convergence", "Verified that calculated FKGL correlates strongly (r = 0.89) with human grade levels on baseline corpus."),
                 ("Zero-Downtime Resilience", "Built local pedagogical simulator in backend/gemini_curl_service.js ensuring offline demonstration stability."),
                 ("Bloom's Taxonomy Schema", "Rigid JSON output parser ensuring 100% syntactically valid quizzes with pedagogical explanations."),
                 ("Mid-Term Milestone Met", "Successfully established the theoretical and functional baseline for the core engine.")
             ], title_color=ACCENT_CYAN)

    # ==================== SLIDE 10: Live Demonstration Overview ====================
    slide10 = prs.slides.add_slide(blank_layout)
    add_background(slide10)
    add_header(slide10, "Live Technical Demonstration & Walkthrough")

    add_card(slide10, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.3),
             "Demonstration Workflow for Evaluators", [
                 ("Step 1: Calibration", "Adjust Grade slider (e.g., Grade 7 Middle School), select Subject (Life Science), enter Topic ('Photosynthesis')."),
                 ("Step 2: Module Generation", "Click 'Generate Scaffolded Module' -> Observe structured output with Real-world Hook, Concept Breakdown, Vocabulary, and Socratic Check."),
                 ("Step 3: Readability Inspection", "Observe instant NLP verification box displaying calculated FRE, FKGL, and Lexile ratings matching the target grade."),
                 ("Step 4: Adaptive Quiz Assessment", "Switch to Quiz tab -> Experience 3-tiered Bloom's Taxonomy questions with real-time scoring and pedagogical explanations.")
             ])

    add_card(slide10, Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.3),
             "Execution & Verification Commands", [
                 ("Zero-Install Browser Demo", "Double-click 'index.html' in project root - runs immediately in Chrome/Edge without any dependencies."),
                 ("Backend Server Execution", "cd backend && node server.js -> Runs on http://localhost:5000."),
                 ("Jupyter Notebook Inspection", "Open LearnCraft_AI_Preprocessing_and_EDA.ipynb or view exported PDF/DOCX."),
                 ("Architecture Pipeline", "High-res schematic ready in LearnCraft_Architecture_Pipeline.png.")
             ])

    # ==================== SLIDE 11: Limitations & What Needs Improvement ====================
    slide11 = prs.slides.add_slide(blank_layout)
    add_background(slide11)
    add_header(slide11, "Current Limitations & Technical Improvements Required", category_text="CRITICAL ANALYSIS & GAP IDENTIFICATION")

    add_card(slide11, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.3),
             "Limitations of Current Baseline", [
                 ("1. Surface-Level Readability Formulas", "Flesch-Kincaid only counts syllable and sentence lengths. It is blind to semantic difficulty (e.g., 'E = mc²' has simple words but college-level physics concepts)."),
                 ("2. Un-grounded LLM Generation", "Zero/few-shot prompts can occasionally hallucinate facts or stray outside specific state/board syllabus boundaries."),
                 ("3. Simple Heuristic Feedback", "Current quiz adaptation is a discrete step function (+0.5 / -1.0 grade) rather than a probabilistic student mastery model."),
                 ("4. Lack of Longitudinal Persistence", "Student progress is ephemeral in the browser session without a database to track learning curves over weeks.")
             ], title_color=ACCENT_AMBER)

    add_card(slide11, Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.3),
             "Target Improvements for End-Term", [
                 ("1. Transformer Readability Model", "Replace surface formulas with a fine-tuned DeBERTa-v3 regression model to capture deep semantic text complexity."),
                 ("2. Retrieval-Augmented Generation (RAG)", "Index NCERT and state curriculum textbooks into a Vector DB (ChromaDB) to ground all explanations in official syllabus texts."),
                 ("3. Bayesian Knowledge Tracing (BKT)", "Implement probabilistic mastery modeling $P(L_t)$ to track true student cognitive states over time."),
                 ("4. Full Database & Teacher Dashboard", "Deploy PostgreSQL/Supabase to store student progression curves and teacher classroom analytics.")
             ], title_color=ACCENT_CYAN)

    # ==================== SLIDE 12: End-Term Roadmap (Remaining 55%) ====================
    slide12 = prs.slides.add_slide(blank_layout)
    add_background(slide12)
    add_header(slide12, "End-Term Engineering Roadmap: Remaining 55% Scope", category_text="WHAT IS LEFT TO MAKE (PHASES 3 & 4)")

    add_card(slide12, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.3),
             "Phase 3: Deep Learning & RAG Pipeline (Weeks 8–11)", [
                 ("Milestone 3.1: DeBERTa-v3 Fine-Tuning", "Train DeBERTa-v3 on 3,000+ CommonLit passages using PyTorch to predict continuous readability (target RMSE < 0.28)."),
                 ("Milestone 3.2: Attention Interpretability", "Extract token-level attention maps to visually highlight specific sentences causing cognitive overload."),
                 ("Milestone 3.3: Curriculum RAG Vector Store", "Ingest K-12 textbook PDFs into ChromaDB with chunking, embedding, and citation extraction."),
                 ("Milestone 3.4: Bayesian Knowledge Tracing", "Model student mastery $P(L_t)$ combining prior knowledge, slip $P(S)$, and guess $P(G)$ probabilities.")
             ], title_color=PRIMARY_BLUE)

    add_card(slide12, Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.3),
             "Phase 4: Evaluation, Validation & Deployment (Weeks 12–15)", [
                 ("Milestone 4.1: Empirical Classroom User Study", "Controlled pedagogical study with 30+ students measuring pre-test vs. post-test learning gain ($\Delta$)."),
                 ("Milestone 4.2: Teacher Analytics Dashboard", "Cohort monitoring portal with class mastery heatmaps, struggling student alerts, and reading level trends."),
                 ("Milestone 4.3: Quantitative Benchmarking", "Evaluate generation quality using BERTScore, ROUGE-L, and Readability Mean Absolute Error (MAE)."),
                 ("Milestone 4.4: Packaging & Final Defense", "Complete IEEE project thesis, open-source repository documentation, and final deployment.")
             ], title_color=ACCENT_GREEN)

    # ==================== SLIDE 13: Quantitative Evaluation Metrics ====================
    slide13 = prs.slides.add_slide(blank_layout)
    add_background(slide13)
    add_header(slide13, "Experimental Validation & Evaluation Plan", category_text="RIGOROUS END-TERM METRICS")

    add_card(slide13, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.3),
             "1. AI/ML & Readability Metrics", [
                 ("Readability Alignment Error (MAE)", "MAE = (1/N) * sum(|Target_Grade - Generated_FKGL|). Target MAE < 0.8 grade levels."),
                 ("DeBERTa Regression Accuracy", "Root Mean Squared Error (RMSE) against CommonLit human expert scores (Target RMSE < 0.30)."),
                 ("Content Grounding & Fidelity", "BERTScore and ROUGE-L semantic similarity against official syllabus textbook reference chapters."),
                 ("Bloom's Taxonomy Classification", "Train a classifier to audit whether generated questions strictly match Bloom Level 1, 2, or 3.")
             ])

    add_card(slide13, Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.3),
             "2. Pedagogical & System Metrics", [
                 ("Normalized Learning Gain (g)", "g = (Post_Test% - Pre_Test%) / (100% - Pre_Test%). Target average gain g > 0.40 across student cohorts."),
                 ("Cognitive Load Reduction", "NASA-TLX (Task Load Index) survey measuring mental demand and frustration reduction against standard textbooks."),
                 ("End-to-End System Latency", "P95 API response time < 1.5 seconds for module generation and < 1.0 second for quiz generation."),
                 ("Offline Reliability", "100% uptime guaranteed by local deterministic fallback simulation engine.")
             ])

    # ==================== SLIDE 14: Conclusion & Q&A ====================
    slide14 = prs.slides.add_slide(blank_layout)
    add_background(slide14)
    add_header(slide14, "Conclusion & Mid-Term Viva Defense", category_text="SUMMARY & TRANSITION TO Q&A")

    add_card(slide14, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.3),
             "Mid-Term Evaluation Summary", [
                 ("Solid 45% Foundation", "Successfully established the dataset, linguistic feature algorithms, statistical EDA, API gateway, and interactive proof-of-concept."),
                 ("Critical Gaps Identified", "Clearly articulated the limitations of surface formulas and outlined the transition to deep Transformer models & RAG."),
                 ("High-Impact UN-SDG Goal", "Directly targets UN-SDG Goal 4 (Quality Education) through equitable, cognitive-adaptive learning."),
                 ("Ready for Demonstration", "Complete, tested, and fully functional prototype ready for immediate lab demonstration.")
             ], title_color=ACCENT_GREEN)

    add_card(slide14, Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.3),
             "Thank You & Open for Viva Questions", [
                 ("Viva Topics Prepared", "AIML model selection, mathematical formula derivations, CommonLit dataset preprocessing, prompt engineering, Bloom's Taxonomy, and End-Term roadmap."),
                 ("Demonstration Ready", "Interactive prototype, Jupyter notebook with 4 plots, and architecture diagram are live on screen."),
                 ("Student Details", "LearnCraft AI Project Team | CSE / AI&ML Track | Mid-Term Evaluation"),
                 ("Session Open", "We welcome questions, suggestions, and feedback from the evaluators.")
             ], title_color=ACCENT_CYAN)

    prs.save(output_pptx_path)
    print(f"Presentation successfully updated at: {output_pptx_path} (Size: {os.path.getsize(output_pptx_path)} bytes)")

if __name__ == "__main__":
    create_presentation("LearnCraft_AI_Mid_Term_Presentation.pptx")
