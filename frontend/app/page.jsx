'use client';
import { useCallback, useEffect, useRef, useState } from 'react';
import Quiz from './components/Quiz';
import CheckPanel from './components/CheckPanel';
import {
  API, CHIP, SUBJECTS, TOOL, TOPICS, bandOf, chooseQuiz, fitFor, markdownToHtml, postJson, predict,
  sampleLesson, toneOk, toneWarn,
} from '../lib/learncraft';

const LEVELS = [['Simpler', 'Simpler'], ['Standard', 'Normal'], ['Challenge', 'Challenge me']];

function Stepper({ step }) {
  const steps = ['Choose a topic', 'Read the lesson', 'Test yourself'];
  return (
    <ol className="flex items-center gap-2 text-sm mb-5 overflow-x-auto" aria-label="Progress">
      {steps.map((label, i) => {
        const n = i + 1;
        const dot = n < step ? 'bg-emerald-500 text-white' : n === step ? 'bg-indigo-600 text-white' : 'bg-slate-200 text-slate-500';
        return (
          <li key={label} className="contents">
            {i > 0 && <span className="hidden sm:block text-slate-300" aria-hidden="true">──</span>}
            <span className={`flex items-center gap-2 whitespace-nowrap ${n <= step ? 'text-slate-900 font-semibold' : 'text-slate-400'}`}
              aria-current={n === step ? 'step' : undefined}>
              <span className={`w-6 h-6 rounded-full grid place-items-center text-xs font-bold ${dot}`}>{n < step ? '✓' : n}</span>
              {label}
            </span>
          </li>
        );
      })}
    </ol>
  );
}

