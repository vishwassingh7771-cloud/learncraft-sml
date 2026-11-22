import os
import json
import base64
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io
import re

# Set random seed for reproducibility
np.random.seed(42)

def generate_dataset():
    print("Generating educational curriculum dataset...")
    subjects = ["Life Science", "Physical Science", "World History", "Literature & Arts", "Mathematics", "Computer Science", "Civics & Economics"]
    grade_levels = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    
    # Sample educational texts with varying complexity
    text_templates = {
        "easy": [
            "Plants need sunlight and water to grow strong. During photosynthesis, green leaves capture light from the sun. The roots drink water from the soil beneath them. This gives food to the plant and makes fresh oxygen for humans and animals to breathe.",
            "Long ago, people built castles out of heavy stones. Castles had high walls and deep moats filled with water. Knights wore shiny metal armor and protected the king and queen from danger. Life inside a castle was busy and full of work.",
            "Computers use tiny switches called bits. A bit can only be on or off, just like a light switch. When we put many bits together, the computer can show colorful pictures, play music, and solve fun math problems very quickly.",
            "The solar system has eight planets traveling around the sun. Mercury is the closest planet to the sun and gets very hot. Earth is our home where liquid water and clean air support all kinds of life.",
            "Money helps people trade goods and services fairly. When you buy a pencil at the store, you exchange coins or paper money for that item. Long ago, people traded items like wheat, salt, or cattle before coins were invented."
        ],
        "medium": [
            "Cellular respiration is the biochemical pathway through which organisms convert glucose into adenosine triphosphate (ATP). In eukaryotic cells, the mitochondria facilitate aerobic respiration, utilizing oxygen to produce energy while yielding carbon dioxide as a metabolic byproduct.",
            "The Industrial Revolution profoundly altered economic structures across Europe in the late eighteenth century. Handcrafted production gave way to steam-powered machinery in mechanized factories, accelerating urbanization and giving rise to modern labor movements.",
            "Algorithms are step-by-step procedures designed to solve computational problems efficiently. Sorting algorithms, such as quicksort and merge sort, organize unordered datasets by systematically comparing values and dividing problems into smaller subproblems.",
            "Newton's laws of motion form the bedrock of classical mechanics. His second law states that the net force applied to an object is proportional to the rate of change of its momentum, commonly formulated as force equals mass multiplied by acceleration (F = ma).",
            "Democratic governance relies upon institutional checks and balances to prevent the centralization of authority. In constitutional republics, legislative, executive, and judicial branches operate with distinct mandates to ensure political accountability."
        ],
        "hard": [
            "Epigenetic mechanisms modulate gene expression without modifying the underlying deoxyribonucleic acid nucleotide sequence. DNA methylation and post-translational histone modifications dynamically regulate chromatin architecture, thereby governing transcriptional accessibility during cellular differentiation.",
            "The socio-political destabilization culminating in the collapse of the Western Roman Empire was an intricate confluence of internal fiscal decay, systemic inflation, bureaucratic corruption, and unsustainable territorial overextension amidst incessant external incursions.",
            "Asymptotic computational complexity analyzes algorithm scalability through Big-O notation. When examining polynomial versus non-deterministic polynomial time algorithms (P versus NP), computer scientists explore the fundamental limits of algorithmic tractability and verifiable problem solving.",
            "Thermodynamic equilibrium dictates macroscopic state variables in isolated physical systems. The second law formalizes entropy maximization, stating that the total entropy of an isolated thermodynamic ensemble must monotonically increase over time, defining the thermodynamic arrow of time.",
            "Keynesian aggregate macroeconomic equilibrium posits that aggregate demand determines output and employment levels during cyclical contractions, asserting that sticky nominal wages preclude instantaneous market clearance absent counter-cyclical fiscal intervention."
        ]
    }
    
    data = []
    sample_id = 1001
    
    for i in range(160):
        grade = int(np.random.choice(grade_levels))
        subj = np.random.choice(subjects)
        
        if grade <= 5:
            tier = "easy"
            base_target = np.random.normal(-0.6, 0.4)
            lexile = int(np.random.normal(550, 100))
        elif grade <= 8:
            tier = "medium"
            base_target = np.random.normal(-1.4, 0.5)
            lexile = int(np.random.normal(900, 120))
        else:
            tier = "hard"
            base_target = np.random.normal(-2.3, 0.5)
            lexile = int(np.random.normal(1200, 150))
            
        base_text = np.random.choice(text_templates[tier])
        # Add slight variation
        words = base_text.split()
        word_count = len(words)
        char_count = len(base_text)
        std_error = round(float(np.random.uniform(0.42, 0.58)), 3)
        target_score = round(float(base_target), 4) # CommonLit target score (-3.5 to +1.5)
        
        data.append({
            "id": f"EXC-{sample_id}",
            "subject": subj,
            "target_grade": grade,
            "complexity_tier": tier.capitalize(),
            "lexile_rating": max(300, min(1600, lexile)),
            "commonlit_target": target_score,
            "standard_error": std_error,
            "excerpt_text": base_text
        })
        sample_id += 1
        
    df = pd.DataFrame(data)
    os.makedirs("dataset", exist_ok=True)
    df.to_csv("dataset/curriculum_reading_dataset.csv", index=False)
    print(f"Dataset generated with {len(df)} records at dataset/curriculum_reading_dataset.csv")
    return df

if __name__ == "__main__":
    generate_dataset()
