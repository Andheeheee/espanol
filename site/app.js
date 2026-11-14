const C = window.COURSE;
const app = document.getElementById('app');
let state = null;
let online = false;
// The public copy (GitHub Pages) has no server: nothing is saved, and anything that writes to the vault is hidden (.vault-only)
const PUBLIC = !!window.PUBLIC_SITE;
if (PUBLIC) document.body.classList.add('public');

// ---------- server sync ----------
async function loadState() {
  try {
    if (PUBLIC) throw new Error('public copy');
    const r = await fetch('/api/state');
    if (!r.ok) throw new Error(r.status);
    state = await r.json();
    online = true;
  } catch {
    online = false;
    state = { weeks: {}, sessions: [], activity: [], current_week: 1, complete: {} };
  }
  document.getElementById('offline').hidden = online || PUBLIC;
  const sync = document.getElementById('sync');
  sync.textContent = online ? 'Saving to Obsidian' : 'Not saving';
  sync.className = 'sync' + (online ? ' ok' : '');
}

async function send(ev, msg) {
  if (PUBLIC) return;
  if (!online) { toast('Not saved — start the server to record progress'); return; }
  try {
    const r = await fetch('/api/event', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(ev) });
    if (!r.ok) throw new Error((await r.json()).error);
    state = await r.json();
    if (msg) toast(msg);
  } catch (e) {
    toast('Save failed: ' + e.message);
  }
}

function toast(text) {
  const t = document.createElement('div');
  t.className = 'toast';
  t.textContent = text;
  document.body.appendChild(t);
  setTimeout(() => t.remove(), 2600);
}

// ---------- audio ----------
const AUDIO = (C.media && C.media.audio) || {};
const IMAGES = (C.media && C.media.images) || {};
const unescape = s => s.replace(/<[^>]+>/g, '').replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&amp;/g, '&');
function playBtn(text) {
  const f = AUDIO[text.trim()];
  return f ? `<button class="play" data-a="media/${f}" title="Listen" aria-label="Listen: ${esc(text)}">🔊</button>` : '';
}
let player = null;
document.addEventListener('click', e => {
  const b = e.target.closest('.play');
  if (!b) return;
  e.preventDefault();
  if (b.dataset.t) return speak(b.dataset.t, b, b.dataset.l);
  window.speechSynthesis?.cancel();
  if (player) player.pause();
  player = new Audio(b.dataset.a);
  document.querySelectorAll('.play.on').forEach(x => x.classList.remove('on'));
  b.classList.add('on');
  player.onended = () => b.classList.remove('on');
  player.play().catch(() => { b.classList.remove('on'); toast('Audio needs the server running'); });
});

