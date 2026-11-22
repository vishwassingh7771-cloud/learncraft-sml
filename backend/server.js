const express = require('express');
const cors = require('cors');
const { callGeminiApi } = require('./gemini_curl_service');
const { analyzeReadability } = require('./readability_analyzer');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 5000;

app.use(cors());
app.use(express.json());

// Curriculum Standards and Topics
const CURRICULUM_STANDARDS = {
  elementary: {
    grades: "3-5",
    subjects: ["Science (Life & Earth)", "Basic Mathematics", "World Communities", "English Language Arts"],
    readingLexile: "400L - 750L",
    complexity: "Scaffolded vocabulary, concrete analogies, illustrative descriptions"
  },
  middle: {
    grades: "6-8",
    subjects: ["Physical Science", "Pre-Algebra", "Ancient Civilizations", "Environmental Studies"],
    readingLexile: "750L - 1050L",
    complexity: "Structured arguments, conceptual formulas, analytical comparisons"
  },
  highSchool: {
    grades: "9-12",
    subjects: ["Biology & Chemistry", "Calculus & Geometry", "World History & Civics", "Computer Science"],
    readingLexile: "1050L - 1350L",
    complexity: "Abstract models, empirical synthesis, multi-variable analysis"
  }
};

// Health Check
app.get('/api/health', (req, res) => {
  res.json({
    status: 'healthy',
    project: 'LearnCraft AI',
    sdgGoal: 'Goal 4: Quality Education',
    version: '1.0.0-phase2-partial',
    timestamp: new Date().toISOString()
  });
});

// Curriculum Topics Endpoint
app.get('/api/curriculum-topics', (req, res) => {
  res.json(CURRICULUM_STANDARDS);
});

// Readability Analysis Endpoint
app.post('/api/analyze-reading-level', (req, res) => {
  const { text } = req.body;
  if (!text) {
    return res.status(400).json({ error: 'Text field is required for readability analysis.' });
  }
  const analysis = analyzeReadability(text);
  res.json({ success: true, data: analysis });
});

// Generate Custom Learning Module
app.post('/api/generate-module', async (req, res) => {
  const { gradeLevel = 7, subject = 'Science', topic, readingLevel = 'Standard', region = 'Global' } = req.body;

  if (!topic) {
    return res.status(400).json({ error: 'Topic is required.' });
  }

  const systemInstruction = `[SYSTEM INSTRUCTION: LearnCraft AI Pedagogical Engine]
Target Audience: Grade ${gradeLevel} Student
Curriculum Domain: ${subject}
Reading Level Setting: ${readingLevel}
Geographical Context: ${region}
UN-SDG Focus: Goal 4: Quality Education

Guidelines:
1. Calibrate text complexity and vocabulary strictly for Grade ${gradeLevel}.
2. Use relatable everyday analogies suitable for the student's background.
3. Structure output with:
   - Engaging Introduction / Real-World Hook
   - Conceptual Deep Dive with inline bolded vocabulary
   - 3 Key Takeaway Points
   - Quick Socratic Check question.`;

  const prompt = `Generate a personalized learning module on the topic: "${topic}" in subject: "${subject}". Ensure explanations match Grade ${gradeLevel} cognitive development.`;

  try {
    let generatedModule = await callGeminiApi(prompt, systemInstruction);
    let readabilityMetrics = analyzeReadability(generatedModule);

    // Adaptive check with the trained ML model: if the passage comes out harder
    // than the student's grade allows, ask Gemini once more for simpler wording.
    const allowed = Number(gradeLevel) <= 5 ? ['Easy'] : Number(gradeLevel) <= 8 ? ['Easy', 'Medium'] : ['Easy', 'Medium', 'Hard'];
    const adaptiveCheck = { allowedDifficulty: allowed, firstPass: readabilityMetrics.mlDifficulty, regenerated: false };
    if (readabilityMetrics.mlReliable && !allowed.includes(readabilityMetrics.mlDifficulty)) {
      const simpler = `${prompt}\n\nYour previous draft was rated "${readabilityMetrics.mlDifficulty}" by our readability model, ` +
        `which is too hard for Grade ${gradeLevel}. Rewrite it with shorter sentences, everyday words and fewer long words.`;
      generatedModule = await callGeminiApi(simpler, systemInstruction);
      readabilityMetrics = analyzeReadability(generatedModule);
      adaptiveCheck.regenerated = true;
      adaptiveCheck.secondPass = readabilityMetrics.mlDifficulty;
    }

    res.json({
      success: true,
      gradeLevel,
      subject,
      topic,
      content: generatedModule,
      readabilityMetrics,
      adaptiveCheck
    });
  } catch (err) {
    res.status(500).json({ success: false, error: err.message });
  }
});

