/**
 * LearnCraft AI - readability model for JavaScript (Node + browser).
 *
 * This is a line-by-line port of ml/features.py. The Ridge coefficients come
 * from models/ridge_features.json, which ml/train.py writes after training on
 * the CLEAR corpus. ml/check_js_parity.js checks that this file and the Python
 * code give the same prediction for the same passage.
 */
(function (root) {
  const FEATURE_NAMES = [
    'n_words', 'n_sentences', 'n_paragraphs', 'avg_sentence_len', 'sd_sentence_len',
    'max_sentence_len', 'avg_word_len', 'avg_syllables', 'pct_long_words',
    'pct_complex_words', 'pct_monosyllabic', 'type_token_ratio', 'root_ttr',
    'pct_common_words', 'commas_per_sentence', 'semicolons_colons', 'quote_density',
    'flesch_reading_ease', 'flesch_kincaid_grade'
  ];

  function countSyllables(word) {
    word = word.toLowerCase().trim();
    if (word.length <= 3) return 1;
    word = word.replace(/(?:[^laeiouy]|ed|es|e)$/, '');
    word = word.replace(/^y/, '');
    const m = word.match(/[aeiouy]{1,2}/g);
    return m ? Math.max(1, m.length) : 1;
  }

  const count = (s, ch) => s.split(ch).length - 1;

  function extractFeatures(text, commonWords) {
    text = typeof text === 'string' ? text : '';
    const words = text.match(/[A-Za-z]+/g) || [];
    const nWords = Math.max(1, words.length);

    const sentences = text.split(/[.?!]+/).filter(s => s.trim().length > 0);
    const nSent = Math.max(1, sentences.length);
    let sentLens = sentences.map(s => (s.match(/[A-Za-z]+/g) || []).length);
    if (sentLens.length === 0) sentLens = [0];
    const meanLen = sentLens.reduce((a, b) => a + b, 0) / sentLens.length;
    const sdLen = Math.sqrt(sentLens.reduce((a, x) => a + (x - meanLen) ** 2, 0) / sentLens.length);

    const paragraphs = text.split(/\n\s*\n|\n/).filter(p => p.trim().length > 0);

    let syl = words.map(countSyllables);
    if (syl.length === 0) syl = [1];
    const lower = words.map(w => w.toLowerCase());
    const uniq = new Set(lower).size;
    const asl = nWords / nSent;
    const asw = syl.reduce((a, b) => a + b, 0) / nWords;
    const common = commonWords instanceof Set ? commonWords : new Set(commonWords || []);

    return {
      n_words: nWords,
      n_sentences: nSent,
      n_paragraphs: Math.max(1, paragraphs.length),
      avg_sentence_len: asl,
      sd_sentence_len: sdLen,
      max_sentence_len: Math.max(...sentLens),
      avg_word_len: words.reduce((a, w) => a + w.length, 0) / nWords,
      avg_syllables: asw,
      pct_long_words: words.filter(w => w.length > 6).length / nWords,
      pct_complex_words: syl.filter(s => s >= 3).length / nWords,
      pct_monosyllabic: syl.filter(s => s === 1).length / nWords,
      type_token_ratio: uniq / nWords,
      root_ttr: uniq / Math.sqrt(nWords),
      pct_common_words: lower.filter(w => common.has(w)).length / nWords,
      commas_per_sentence: count(text, ',') / nSent,
      semicolons_colons: (count(text, ';') + count(text, ':')) / nSent,
      quote_density: (count(text, '"') + count(text, '“') + count(text, '”')) / nWords,
      flesch_reading_ease: 206.835 - 1.015 * asl - 84.6 * asw,
      flesch_kincaid_grade: 0.39 * asl + 11.8 * asw - 15.59
    };
  }

  // Rough mapping from BT_easiness to a US grade band. The cut-offs are the
  // CLEAR corpus tertiles stored with the model; the grade labels are only a
  // friendly description for students and teachers.
  function describe(easiness, cuts) {
    if (easiness < cuts[0]) return { difficulty: 'Hard', band: 'High School (Grades 9-12)' };
    if (easiness < cuts[1]) return { difficulty: 'Medium', band: 'Middle School (Grades 6-8)' };
    return { difficulty: 'Easy', band: 'Elementary (Grades 3-5)' };
  }

  function predictEasiness(text, model) {
    const f = extractFeatures(text, model.common_words);
    let y = model.intercept;
    model.features.forEach((name, i) => {
      y += model.coef[i] * ((f[name] - model.mean[i]) / model.scale[i]);
    });
    // CLEAR passages are 140-200 words long. Very short inputs are outside what
    // the model has seen, so we flag them instead of pretending to be sure.
    const reliable = f.n_words >= 80;
    return { easiness: y, features: f, reliable, ...describe(y, model.tertile_cuts) };
  }

  const api = { FEATURE_NAMES, countSyllables, extractFeatures, predictEasiness };
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  else root.LearnCraftML = api;
})(typeof window !== 'undefined' ? window : globalThis);
