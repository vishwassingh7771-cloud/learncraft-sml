import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.offsetbox import AnchoredText

def create_architecture_diagram(output_path="assets/LearnCraft_Architecture_Pipeline.png"):
    # Set up figure
    fig = plt.figure(figsize=(16, 10), dpi=300)
    ax = fig.add_subplot(111)
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 10)
    ax.axis('off')

    # Background color
    fig.patch.set_facecolor('#0B0F19')
    ax.set_facecolor('#0B0F19')

    # Title Banner
    title_box = patches.FancyBboxPatch((0.8, 8.8), 14.4, 0.9, boxstyle="round,pad=0.2",
                                       fc="#161F30", ec="#3B82F6", lw=2)
    ax.add_patch(title_box)
    ax.text(8.0, 9.35, "LearnCraft AI — System Pipeline & Architecture", 
            ha='center', va='center', fontsize=20, fontweight='bold', color='#F8FAFC', fontfamily='sans-serif')
    ax.text(8.0, 8.95, "Personalized Study Assistant Powered by Dynamic Content Generation & Curriculum-Adaptive NLP (UN-SDG 4)", 
            ha='center', va='center', fontsize=11, color='#94A3B8', fontfamily='sans-serif')

    # Color Palette
    c_client = "#1E293B"       # Slate
    c_client_border = "#0EA5E9"# Sky
    c_server = "#1E293B"       # Slate
    c_server_border = "#6366F1"# Indigo
    c_nlp = "#1E293B"          # Slate
    c_nlp_border = "#10B981"   # Emerald
    c_ai = "#1E293B"           # Slate
    c_ai_border = "#F59E0B"    # Amber
    c_out = "#1E293B"          # Slate
    c_out_border = "#EC4899"   # Pink

    # Helper function to draw cards
    def draw_card(x, y, w, h, bg_color, border_color, title, items, tag=""):
        card = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.15",
                                      fc=bg_color, ec=border_color, lw=2)
        ax.add_patch(card)
        
        # Header bar
        header = patches.FancyBboxPatch((x, y + h - 0.7), w, 0.7, boxstyle="round,pad=0.08",
                                        fc=border_color, ec=border_color, lw=1)
        ax.add_patch(header)
        ax.text(x + w/2, y + h - 0.35, title, ha='center', va='center',
                fontsize=11, fontweight='bold', color='#FFFFFF', fontfamily='sans-serif')
        
        if tag:
            tag_box = patches.FancyBboxPatch((x + w - 1.2, y + h - 0.6), 1.0, 0.28,
                                             boxstyle="round,pad=0.04", fc="#0B0F19", ec="none")
            ax.add_patch(tag_box)
            ax.text(x + w - 0.7, y + h - 0.46, tag, ha='center', va='center',
                    fontsize=7, fontweight='bold', color=border_color)

        # Item text
        start_y = y + h - 1.05
        spacing = (h - 1.0) / (len(items) + 0.5)
        for i, item in enumerate(items):
            cur_y = start_y - (i * spacing)
            bullet = patches.Circle((x + 0.35, cur_y), 0.08, fc=border_color, ec="none")
            ax.add_patch(bullet)
            ax.text(x + 0.55, cur_y, item, ha='left', va='center',
                    fontsize=9, color='#E2E8F0', fontfamily='sans-serif')

    # Column 1: Client Layer (Frontend)
    draw_card(0.8, 4.4, 3.2, 3.8, c_client, c_client_border, 
              "1. Client Layer (Next.js)", 
              ["Next.js 14 App Router UI", 
               "Curriculum & Grade Selector", 
               "Reading Level (K-12 / Lexile)", 
               "Topic & Goal Prompt Builder", 
               "Interactive Quiz Console", 
               "Real-time Socratic Chat"], 
              "Frontend")

    # Column 2: Backend API & Gateway
    draw_card(4.4, 4.4, 3.2, 3.8, c_server, c_server_border, 
              "2. API Gateway & Controller", 
              ["Node.js / Express Server", 
               "Session & Auth Management", 
               "Input Sanitization & Guardrails", 
               "Curriculum Context Injector", 
               "cURL / HTTP Gemini API Client", 
               "Response Schema Validator"], 
              "Backend")

    # Column 3: Data Preprocessing & NLP
    draw_card(8.0, 4.4, 3.4, 3.8, c_nlp, c_nlp_border, 
              "3. Preprocessing & Readability", 
              ["CommonLit & Curriculum Dataset", 
               "Text Cleaning & Lemmatization", 
               "Flesch-Kincaid & Lexile Metric", 
               "Bloom's Taxonomy Difficulty Map", 
               "RoBERTa Reading Level Scorer", 
               "Context Window Chunking"], 
              "NLP / EDA")

    # Column 4: Generative AI Core
    draw_card(11.8, 4.4, 3.4, 3.8, c_ai, c_ai_border, 
              "4. Generative AI Engine", 
              ["Google Gemini 1.5 Flash / Pro", 
               "Multi-Turn Educational Context", 
               "Custom Module Generation", 
               "Adaptive Quiz Synthesis", 
               "Explain-Like-I'm-Grade-X", 
               "Localized Dialect / Guides"], 
              "LLM Core")

    # Horizontal Connecting Arrows along top flow
    arrow_props = dict(arrowstyle="->,head_width=0.4,head_length=0.6", lw=2.5, color="#60A5FA")
    ax.annotate("", xy=(4.35, 6.3), xytext=(4.05, 6.3), arrowprops=arrow_props)
    ax.annotate("", xy=(7.95, 6.3), xytext=(7.65, 6.3), arrowprops=arrow_props)
    ax.annotate("", xy=(11.75, 6.3), xytext=(11.45, 6.3), arrowprops=arrow_props)

    # Bottom Output & Adaptive Feedback Layer
    out_box = patches.FancyBboxPatch((0.8, 0.9), 14.4, 2.7, boxstyle="round,pad=0.2",
                                     fc="#131B2E", ec="#A855F7", lw=2)
    ax.add_patch(out_box)
    
    # Output Header
    ax.text(8.0, 3.25, "5. Educational Deliverables & Adaptive Student Feedback Loop", 
            ha='center', va='center', fontsize=13, fontweight='bold', color="#C084FC")

    # Deliverables cards inside bottom box
    sub_cards = [
        ("Tailored Learning Modules", "Grade-specific, scaffolded explanations with real-world analogies.", "#38BDF8", 1.2),
        ("Curriculum-Aligned Quizzes", "Dynamic MCQs + short answers mapped to Bloom's cognitive levels.", "#34D399", 4.7),
        ("Localized Study Guides", "Custom summaries localized with regional examples and multilingual support.", "#FBBF24", 8.2),
        ("Student Progress Tracker", "Quiz scoring feedback loop adjusts future module complexity in real-time.", "#F472B6", 11.7)
    ]

    for title, desc, col, x_pos in sub_cards:
        sc = patches.FancyBboxPatch((x_pos, 1.2), 3.1, 1.7, boxstyle="round,pad=0.1",
                                    fc="#1E293B", ec=col, lw=1.5)
        ax.add_patch(sc)
        ax.text(x_pos + 1.55, 2.55, title, ha='center', va='center',
                fontsize=9.5, fontweight='bold', color=col)
        ax.text(x_pos + 1.55, 1.85, desc, ha='center', va='center',
                fontsize=8, color="#CBD5E1", wrap=True, multialignment='center')

    # Downward and upward loop arrows
    # Down from Gemini to Outputs
    ax.annotate("", xy=(13.5, 3.65), xytext=(13.5, 4.35),
                arrowprops=dict(arrowstyle="->,head_width=0.4,head_length=0.6", lw=2.5, color="#F59E0B"))
    ax.text(13.6, 4.0, "Deliverables", fontsize=8, color="#FCD34D", fontweight='bold')

    # Upward Feedback Loop from Student Progress back to Frontend / Backend
    ax.annotate("", xy=(2.4, 4.35), xytext=(2.4, 3.65),
                arrowprops=dict(arrowstyle="->,head_width=0.4,head_length=0.6", lw=2.5, color="#F472B6"))
    ax.text(2.5, 4.0, "Adaptive Loop", fontsize=8, color="#F472B6", fontweight='bold')

    # Footer Notes
    ax.text(8.0, 0.45, "Tech Stack: Next.js 14 • Node.js Express • Google Gemini Generative API • CommonLit Dataset • RoBERTa NLP • UN-SDG Goal 4 Quality Education",
            ha='center', va='center', fontsize=9, color='#64748B', style='italic')

    plt.tight_layout()
    plt.savefig(output_path, facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight')
    plt.close()
    print(f"Architecture diagram successfully saved to {output_path}")

if __name__ == "__main__":
    create_architecture_diagram("assets/LearnCraft_Architecture_Pipeline.png")
    create_architecture_diagram("LearnCraft_Architecture_Pipeline.png")