export default function Home() {
  // connection
  const [backend, setBackend] = useState(null);          // null = checking, false = offline, 'gemini' | 'simulator'
  // choices
  const [tab, setTab] = useState('learn');
  const [grade, setGrade] = useState(7);
  const [subject, setSubject] = useState('Science');
  const [topic, setTopic] = useState('Photosynthesis');
  const [level, setLevel] = useState('Standard');
  const [topicError, setTopicError] = useState(false);
  // lesson + quiz
  const [lesson, setLesson] = useState(null);             // { title, meta, html, adaptive, grade }
  const [loading, setLoading] = useState(false);
  const [fit, setFit] = useState(null);
  const [quiz, setQuiz] = useState(null);                 // { key, questions }
  const [step, setStep] = useState(1);
  const [speaking, setSpeaking] = useState(false);

  const req = useRef(0);
  const bodyRef = useRef(null);
  const lessonRef = useRef(null);

  useEffect(() => {
    fetch(`${API}/api/health`, { signal: AbortSignal.timeout(1500) })
      .then((r) => r.json())
      .then((j) => setBackend(j.aiMode === 'gemini' ? 'gemini' : 'simulator'))
      .catch(() => setBackend(false));
  }, []);

  const stopReading = useCallback(() => {
    if (typeof window !== 'undefined' && 'speechSynthesis' in window) window.speechSynthesis.cancel();
    setSpeaking(false);
  }, []);

  const createLesson = useCallback(async (overrides = {}) => {
    const o = { grade, subject, topic, level, scroll: true, ...overrides };
    const t = o.topic.trim();
    if (!t) { setTopicError(true); return; }
    setTopicError(false);
    stopReading();
    const id = ++req.current;                            // ignore answers from older, slower requests
    setLoading(true);
    setQuiz(null);

    let html = null, adaptive = null, source = 'sample';
    if (backend) {
      try {
        const j = await postJson('/api/generate-module', { gradeLevel: o.grade, subject: o.subject, topic: t, readingLevel: o.level });
        if (j.success && j.content) { html = markdownToHtml(j.content); adaptive = j.adaptiveCheck; source = 'ai'; }
      } catch (e) { console.warn('Backend lesson failed, using sample', e); }
    }
    if (id !== req.current) return;
    if (!html) ({ html, source } = sampleLesson(t, o.subject, o.grade, o.level));

    setLesson({
      title: t, html, adaptive, grade: o.grade,
      meta: `${o.subject} · Grade ${o.grade} · ${o.level === 'Standard' ? 'Normal' : o.level} explanation` +
        (source === 'ai' ? ' · AI-written' : source === 'sample' ? ' · Sample lesson' : ''),
    });
    setLoading(false);
    setStep(2);
    if (o.scroll) lessonRef.current?.scrollIntoView({ behavior: 'smooth', block: 'start' });

    let questions = null;
    if (backend) {
      try {
        const j = await postJson('/api/generate-quiz', { gradeLevel: o.grade, topic: t, subject: o.subject });
        const list = j.quiz && j.quiz.questions;
        if (list && list.length) questions = list.slice(0, 3).map((q) => [q.question, q.options, q.correctIndex ?? 0, q.explanation || '']);
      } catch (e) { console.warn('Backend quiz failed, using sample', e); }
    }
    if (id !== req.current) return;
    setQuiz({ key: id, questions: chooseQuiz(t, questions) });
  }, [backend, grade, level, subject, topic, stopReading]);

  // first lesson once we know whether the backend is up
  useEffect(() => { if (backend !== null) createLesson({ scroll: false }); }, [backend]); // eslint-disable-line react-hooks/exhaustive-deps

  // score the rendered lesson with the ML model (same text the student sees)
  useEffect(() => {
    if (!lesson || !bodyRef.current) return;
    const p = predict(bodyRef.current.innerText);
    setFit({ ...p, ...fitFor(p.difficulty, lesson.grade) });
  }, [lesson]);

  function toggleRead() {
    if (!('speechSynthesis' in window)) { alert('Your browser cannot read text aloud.'); return; }
    if (speaking) { stopReading(); return; }
    const u = new SpeechSynthesisUtterance(`${lesson.title}. ${bodyRef.current.innerText}`);
    u.rate = 0.95;
    u.onend = () => setSpeaking(false);
    window.speechSynthesis.speak(u);
    setSpeaking(true);
  }

  const pickTopic = (t) => { setTopic(t.topic); setSubject(t.subject); createLesson({ topic: t.topic, subject: t.subject }); };
  const simplify = () => { setLevel('Simpler'); createLesson({ level: 'Simpler' }); };
  const levelUp = () => { const g = Math.min(12, grade + 1); setGrade(g); setLevel('Standard'); createLesson({ grade: g, level: 'Standard' }); };
  const challenge = () => { setLevel('Challenge'); createLesson({ level: 'Challenge' }); };

  const pill = backend === null
    ? ['Checking connection…', 'bg-slate-100 text-slate-600 border-slate-200']
    : backend === false
      ? ['● Offline demo', 'bg-amber-50 text-amber-800 border-amber-200']
      : backend === 'gemini'
        ? ['● Connected · Gemini AI', 'bg-emerald-50 text-emerald-700 border-emerald-200']
        : ['● Connected · offline AI simulator', 'bg-sky-50 text-sky-700 border-sky-200'];

  return (
    <>
      <header className="bg-white border-b border-slate-200">
        <div className="max-w-6xl mx-auto px-4 py-3 flex items-center justify-between gap-3">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-indigo-600 text-white grid place-items-center text-lg font-bold font-display" aria-hidden="true">L</div>
            <div>
              <h1 className="text-xl font-extrabold text-slate-900 leading-tight">LearnCraft <span className="text-indigo-600">AI</span></h1>
              <p className="text-sm text-slate-500 leading-tight">Learn any topic at your reading level</p>
            </div>
          </div>
          <div className="flex items-center gap-2">
            <span className={`text-xs font-semibold px-3 py-1.5 rounded-full border ${pill[1]}`} role="status">{pill[0]}</span>
            <span className="hidden sm:inline-flex items-center gap-1.5 text-xs font-semibold px-3 py-1.5 rounded-full bg-red-50 text-red-700 border border-red-200"
              title="UN Sustainable Development Goal 4: Quality Education">
              <span className="w-4 h-4 rounded bg-red-600 text-white grid place-items-center text-[10px]">4</span> Quality Education
            </span>
          </div>
        </div>
      </header>

      <main className="max-w-6xl mx-auto px-4 py-5">
        {backend === false && (
          <div className="no-print mb-4 p-3 rounded-xl bg-amber-50 border border-amber-200 text-amber-900 text-sm flex items-start gap-2">
            <span aria-hidden="true">💡</span>
            <div><strong>Offline demo mode.</strong> You&apos;ll see ready-made sample lessons. To get AI-written lessons for any topic, start the
              backend (<code className="bg-amber-100 px-1 rounded">cd backend</code> then <code className="bg-amber-100 px-1 rounded">node server.js</code>)
              and refresh. The reading-level checker works either way.</div>
          </div>
        )}

        <div className="no-print flex gap-1 p-1 bg-slate-200/70 rounded-xl w-full sm:w-fit mb-5" role="tablist">
          {[['learn', '📚 Learn a topic'], ['check', '🔍 Check any text']].map(([id, label]) => (
            <button key={id} role="tab" aria-selected={tab === id} onClick={() => setTab(id)}
              className={`flex-1 sm:flex-none px-5 py-2 rounded-lg text-sm font-semibold ${tab === id ? 'bg-white text-slate-900 shadow-sm' : 'text-slate-600 hover:text-slate-900'}`}>
              {label}
            </button>
          ))}
        </div>

        {tab === 'check' ? <CheckPanel defaultGrade={grade} /> : (
          <section role="tabpanel">
            <div className="no-print"><Stepper step={step} /></div>
            <div className="grid grid-cols-1 lg:grid-cols-12 gap-5">
              <aside className="lg:col-span-4">
                <form className="bg-white border border-slate-200 rounded-2xl p-5 shadow-sm space-y-5 lg:sticky lg:top-4"
                  onSubmit={(e) => { e.preventDefault(); createLesson(); }}>
                  <h2 className="text-lg font-bold text-slate-900">What do you want to learn?</h2>

                  <div>
                    <div className="flex items-baseline justify-between mb-2">
                      <span id="gradeLabel" className="text-sm font-semibold text-slate-700">Your grade</span>
                      <span className="text-xs text-slate-500">{bandOf(grade)} · Grade {grade}</span>
                    </div>
                    <div className="grid grid-cols-5 gap-1.5" role="radiogroup" aria-labelledby="gradeLabel">
                      {Array.from({ length: 10 }, (_, i) => i + 3).map((g) => (
                        <button key={g} type="button" role="radio" aria-checked={g === grade} aria-label={`Grade ${g}`} onClick={() => setGrade(g)}
                          className={`py-2 rounded-lg text-base font-semibold border ${g === grade ? 'bg-indigo-600 border-indigo-600 text-white' : 'bg-white border-slate-300 text-slate-700 hover:border-indigo-400'}`}>
                          {g}
                        </button>
                      ))}
                    </div>
                  </div>

                  <div>
                    <label htmlFor="subject" className="block text-sm font-semibold text-slate-700 mb-1.5">Subject</label>
                    <select id="subject" value={subject} onChange={(e) => setSubject(e.target.value)}
                      className="w-full bg-white border border-slate-300 rounded-xl px-3 py-2.5 text-base focus:border-indigo-500">
                      {SUBJECTS.map((s) => <option key={s}>{s}</option>)}
                    </select>
                  </div>

                  <div>
                    <label htmlFor="topic" className="block text-sm font-semibold text-slate-700 mb-1.5">Topic</label>
                    <input id="topic" type="text" autoComplete="off" placeholder="e.g. The water cycle" value={topic}
                      onChange={(e) => setTopic(e.target.value)} aria-invalid={topicError}
                      className="w-full bg-white border border-slate-300 rounded-xl px-3 py-2.5 text-base focus:border-indigo-500" />
                    {topicError && <p className="text-sm text-red-600 mt-1">Type a topic first, or pick one below.</p>}
                    <div className="flex flex-wrap gap-1.5 mt-2">
                      <span className="text-xs text-slate-500 w-full">Try one:</span>
                      {TOPICS.map((t) => (
                        <button key={t.topic} type="button" className={CHIP} onClick={() => pickTopic(t)}>{t.icon} {t.label}</button>
                      ))}
                    </div>
                  </div>

                  <div>
                    <span id="levelLabel" className="block text-sm font-semibold text-slate-700 mb-1.5">How should it be explained?</span>
                    <div className="grid grid-cols-3 gap-1.5" role="radiogroup" aria-labelledby="levelLabel">
                      {LEVELS.map(([id, label]) => (
                        <button key={id} type="button" role="radio" aria-checked={level === id} onClick={() => setLevel(id)}
                          className={`py-2 rounded-lg text-sm font-semibold border ${level === id ? 'bg-indigo-50 border-indigo-500 text-indigo-700' : 'bg-white border-slate-300 text-slate-700 hover:border-indigo-400'}`}>
                          {label}
                        </button>
                      ))}
                    </div>
                  </div>

                  <button type="submit" disabled={loading}
                    className="w-full bg-indigo-600 hover:bg-indigo-700 disabled:opacity-60 text-white font-bold py-3 rounded-xl text-base shadow-sm">
                    {loading ? 'Writing your lesson…' : 'Create my lesson'}
                  </button>
                </form>
              </aside>

              <div className="lg:col-span-8 space-y-5">
                <article ref={lessonRef} className="bg-white border border-slate-200 rounded-2xl shadow-sm scroll-mt-4" aria-live="polite">
                  <div className="p-5 border-b border-slate-100 flex flex-wrap items-start justify-between gap-3">
                    <div>
                      <p className="text-xs font-semibold uppercase tracking-wide text-indigo-600">{lesson ? lesson.meta : 'Lesson'}</p>
                      <h2 className="text-xl font-bold text-slate-900">{lesson ? lesson.title : 'Pick a topic to begin'}</h2>
                    </div>
                    {lesson && !loading && (
                      <div className="flex gap-2 no-print">
                        <button type="button" onClick={toggleRead} className={TOOL} title="Read the lesson out loud">{speaking ? '⏹️ Stop' : '🔊 Read aloud'}</button>
                        <button type="button" onClick={() => window.print()} className={TOOL} title="Print or save as PDF">🖨️ Print</button>
                      </div>
                    )}
                  </div>

                  {fit && lesson && !loading && (
                    <div className={`mx-5 mt-4 p-3 rounded-xl border text-sm flex items-start gap-2 ${fit.ok ? toneOk : toneWarn}`}>
                      <span aria-hidden="true">{fit.ok ? '✅' : '⚠️'}</span>
                      <div>
                        <strong>Reading level: {fit.msg}.</strong> Our model rates this lesson <strong>{fit.difficulty}</strong> to read.
                        {lesson.adaptive?.regenerated && <> The first draft was rated <strong>{lesson.adaptive.firstPass}</strong>, so we asked the AI to rewrite it more simply.</>}
                        {!fit.reliable && ' (Short text, so this check is only a rough guide.)'}
                        {!fit.ok && <> <button type="button" className="underline font-semibold" onClick={simplify}>Make it simpler</button></>}
                      </div>
                    </div>
                  )}

                  <div className="lesson p-5 text-[17px] leading-relaxed text-slate-700">
                    {loading ? (
                      <div className="space-y-3"><div className="skeleton h-5 w-3/4" /><div className="skeleton h-4 w-full" /><div className="skeleton h-4 w-11/12" /><div className="skeleton h-4 w-2/3" /></div>
                    ) : lesson ? (
                      // lesson HTML is either our own sample content or AI markdown escaped by markdownToHtml
                      <div ref={bodyRef} className="fade-in" dangerouslySetInnerHTML={{ __html: lesson.html }} />
                    ) : (
                      <p className="text-slate-500">Choose your grade and a topic on the left, then press <strong>Create my lesson</strong>.</p>
                    )}
                  </div>
                </article>

                {quiz && (
                  <Quiz key={quiz.key} questions={quiz.questions} grade={grade} onGraded={() => setStep(3)}
                    onSimplify={simplify} onLevelUp={levelUp} onChallenge={challenge} />
                )}
              </div>
            </div>
          </section>
        )}

        <footer className="text-center text-xs text-slate-400 mt-10 mb-4">
          LearnCraft AI · Statistical Machine Learning Lab project · Vishwas, Yagnesh, Kushal
        </footer>
      </main>
    </>
  );
}