// Voice for words without a recorded clip (the Vocabulary Bank): a Latin American browser voice if the device has one
// (phones usually do), else the server makes an es-MX clip in the course voice, else any Spanish browser voice.
const VOICE_ORDER = ['es-MX', 'es-US', 'es-419', 'es-CO', 'es-AR', 'es-CL', 'es-PE', 'es-VE'];
function spanishVoice(latamOnly, spain) {
  const vs = (window.speechSynthesis?.getVoices() || []).filter(v => /^es([-_]|$)/i.test(v.lang));
  if (spain) return vs.find(v => /^es[-_]ES$/i.test(v.lang));
  const rank = v => { const i = VOICE_ORDER.indexOf(v.lang.replace('_', '-')); return i < 0 ? (/ES$/i.test(v.lang) ? 99 : 50) : i; };
  return vs.filter(v => !latamOnly || rank(v) < 99).sort((a, b) => rank(a) - rank(b))[0];
}
window.speechSynthesis?.getVoices();  // some browsers load the voice list lazily
function speak(text, b, lang) {  // lang 'es-ES' = say it like in Spain
  const on = () => { document.querySelectorAll('.play.on').forEach(x => x.classList.remove('on')); b.classList.add('on'); };
  const off = () => b.classList.remove('on');
  const browserVoice = v => {
    const u = new SpeechSynthesisUtterance(text);
    u.voice = v;
    u.lang = v.lang;
    u.rate = 0.9;
    u.onend = u.onerror = off;
    on();
    speechSynthesis.speak(u);
  };
  if (player) player.pause();
  window.speechSynthesis?.cancel();
  const spain = lang === 'es-ES';
  const best = spanishVoice(true, spain);
  if (best) return browserVoice(best);
  const fallback = () => { const v = spanishVoice(false); v ? browserVoice(v) : (off(), toast('No Spanish voice available — start the server for audio')); };
  if (!online) return fallback();
  player = new Audio('/api/say?t=' + encodeURIComponent(text) + (spain ? '&v=es' : ''));
  player.onended = off;
  on();
  player.play().catch(fallback);
}
// 🔊 for any Spanish text: the recorded es-MX clip when there is one, otherwise speak()
const attr = s => esc(s).replace(/"/g, '&quot;');
const sayBtn = (text, lang) => (!lang && playBtn(text)) || `<button class="play" data-t="${attr(text)}"${lang ? ` data-l="${lang}"` : ''} title="Listen${lang === 'es-ES' ? ' (Spain)' : ''}" aria-label="Listen: ${attr(text)}">🔊</button>`;

// ---------- tiny markdown renderer ----------
const esc = s => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
const inline = s => esc(s)
  .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
  .replace(/\*(.+?)\*/g, (_, t) => `<em>${t}</em>${playBtn(unescape(t))}`)
  .replace(/~~(.+?)~~/g, '<s>$1</s>')
  .replace(/`(.+?)`/g, '<code>$1</code>')
  .replace(/\[([^\]]+)\]\((#[^)\s]+)\)/g, '<a href="$2">$1</a>');

function md(src) {
  const lines = src.trim().split('\n');
  let html = '', i = 0;
  while (i < lines.length) {
    const l = lines[i];
    if (l.startsWith('### ')) { html += `<h3>${inline(l.slice(4))}</h3>`; i++; }
    else if (l.startsWith('## ')) { html += `<h2>${inline(l.slice(3))}</h2>`; i++; }
    else if (l.startsWith('|')) {
      const rows = [];
      while (i < lines.length && lines[i].startsWith('|')) rows.push(lines[i++]);
      const cells = r => r.replace(/^\||\|$/g, '').split('|').map(c => c.trim());
      const body = rows.filter((r, k) => !(k === 1 && /^[|\s:-]+$/.test(r)));
      html += '<table><thead><tr>' + cells(body[0]).map(c => `<th>${inline(c)}</th>`).join('') + '</tr></thead><tbody>'
        + body.slice(1).map(r => '<tr>' + cells(r).map(c => `<td>${inline(c)}</td>`).join('') + '</tr>').join('') + '</tbody></table>';
    } else if (/^\s*- /.test(l)) {
      html += '<ul>';
      while (i < lines.length && /^\s*- /.test(lines[i])) html += `<li>${inline(lines[i++].replace(/^\s*- /, ''))}</li>`;
      html += '</ul>';
    } else if (/^\d+\. /.test(l)) {
      html += '<ol>';
      while (i < lines.length && /^\d+\. /.test(lines[i])) html += `<li>${inline(lines[i++].replace(/^\d+\. /, ''))}</li>`;
      html += '</ol>';
    } else if (l.startsWith('> ')) {
      const q = [];
      while (i < lines.length && lines[i].startsWith('> ')) q.push(inline(lines[i++].slice(2)));
      html += `<blockquote>${q.join('<br>')}</blockquote>`;
    } else if (!l.trim()) { i++; }
    else {
      const p = [];
      while (i < lines.length && lines[i].trim() && !/^(#|\||>|\s*- |\d+\. )/.test(lines[i])) p.push(inline(lines[i++]));
      html += `<p>${p.join(' ')}</p>`;
    }
  }
  return html;
}

// ---------- grading ----------
const norm = s => s.toLowerCase().replace(/[¿?¡!.,;:"“”]/g, '').replace(/\s+/g, ' ').trim();
const deaccent = s => s.normalize('NFD').replace(/[̀-ͯ]/g, '');

function grade(given, accepted) {
  const g = norm(given);
  if (!g) return { ok: false, kind: 'bad', msg: `Answer: ${accepted[0]}` };
  if (accepted.some(a => norm(a) === g)) return { ok: true, kind: 'good', msg: '✓ Correct' };
  if (accepted.some(a => deaccent(norm(a)) === deaccent(g)))
    return { ok: false, kind: 'warn', msg: `Almost — check the accents: ${accepted[0]}. In Spanish accents change meaning (hablo ≠ habló).` };
  return { ok: false, kind: 'bad', msg: `Answer: ${accepted[0]}` + (accepted.length > 1 ? `  (also OK: ${accepted.slice(1).join(' · ')})` : '') };
}

const shuffle = a => { a = a.slice(); for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; };

// ---------- views ----------
const wk = n => state.weeks[String(n)] || {};
const byWeek = n => C.weeks.find(w => w.week === n);
const FIRST = C.weeks[0].week, LAST = C.weeks[C.weeks.length - 1].week;
const pct = (s, t) => t ? Math.round(100 * s / t) : 0;

// Palabra del día: same word on every device for the local date; 🔀 picks a random one
function wordOfTheDay(box, i) {
  const D = C.daily || [];
  if (!D.length) return box.remove();
  const today = Math.floor((Date.now() - new Date().getTimezoneOffset() * 60000) / 86400000);
  const n = i ?? today % D.length, d = D[n];
  box.innerHTML = `<div class="muted">🎲 ${i === undefined ? 'Palabra del día' : 'Palabra al azar'} · ${esc(d.topic)}</div>
    <div class="wotd-word">${esc(d.es)} ${playBtn(d.es)}</div>
    <div class="say-syl">${esc(d.say)}</div>
    <div class="wotd-en">${esc(d.en)}</div>
    <p><em>${esc(d.ex)}</em> ${playBtn(d.ex)}<br><span class="muted">${esc(d.ex_en)}</span></p>
    <div class="row"><button class="btn ghost" id="wotd-next">🔀 Another word</button><button class="btn vault-only" id="wotd-add">➕ Add to my Vocab</button></div>`;
  box.querySelector('#wotd-next').onclick = () => {
    let k; do k = Math.floor(Math.random() * D.length); while (D.length > 1 && k === n);
    wordOfTheDay(box, k);
  };
  box.querySelector('#wotd-add').onclick = () => send({ type: 'vocab', es: d.es, en: d.en, topic: d.topic.replace(/^\S+\s/, '') }, `Added “${d.es}” to Vocab`);
}

function home() {
  const cur = state.current_week ?? FIRST;
  const cw = byWeek(cur);
  const done = Object.values(state.complete || {}).filter(Boolean).length;
  const minutes = state.sessions.reduce((a, s) => a + s.minutes, 0);
  let html = `
  <div class="card hero">
    <div>
      <div class="muted">Week ${cur} of ${LAST} · ${C.phases[cw.phase]}</div>
      <h1>${esc(cw.title)}</h1>
      <div class="muted">${esc(cw.goal)}</div>
    </div>
    <a class="btn" href="#/week/${cur}">${Object.keys(wk(cur)).length ? 'Continue' : 'Start'} →</a>
  </div>
  <div class="stats vault-only">
    <div class="card stat"><b>${done}/${C.weeks.length}</b><span>weeks complete</span></div>
    <div class="card stat"><b>${minutes}</b><span>minutes studied</span></div>
    <div class="card stat"><b>${state.sessions.length}</b><span>study sessions</span></div>
  </div>
  <div class="card wotd" id="wotd"></div>`;
  for (const ph of Object.keys(C.phases).map(Number)) {
    html += `<div class="phase-label">Phase ${ph} · ${C.phases[ph]}</div><div class="grid">`;
    for (const w of C.weeks.filter(w => w.phase === ph)) {
      const p = wk(w.week);
      const chip = (on, label) => `<span class="chip ${on ? 'on' : ''}">${label}</span>`;
      const status = state.complete?.[w.week] ? '<span class="chip on">✓ complete</span>'
        : w.week === cur ? '<span class="chip cur">current</span>' : '';
      html += `<a class="card week-card ${w.week === cur ? 'current' : ''}" href="#/week/${w.week}">
        <div class="num">Week ${w.week}</div><div class="t">${esc(w.title)}</div>
        <div class="chips">${status}${chip(p.lesson_done, 'Lesson')}${chip(p.worksheet_attempts, 'Worksheet')}
        ${chip(p.quiz_total && p.quiz_best / p.quiz_total >= .8, p.quiz_attempts ? `Quiz ${pct(p.quiz_best, p.quiz_total)}%` : 'Quiz')}
        ${w.cyber ? chip(p.cyber_attempts, 'Cyber') : ''}${chip(p.practice_done, 'Practice')}</div></a>`;
    }
    html += '</div>';
  }
  html += `
  <h2>Grammar guides</h2>
  <div class="grid">${(C.guides || []).map(g => `<a class="card week-card" href="#/guide/${g.id}">
    <div class="num">${g.weeks.length ? `With week ${g.weeks.join(', ')}` : 'Reference'}</div><div class="t">${g.icon} ${esc(g.title)}</div>
    <div class="muted" style="font-size:.9rem">${esc(g.blurb)}</div></a>`).join('')}</div>
  <a class="card lab-card" href="#/lab/rr"><b>🌀 R Trill Lab</b><span class="muted">Can't roll your r yet? 7 techniques, a practice ladder, slow audio and a 5-minute daily routine.</span></a>
  <a class="card lab-card vault-only" href="#/vocab"><b>📚 Vocabulary Bank</b><span class="muted">5,800+ words in 24 topics from the Quizlet class — searchable, with Spain-only words swapped for the Latin American ones.</span></a>
  <h2 class="vault-only">Log a study session</h2>
  <div class="card vault-only">
    <div class="row">
      <input type="number" id="mins" min="1" max="600" value="30" style="width:90px"> minutes
      <input type="text" id="snote" placeholder="What did you do? (e.g. Anki + Dreaming Spanish)" style="flex:1;min-width:200px">
      <button class="btn" id="logbtn">Log it</button>
    </div>
    <p class="muted" style="margin:10px 0 0;font-size:.9rem">Daily routine: 10 min grammar · 10 min flashcards · 10 min listening · 5–10 min speaking/writing. A week is complete when the lesson, worksheet and practice are done and the quiz is ≥ 80%.</p>
  </div>`;
  if (state.activity.length) html += `<h2>Recent activity</h2><div class="card"><ul style="margin:0;padding-left:20px">${state.activity.slice(-8).reverse().map(a => `<li>${esc(a)}</li>`).join('')}</ul></div>`;
  app.innerHTML = html;
  wordOfTheDay(document.getElementById('wotd'));
  document.getElementById('logbtn').onclick = async () => {
    const minutes = parseInt(document.getElementById('mins').value, 10);
    if (!(minutes > 0)) return toast('Enter minutes');
    await send({ type: 'session', minutes, note: document.getElementById('snote').value }, 'Session logged');
    home();
  };
}

const TABS = [['lesson', 'Lesson'], ['drills', '🎯 Drills'], ['worksheet', 'Worksheet'], ['quiz', 'Quiz'], ['grammar', '✅ Grammar'], ['cyber', '🛡️ Cyber'], ['practice', 'Practice']];
const tabsFor = w => TABS.filter(([k]) => (k !== 'drills' || w.drills) && (k !== 'grammar' || w.grammar.length) && (k !== 'cyber' || w.cyber));
// The tab after `tab` for this week, so "Next →" never points at a tab the week doesn't have.
const tabAfter = (w, tab) => { const t = tabsFor(w).map(([k]) => k); return t[t.indexOf(tab) + 1] || 'practice'; };

function week(n, tab) {
  const w = byWeek(n);
  if (!w) return (location.hash = '#/');
  const p = wk(n);
  const ticks = { grammar: p.grammar_attempts, lesson: p.lesson_done, worksheet: p.worksheet_attempts, quiz: p.quiz_total && p.quiz_best / p.quiz_total >= .8, cyber: p.cyber_attempts, practice: p.practice_done };
  app.innerHTML = `
    <div class="muted"><a href="#/">← All weeks</a> · Phase ${w.phase} · ${C.phases[w.phase]}</div>
    <h1>Week ${n}: ${esc(w.title)}</h1>
    <div class="muted">${esc(w.goal)}</div>
    <nav class="tabs">${tabsFor(w).map(([k, l]) => `<a href="#/week/${n}/${k}" class="${k === tab ? 'active' : ''}">${l}${ticks[k] ? ' <span class="tick">✓</span>' : ''}</a>`).join('')}</nav>
    <section id="pane"></section>
    <div class="row" style="justify-content:space-between;margin-top:32px">
      ${n > FIRST ? `<a href="#/week/${n - 1}">← Week ${n - 1}</a>` : '<span></span>'}
      ${n < LAST ? `<a href="#/week/${n + 1}">Week ${n + 1} →</a>` : ''}
    </div>`;
  const pane = document.getElementById('pane');
  if (!tabsFor(w).some(([k]) => k === tab)) tab = 'lesson';
  ({ lesson: lessonPane, drills: drillsPane, grammar: grammarPane, worksheet: worksheetPane, quiz: quizPane, cyber: cyberPane, practice: practicePane })[tab](pane, w, p);
}

function photoGallery(w) {
  const cards = w.photos.map((ph, i) => {
    const img = IMAGES[`${w.id}-${i + 1}`];
    if (!img) return '';
    return `<figure class="photo card">
      <img src="media/${img.file}" alt="${esc(ph.en)}" loading="lazy">
      <figcaption><div class="es">${esc(ph.es)} ${playBtn(ph.es)}</div><div class="en">${esc(ph.en)}</div>
      <a class="credit" href="${img.source}" target="_blank" rel="noopener">${esc(img.artist)} · ${esc(img.license)}</a></figcaption>
    </figure>`;
  }).join('');
  return cards ? `<h2 style="margin-top:0">📷 Picture vocabulary</h2><div class="photos">${cards}</div>` : '';
}

function sayFirst(w) {
  if (!w.say_first.length) return '';
  const hide = (() => { try { return localStorage.getItem('hide-syll') === '1'; } catch { return false; } })();
  return `<div class="card say-first ${hide ? 'hide-syll' : ''}">
    <div class="row" style="justify-content:space-between">
      <h2 style="margin:0">🔤 Say it first</h2>
      <label class="muted" style="font-size:.9rem"><input type="checkbox" id="syll-toggle" ${hide ? '' : 'checked'}> Show syllables</label>
    </div>
    <p class="muted" style="margin:6px 0 12px">Read each word out loud <b>before</b> pressing 🔊. Syllables are split with · and the <b>STRESSED</b> one is in capitals. Then check yourself.</p>
    <div class="say-grid">${w.say_first.map(x => `<div class="say-item"><div class="say-es">${esc(x.es)} ${playBtn(x.es)}</div><div class="say-syl">${esc(x.say)}</div></div>`).join('')}</div>
  </div>`;
}

// Grammar guides that go with this week, shown above the lesson
function guideLinks(w) {
  const gs = (C.guides || []).filter(g => g.weeks.includes(w.week));
  return gs.length ? `<div class="guide-links muted">📚 Extra grammar for this week: ${gs.map(g => `<a href="#/guide/${g.id}">${g.icon} ${esc(g.title)}</a>`).join(' · ')}</div>` : '';
}

function lessonPane(pane, w, p) {
  pane.innerHTML = `${guideLinks(w)}${w.week === 0 ? '<a class="card lab-card" href="#/lab/rr" style="margin-bottom:16px"><b>🌀 R Trill Lab</b><span class="muted">Can\'t roll your r yet? Practice it here — 7 techniques, slow audio, record yourself.</span></a>' : ''}${sayFirst(w)}${photoGallery(w)}<p class="muted" style="font-size:.9rem">Tap 🔊 next to any Spanish phrase to hear it (Mexican Spanish voice).</p><div class="prose">${md(w.lesson)}</div>
    <div class="row" style="margin-top:24px">
      <button class="btn" id="read" ${p.lesson_done ? 'disabled' : ''}>${p.lesson_done ? '✓ Lesson read' : 'Mark lesson as read'}</button>
      <a class="btn ghost" href="#/week/${w.week}/worksheet">Go to worksheet →</a>
    </div>`;
  const tog = document.getElementById('syll-toggle');
  if (tog) tog.onchange = () => {
    pane.querySelector('.say-first').classList.toggle('hide-syll', !tog.checked);
    try { localStorage.setItem('hide-syll', tog.checked ? '0' : '1'); } catch {}
  };
  document.getElementById('read').onclick = async () => { await send({ type: 'lesson', week: w.week }, 'Lesson marked as read'); route(); };
}

// Typed-answer exercise used by both the worksheet and the cyber drill.
function typedExercise(pane, w, items, kind, intro, nextTab) {
  pane.innerHTML = `<p class="muted">${intro}</p>
    <div class="card">${items.map((it, i) => `
      <div class="item">
        <div class="q"><span class="n">${i + 1}.</span>${it.listen ? playBtn(it.listen) + ' ' : ''}${inline(it.q)}${it.h ? ` <span class="hint">(${esc(it.h)})</span>` : ''}</div>
        <input type="text" data-i="${i}" autocomplete="off" autocapitalize="off" spellcheck="false">
        <div class="fb" hidden></div>
      </div>`).join('')}</div>
    <div class="result" id="result"></div>
    <div class="row"><button class="btn" id="check">Check answers</button><button class="btn ghost" id="retry" hidden>Try again</button>
    <a class="btn ghost" id="next" href="#/week/${w.week}/${nextTab || tabAfter(w, kind)}" hidden>Next →</a></div>`;
  const inputs = [...pane.querySelectorAll('input')];
  inputs.forEach((inp, i) => inp.addEventListener('keydown', e => {
    if (e.key === 'Enter') (inputs[i + 1] || document.getElementById('check')).focus();
  }));
  document.getElementById('check').onclick = async () => {
    let score = 0;
    const missed = [];
    inputs.forEach((inp, i) => {
      const r = grade(inp.value, items[i].a);
      const fb = inp.nextElementSibling;
      fb.hidden = false; fb.className = 'fb ' + r.kind; fb.innerHTML = esc(r.msg) + ' ' + playBtn(items[i].a[0]);
      inp.disabled = true;
      if (r.ok) score++; else missed.push({ q: items[i].listen ? `Dictation: ${items[i].listen}` : items[i].q, given: inp.value.trim(), correct: items[i].a[0] });
    });
    document.getElementById('result').innerHTML = `<b>${score}/${items.length}</b> (${pct(score, items.length)}%)`;
    document.getElementById('check').hidden = true;
    document.getElementById('retry').hidden = false;
    document.getElementById('next').hidden = false;
    await send({ type: kind, week: w.week, score, total: items.length, missed }, 'Score saved to Obsidian');
  };
  document.getElementById('retry').onclick = () => route();
}

function worksheetPane(pane, w, p) {
  const best = p.worksheet_attempts ? ` Best so far: ${p.worksheet_best}/${p.worksheet_total}.` : '';
  typedExercise(pane, w, w.worksheet, 'worksheet', `Type each answer. Press Enter to jump to the next one. Use the accent bar at the bottom for á é í ó ú ñ.${best}`);
}

function cyberPane(pane, w, p) {
  const c = w.cyber;
  const best = p.cyber_attempts ? ` Best so far: ${p.cyber_best}/${p.cyber_total}.` : '';
  pane.innerHTML = `<div class="prose">
      <p>${inline(c.focus)}</p>
      <h2>Vocabulary</h2>
      <table><thead><tr><th>Español</th><th>English</th></tr></thead><tbody>
      ${c.terms.map(([es, en], i) => `<tr><td><strong>${esc(es)}</strong> ${playBtn(es)}<div class="say-syl">${esc(c.say[i])}</div></td><td>${esc(en)}</td></tr>`).join('')}</tbody></table>
      <h2>Using this week's grammar</h2>
      <ul>${c.examples.map(([es, en]) => `<li><em>${esc(es)}</em> ${playBtn(es)} — ${esc(en)}</li>`).join('')}</ul>
      <h2>Drill</h2></div><div id="drill"></div>`;
  typedExercise(document.getElementById('drill'), w, c.drill, 'cyber', `Translate into Spanish.${best}`);
}

function quizPane(pane, w, p) {
  const best = p.quiz_attempts ? ` Best so far: ${p.quiz_best}/${p.quiz_total}.` : '';
  const qs = w.quiz.map(q => ({ ...q, order: shuffle(q.o.map((_, i) => i)) }));
  pane.innerHTML = `<p class="muted">Pick one answer for each question. You need 80% to pass this week.${best}</p>
    <div class="card">${qs.map((q, i) => `
      <div class="item">
        <div class="q"><span class="n">${i + 1}.</span>${inline(q.q)}</div>
        <div class="opts">${q.order.map(oi => `<label><input type="radio" name="q${i}" value="${oi}"> ${inline(q.o[oi])}</label>`).join('')}</div>
        <div class="fb" hidden></div>
      </div>`).join('')}</div>
    <div class="result" id="result"></div>
    <div class="row"><button class="btn" id="submit">Submit quiz</button><button class="btn ghost" id="retry" hidden>Retake</button>
    <a class="btn ghost" id="next" href="#/week/${w.week}/${tabAfter(w, 'quiz')}" hidden>Next →</a></div>`;
  document.getElementById('submit').onclick = async () => {
    let score = 0;
    const missed = [];
    qs.forEach((q, i) => {
      const item = pane.querySelectorAll('.item')[i];
      const picked = item.querySelector('input:checked');
      const val = picked ? +picked.value : -1;
      item.querySelectorAll('label').forEach(l => {
        const v = +l.querySelector('input').value;
        if (v === q.a) l.classList.add('right'); else if (v === val) l.classList.add('wrong');
        l.querySelector('input').disabled = true;
      });
      const fb = item.querySelector('.fb');
      fb.hidden = false;
      if (val === q.a) { score++; fb.className = 'fb good'; fb.textContent = '✓ ' + q.x; }
      else { fb.className = 'fb bad'; fb.textContent = q.x; missed.push({ q: q.q, given: val >= 0 ? q.o[val] : '', correct: q.o[q.a] }); }
    });
    const passed = score / qs.length >= .8;
    document.getElementById('result').innerHTML = `<b>${score}/${qs.length}</b> (${pct(score, qs.length)}%) — ${passed ? '🎉 Passed!' : 'Need 80% to pass. Review the explanations and retake.'}`;
    document.getElementById('submit').hidden = true;
    document.getElementById('retry').hidden = false;
    document.getElementById('next').hidden = false;
    await send({ type: 'quiz', week: w.week, score, total: qs.length, missed }, 'Quiz saved to Obsidian');
  };
  document.getElementById('retry').onclick = () => route();
}

// Shadowing: hear the model, record yourself, compare. Recordings stay in the browser.
let micStream = null;
function speakSection(w) {
  const phrases = (w.speak || [...(w.cyber ? w.cyber.examples.map(e => e[0]) : []), ...w.photos.map(p => p.es)]).filter(t => AUDIO[t]);
  if (!phrases.length) return '';
  return `<h2>🗣️ Say it out loud</h2>
    <p class="muted">Play 🔊, then press 🎙 and say it yourself. Press ■ to stop, then ▶ to hear yourself next to the model. Recordings aren't saved anywhere.</p>
    <div class="card">${phrases.map((t, i) => `
      <div class="speak-row"><span class="speak-text">${esc(t)}</span>
        <span class="row">${playBtn(t)}<button class="rec" data-i="${i}" title="Record">🎙</button><button class="mine" data-i="${i}" title="Play my recording" disabled>▶ Me</button></span>
      </div>`).join('')}</div>`;
}

function wireRecorder(pane) {
  const takes = {};
  let rec = null;
  pane.querySelectorAll('.rec').forEach(btn => btn.onclick = async () => {
    if (rec && rec.state === 'recording') { rec.stop(); return; }
    try {
      micStream = micStream || await navigator.mediaDevices.getUserMedia({ audio: true });
    } catch { return toast('Microphone blocked — allow it in the browser to record'); }
    const chunks = [];
    rec = new MediaRecorder(micStream);
    rec.ondataavailable = e => chunks.push(e.data);
    rec.onstop = () => {
      takes[btn.dataset.i] = URL.createObjectURL(new Blob(chunks, { type: rec.mimeType }));
      btn.textContent = '🎙'; btn.classList.remove('on');
      const mine = pane.querySelector(`.mine[data-i="${btn.dataset.i}"]`);
      mine.disabled = false;
      mine.onclick = () => new Audio(takes[btn.dataset.i]).play();
    };
    rec.start();
    btn.textContent = '■'; btn.classList.add('on');
  });
}

function practicePane(pane, w, p) {
  let draft = '';
  try { draft = localStorage.getItem('draft-' + w.week) || ''; } catch {}
  pane.innerHTML = `<div class="card prose"><h3 style="margin-top:0">Task</h3><p>${inline(w.practice)}</p></div>
    ${speakSection(w)}
    <h2>Your writing</h2>
    <p class="muted vault-only">Saved into your Obsidian vault under <code>Practice/</code> so a Claude session can review it and correct mistakes.${p.practice_entries ? ` You've saved ${p.practice_entries} entr${p.practice_entries === 1 ? 'y' : 'ies'} for this week.` : ''}</p>
    <textarea id="txt" placeholder="Escribe aquí…">${esc(draft)}</textarea>
    <div class="row vault-only" style="margin-top:12px">
      <button class="btn" id="save">Save to Obsidian</button>
      <button class="btn ghost" id="done" ${p.practice_done ? 'disabled' : ''}>${p.practice_done ? '✓ Practice done' : 'Mark done (spoken/offline practice)'}</button>
    </div>`;
  wireRecorder(pane);
  const txt = document.getElementById('txt');
  txt.oninput = () => { try { localStorage.setItem('draft-' + w.week, txt.value); } catch {} };
  document.getElementById('save').onclick = async () => {
    if (!txt.value.trim()) return toast('Write something first');
    await send({ type: 'practice', week: w.week, text: txt.value }, 'Saved to Obsidian');
    try { localStorage.removeItem('draft-' + w.week); } catch {}
    route();
  };
  document.getElementById('done').onclick = async () => { await send({ type: 'practice', week: w.week, text: '' }, 'Practice marked done'); route(); };
}

// ---------- accent bar ----------
let lastField = null;
document.addEventListener('focusin', e => {
  if (e.target.matches('input[type=text], textarea')) { lastField = e.target; document.getElementById('accents').hidden = false; }
});
document.querySelectorAll('#accents button').forEach(b => {
  b.addEventListener('mousedown', e => e.preventDefault());
  b.onclick = () => {
    if (!lastField || lastField.disabled) return;
    const { selectionStart: s, selectionEnd: en, value } = lastField;
    lastField.value = value.slice(0, s) + b.textContent + value.slice(en);
    lastField.selectionStart = lastField.selectionEnd = s + 1;
    lastField.dispatchEvent(new Event('input'));
    lastField.focus();
  };
});

// ---------- Week 0 drills ----------
// Play several clips back to back (used for spelling). onStep(i) fires as clip i starts, onStep(-1) at the end.
function playSeq(texts, onStep) {
  if (player) player.pause();
  let i = 0;
  const go = () => {
    if (i >= texts.length) { if (onStep) onStep(-1); return; }
    const f = AUDIO[texts[i]];
    if (onStep) onStep(i);
    i++;
    if (!f) return go();
    player = new Audio('media/' + f);
    player.onended = go;
    player.play().catch(() => toast('Audio needs the server running'));
  };
  go();
}

function spellTokens(text, D, caps = true) {
  return [...text].map(ch => {
    const lower = ch.toLowerCase();
    let say = [];
    if (lower === 'ñ') say = ['eñe'];
    else {
      const [base, ...marks] = lower.normalize('NFD');
      if (D.spell[base] !== undefined) {
        say = [D.spell[base]];
        if (marks.includes('́')) say.push('con tilde');
        if (marks.includes('̈')) say.push('con diéresis');
      }
    }
    if (say.length && caps && ch !== lower) say.push('mayúscula');
    return { ch, say };
  });
}

const pick = a => a[Math.floor(Math.random() * a.length)];

function drillModes(D) {
  const letters = D.alphabet.filter(l => l.letter.length === 1);
  const plain = w => w.replace(/[\[\]]/g, '');
  return {
    vowel: { name: 'Which vowel?', make() {
      const s = pick(D.vowels);
      return { prompt: 'Listen — which vowel do you hear?', audio: [s], options: ['a', 'e', 'i', 'o', 'u'], answer: 'aeiou'.indexOf(s.slice(-1)), reveal: s };
    } },
    letter: { name: 'Which letter?', make() {
      const L = pick(letters);
      const opts = shuffle([L, ...shuffle(letters.filter(x => x !== L)).slice(0, 3)]);
      return { prompt: 'Listen — which letter is this?', audio: [L.name], options: opts.map(x => x.letter), answer: opts.indexOf(L), reveal: `${L.letter} = ${L.name}` };
    } },
    trill: { name: 'Tap or trill?', make() {
      const pair = pick(D.pairs), w = pick(pair);
      return { prompt: 'Listen — one tap (r) or rolled (rr)?', audio: [w], options: pair, answer: pair.indexOf(w), reveal: w };
    } },
    stress: { name: "Where's the stress?", make() {
      const x = pick(D.stress);
      return { prompt: `Which syllable is stressed in <span class="big">${esc(x.w)}</span>?`, options: x.syl, answer: x.k, after: [x.w],
               reveal: x.syl.map((s, i) => i === x.k ? s.toUpperCase() : s).join('·') };
    } },
    rules: { name: 'Rule detective', make() {
      const r = pick(D.rules);
      const order = shuffle(r.o.map((_, i) => i));
      return { prompt: `How does the highlighted part sound? <span class="big">${esc(r.w).replace(/\[(.+?)\]/, '<mark>$1</mark>')}</span>`,
               options: order.map(i => r.o[i]), answer: order.indexOf(0), after: [plain(r.w)], reveal: `${plain(r.w)}: ${r.o[0]}` };
    } },
    spelled: { name: 'Spelled dictation', make() {
      const w = pick(D.dictation);
      return { prompt: 'Listen to the letters being spelled, then type the word', audio: spellTokens(w, D, false).flatMap(t => t.say), typed: true, accept: [w], after: [w], reveal: w };
    } },
  };
}

function drillsPane(pane, w) {
  const D = w.drills;
  const modes = drillModes(D);
  pane.innerHTML = `
    <h2 style="margin-top:0">🔤 Alphabet explorer</h2>
    <p class="muted">Tap a letter to hear its name, how it sounds and example words.</p>
    <div class="letters">${D.alphabet.map((l, i) => `<button class="letter" data-i="${i}">${l.letter}</button>`).join('')}</div>
    <div id="letter-detail" class="card" hidden></div>

    <h2>🗣️ Spell it out — usernames, emails, passwords</h2>
    <p class="muted">Type anything and hear it spelled the way you'd read it to a student or IT help desk. B is said <em>be larga</em> and V <em>ve corta</em> so they can't be confused.</p>
    <div class="card">
      <div class="row"><input type="text" id="spell-in" placeholder="e.g. profe_ruiz23@colegio.edu" style="flex:1;min-width:220px" autocomplete="off" spellcheck="false">
      <button class="btn" id="spell-go">🔊 Spell it</button></div>
      <label class="muted" style="font-size:.9rem;display:block;margin-top:8px"><input type="checkbox" id="spell-caps" checked> Say <em>mayúscula</em> for capital letters</label>
      <div id="spell-out" class="spell-out"></div>
    </div>

    <h2>⚡ Quick-fire drills</h2>
    <p class="muted">10 questions per round.<span class="vault-only"> Scores go to your Obsidian Quiz Log, and missed items show up as weak spots.</span></p>
    <div class="row drill-modes">${Object.entries(modes).map(([k, m]) => `<button class="btn ghost" data-mode="${k}">${m.name}</button>`).join('')}</div>
    <div id="drill" class="card" hidden></div>`;

  // alphabet explorer
  const detail = document.getElementById('letter-detail');
  pane.querySelectorAll('.letter').forEach(b => b.onclick = () => {
    const l = D.alphabet[+b.dataset.i];
    pane.querySelectorAll('.letter.on').forEach(x => x.classList.remove('on'));
    b.classList.add('on');
    detail.hidden = false;
    detail.innerHTML = `<div class="row" style="gap:18px;align-items:flex-start">
      <div class="big-letter">${l.letter}</div>
      <div style="flex:1;min-width:220px">
        <div class="say-es" style="font-size:1.2rem">${esc(l.name)} ${playBtn(l.name)}</div>
        <p style="margin:6px 0">${inline(l.sound)}</p>
        ${l.examples.map((e, i) => `<div class="say-item" style="margin:6px 0"><span class="say-es">${esc(e)} ${playBtn(e)}</span> <span class="say-syl">${esc(l.say[i])}</span></div>`).join('')}
        ${l.tip ? `<p class="muted" style="margin:8px 0 0">💡 ${inline(l.tip)}</p>` : ''}
      </div></div>`;
    playSeq([l.name]);
  });

  // speller
  const out = document.getElementById('spell-out');
  const spell = () => {
    const toks = spellTokens(document.getElementById('spell-in').value, D, document.getElementById('spell-caps').checked);
    if (!toks.length) return toast('Type something to spell');
    out.innerHTML = toks.map((t, i) => `<span class="chip spell-chip" data-t="${i}"><b>${esc(t.ch === ' ' ? '␣' : t.ch)}</b> ${esc(t.say.join(' ') || '?')}</span>`).join('');
    const seq = [], owner = [];
    toks.forEach((t, i) => t.say.forEach(x => { seq.push(x); owner.push(i); }));
    playSeq(seq, k => {
      out.querySelectorAll('.spell-chip.on').forEach(c => c.classList.remove('on'));
      if (k >= 0) out.querySelector(`[data-t="${owner[k]}"]`).classList.add('on');
    });
  };
  document.getElementById('spell-go').onclick = spell;
  document.getElementById('spell-in').addEventListener('keydown', e => { if (e.key === 'Enter') spell(); });

  // quick-fire rounds
  const box = document.getElementById('drill');
  pane.querySelectorAll('[data-mode]').forEach(b => b.onclick = () => {
    const key = b.dataset.mode, mode = modes[key];
    pane.querySelectorAll('[data-mode]').forEach(x => x.classList.toggle('active', x.dataset.mode === key));
    runRound(box, mode.name, () => mode.make(), (score, missed) =>
      send({ type: 'drill', week: w.week, label: mode.name, score, total: 10, missed }, 'Drill saved to Obsidian'));
  });
}

// One round of 10 questions. make() returns a question:
//   prompt (html), audio [texts to auto-play], clips [texts to pick between], options + answer (index),
//   or typed + accept [answers]; after [text to play when answered], reveal (text), detail (html).
function runRound(box, name, make, onFinish, total = 10) {
  const round = { i: 0, score: 0, missed: [] };
  box.hidden = false;
  const ask = () => {
    if (round.i === total) return finish();
    const q = make(round.i);
    box.innerHTML = `<div class="muted">${esc(name)} · ${round.i + 1} / ${total} · score ${round.score}</div>
      <div class="drill-q">${q.prompt}</div>
      ${q.audio ? `<button class="btn ghost" id="replay">🔊 Play again</button>` : ''}
      ${q.clips ? `<div class="row clips">${q.clips.map((_, i) => `<button class="btn ghost clip" data-c="${i}">▶ Clip ${'ABC'[i]}</button>`).join('')}</div>` : ''}
      ${q.typed ? `<div class="row" style="margin-top:12px"><input type="text" id="typed" autocomplete="off" spellcheck="false" style="flex:1;min-width:180px"><button class="btn" id="check1">Check</button></div>`
                : `<div class="row opts-row" style="margin-top:12px">${q.options.map((o, i) => `<button class="opt" data-o="${i}">${esc(o)}</button>`).join('')}</div>`}
      <div id="fb1" class="fb" hidden></div>
      <button class="btn" id="next1" hidden style="margin-top:12px">${round.i === total - 1 ? 'See results' : 'Next →'}</button>`;
    if (q.audio) { playSeq(q.audio); document.getElementById('replay').onclick = () => playSeq(q.audio); }
    box.querySelectorAll('.clip').forEach(c => c.onclick = () => playSeq([q.clips[+c.dataset.c]]));
    const done = (ok, given, correct, msg) => {
      round.i++;
      if (ok) round.score++; else round.missed.push({ q: `${name} — ${q.reveal}`, given, correct });
      const fb = document.getElementById('fb1');
      fb.hidden = false; fb.className = 'fb ' + (ok ? 'good' : 'bad');
      fb.innerHTML = (msg || ((ok ? '✓ Correct — ' : '✗ Not quite. The correct answer is: ') + esc(q.reveal))) + ' ' + (q.after ? playBtn(q.after[0]) : '') + (q.detail || '');
      if (q.after) playSeq(q.after);
      const nx = document.getElementById('next1');
      nx.hidden = false; nx.focus(); nx.onclick = ask;
    };
    if (q.typed) {
      const inp = document.getElementById('typed');
      inp.focus();
      const check = () => {
        if (!inp.value.trim()) return;
        inp.disabled = true; document.getElementById('check1').disabled = true;
        const r = grade(inp.value, q.accept);
        done(r.ok, inp.value.trim(), q.accept[0], (r.ok ? '✓ Correct — ' + esc(q.accept[0]) : esc(r.msg)));
      };
      document.getElementById('check1').onclick = check;
      inp.addEventListener('keydown', e => { if (e.key === 'Enter') check(); });
    } else {
      box.querySelectorAll('.opt').forEach(o => o.onclick = () => {
        const i = +o.dataset.o;
        box.querySelectorAll('.opt').forEach(x => { x.disabled = true; if (+x.dataset.o === q.answer) x.classList.add('right'); });
        if (i !== q.answer) o.classList.add('wrong');
        done(i === q.answer, q.options[i], q.options[q.answer]);
      });
    }
  };
  const finish = () => {
    box.innerHTML = `<p class="result"><b>${round.score}/${total}</b> — ${esc(name)} ${round.score >= 0.8 * total ? '🎉' : ''}</p>
      ${round.missed.length ? `<p class="muted">Missed:</p><ul>${round.missed.map(m => `<li>${esc(m.q)}</li>`).join('')}</ul>` : ''}
      <button class="btn" id="again">Play again</button>`;
    document.getElementById('again').onclick = () => runRound(box, name, make, onFinish, total);
    onFinish(round.score, round.missed);
  };
  ask();
}

// ---------- Grammar check ----------
const FORMATS = { mixed: 'Mixed', mc: 'Multiple choice', fix: 'Type the fix', audio: 'Listen & choose' };

function grammarQuestion(g, fmt) {
  const meaning = `<div class="meaning">Meaning: “${esc(g.en)}”</div>`;
  const why = `<div class="why">${esc(g.x)}</div>`;
  if (fmt === 'fix') {
    return { prompt: `This has a mistake — type it correctly:<span class="big">${esc(g.bad[0])}</span>${meaning}`,
             typed: true, accept: [g.ok, ...g.alt], after: [g.ok], reveal: g.ok, detail: why };
  }
  const opts = shuffle([g.ok, ...g.bad]);
  if (fmt === 'audio') {
    const letters = opts.map((_, i) => 'ABC'[i]);
    return { prompt: `Listen to each clip. Which one is grammatically correct?${meaning}`, clips: opts, options: letters,
             answer: opts.indexOf(g.ok), after: [g.ok], reveal: g.ok,
             detail: why + `<ul class="clip-list">${opts.map((t, i) => `<li>${t === g.ok ? '✅' : '❌'} <b>${letters[i]}:</b> ${esc(t)}</li>`).join('')}</ul>` };
  }
  return { prompt: `Which is grammatically correct?${meaning}`, options: opts, answer: opts.indexOf(g.ok), after: [g.ok], reveal: g.ok, detail: why };
}

function grammarPane(pane, w, p) {
  const best = p.grammar_attempts ? ` Best so far: ${p.grammar_best}/${p.grammar_total}.` : '';
  pane.innerHTML = `<p class="muted">Is it grammatically correct? 10 questions per round in three formats.${best}</p>
    <div class="card">
      <div class="muted" style="font-size:.85rem;margin-bottom:6px">Format</div>
      <div class="row drill-modes">${Object.entries(FORMATS).map(([k, n]) => `<button class="btn ghost" data-fmt="${k}">${n}</button>`).join('')}</div>
      <div class="muted" style="font-size:.85rem;margin:10px 0 6px">Questions from</div>
      <div class="row"><label><input type="radio" name="scope" value="week" checked> This week only</label>
      ${w.week > 1 ? `<label><input type="radio" name="scope" value="review"> Review weeks 1–${w.week}</label>` : ''}</div>
    </div>
    <div id="gbox" class="card" hidden style="margin-top:12px"></div>`;
  const box = document.getElementById('gbox');
  pane.querySelectorAll('[data-fmt]').forEach(b => b.onclick = () => {
    const fmt = b.dataset.fmt;
    pane.querySelectorAll('[data-fmt]').forEach(x => x.classList.toggle('active', x === b));
    const review = pane.querySelector('input[name=scope]:checked').value === 'review';
    const pool = shuffle(review ? C.weeks.filter(x => x.week >= 1 && x.week <= w.week).flatMap(x => x.grammar) : w.grammar);
    const label = `${FORMATS[fmt]}${review ? ' (review)' : ''}`;
    runRound(box, `Grammar — ${label}`, i => grammarQuestion(pool[i % pool.length], fmt === 'mixed' ? pick(['mc', 'fix', 'audio']) : fmt),
      (score, missed) => send({ type: 'grammar', week: w.week, label, score, total: 10, missed }, 'Grammar score saved to Obsidian'));
  });
}

// ---------- R Trill Lab ----------
function slowBtn(text) {
  const f = AUDIO['slow:' + text];
  return f ? `<button class="play" data-a="media/${f}" title="Slow" aria-label="Slow: ${esc(text)}">🐢</button>` : '';
}

function rrLab() {
  const L = C.rr_lab;
  let n = 0;
  const row = t => `<div class="speak-row"><span><span class="speak-text">${esc(t)}</span>${L.say[t] && L.say[t] !== t ? `<div class="say-syl">${esc(L.say[t])}</div>` : ''}</span>
    <span class="row">${playBtn(t)}${slowBtn(t)}<button class="rec" data-i="${n}" title="Record">🎙</button><button class="mine" data-i="${n++}" title="Play my recording" disabled>▶ Me</button></span></div>`;
  app.innerHTML = `
    <div class="muted"><a href="#/">← Home</a> · <a href="#/week/0/lesson">Week 0</a></div>
    <h1>🌀 R Trill Lab</h1>
    <p class="prose">${inline(L.intro)}</p>
    <div class="card"><h2 style="margin-top:0">Your daily 5 minutes</h2><ol class="prose">${L.routine.map(r => `<li>${inline(r)}</li>`).join('')}</ol>
      <div class="row vault-only"><select id="tech">${L.techniques.map(t => `<option>${esc(t.name)}</option>`).join('')}<option>Mixed / full routine</option></select>
      <input type="number" id="rr-min" value="5" min="1" max="60" style="width:70px"> min
      <button class="btn" id="rr-log">Log today's practice</button></div>
      <p class="muted" style="margin:8px 0 0;font-size:.85rem">🔊 normal speed · 🐢 slow · 🎙 record yourself · ▶ hear yourself.<span class="vault-only"> Logged practice goes to your Obsidian Study Log.</span></p></div>
    <h2>Techniques — try them all</h2>
    ${L.techniques.map(t => `<div class="card tech"><h3 style="margin-top:0">${esc(t.name)}</h3>
      <p class="muted">${inline(t.why)}</p><ol class="prose">${t.steps.map(x => `<li>${inline(x)}</li>`).join('')}</ol>
      ${t.say.map(row).join('')}</div>`).join('')}
    <h2>Practice ladder</h2><p class="muted">Move up a stage when the current one feels easy.</p>
    ${L.ladder.map(st => `<div class="card tech"><h3 style="margin-top:0">${esc(st.stage)}</h3>${st.words.map(row).join('')}</div>`).join('')}
    <h2>Tongue twisters</h2><div class="card">${L.twisters.map(row).join('')}</div>
    <h2>Troubleshooting</h2><div class="card prose">${L.troubleshooting.map(([q, a]) => `<p><strong>${esc(q)}</strong><br>${esc(a)}</p>`).join('')}</div>`;
  wireRecorder(app);
  document.getElementById('rr-log').onclick = async () => {
    const minutes = parseInt(document.getElementById('rr-min').value, 10);
    if (!(minutes > 0)) return toast('Enter minutes');
    await send({ type: 'session', minutes, note: 'R trill practice — ' + document.getElementById('tech').value }, 'Trill practice logged');
  };
}

function guide(id) {
  const g = (C.guides || []).find(g => g.id === id);
  if (!g) return (location.hash = '#/');
  app.innerHTML = `<div class="muted"><a href="#/">← Home</a></div><h1>${g.icon} ${esc(g.title)}</h1>
    <p class="muted" style="font-size:.9rem">Tap 🔊 next to any Spanish phrase to hear it.</p><div class="prose">${md(g.md)}</div>`;
}

// ---------- vocabulary bank (Quizlet folders, loaded on demand from quizlet.js) ----------
function loadQuizlet() {
  if (window.QUIZLET) return Promise.resolve(window.QUIZLET);
  return new Promise((ok, fail) => {
    const s = document.createElement('script');
    s.src = 'quizlet.js';
    s.onload = () => ok(window.QUIZLET);
    s.onerror = fail;
    document.head.appendChild(s);
  });
}
const fold = s => s.normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase();
const LATAM_TAG = /^(.*\((?:L\.A\.|Mex|Ven|Col)\))[.,]?\s*(.*?)\s*\(Sp\)$/;  // Americanisms: "X (L.A.), Y (Sp)"

// What the voice reads: drop notes in brackets like (MX) or (L.A.) and read "caro/cara" as "caro, cara"
const spoken = s => s.replace(/\((s|es)\)/g, '$1').replace(/\([^)]*\)/g, ', ').replace(/[\/;]|\.\.\./g, ', ').replace(/\s+/g, ' ').replace(/(\s*,\s*)+/g, ', ').replace(/^[\s,]+|[\s,]+$/g, '');

// One table row. w = [English, Spanish, what to say instead (only for Spain-only words)]
function vocabRow(w, topic) {
  const [en, es, instead, kind] = w;
  // The Spain-side word: 🇪🇸 with a Spain voice when it's Spain-only, 🌎 with the Mexican voice when Latin America uses it too
  const other = word => {
    if (/^— vulgar/.test(instead || '')) return `<span class="muted">${esc(word)}</span> ${sayBtn(spoken(word), 'es-ES')} <span class="chip">🇪🇸 Spain</span> <span class="chip">🔞 vulgar</span>`;
    return kind === 'also'
      ? `<span class="muted">${esc(word)}</span> ${sayBtn(spoken(word))} <span class="chip on">🌎 also Latin America</span>`
      : `<span class="muted">${esc(word)}</span> ${sayBtn(spoken(word), 'es-ES')} <span class="chip">🇪🇸 Spain</span>` + (/\bcoger\b/.test(word) ? ' <span class="chip">⚠️ rude in Mexico</span>' : '');
  };
  let spanish = esc(es), add = es;
  const m = !instead && es.match(LATAM_TAG);
  if (instead) {
    add = instead.startsWith('—') ? '' : instead.replace(/\s*\(.*$/, '');
    spanish = `<strong>${esc(instead)}</strong>${add ? ' ' + sayBtn(spoken(instead)) : ''}<br>${other(es)}`;
  } else if (m) {
    add = spoken(m[1]);
    spanish = `${esc(m[1])} ${sayBtn(add)}<br>${other(m[2])}`;
  } else if (spoken(es)) {
    spanish += ' ' + sayBtn(spoken(es));
  }
  const btn = add ? `<button class="add" data-es="${attr(add)}" data-en="${attr(en)}" data-topic="${attr(topic)}" title="Add to my Vocab">➕</button>` : '';
  return `<tr><td>${spanish}</td><td>${esc(en)}</td><td>${btn}</td></tr>`;
}
const vocabTable = (rows, topic) => `<table class="vocab"><thead><tr><th>Español</th><th>English</th><th></th></tr></thead><tbody>${rows.map(w => vocabRow(w, topic)).join('')}</tbody></table>`;

app.addEventListener('click', e => {
  const b = e.target.closest('button.add');
  if (b) send({ type: 'vocab', es: b.dataset.es, en: b.dataset.en, topic: b.dataset.topic }, `Added “${b.dataset.es}” to Vocab`);
});

async function vocab(id) {
  app.innerHTML = '<p class="muted">Loading vocabulary…</p>';
  let Q;
  try { Q = await loadQuizlet(); } catch { app.innerHTML = '<p>Couldn\'t load the vocabulary list.</p>'; return; }
  const total = Q.reduce((a, f) => a + f.sets.reduce((b, s) => b + s.words.length, 0), 0);
  const f = Q.find(f => f.id === id);
  const head = `<p class="muted" style="font-size:.9rem">From the Quizlet class “Mastering Spanish Vocabulary”. Where Quizlet gives a Spain word, the Latin American word is in bold and the Spain one is underneath — 🇪🇸 Spain-only, or 🌎 also used in Latin America. ➕ copies a word into My Notes/Vocab.md.</p>
    <input type="search" id="vq" placeholder="Search English or Spanish…" style="width:100%;margin:8px 0 4px">`;
  if (!f) {
    app.innerHTML = `<div class="muted"><a href="#/">← Home</a></div><h1>📚 Vocabulary Bank</h1>${head}
      <div id="vres"></div>
      <div class="grid" id="vgrid">${Q.map(f => `<a class="card week-card" href="#/vocab/${f.id}">
        <div class="num">${f.sets.reduce((a, s) => a + s.words.length, 0)} words</div><div class="t">${f.id}. ${esc(f.title)}</div></a>`).join('')}</div>
      <p class="muted" style="font-size:.9rem">${total.toLocaleString()} words in ${Q.length} topics.</p>`;
    const all = Q.flatMap(f => f.sets.flatMap(s => s.words.map(w => ({ w, f, key: fold(w.join(' ')) }))));
    document.getElementById('vq').oninput = e => {
      const q = fold(e.target.value.trim());
      document.getElementById('vgrid').hidden = !!q;
      const hits = q ? all.filter(x => x.key.includes(q)) : [];
      document.getElementById('vres').innerHTML = !q ? '' : !hits.length ? '<p class="muted">No matches.</p>'
        : `<div class="prose">${hits.length > 200 ? `<p class="muted">Showing 200 of ${hits.length} — keep typing to narrow it down.</p>` : ''}
          <table class="vocab search"><thead><tr><th>Español</th><th>English</th><th></th><th>Topic</th></tr></thead><tbody>${hits.slice(0, 200).map(x =>
            vocabRow(x.w, x.f.title).replace('</tr>', `<td><a href="#/vocab/${x.f.id}">${esc(x.f.title)}</a></td></tr>`)).join('')}</tbody></table></div>`;
    };
    return;
  }
  const i = Q.indexOf(f), prev = Q[i - 1], next = Q[i + 1];
  const sets = () => f.sets.map((s, k) => `<h2 id="set-${k}">${esc(s.title)}</h2>${vocabTable(s.words, f.title)}`).join('');
  app.innerHTML = `<div class="muted"><a href="#/">← Home</a> · <a href="#/vocab">📚 Vocabulary Bank</a></div>
    <h1>${f.id}. ${esc(f.title)}</h1>${head}
    <div class="chips" id="vsets">${f.sets.map((s, k) => `<a class="chip" href="javascript:void 0" data-k="${k}">${esc(s.title)}</a>`).join('')}</div>
    <div class="prose" id="vbody">${sets()}</div>
    <div class="row" style="justify-content:space-between;margin-top:16px">
      ${prev ? `<a class="btn ghost" href="#/vocab/${prev.id}">← ${esc(prev.title)}</a>` : '<span></span>'}
      ${next ? `<a class="btn ghost" href="#/vocab/${next.id}">${esc(next.title)} →</a>` : ''}</div>`;
  document.getElementById('vsets').onclick = e => {
    const c = e.target.closest('[data-k]');
    if (c) document.getElementById('set-' + c.dataset.k)?.scrollIntoView({ behavior: 'smooth' });
  };
  document.getElementById('vq').oninput = e => {
    const q = fold(e.target.value.trim());
    document.getElementById('vsets').hidden = !!q;
    document.getElementById('vbody').innerHTML = !q ? sets()
      : vocabTable(f.sets.flatMap(s => s.words).filter(w => fold(w.join(' ')).includes(q)), f.title);
  };
}

// ---------- router ----------
function route() {
  const [, view, n, tab] = location.hash.split('/');
  document.getElementById('accents').hidden = true;
  if (view === 'week') week(+n, TABS.some(t => t[0] === tab) ? tab : 'lesson');
  else if (view === 'lab') rrLab();
  else if (view === 'guide') guide(n);
  else if (view === 'vocab' && !PUBLIC) vocab(n);
  else home();
  window.scrollTo(0, 0);
}
window.addEventListener('hashchange', route);
loadState().then(route);
