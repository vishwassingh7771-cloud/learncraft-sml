// One place where the Next.js app pulls in the shared code and the trained model.
// These are the same files index.html loads, so both front ends behave identically.
import ml from '../../shared/readability_ml.js';
import content from '../../shared/learncraft_content.js';
import model from '../../models/ridge_features.json';

export const API = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000';

export const {
  SAMPLE_TEXT, markdownToHtml, fitFor, sampleLesson, chooseQuiz, readingTips,
} = content;

export function predict(text) {
  return ml.predictEasiness(text, model);
}

export const bandOf = (g) => (g <= 5 ? 'Elementary school' : g <= 8 ? 'Middle school' : 'High school');

export const TOPICS = [
  { topic: 'Photosynthesis', subject: 'Science', icon: '🌱', label: 'Photosynthesis' },
  { topic: 'The water cycle', subject: 'Science', icon: '💧', label: 'Water cycle' },
  { topic: "Ohm's law", subject: 'Science', icon: '⚡', label: "Ohm's law" },
  { topic: 'The Roman Republic', subject: 'History', icon: '🏛️', label: 'Roman Republic' },
  { topic: 'Quadratic equations', subject: 'Mathematics', icon: '📈', label: 'Quadratics' },
];

export const SUBJECTS = ['Science', 'Mathematics', 'History', 'Computer Science', 'Civics & Economics', 'English'];

export async function postJson(path, body) {
  const r = await fetch(`${API}${path}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
    signal: AbortSignal.timeout(30000),
  });
  return r.json();
}

// Small shared class strings
export const CHIP = 'text-sm px-3 py-1.5 rounded-full border border-slate-300 bg-white hover:border-indigo-400 hover:bg-indigo-50';
export const TOOL = 'text-sm px-3 py-1.5 rounded-lg border border-slate-300 bg-white hover:bg-slate-50 flex items-center gap-1.5';
export const toneOk = 'bg-emerald-50 border-emerald-200 text-emerald-900';
export const toneWarn = 'bg-amber-50 border-amber-200 text-amber-900';
