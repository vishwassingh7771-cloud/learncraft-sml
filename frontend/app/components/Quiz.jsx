'use client';
import { useState } from 'react';

const BLOOM = [
  ['Remember', 'bg-sky-100 text-sky-800'],
  ['Understand', 'bg-violet-100 text-violet-800'],
  ['Apply', 'bg-amber-100 text-amber-800'],
];

// questions: [question, options[], correctIndex, explanation][]
export default function Quiz({ questions, grade, onGraded, onSimplify, onLevelUp, onChallenge }) {
  const [answers, setAnswers] = useState({});
  const [graded, setGraded] = useState(false);
  const total = questions.length;
  const answered = Object.keys(answers).length;
  const score = questions.reduce((n, q, i) => n + (answers[i] === q[2] ? 1 : 0), 0);

  const retry = () => { setAnswers({}); setGraded(false); };

  function optionClass(i, j) {
    const base = 'text-left px-3 py-2.5 rounded-lg text-[15px] ';
    if (graded) {
      if (j === questions[i][2]) return base + 'border-2 border-emerald-500 bg-emerald-50 text-emerald-900 font-semibold';
      if (j === answers[i]) return base + 'border-2 border-rose-400 bg-rose-50 text-rose-900';
      return base + 'border border-slate-300 bg-white';
    }
    return base + (answers[i] === j
      ? 'border border-indigo-500 bg-indigo-50 text-indigo-900 font-semibold'
      : 'border border-slate-300 bg-white hover:border-indigo-400');
  }

  let result = null;
  if (graded) {
    const btn = 'px-4 py-2 rounded-lg bg-indigo-600 hover:bg-indigo-700 text-white font-semibold text-sm';
    const btn2 = 'px-4 py-2 rounded-lg border border-slate-300 bg-white hover:bg-slate-50 font-semibold text-sm';
    if (score === total) {
      result = { tone: 'bg-emerald-50 border-emerald-200 text-emerald-900', title: `🎉 ${score}/${total}: you've got it!`,
        text: 'Ready for something a bit harder?',
        actions: grade < 12
          ? <button className={btn} onClick={onLevelUp}>Try Grade {grade + 1}</button>
          : <button className={btn} onClick={onChallenge}>Challenge me</button> };
    } else if (score >= total - 1) {
      result = { tone: 'bg-sky-50 border-sky-200 text-sky-900', title: `👍 ${score}/${total}: nearly there`,
        text: 'Read the explanations above, then have another go.',
        actions: <button className={btn} onClick={retry}>Try again</button> };
    } else {
      result = { tone: 'bg-amber-50 border-amber-200 text-amber-900', title: `${score}/${total}: let's go over it again`,
        text: 'No problem. A simpler explanation often helps.',
        actions: <><button className={btn} onClick={onSimplify}>Explain it more simply</button>
          <button className={btn2} onClick={retry}>Try again</button></> };
    }
  }

  return (
    <section id="quiz" className="bg-white border border-slate-200 rounded-2xl shadow-sm" aria-labelledby="quizTitle">
      <div className="p-5 border-b border-slate-100 flex items-center justify-between gap-3">
        <div>
          <h2 id="quizTitle" className="text-xl font-bold text-slate-900">Test yourself</h2>
          <p className="text-sm text-slate-500">Three questions: remember → understand → apply</p>
        </div>
        <span className="text-sm font-semibold text-slate-600 bg-slate-100 px-3 py-1 rounded-full">{answered} / {total} answered</span>
      </div>

      <div className="p-5 space-y-4">
        {questions.map((q, i) => (
          <fieldset key={i} className="p-4 rounded-xl border border-slate-200">
            <legend className="sr-only">Question {i + 1}</legend>
            {BLOOM[i] && <span className={`text-xs font-bold px-2 py-0.5 rounded-full ${BLOOM[i][1]}`}>{BLOOM[i][0]}</span>}
            <p className="font-semibold text-slate-900 mt-2 mb-3">{i + 1}. {q[0]}</p>
            <div className="grid sm:grid-cols-2 gap-2">
              {q[1].map((o, j) => (
                <button key={j} type="button" className={optionClass(i, j)} aria-pressed={answers[i] === j}
                  onClick={() => !graded && setAnswers((prev) => ({ ...prev, [i]: j }))}>
                  <span className="font-bold text-slate-400 mr-1">{'ABCD'[j]}</span> {o}
                </button>
              ))}
            </div>
            {graded && (
              <p className="mt-3 text-sm p-2.5 rounded-lg bg-slate-50 text-slate-700">
                {answers[i] === q[2] ? '✅ Correct.' : '❌ Not quite.'} {q[3]}
              </p>
            )}
          </fieldset>
        ))}
      </div>

      <div className="px-5 pb-5 space-y-3">
        <button type="button" onClick={() => { setGraded(true); onGraded && onGraded(); }} disabled={graded || answered < total}
          className="w-full bg-emerald-600 hover:bg-emerald-700 disabled:bg-slate-300 disabled:cursor-not-allowed text-white font-bold py-3 rounded-xl text-base">
          {graded ? 'Answers checked' : answered < total ? `Answer all ${total} questions to check` : 'Check my answers'}
        </button>
        {result && (
          <div className={`p-4 rounded-xl border ${result.tone}`} aria-live="polite">
            <p className="font-bold text-lg">{result.title}</p>
            <p className="text-sm mb-3">{result.text}</p>
            <div className="flex flex-wrap gap-2">{result.actions}</div>
          </div>
        )}
      </div>
    </section>
  );
}
