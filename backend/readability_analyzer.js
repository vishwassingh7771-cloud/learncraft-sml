/**
 * LearnCraft AI - Linguistic Readability Analysis Engine
 * Calculates standard educational metrics:
 * - Flesch Reading Ease (FRE)
 * - Flesch-Kincaid Grade Level (FKGL)
 * - Estimated Lexile Measure
 * - Lexical Diversity & Complexity Metrics
 */

const path = require('path');
const ml = require(path.join(__dirname, '..', 'shared', 'readability_ml.js'));
let RIDGE_MODEL = null;
try {
  RIDGE_MODEL = require(path.join(__dirname, '..', 'models', 'ridge_features.json'));
} catch (e) {
  console.warn('[readability] models/ridge_features.json not found - run `python ml/train.py`');
}

function countSyllables(word) {
  word = word.toLowerCase().trim();
  if (word.length <= 3) return 1;
  word = word.replace(/(?:[^laeiouy]|ed|es|e)$/, '');
  word = word.replace(/^y/, '');
  const matches = word.match(/[aeiouy]{1,2}/g);
  return matches ? Math.max(1, matches.length) : 1;
}

function analyzeReadability(text) {
  if (!text || typeof text !== 'string' || text.trim().length === 0) {
    return { error: "Invalid text input" };
  }

  const sentences = text.split(/[\.\?!]+/).filter(s => s.trim().length > 0);
  const numSentences = Math.max(1, sentences.length);

  const words = text.match(/\b[a-zA-Z]+\b/g) || [];
  const numWords = Math.max(1, words.length);

  const syllables = words.map(w => countSyllables(w));
  const totalSyllables = syllables.reduce((a, b) => a + b, 0);

  const asl = numWords / numSentences; // Average Sentence Length
  const asw = totalSyllables / numWords; // Average Syllables per Word

  // Classical Flesch Reading Ease formula
  const fre = 206.835 - (1.015 * asl) - (84.6 * asw);

  // Flesch-Kincaid Grade Level formula
  const fkgl = (0.39 * asl) + (11.8 * asw) - 15.59;

  // Approximate Lexile Rating mapping
  // Grade 3 ~ 450L, Grade 6 ~ 850L, Grade 9 ~ 1100L, Grade 12 ~ 1300L
  const estimatedLexile = Math.max(200, Math.min(1600, Math.round(fkgl * 95 + 220)));

  // Vocabulary Diversity (Type-Token Ratio)
  const uniqueWords = new Set(words.map(w => w.toLowerCase()));
  const lexicalDiversity = uniqueWords.size / numWords;

  // Complex word ratio (words with 3+ syllables)
  const complexWords = syllables.filter(s => s >= 3).length;
  const complexWordRatio = complexWords / numWords;

  // Grade classification band
  let gradeBand = "Elementary (Grades 3-5)";
  if (fkgl > 12) gradeBand = "Advanced / Undergraduate";
  else if (fkgl >= 9) gradeBand = "High School (Grades 9-12)";
  else if (fkgl >= 6) gradeBand = "Middle School (Grades 6-8)";

  return {
    numWords,
    numSentences,
    avgSentenceLength: Number(asl.toFixed(2)),
    avgSyllablesPerWord: Number(asw.toFixed(2)),
    fleschReadingEase: Number(fre.toFixed(1)),
    fleschKincaidGrade: Number(Math.max(1, fkgl).toFixed(1)),
    estimatedLexile: `${estimatedLexile}L`,
    lexicalDiversity: Number(lexicalDiversity.toFixed(2)),
    complexWordRatio: Number(complexWordRatio.toFixed(2)),
    gradeBand,
    ...mlPrediction(text)
  };
}

// Prediction from the Ridge model trained on the CLEAR corpus (ml/train.py)
function mlPrediction(text) {
  if (!RIDGE_MODEL) return {};
  const p = ml.predictEasiness(text, RIDGE_MODEL);
  return {
    mlEasiness: Number(p.easiness.toFixed(3)),
    mlDifficulty: p.difficulty,
    mlGradeBand: p.band,
    mlReliable: p.reliable,
    mlModel: RIDGE_MODEL.model
  };
}

module.exports = {
  analyzeReadability,
  countSyllables
};
