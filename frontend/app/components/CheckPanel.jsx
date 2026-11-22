'use client';
import { useMemo, useState } from 'react';
import { CHIP, SAMPLE_TEXT, fitFor, predict, readingTips, toneOk, toneWarn } from '../../lib/learncraft';

export default function CheckPanel({ defaultGrade }) {
  const [text, setText] = useState(SAMPLE_TEXT.easy);
  const [grade, setGrade] = useState(defaultGrade);

  const words = (text.match(/[A-Za-z]+/g) || []).length;
  const p = useMemo(() => (words ? predict(text) : null), [text, words]);
  const fit = p && fitFor(p.difficulty, grade);
  const tips = p && p.difficulty !== 'Easy' ? readingTips(p.features) : [];
  const color = !p ? '' : p.difficulty === 'Easy' ? 'text-emerald-600' : p.difficulty === 'Medium' ? 'text-amber-600' : 'text-rose-600';
  const pos = p ? Math.max(2, Math.min(98, ((p.easiness + 3.7) / 5.4) * 100)) : 50;

  return (
    <div className="grid grid-cols-1 lg:grid-cols-12 gap-5">
      <div className="lg:col-span-7 bg-white border border-slate-200 rounded-2xl p-5 shadow-sm">
        <h2 className="text-lg font-bold text-slate-900">How hard is this text to read?</h2>
        <p className="text-sm text-slate-500 mb-3">Paste a paragraph from a textbook, article or your own writing. Works best with 80+ words.</p>
        <label htmlFor="checkInput" className="sr-only">Text to check</label>
        <textarea id="checkInput" rows={10} value={text} onChange={(e) => setText(e.target.value)} placeholder="Paste your text here…"
          className="w-full border border-slate-300 rounded-xl p-3 text-base leading-relaxed focus:border-indigo-500" />
        <div className="flex flex-wrap items-center justify-between gap-2 mt-2">
          <span className="text-sm text-slate-500">
            {words} word{words === 1 ? '' : 's'}{words > 0 && words < 80 ? ' · add more for a reliable result' : ''}
          </span>
          <div className="flex flex-wrap gap-1.5">
            <span className="text-xs text-slate-500 self-center">Try:</span>
            <button type="button" className={CHIP} onClick={() => setText(SAMPLE_TEXT.easy)}>Easy sample</button>
            <button type="button" className={CHIP} onClick={() => setText(SAMPLE_TEXT.hard)}>Hard sample</button>
            <button type="button" className={CHIP} onClick={() => setText('')}>Clear</button>
          </div>
        </div>
        <div className="flex items-center gap-3 mt-4">
          <label htmlFor="checkGrade" className="text-sm font-semibold text-slate-700">Compare with grade</label>
          <select id="checkGrade" value={grade} onChange={(e) => setGrade(Number(e.target.value))}
            className="border border-slate-300 rounded-lg px-2 py-1.5 text-base">
            {Array.from({ length: 10 }, (_, i) => i + 3).map((g) => <option key={g} value={g}>Grade {g}</option>)}
          </select>
        </div>
      </div>

      <div className="lg:col-span-5 bg-white border border-slate-200 rounded-2xl p-5 shadow-sm" aria-live="polite">
        <h2 className="text-lg font-bold text-slate-900 mb-3">Result</h2>
        {!p ? (
          <p className="text-slate-500 text-sm">Start typing or paste some text. The result updates as you type.</p>
        ) : (
          <div className="space-y-4">
            <div>
              <div className={`text-2xl font-extrabold font-display ${color}`}>{p.difficulty} to read</div>
              <div className="text-sm text-slate-600">Roughly suits: {p.band}{p.reliable ? '' : ' · low confidence (under 80 words)'}</div>
            </div>
            <div>
              <div className="relative h-3 rounded-full bg-gradient-to-r from-rose-400 via-amber-300 to-emerald-400" aria-hidden="true">
                <div className="absolute -top-1.5 w-6 h-6 rounded-full bg-white border-4 border-slate-800 shadow"
                  style={{ left: `${pos}%`, transform: 'translateX(-50%)' }} />
              </div>
              <div className="flex justify-between text-xs text-slate-500 mt-1.5"><span>Hard</span><span>Medium</span><span>Easy</span></div>
            </div>
            <div className={`p-3 rounded-xl border text-sm ${fit.ok ? toneOk : toneWarn}`}>
              {fit.ok ? '✅' : '⚠️'} <strong>{fit.msg}.</strong>
            </div>
            {tips.length > 0 && (
              <div className="text-sm text-slate-700">
                <p className="font-semibold mb-1">To make it easier:</p>
                <ul className="list-disc pl-5 space-y-1">{tips.map((t) => <li key={t}>{t}</li>)}</ul>
              </div>
            )}
            <details className="text-sm">
              <summary className="cursor-pointer font-semibold text-slate-700">Details for teachers</summary>
              <dl className="grid grid-cols-2 gap-x-3 gap-y-1.5 mt-2 text-slate-600">
                <dt>ML easiness score</dt><dd className="text-right font-semibold">{p.easiness.toFixed(2)}</dd>
                <dt>Flesch Reading Ease</dt><dd className="text-right font-semibold">{p.features.flesch_reading_ease.toFixed(1)}</dd>
                <dt>Flesch-Kincaid grade</dt><dd className="text-right font-semibold">{Math.max(0, p.features.flesch_kincaid_grade).toFixed(1)}</dd>
                <dt>Avg. sentence length</dt><dd className="text-right font-semibold">{p.features.avg_sentence_len.toFixed(1)} words</dd>
                <dt>Long words (7+ letters)</dt><dd className="text-right font-semibold">{Math.round(p.features.pct_long_words * 100)}%</dd>
              </dl>
              <p className="text-xs text-slate-500 mt-2">Score from a Ridge regression model trained on 4,723 teacher-rated passages (CommonLit CLEAR corpus). Higher means easier.</p>
            </details>
          </div>
        )}
      </div>
    </div>
  );
}