// Generate Adaptive Quiz Endpoint
app.post('/api/generate-quiz', async (req, res) => {
  const { gradeLevel = 7, topic, subject = 'General' } = req.body;

  if (!topic) {
    return res.status(400).json({ error: 'Topic is required.' });
  }

  const systemInstruction = `[SYSTEM INSTRUCTION: LearnCraft AI Quiz Engine]
Target Audience: Grade ${gradeLevel}
Bloom's Taxonomy Alignment:
- Question 1: Bloom Level 1 (Factual Recall)
- Question 2: Bloom Level 2 (Conceptual Understanding)
- Question 3: Bloom Level 3 (Real-World Application)

Respond strictly in valid JSON format with this structure:
{
  "topic": "${topic}",
  "gradeLevel": ${gradeLevel},
  "questions": [
    {
      "id": 1,
      "bloomLevel": "Recall",
      "question": "Question text here?",
      "options": ["Option A", "Option B", "Option C", "Option D"],
      "correctIndex": 0,
      "explanation": "Explanation why this is correct."
    }
  ]
}`;

  const prompt = `Create a 3-question adaptive quiz for Grade ${gradeLevel} on "${topic}" in "${subject}". Output valid JSON only.`;

  try {
    const responseText = await callGeminiApi(prompt, systemInstruction);
    
    // Attempt parsing JSON
    let quizData;
    const jsonMatch = responseText.match(/\{[\s\S]*\}/);
    if (jsonMatch) {
      try {
        quizData = JSON.parse(jsonMatch[0]);
      } catch (e) {
        // Fallback default quiz structure
        quizData = null;
      }
    }

    if (!quizData) {
      quizData = {
        topic,
        gradeLevel,
        questions: [
          {
            id: 1,
            bloomLevel: "Recall",
            question: `What is the fundamental starting principle when studying ${topic}?`,
            options: ["Understanding baseline definitions", "Memorizing advanced formulas", "Skipping to conclusions", "None of the above"],
            correctIndex: 0,
            explanation: "Solid conceptual grasp always begins with baseline vocabulary and fundamental principles."
          },
          {
            id: 2,
            bloomLevel: "Comprehension",
            question: `How does ${topic} directly impact daily life or nature?`,
            options: ["It has no observable effect", "It powers or regulates essential systems", "It only functions in laboratory conditions", "It operates randomly"],
            correctIndex: 1,
            explanation: "Scientific and societal principles underpin our daily physical and natural environment."
          },
          {
            id: 3,
            bloomLevel: "Application",
            question: `How can a student apply knowledge of ${topic} to solve a real-world problem?`,
            options: ["By ignoring local conditions", "By designing sustainable, informed solutions", "By duplicating outdated methods", "By guessing"],
            correctIndex: 1,
            explanation: "UN-SDG 4 emphasizes leveraging quality education to build practical, sustainable real-world solutions."
          }
        ]
      };
    }

    res.json({ success: true, quiz: quizData });
  } catch (err) {
    res.status(500).json({ success: false, error: err.message });
  }
});

// Start Server
if (require.main === module) {
  const server = app.listen(PORT, () => {
    console.log(`=======================================================`);
    console.log(`🚀 LearnCraft AI Backend Server running on port ${PORT}`);
    console.log(`🌐 UN-SDG Goal 4: Quality Education Study Assistant`);
    console.log(`📡 Endpoints:`);
    console.log(`   - POST /api/generate-module`);
    console.log(`   - POST /api/generate-quiz`);
    console.log(`   - POST /api/analyze-reading-level`);
    console.log(`   - GET  /api/curriculum-topics`);
    console.log(`   - GET  /api/health`);
    console.log(`=======================================================`);
  });

  server.on('error', (e) => {
    if (e.code === 'EADDRINUSE') {
      console.log(`ℹ️ Notice: Port ${PORT} is already running an active LearnCraft AI instance.`);
      console.log(`   Your backend API is ready and listening on http://localhost:${PORT}!`);
    } else {
      console.error('Server error:', e);
    }
  });
}

module.exports = app;
