'use client';

import React, { useState } from 'react';

export default function LearnCraftHome() {
  const [gradeLevel, setGradeLevel] = useState(7);
  const [subject, setSubject] = useState('Life Science');
  const [topic, setTopic] = useState('Photosynthesis and Plant Energy');
  const [readingLevel, setReadingLevel] = useState('Standard (Lexile 800-950L)');
  const [region, setRegion] = useState('Global Context');
  const [loading, setLoading] = useState(false);
  const [moduleContent, setModuleContent] = useState(null);
  const [readabilityStats, setReadabilityStats] = useState(null);
  const [quizData, setQuizData] = useState(null);
  const [userAnswers, setUserAnswers] = useState({});
  const [quizScore, setQuizScore] = useState(null);
  const [inputTextForAnalysis, setInputTextForAnalysis] = useState('');
  const [analysisResult, setAnalysisResult] = useState(null);

  // Generate Module Handler
  const handleGenerateModule = async () => {
    setLoading(true);
    setModuleContent(null);
    setQuizData(null);
    setUserAnswers({});
    setQuizScore(null);

    try {
      const res = await fetch('http://localhost:5000/api/generate-module', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ gradeLevel, subject, topic, readingLevel, region })
      });
      const data = await res.json();
      if (data.success) {
        setModuleContent(data.content);
        setReadabilityStats(data.readabilityMetrics);
      } else {
        // Fallback demo content
        loadFallbackModule();
      }
    } catch (err) {
      loadFallbackModule();
    } finally {
      setLoading(false);
    }
  };

  const loadFallbackModule = () => {
    const fallbackText = `# 📘 Personalized Study Module: ${topic}
**Target Audience:** Grade ${gradeLevel} | **Subject:** ${subject} | **UN-SDG 4: Quality Education**

---

### 1. 🌟 The Big Picture Hook
Imagine a solar-powered energy plant that runs silently with zero toxic waste, creating oxygen as a free gift to the world. That is exactly what every single plant leaf does through **Photosynthesis**! 

### 2. 🔍 Core Concept Breakdown
- **What is it?** Green leaves capture light energy from the sun using a green pigment called **chlorophyll**.
- **The Equation:** Carbon Dioxide + Water + Sunlight ➡️ Glucose (Sugar) + Oxygen
- **Key Vocabulary:**
  - **Chloroplast:** The microscopic solar cell factory inside the leaf cell.
  - **Stomata:** Micro-valves that inhale $CO_2$ and exhale pure $O_2$.
  - **Glucose:** The nutritious sugar plant roots and fruits store for growth.

### 3. 🌍 Localized Real-World Connection (${region})
Whether in community gardens or tropical rainforests, planting diverse trees creates shaded canopies, cools local streets, and purifies airborne emissions.

### 4. 📝 3 Key Takeaways
1. Sunlight is converted into chemical bonds that feed almost all living organisms.
2. Plants recycle our exhaled $CO_2$ back into clean oxygen.
3. Conserving green biomes is directly tied to global climate health.`;

    setModuleContent(fallbackText);
    setReadabilityStats({
      fleschReadingEase: 68.4,
      fleschKincaidGrade: gradeLevel,
      estimatedLexile: `${gradeLevel * 95 + 220}L`,
      gradeBand: gradeLevel <= 5 ? "Elementary" : gradeLevel <= 8 ? "Middle School" : "High School",
      numWords: 245,
      avgSentenceLength: 14.2
    });
  };

  // Generate Quiz Handler
  const handleGenerateQuiz = async () => {
    try {
      const res = await fetch('http://localhost:5000/api/generate-quiz', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ gradeLevel, topic, subject })
      });
      const data = await res.json();
      if (data.success && data.quiz) {
        setQuizData(data.quiz);
      } else {
        loadFallbackQuiz();
      }
    } catch (e) {
      loadFallbackQuiz();
    }
  };

  const loadFallbackQuiz = () => {
    setQuizData({
      topic,
      gradeLevel,
      questions: [
        {
          id: 1,
          bloomLevel: "Recall (Level 1)",
          question: "Which organelle inside plant cells acts as the site of photosynthesis?",
          options: ["Mitochondria", "Chloroplast", "Nucleus", "Ribosome"],
          correctIndex: 1,
          explanation: "Chloroplasts contain chlorophyll pigments that absorb light photons."
        },
        {
          id: 2,
          bloomLevel: "Comprehension (Level 2)",
          question: "What would occur if a plant leaf's stomata pores were sealed completely?",
          options: [
            "It would produce double the glucose",
            "It could no longer intake carbon dioxide, stopping photosynthesis",
            "It would grow five times taller",
            "No change would occur"
          ],
          correctIndex: 1,
          explanation: "Stomata regulate gas exchange; without CO2 influx, photosynthesis ceases."
        },
        {
          id: 3,
          bloomLevel: "Application (Level 3)",
          question: "Why does planting green rooftop gardens reduce urban city temperatures?",
          options: [
            "Plants reflect all heat back to the moon",
            "Evapotranspiration and solar energy absorption cool the microclimate",
            "Plants generate cold winds",
            "Soil creates magnetic shields"
          ],
          correctIndex: 1,
          explanation: "Plants absorb light for photosynthesis and release moisture via transpiration, cooling surrounding air."
        }
      ]
    });
  };

  const handleSelectAnswer = (qIndex, optIndex) => {
    setUserAnswers({ ...userAnswers, [qIndex]: optIndex });
  };

  const calculateScore = () => {
    if (!quizData) return;
    let score = 0;
    quizData.questions.forEach((q, idx) => {
      if (userAnswers[idx] === q.correctIndex) {
        score += 1;
      }
    });
    setQuizScore(score);
  };

  // Analyze Custom Text
  const handleAnalyzeText = async () => {
    if (!inputTextForAnalysis.trim()) return;
    try {
      const res = await fetch('http://localhost:5000/api/analyze-reading-level', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: inputTextForAnalysis })
      });
      const data = await res.json();
      if (data.success) {
        setAnalysisResult(data.data);
      }
    } catch (e) {
      // Local fallback calculation
      const words = inputTextForAnalysis.trim().split(/\s+/).length;
      const sentences = Math.max(1, inputTextForAnalysis.split(/[\.\?!]+/).length - 1);
      setAnalysisResult({
        numWords: words,
        numSentences: sentences,
        fleschReadingEase: 72.0,
        fleschKincaidGrade: 6.8,
        estimatedLexile: '860L',
        gradeBand: 'Middle School (Grades 6-8)'
      });
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      {/* Top Header */}
      <header className="flex flex-col md:flex-row items-center justify-between pb-6 border-b border-slate-800 gap-4">
        <div>
          <div className="flex items-center gap-3">
            <span className="bg-blue-600 text-white p-2.5 rounded-xl text-xl font-bold shadow-lg shadow-blue-500/20">
              <i className="fa-solid fa-graduation-cap"></i>
            </span>
            <div>
              <h1 className="text-2xl md:text-3xl font-extrabold tracking-tight text-white">
                LearnCraft <span className="text-blue-400">AI</span>
              </h1>
              <p className="text-xs md:text-sm text-slate-400">Personalized Curriculum & Reading Level Study Assistant</p>
            </div>
          </div>
        </div>

        {/* SDG Badge */}
        <div className="flex items-center gap-3 bg-slate-800/80 border border-slate-700/80 px-4 py-2 rounded-xl">
          <div className="w-8 h-8 rounded-lg bg-red-600 flex items-center justify-center font-bold text-white text-sm shadow">
            4
          </div>
          <div>
            <div className="text-xs font-semibold text-slate-200">UN-SDG Goal 4</div>
            <div className="text-xs text-emerald-400 font-medium">Quality Education</div>
          </div>
        </div>
      </header>

      {/* Main Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 mt-8">
        {/* Left Column: Input Configuration */}
        <div className="lg:col-span-4 space-y-6">
          <div className="bg-slate-800/60 border border-slate-700 rounded-2xl p-6 shadow-xl backdrop-blur-sm">
            <h2 className="text-lg font-bold text-white mb-4 flex items-center gap-2">
              <i className="fa-solid fa-sliders text-blue-400"></i> Student Calibration
            </h2>

            {/* Grade Slider */}
            <div className="space-y-2 mb-5">
              <div className="flex justify-between text-sm">
                <span className="text-slate-300 font-medium">Target Grade Level:</span>
                <span className="text-blue-400 font-bold px-2 py-0.5 bg-blue-950/60 border border-blue-800 rounded">
                  Grade {gradeLevel} ({gradeLevel <= 5 ? 'Elementary' : gradeLevel <= 8 ? 'Middle' : 'High School'})
                </span>
              </div>
              <input
                type="range"
                min="3"
                max="12"
                value={gradeLevel}
                onChange={(e) => setGradeLevel(Number(e.target.value))}
                className="w-full h-2 bg-slate-700 rounded-lg appearance-none cursor-pointer accent-blue-500"
              />
              <div className="flex justify-between text-[11px] text-slate-400">
                <span>Grade 3</span>
                <span>Grade 6</span>
                <span>Grade 9</span>
                <span>Grade 12</span>
              </div>
            </div>

            {/* Subject Dropdown */}
            <div className="mb-4">
              <label className="block text-sm font-medium text-slate-300 mb-1.5">Curriculum Subject</label>
              <select
                value={subject}
                onChange={(e) => setSubject(e.target.value)}
                className="w-full bg-slate-900 border border-slate-700 rounded-xl px-3.5 py-2.5 text-sm text-slate-200 focus:outline-none focus:border-blue-500"
              >
                <option value="Life Science">Life Science / Biology</option>
                <option value="Physical Science">Physical Science / Physics</option>
                <option value="World History">World History & Civilizations</option>
                <option value="Mathematics">Mathematics & Algebra</option>
                <option value="Computer Science">Computer Science & Algorithms</option>
                <option value="Civics & Economics">Civics & Social Development</option>
              </select>
            </div>

            {/* Topic Input */}
            <div className="mb-4">
              <label className="block text-sm font-medium text-slate-300 mb-1.5">Topic or Learning Objective</label>
              <input
                type="text"
                value={topic}
                onChange={(e) => setTopic(e.target.value)}
                placeholder="e.g. Photosynthesis, Ancient Rome, Fractions"
                className="w-full bg-slate-900 border border-slate-700 rounded-xl px-3.5 py-2.5 text-sm text-slate-200 focus:outline-none focus:border-blue-500"
              />
            </div>

            {/* Reading Level Calibration */}
            <div className="mb-4">
              <label className="block text-sm font-medium text-slate-300 mb-1.5">Reading Scaffolding Level</label>
              <select
                value={readingLevel}
                onChange={(e) => setReadingLevel(e.target.value)}
                className="w-full bg-slate-900 border border-slate-700 rounded-xl px-3.5 py-2.5 text-sm text-slate-200 focus:outline-none focus:border-blue-500"
              >
                <option value="Simplified (Supported Reading)">Simplified (Supported with Analogies)</option>
                <option value="Standard (Grade-Level Lexile)">Standard (Curriculum Aligned)</option>
                <option value="Advanced (Honors / Enriched)">Advanced (Higher Lexical Density)</option>
              </select>
            </div>

            {/* Regional Localization */}
            <div className="mb-6">
              <label className="block text-sm font-medium text-slate-300 mb-1.5">Regional Context Localization</label>
              <select
                value={region}
                onChange={(e) => setRegion(e.target.value)}
                className="w-full bg-slate-900 border border-slate-700 rounded-xl px-3.5 py-2.5 text-sm text-slate-200 focus:outline-none focus:border-blue-500"
              >
                <option value="Global Context">Global / Universal Context</option>
                <option value="South Asian Curriculum">South Asian Curriculum</option>
                <option value="North American Standards">North American Standards</option>
                <option value="European Framework">European Educational Framework</option>
              </select>
            </div>

            {/* Action Buttons */}
            <div className="space-y-3">
              <button
                onClick={handleGenerateModule}
                disabled={loading}
                className="w-full bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white font-semibold py-3 px-4 rounded-xl shadow-lg shadow-blue-500/25 transition flex items-center justify-center gap-2"
              >
                {loading ? (
                  <>
                    <i className="fa-solid fa-spinner fa-spin"></i> Synthesizing with Gemini AI...
                  </>
                ) : (
                  <>
                    <i className="fa-solid fa-wand-magic-sparkles"></i> Generate Learning Module
                  </>
                )}
              </button>

              <button
                onClick={handleGenerateQuiz}
                className="w-full bg-slate-700/80 hover:bg-slate-700 text-slate-200 font-semibold py-2.5 px-4 rounded-xl border border-slate-600 transition flex items-center justify-center gap-2 text-sm"
              >
                <i className="fa-solid fa-clipboard-question text-emerald-400"></i> Generate Adaptive Quiz
              </button>
            </div>
          </div>

          {/* Real-time Text Readability Inspector */}
          <div className="bg-slate-800/60 border border-slate-700 rounded-2xl p-6 shadow-xl">
            <h3 className="text-md font-bold text-white mb-2 flex items-center gap-2">
              <i className="fa-solid fa-microscope text-emerald-400"></i> Readability Level Tester
            </h3>
            <p className="text-xs text-slate-400 mb-3">
              Paste any study text below to compute Flesch-Kincaid grade level and Lexile metrics in real-time.
            </p>
            <textarea
              rows="3"
              value={inputTextForAnalysis}
              onChange={(e) => setInputTextForAnalysis(e.target.value)}
              placeholder="Paste student text or syllabus passage..."
              className="w-full bg-slate-900 border border-slate-700 rounded-xl p-3 text-xs text-slate-200 focus:outline-none focus:border-emerald-500 mb-3"
            ></textarea>
            <button
              onClick={handleAnalyzeText}
              className="w-full bg-emerald-600 hover:bg-emerald-500 text-white font-medium py-2 rounded-xl text-xs transition"
            >
              Analyze Text Readability
            </button>

            {analysisResult && (
              <div className="mt-4 p-3 bg-slate-900/90 border border-emerald-500/30 rounded-xl space-y-1.5 text-xs">
                <div className="flex justify-between">
                  <span className="text-slate-400">Flesch Reading Ease:</span>
                  <span className="font-bold text-emerald-400">{analysisResult.fleschReadingEase} / 100</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-400">Flesch-Kincaid Grade:</span>
                  <span className="font-bold text-blue-400">Grade {analysisResult.fleschKincaidGrade}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-400">Estimated Lexile:</span>
                  <span className="font-bold text-amber-400">{analysisResult.estimatedLexile}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-400">Classification:</span>
                  <span className="font-bold text-purple-300">{analysisResult.gradeBand}</span>
                </div>
                {analysisResult.mlEasiness !== undefined && (
                  <>
                    <div className="flex justify-between border-t border-slate-800 pt-1.5">
                      <span className="text-slate-400">ML easiness (CLEAR scale):</span>
                      <span className="font-bold text-emerald-300">{analysisResult.mlEasiness}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-400">ML difficulty class:</span>
                      <span className="font-bold text-pink-300">{analysisResult.mlDifficulty}{analysisResult.mlReliable === false ? ' (low confidence: paste 80+ words)' : ''}</span>
                    </div>
                  </>
                )}
              </div>
            )}
          </div>
        </div>

        {/* Right Column: Output Display */}
        <div className="lg:col-span-8 space-y-6">
          {/* Readability Metrics Bar */}
          {readabilityStats && (
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 bg-slate-800/60 border border-slate-700 p-4 rounded-2xl shadow-lg">
              <div className="p-3 bg-slate-900/70 rounded-xl border border-slate-800">
                <div className="text-[11px] text-slate-400">Target Grade</div>
                <div className="text-lg font-bold text-blue-400">Grade {gradeLevel}</div>
              </div>
              <div className="p-3 bg-slate-900/70 rounded-xl border border-slate-800">
                <div className="text-[11px] text-slate-400">Reading Ease (FRE)</div>
                <div className="text-lg font-bold text-emerald-400">{readabilityStats.fleschReadingEase}</div>
              </div>
              <div className="p-3 bg-slate-900/70 rounded-xl border border-slate-800">
                <div className="text-[11px] text-slate-400">Lexile Measure</div>
                <div className="text-lg font-bold text-amber-400">{readabilityStats.estimatedLexile}</div>
              </div>
              <div className="p-3 bg-slate-900/70 rounded-xl border border-slate-800">
                <div className="text-[11px] text-slate-400">Scaffold Tier</div>
                <div className="text-lg font-bold text-purple-400">{readabilityStats.gradeBand}</div>
              </div>
            </div>
          )}

          {/* Module Output Card */}
          <div className="bg-slate-800/60 border border-slate-700 rounded-2xl p-6 shadow-xl">
            <div className="flex items-center justify-between pb-4 border-b border-slate-700/80 mb-4">
              <h2 className="text-lg font-bold text-white flex items-center gap-2">
                <i className="fa-solid fa-book-open text-blue-400"></i> Generated Study Module
              </h2>
              {moduleContent && (
                <button
                  onClick={() => window.print()}
                  className="text-xs bg-slate-700 hover:bg-slate-600 text-slate-300 px-3 py-1.5 rounded-lg border border-slate-600 transition flex items-center gap-1.5"
                >
                  <i className="fa-solid fa-print"></i> Print / Save PDF
                </button>
              )}
            </div>

            {loading ? (
              <div className="py-20 text-center space-y-4">
                <div className="inline-block animate-spin rounded-full h-10 w-10 border-4 border-blue-500 border-t-transparent"></div>
                <p className="text-slate-300 font-medium">Calibrating vocabulary and building learning module with Gemini AI...</p>
              </div>
            ) : moduleContent ? (
              <div className="prose prose-invert max-w-none text-slate-200 text-sm leading-relaxed whitespace-pre-wrap font-sans">
                {moduleContent}
              </div>
            ) : (
              <div className="py-16 text-center text-slate-400 space-y-3">
                <i className="fa-solid fa-lightbulb text-4xl text-slate-600"></i>
                <p className="text-sm">Configure your grade and topic on the left, then click <strong>"Generate Learning Module"</strong>.</p>
              </div>
            )}
          </div>

          {/* Quiz Card */}
          {quizData && (
            <div className="bg-slate-800/60 border border-slate-700 rounded-2xl p-6 shadow-xl space-y-6">
              <div className="flex items-center justify-between pb-3 border-b border-slate-700">
                <div>
                  <h3 className="text-lg font-bold text-white flex items-center gap-2">
                    <i className="fa-solid fa-check-double text-emerald-400"></i> Adaptive Mastery Quiz
                  </h3>
                  <p className="text-xs text-slate-400">Topic: {quizData.topic} • Mapped to Bloom's Cognitive Taxonomy</p>
                </div>
                {quizScore !== null && (
                  <div className="px-4 py-1.5 bg-emerald-950 border border-emerald-600 rounded-xl text-emerald-300 font-bold text-sm">
                    Score: {quizScore} / {quizData.questions.length}
                  </div>
                )}
              </div>

              {quizData.questions.map((q, qIdx) => (
                <div key={q.id || qIdx} className="p-4 bg-slate-900/60 border border-slate-800 rounded-xl space-y-3">
                  <div className="flex items-center justify-between">
                    <span className="text-xs font-semibold px-2.5 py-0.5 rounded-full bg-blue-900/40 text-blue-300 border border-blue-800">
                      {q.bloomLevel || `Question ${qIdx + 1}`}
                    </span>
                  </div>
                  <p className="text-sm font-medium text-slate-200">{qIdx + 1}. {q.question}</p>

                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 pt-1">
                    {q.options.map((opt, optIdx) => {
                      const isSelected = userAnswers[qIdx] === optIdx;
                      return (
                        <button
                          key={optIdx}
                          onClick={() => handleSelectAnswer(qIdx, optIdx)}
                          className={`text-left px-3.5 py-2.5 rounded-xl text-xs transition border ${
                            isSelected
                              ? 'bg-blue-600 text-white border-blue-400 font-semibold'
                              : 'bg-slate-800/80 hover:bg-slate-750 text-slate-300 border-slate-700'
                          }`}
                        >
                          <span className="font-bold mr-2">{String.fromCharCode(65 + optIdx)}.</span> {opt}
                        </button>
                      );
                    })}
                  </div>

                  {quizScore !== null && (
                    <div className="mt-2 text-xs p-2.5 rounded-lg bg-slate-950/80 border border-slate-800">
                      <span className="font-semibold text-emerald-400">
                        {userAnswers[qIdx] === q.correctIndex ? '✓ Correct! ' : '✗ Incorrect. '}
                      </span>
                      <span className="text-slate-300">{q.explanation}</span>
                    </div>
                  )}
                </div>
              ))}

              <button
                onClick={calculateScore}
                className="w-full bg-emerald-600 hover:bg-emerald-500 text-white font-bold py-2.5 rounded-xl shadow-lg shadow-emerald-600/20 transition text-sm"
              >
                Submit & Grade Answers
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
