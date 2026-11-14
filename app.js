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
  sync.textContent = online ? T('Saving to Obsidian') : T('Not saving');
  sync.className = 'sync' + (online ? ' ok' : '');
}

async function send(ev, msg) {
  if (PUBLIC) return;
  if (!online) { toast(T('Not saved — start the server to record progress')); return; }
  try {
    const r = await fetch('/api/event', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(ev) });
    if (!r.ok) throw new Error((await r.json()).error);
    state = await r.json();
    if (msg) toast(msg);
  } catch (e) {
    toast(T('Save failed: ') + e.message);
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
  return f ? `<button class="play" data-a="media/${f}" title="${T('Listen')}" aria-label="${T('Listen: ')}${esc(text)}">🔊</button>` : '';
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
  player.play().catch(() => { b.classList.remove('on'); toast(T('Audio needs the server running')); });
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
  const fallback = () => { const v = spanishVoice(false); v ? browserVoice(v) : (off(), toast(T('No Spanish voice available — start the server for audio'))); };
  if (!online) return fallback();
  player = new Audio('/api/say?t=' + encodeURIComponent(text) + (spain ? '&v=es' : ''));
  player.onended = off;
  on();
  player.play().catch(fallback);
}
// 🔊 for any Spanish text: the recorded es-MX clip when there is one, otherwise speak()
const attr = s => esc(s).replace(/"/g, '&quot;');
const sayBtn = (text, lang) => (!lang && playBtn(text)) || `<button class="play" data-t="${attr(text)}"${lang ? ` data-l="${lang}"` : ''} title="${lang === 'es-ES' ? T('Listen (Spain)') : T('Listen')}" aria-label="${T('Listen: ')}${attr(text)}">🔊</button>`;

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
  if (!g) return { ok: false, kind: 'bad', msg: T('Answer: {a}', { a: accepted[0] }) };
  if (accepted.some(a => norm(a) === g)) return { ok: true, kind: 'good', msg: T('✓ Correct') };
  if (accepted.some(a => deaccent(norm(a)) === deaccent(g)))
    return { ok: false, kind: 'warn', msg: T('Almost — check the accents: {a}. In Spanish accents change meaning (hablo ≠ habló).', { a: accepted[0] }) };
  return { ok: false, kind: 'bad', msg: T('Answer: {a}', { a: accepted[0] }) + (accepted.length > 1 ? T('  (also OK: {a})', { a: accepted.slice(1).join(' · ') }) : '') };
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
  box.innerHTML = `<div class="muted">🎲 ${i === undefined ? T('Palabra del día') : T('Palabra al azar')} · ${esc(d.topic)}</div>
    <div class="wotd-word">${esc(d.es)} ${playBtn(d.es)}</div>
    <div class="say-syl">${esc(d.say)}</div>
    <div class="wotd-en">${esc(d.en)}</div>
    <p><em>${esc(d.ex)}</em> ${playBtn(d.ex)}<br><span class="muted">${esc(d.ex_en)}</span></p>
    <div class="row"><button class="btn ghost" id="wotd-next">${T('🔀 Another word')}</button><button class="btn vault-only" id="wotd-add">${T('➕ Add to my Vocab')}</button></div>`;
  box.querySelector('#wotd-next').onclick = () => {
    let k; do k = Math.floor(Math.random() * D.length); while (D.length > 1 && k === n);
    wordOfTheDay(box, k);
  };
  box.querySelector('#wotd-add').onclick = () => send({ type: 'vocab', es: d.es, en: d.en, topic: d.topic.replace(/^\S+\s/, '') }, T('Added “{w}” to Vocab', { w: d.es }));
}

function home() {
  const cur = state.current_week ?? FIRST;
  const cw = byWeek(cur);
  const done = Object.values(state.complete || {}).filter(Boolean).length;
  const minutes = state.sessions.reduce((a, s) => a + s.minutes, 0);
  let html = `
  <div class="card hero">
    <div>
      <div class="muted">${T('Week {n} of {m}', { n: cur, m: LAST })} · ${T(C.phases[cw.phase])}</div>
      <h1>${esc(T(cw.title))}</h1>
      <div class="muted">${esc(T(cw.goal))}</div>
    </div>
    <a class="btn" href="#/week/${cur}">${Object.keys(wk(cur)).length ? T('Continue') : T('Start')} →</a>
  </div>
  <div class="stats vault-only">
    <div class="card stat"><b>${done}/${C.weeks.length}</b><span>${T('weeks complete')}</span></div>
    <div class="card stat"><b>${minutes}</b><span>${T('minutes studied')}</span></div>
    <div class="card stat"><b>${state.sessions.length}</b><span>${T('study sessions')}</span></div>
  </div>
  <div class="card wotd" id="wotd"></div>`;
  for (const ph of Object.keys(C.phases).map(Number)) {
    html += `<div class="phase-label">${T('Phase {n}', { n: ph })} · ${T(C.phases[ph])}</div><div class="grid">`;
    for (const w of C.weeks.filter(w => w.phase === ph)) {
      const p = wk(w.week);
      const chip = (on, label) => `<span class="chip ${on ? 'on' : ''}">${label}</span>`;
      const status = state.complete?.[w.week] ? `<span class="chip on">${T('✓ complete')}</span>`
        : w.week === cur ? `<span class="chip cur">${T('current')}</span>` : '';
      html += `<a class="card week-card ${w.week === cur ? 'current' : ''}" href="#/week/${w.week}">
        <div class="num">${T('Week {n}', { n: w.week })}</div><div class="t">${esc(T(w.title))}</div>
        <div class="chips">${status}${chip(p.lesson_done, T('Lesson'))}${chip(p.worksheet_attempts, T('Worksheet'))}
        ${chip(p.quiz_total && p.quiz_best / p.quiz_total >= .8, p.quiz_attempts ? T('Quiz {p}%', { p: pct(p.quiz_best, p.quiz_total) }) : T('Quiz'))}
        ${w.cyber ? chip(p.cyber_attempts, T('Cyber')) : ''}${chip(p.practice_done, T('Practice'))}</div></a>`;
    }
    html += '</div>';
  }
  html += `
  <h2>${T('Grammar guides')}</h2>
  <div class="grid">${(C.guides || []).map(g => `<a class="card week-card" href="#/guide/${g.id}">
    <div class="num">${g.weeks.length ? T('With week {n}', { n: g.weeks.join(', ') }) : T('Reference')}</div><div class="t">${g.icon} ${esc(T(g.title))}</div>
    <div class="muted" style="font-size:.9rem">${esc(T(g.blurb))}</div></a>`).join('')}</div>
  <a class="card lab-card" href="#/lab/rr"><b>${T('🌀 R Trill Lab')}</b><span class="muted">${T('Can\'t roll your r yet? 7 techniques, a practice ladder, slow audio and a 5-minute daily routine.')}</span></a>
  <a class="card lab-card vault-only" href="#/vocab"><b>${T('📚 Vocabulary Bank')}</b><span class="muted">${T('5,800+ words in 24 topics from the Quizlet class — searchable, with Spain-only words swapped for the Latin American ones.')}</span></a>
  <h2 class="vault-only">${T('Log a study session')}</h2>
  <div class="card vault-only">
    <div class="row">
      <input type="number" id="mins" min="1" max="600" value="30" style="width:90px"> ${T('minutes')}
      <input type="text" id="snote" placeholder="${T('What did you do? (e.g. Anki + Dreaming Spanish)')}" style="flex:1;min-width:200px">
      <button class="btn" id="logbtn">${T('Log it')}</button>
    </div>
    <p class="muted" style="margin:10px 0 0;font-size:.9rem">${T('Daily routine: 10 min grammar · 10 min flashcards · 10 min listening · 5–10 min speaking/writing. A week is complete when the lesson, worksheet and practice are done and the quiz is ≥ 80%.')}</p>
  </div>`;
  if (state.activity.length) html += `<h2>${T('Recent activity')}</h2><div class="card"><ul style="margin:0;padding-left:20px">${state.activity.slice(-8).reverse().map(a => `<li>${esc(a)}</li>`).join('')}</ul></div>`;
  app.innerHTML = html;
  wordOfTheDay(document.getElementById('wotd'));
  document.getElementById('logbtn').onclick = async () => {
    const minutes = parseInt(document.getElementById('mins').value, 10);
    if (!(minutes > 0)) return toast(T('Enter minutes'));
    await send({ type: 'session', minutes, note: document.getElementById('snote').value }, T('Session logged'));
    home();
  };
}

const TABS = [['lesson', T('Lesson')], ['words', T('📖 Words')], ['drills', T('🎯 Drills')], ['worksheet', T('Worksheet')], ['quiz', T('Quiz')], ['grammar', T('✅ Grammar')], ['cyber', T('🛡️ Cyber')], ['practice', T('Practice')]];
const tabsFor = w => TABS.filter(([k]) => (k !== 'drills' || w.drills) && (k !== 'words' || (w.words || []).length) && (k !== 'grammar' || w.grammar.length) && (k !== 'cyber' || w.cyber));
// The tab after `tab` for this week, so "Next →" never points at a tab the week doesn't have.
const tabAfter = (w, tab) => { const t = tabsFor(w).map(([k]) => k); return t[t.indexOf(tab) + 1] || 'practice'; };

function week(n, tab) {
  const w = byWeek(n);
  if (!w) return (location.hash = '#/');
  const p = wk(n);
  const ticks = { grammar: p.grammar_attempts, lesson: p.lesson_done, worksheet: p.worksheet_attempts, quiz: p.quiz_total && p.quiz_best / p.quiz_total >= .8, cyber: p.cyber_attempts, practice: p.practice_done };
  app.innerHTML = `
    <div class="muted"><a href="#/">${T('← All weeks')}</a> · ${T('Phase {n}', { n: w.phase })} · ${T(C.phases[w.phase])}</div>
    <h1>${T('Week {n}', { n })}: ${esc(T(w.title))}</h1>
    <div class="muted">${esc(T(w.goal))}</div>
    <nav class="tabs">${tabsFor(w).map(([k, l]) => `<a href="#/week/${n}/${k}" class="${k === tab ? 'active' : ''}">${l}${ticks[k] ? ' <span class="tick">✓</span>' : ''}</a>`).join('')}</nav>
    <section id="pane"></section>
    <div class="row" style="justify-content:space-between;margin-top:32px">
      ${n > FIRST ? `<a href="#/week/${n - 1}">← ${T('Week {n}', { n: n - 1 })}</a>` : '<span></span>'}
      ${n < LAST ? `<a href="#/week/${n + 1}">${T('Week {n}', { n: n + 1 })} →</a>` : ''}
    </div>`;
  const pane = document.getElementById('pane');
  if (!tabsFor(w).some(([k]) => k === tab)) tab = 'lesson';
  ({ lesson: lessonPane, words: wordsPane, drills: drillsPane, grammar: grammarPane, worksheet: worksheetPane, quiz: quizPane, cyber: cyberPane, practice: practicePane })[tab](pane, w, p);
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
  return cards ? `<h2 style="margin-top:0">${T('📷 Picture vocabulary')}</h2><div class="photos">${cards}</div>` : '';
}

function sayFirst(w) {
  if (!w.say_first.length) return '';
  const hide = (() => { try { return localStorage.getItem('hide-syll') === '1'; } catch { return false; } })();
  return `<div class="card say-first ${hide ? 'hide-syll' : ''}">
    <div class="row" style="justify-content:space-between">
      <h2 style="margin:0">${T('🔤 Say it first')}</h2>
      <label class="muted" style="font-size:.9rem"><input type="checkbox" id="syll-toggle" ${hide ? '' : 'checked'}> ${T('Show syllables')}</label>
    </div>
    <p class="muted" style="margin:6px 0 12px">${T('Read each word out loud <b>before</b> pressing 🔊. Syllables are split with · and the <b>STRESSED</b> one is in capitals. Then check yourself.')}</p>
    <div class="say-grid">${w.say_first.map(x => `<div class="say-item"><div class="say-es">${esc(x.es)} ${playBtn(x.es)}</div><div class="say-syl">${esc(x.say)}</div></div>`).join('')}</div>
  </div>`;
}

// Grammar guides that go with this week, shown above the lesson
function guideLinks(w) {
  const gs = (C.guides || []).filter(g => g.weeks.includes(w.week));
  return gs.length ? `<div class="guide-links muted">${T('📚 Extra grammar for this week:')} ${gs.map(g => `<a href="#/guide/${g.id}">${g.icon} ${esc(T(g.title))}</a>`).join(' · ')}</div>` : '';
}

function lessonPane(pane, w, p) {
  pane.innerHTML = `${guideLinks(w)}${w.week === 0 ? `<a class="card lab-card" href="#/lab/rr" style="margin-bottom:16px"><b>${T('🌀 R Trill Lab')}</b><span class="muted">${T('Can\'t roll your r yet? Practice it here — 7 techniques, slow audio, record yourself.')}</span></a>` : ''}${sayFirst(w)}${photoGallery(w)}<p class="muted" style="font-size:.9rem">${T('Tap 🔊 next to any Spanish phrase to hear it (Mexican Spanish voice).')}</p><div class="prose">${md(w.lesson)}</div>
    <div class="row" style="margin-top:24px">
      <button class="btn" id="read" ${p.lesson_done ? 'disabled' : ''}>${p.lesson_done ? T('✓ Lesson read') : T('Mark lesson as read')}</button>
      <a class="btn ghost" href="#/week/${w.week}/worksheet">${T('Go to worksheet →')}</a>
    </div>`;
  const tog = document.getElementById('syll-toggle');
  if (tog) tog.onchange = () => {
    pane.querySelector('.say-first').classList.toggle('hide-syll', !tog.checked);
    try { localStorage.setItem('hide-syll', tog.checked ? '0' : '1'); } catch {}
  };
  document.getElementById('read').onclick = async () => { await send({ type: 'lesson', week: w.week }, T('Lesson marked as read')); route(); };
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
    <div class="row"><button class="btn" id="check">${T('Check answers')}</button><button class="btn ghost" id="retry" hidden>${T('Try again')}</button>
    <a class="btn ghost" id="next" href="#/week/${w.week}/${nextTab || tabAfter(w, kind)}" hidden>${T('Next →')}</a></div>`;
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
    await send({ type: kind, week: w.week, score, total: items.length, missed }, T('Score saved to Obsidian'));
  };
  document.getElementById('retry').onclick = () => route();
}

function worksheetPane(pane, w, p) {
  const best = p.worksheet_attempts ? T(' Best so far: {a}/{b}.', { a: p.worksheet_best, b: p.worksheet_total }) : '';
  typedExercise(pane, w, w.worksheet, 'worksheet', T('Type each answer. Press Enter to jump to the next one. Use the accent bar at the bottom for á é í ó ú ñ.') + best);
}

function cyberPane(pane, w, p) {
  const c = w.cyber;
  const best = p.cyber_attempts ? T(' Best so far: {a}/{b}.', { a: p.cyber_best, b: p.cyber_total }) : '';
  pane.innerHTML = `<div class="prose">
      <p>${inline(c.focus)}</p>
      <h2>${T('Vocabulary')}</h2>
      <table><thead><tr><th>Español</th><th>English</th></tr></thead><tbody>
      ${c.terms.map(([es, en], i) => `<tr><td><strong>${esc(es)}</strong> ${playBtn(es)}<div class="say-syl">${esc(c.say[i])}</div></td><td>${esc(en)}</td></tr>`).join('')}</tbody></table>
      <h2>${T('Using this week\'s grammar')}</h2>
      <ul>${c.examples.map(([es, en]) => `<li><em>${esc(es)}</em> ${playBtn(es)} — ${esc(en)}</li>`).join('')}</ul>
      <h2>${T('Drill')}</h2></div><div id="drill"></div>`;
  typedExercise(document.getElementById('drill'), w, c.drill, 'cyber', T('Translate into Spanish.') + best);
}

function quizPane(pane, w, p) {
  const best = p.quiz_attempts ? T(' Best so far: {a}/{b}.', { a: p.quiz_best, b: p.quiz_total }) : '';
  const qs = w.quiz.map(q => ({ ...q, order: shuffle(q.o.map((_, i) => i)) }));
  pane.innerHTML = `<p class="muted">${T('Pick one answer for each question. You need 80% to pass this week.')}${best}</p>
    <div class="card">${qs.map((q, i) => `
      <div class="item">
        <div class="q"><span class="n">${i + 1}.</span>${inline(q.q)}</div>
        <div class="opts">${q.order.map(oi => `<label><input type="radio" name="q${i}" value="${oi}"> ${inline(q.o[oi])}</label>`).join('')}</div>
        <div class="fb" hidden></div>
      </div>`).join('')}</div>
    <div class="result" id="result"></div>
    <div class="row"><button class="btn" id="submit">${T('Submit quiz')}</button><button class="btn ghost" id="retry" hidden>${T('Retake')}</button>
    <a class="btn ghost" id="next" href="#/week/${w.week}/${tabAfter(w, 'quiz')}" hidden>${T('Next →')}</a></div>`;
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
    document.getElementById('result').innerHTML = `<b>${score}/${qs.length}</b> (${pct(score, qs.length)}%) — ${passed ? T('🎉 Passed!') : T('Need 80% to pass. Review the explanations and retake.')}`;
    document.getElementById('submit').hidden = true;
    document.getElementById('retry').hidden = false;
    document.getElementById('next').hidden = false;
    await send({ type: 'quiz', week: w.week, score, total: qs.length, missed }, T('Quiz saved to Obsidian'));
  };
  document.getElementById('retry').onclick = () => route();
}

// Shadowing: hear the model, record yourself, compare. Recordings stay in the browser.
let micStream = null;
function speakSection(w) {
  const phrases = (w.speak || [...(w.cyber ? w.cyber.examples.map(e => e[0]) : []), ...w.photos.map(p => p.es)]).filter(t => AUDIO[t]);
  if (!phrases.length) return '';
  return `<h2>${T('🗣️ Say it out loud')}</h2>
    <p class="muted">${T('Play 🔊, then press 🎙 and say it yourself. Press ■ to stop, then ▶ to hear yourself next to the model. Recordings aren\'t saved anywhere.')}</p>
    <div class="card">${phrases.map((t, i) => `
      <div class="speak-row"><span class="speak-text">${esc(t)}</span>
        <span class="row">${playBtn(t)}<button class="rec" data-i="${i}" title="${T('Record')}">🎙</button><button class="mine" data-i="${i}" title="${T('Play my recording')}" disabled>${T('▶ Me')}</button></span>
      </div>`).join('')}</div>`;
}

function wireRecorder(pane) {
  const takes = {};
  let rec = null;
  pane.querySelectorAll('.rec').forEach(btn => btn.onclick = async () => {
    if (rec && rec.state === 'recording') { rec.stop(); return; }
    try {
      micStream = micStream || await navigator.mediaDevices.getUserMedia({ audio: true });
    } catch { return toast(T('Microphone blocked — allow it in the browser to record')); }
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
  pane.innerHTML = `<div class="card prose"><h3 style="margin-top:0">${T('Task')}</h3><p>${inline(w.practice)}</p></div>
    ${speakSection(w)}
    <h2>${T('Your writing')}</h2>
    <p class="muted vault-only">${T('Saved into your Obsidian vault under <code>Practice/</code> so a Claude session can review it and correct mistakes.')}${p.practice_entries ? (p.practice_entries === 1 ? T(' You\'ve saved 1 entry for this week.') : T(' You\'ve saved {n} entries for this week.', { n: p.practice_entries })) : ''}</p>
    <textarea id="txt" placeholder="Escribe aquí…">${esc(draft)}</textarea>
    <div class="row vault-only" style="margin-top:12px">
      <button class="btn" id="save">${T('Save to Obsidian')}</button>
      <button class="btn ghost" id="done" ${p.practice_done ? 'disabled' : ''}>${p.practice_done ? T('✓ Practice done') : T('Mark done (spoken/offline practice)')}</button>
    </div>`;
  wireRecorder(pane);
  const txt = document.getElementById('txt');
  txt.oninput = () => { try { localStorage.setItem('draft-' + w.week, txt.value); } catch {} };
  document.getElementById('save').onclick = async () => {
    if (!txt.value.trim()) return toast(T('Write something first'));
    await send({ type: 'practice', week: w.week, text: txt.value }, T('Saved to Obsidian'));
    try { localStorage.removeItem('draft-' + w.week); } catch {}
    route();
  };
  document.getElementById('done').onclick = async () => { await send({ type: 'practice', week: w.week, text: '' }, T('Practice marked done')); route(); };
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
    player.play().catch(() => toast(T('Audio needs the server running')));
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
    vowel: { name: T('Which vowel?'), make() {
      const s = pick(D.vowels);
      return { prompt: T('Listen — which vowel do you hear?'), audio: [s], options: ['a', 'e', 'i', 'o', 'u'], answer: 'aeiou'.indexOf(s.slice(-1)), reveal: s };
    } },
    letter: { name: T('Which letter?'), make() {
      const L = pick(letters);
      const opts = shuffle([L, ...shuffle(letters.filter(x => x !== L)).slice(0, 3)]);
      return { prompt: T('Listen — which letter is this?'), audio: [L.name], options: opts.map(x => x.letter), answer: opts.indexOf(L), reveal: `${L.letter} = ${L.name}` };
    } },
    trill: { name: T('Tap or trill?'), make() {
      const pair = pick(D.pairs), w = pick(pair);
      return { prompt: T('Listen — one tap (r) or rolled (rr)?'), audio: [w], options: pair, answer: pair.indexOf(w), reveal: w };
    } },
    stress: { name: T('Where\'s the stress?'), make() {
      const x = pick(D.stress);
      return { prompt: `${T('Which syllable is stressed in')} <span class="big">${esc(x.w)}</span>?`, options: x.syl, answer: x.k, after: [x.w],
               reveal: x.syl.map((s, i) => i === x.k ? s.toUpperCase() : s).join('·') };
    } },
    rules: { name: T('Rule detective'), make() {
      const r = pick(D.rules);
      const order = shuffle(r.o.map((_, i) => i));
      return { prompt: `${T('How does the highlighted part sound?')} <span class="big">${esc(r.w).replace(/\[(.+?)\]/, '<mark>$1</mark>')}</span>`,
               options: order.map(i => r.o[i]), answer: order.indexOf(0), after: [plain(r.w)], reveal: `${plain(r.w)}: ${r.o[0]}` };
    } },
    spelled: { name: T('Spelled dictation'), make() {
      const w = pick(D.dictation);
      return { prompt: T('Listen to the letters being spelled, then type the word'), audio: spellTokens(w, D, false).flatMap(t => t.say), typed: true, accept: [w], after: [w], reveal: w };
    } },
  };
}

// 📖 Words: themed word lists for the week (words.py) as cards — 🔊, ➕, filter, hide-English self-test and a quiz per list
const ARTICLE = /^(el|la|los|las)\s+(.+)$/i;
const artWord = es => {
  const parts = es.split('/');  // "el mesero/la mesera": colour both articles
  if (parts.length > 1 && parts.every(x => ARTICLE.test(x.trim()))) return parts.map(x => artWord(x.trim())).join(' / ');
  const m = es.match(ARTICLE);
  return m ? `<span class="art ${/^(el|los)$/i.test(m[1]) ? 'm' : 'f'}">${esc(m[1])}</span> ${esc(m[2])}` : esc(es);
};
const notePills = note => (note ? note.split(' · ') : []).map(n =>
  `<span class="pill ${n.startsWith('🌎') ? 'latam' : n.startsWith('🇪🇸') ? 'spain' : 'tip'}">${esc(n)}</span>`).join('');
const rowCard = ([es, en, note, clip]) => ({ es, en, note, clip });  // a Words-tab row as a flashcard
function wordCard([es, en, note, clip], topic) {
  const word = artWord(es);
  const pills = notePills(note) + (isKnown({ es }) ? `<span class="pill known">${T('✅ known')}</span>` : '');
  return `<div class="wcard" data-f="${attr(fold([es, en, note].join(' ')))}">
    <div class="es">${word} ${sayBtn(clip)}</div><div class="en">${esc(en)}</div>${pills ? `<div class="pills">${pills}</div>` : ''}
    <button class="add vault-only" data-es="${attr(clip)}" data-en="${attr(en)}" data-topic="${attr(topic)}" title="${T('Add to my Vocab')}">➕</button></div>`;
}
function wordGrid(rows, topic) {
  let group = null, html = '';
  for (const r of rows) {
    if (r[4] !== group && (group = r[4])) html += `<h3 class="wgroup">${esc(T(group))}</h3>`;
    html += wordCard(r, topic);
  }
  return `<div class="wgrid">${html}</div>`;
}
function wordsPane(pane, w) {
  const S = w.words, topic = `Week ${w.week} words`;  // topic goes into Vocab.md, so it stays English
  const countText = s => { const k = s.rows.filter(r => isKnown({ es: r[0] })).length; return T('{n} words', { n: s.rows.length }) + (k ? T(' · ✅ {k} known', { k }) : ''); };
  const refresh = () => {  // after a flashcard round: update ✅ badges and counts, keep the filter
    pane.querySelectorAll('.wsec').forEach((sec, i) => {
      sec.querySelector('.count').textContent = countText(S[i]);
      sec.querySelector('.wgrid').outerHTML = wordGrid(S[i].rows, topic);
    });
    pane.querySelector('#wfilter').dispatchEvent(new Event('input'));
  };
  pane.innerHTML = `<p class="muted wintro">${T('{n} words in {m} lists. Mexican Spanish first —', { n: S.reduce((a, s) => a + s.rows.length, 0), m: S.length })}
      <span class="pill latam">${T('🌎 other Latin America')}</span> <span class="pill spain">${T('🇪🇸 Spain')}</span> <span class="pill tip">${T('💡 tip')}</span>
      <span class="art m">el / los</span> <span class="art f">la / las</span></p>
    <div class="wbar">
      <div class="wtools"><input type="search" id="wfilter" placeholder="${T('Filter: fruit, mango, spicy…')}">
        <label class="chip"><input type="checkbox" id="hide-en"> ${T('🙈 Hide English')}</label>
        <button class="btn ghost" data-flash="all">${T('🎴 Flashcards: all lists')}</button></div>
      <div id="wsets">${S.map((s, i) => `<button class="chip" data-go="${i}">${esc(T(s.title))}</button>`).join('')}</div>
    </div>
    ${S.map((s, i) => `<section class="wsec" id="ws-${i}">
      <div class="wsec-head"><h2>${esc(T(s.title))} <span class="count">${countText(s)}</span></h2>
        <div class="wsec-btns"><button class="btn ghost" data-flash="${i}">${T('🎴 Flashcards')}</button><button class="btn ghost" data-quiz="${i}">${T('🎲 Quiz me')}</button>${s.bank ? `<a class="btn ghost vault-only" href="#/vocab/${s.bank}">${T('📚 Vocabulary Bank')}</a>` : ''}</div></div>
      <div class="wquiz" id="wq-${i}"></div>${wordGrid(s.rows, topic)}</section>`).join('')}
    <p class="muted" id="wnone" hidden>${T('No words match.')}</p>`;
  pane.querySelector('#hide-en').onchange = e => pane.classList.toggle('hide-en', e.target.checked);
  pane.querySelector('#wfilter').oninput = e => {
    const q = fold(e.target.value.trim());
    let any = false;
    pane.querySelectorAll('.wsec').forEach(sec => {
      let shown = 0, head = null, headShown = 0;
      const closeGroup = () => { if (head) head.hidden = !headShown; };
      for (const el of sec.querySelector('.wgrid').children) {
        if (el.tagName === 'H3') { closeGroup(); head = el; headShown = 0; continue; }
        el.hidden = !!q && !el.dataset.f.includes(q);
        if (!el.hidden) { shown++; headShown++; }
      }
      closeGroup();
      sec.hidden = !shown;
      any ||= !!shown;
    });
    pane.querySelector('#wnone').hidden = any;
  };
  pane.onclick = e => {
    const go = e.target.closest('[data-go]'), qz = e.target.closest('[data-quiz]'), card = e.target.closest('.wcard'), fl = e.target.closest('[data-flash]');
    if (fl) {
      const all = fl.dataset.flash === 'all', s = S[+fl.dataset.flash];
      flashcards(all ? T('Week {n} words', { n: w.week }) : `${T('Week {n}', { n: w.week })} › ${T(s.title)}`, (all ? S.flatMap(x => x.rows) : s.rows).map(rowCard), refresh);
    } else if (go) document.getElementById('ws-' + go.dataset.go).scrollIntoView({ behavior: 'smooth' });
    else if (qz) wordQuiz(document.getElementById('wq-' + qz.dataset.quiz), S[+qz.dataset.quiz].rows);
    else if (card && pane.classList.contains('hide-en') && !e.target.closest('button')) card.classList.toggle('peek');
  };
}

// 10 questions: see the English, pick the Spanish. Right answers play the word.
function wordQuiz(box, rows) {
  const qs = shuffle(rows).slice(0, 10);
  let i = 0, score = 0;
  const ask = () => {
    if (i === qs.length) {
      box.innerHTML = `<div class="card result"><b>${score}/${qs.length}</b> — ${score === qs.length ? T('🎉 Perfect!') : score >= qs.length * .8 ? T('Nice work!') : T('Keep practicing — try again.')}
        <div class="row"><button class="btn ghost" data-again>${T('Again')}</button><button class="btn ghost" data-close>${T('Close')}</button></div></div>`;
      box.querySelector('[data-again]').onclick = () => wordQuiz(box, rows);
      box.querySelector('[data-close]').onclick = () => { box.innerHTML = ''; };
      return;
    }
    const q = qs[i], opts = shuffle([q, ...shuffle(rows.filter(r => r !== q && r[1] !== q[1])).slice(0, 3)]);
    box.innerHTML = `<div class="card"><div class="muted" style="font-size:.85rem">${i + 1} / ${qs.length}</div>
      <div class="q" style="margin:6px 0"><b>${esc(q[1])}</b></div>
      <div class="opts">${opts.map((o, k) => `<label data-k="${k}">${esc(o[0])}</label>`).join('')}</div><div class="fb" hidden></div></div>`;
    box.querySelectorAll('.opts label').forEach(l => l.onclick = () => {
      if (box.querySelector('.opts .right')) return;
      const o = opts[+l.dataset.k], fb = box.querySelector('.fb');
      box.querySelectorAll('.opts label').forEach(x => opts[+x.dataset.k] === q && x.classList.add('right'));
      if (o === q) score++; else l.classList.add('wrong');
      fb.hidden = false;
      fb.className = 'fb ' + (o === q ? 'good' : 'bad');
      fb.innerHTML = `${o === q ? '✓' : '✗'} ${esc(q[0])} — ${esc(q[1])} ${sayBtn(q[3])}${q[2] ? `<div class="note">${esc(q[2])}</div>` : ''}`;
      const b = fb.querySelector('.play');
      if (o === q && b) b.click();
      setTimeout(() => { i++; ask(); }, o === q ? 1300 : 2600);
    });
  };
  ask();
}

function drillsPane(pane, w) {
  const D = w.drills;
  const modes = drillModes(D);
  pane.innerHTML = `
    <h2 style="margin-top:0">${T('🔤 Alphabet explorer')}</h2>
    <p class="muted">${T('Tap a letter to hear its name, how it sounds and example words.')}</p>
    <div class="letters">${D.alphabet.map((l, i) => `<button class="letter" data-i="${i}">${l.letter}</button>`).join('')}</div>
    <div id="letter-detail" class="card" hidden></div>

    <h2>${T('🗣️ Spell it out — usernames, emails, passwords')}</h2>
    <p class="muted">${T('Type anything and hear it spelled the way you\'d read it to a student or IT help desk. B is said <em>be larga</em> and V <em>ve corta</em> so they can\'t be confused.')}</p>
    <div class="card">
      <div class="row"><input type="text" id="spell-in" placeholder="${T('e.g. profe_ruiz23@colegio.edu')}" style="flex:1;min-width:220px" autocomplete="off" spellcheck="false">
      <button class="btn" id="spell-go">${T('🔊 Spell it')}</button></div>
      <label class="muted" style="font-size:.9rem;display:block;margin-top:8px"><input type="checkbox" id="spell-caps" checked> ${T('Say <em>mayúscula</em> for capital letters')}</label>
      <div id="spell-out" class="spell-out"></div>
    </div>

    <h2>${T('⚡ Quick-fire drills')}</h2>
    <p class="muted">${T('10 questions per round.')}<span class="vault-only">${T(' Scores go to your Obsidian Quiz Log, and missed items show up as weak spots.')}</span></p>
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
    if (!toks.length) return toast(T('Type something to spell'));
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
      send({ type: 'drill', week: w.week, label: mode.name, score, total: 10, missed }, T('Drill saved to Obsidian')));
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
    box.innerHTML = `<div class="muted">${T('{name} · {i} / {t} · score {s}', { name: esc(name), i: round.i + 1, t: total, s: round.score })}</div>
      <div class="drill-q">${q.prompt}</div>
      ${q.audio ? `<button class="btn ghost" id="replay">${T('🔊 Play again')}</button>` : ''}
      ${q.clips ? `<div class="row clips">${q.clips.map((_, i) => `<button class="btn ghost clip" data-c="${i}">${T('▶ Clip {c}', { c: 'ABC'[i] })}</button>`).join('')}</div>` : ''}
      ${q.typed ? `<div class="row" style="margin-top:12px"><input type="text" id="typed" autocomplete="off" spellcheck="false" style="flex:1;min-width:180px"><button class="btn" id="check1">${T('Check')}</button></div>`
                : `<div class="row opts-row" style="margin-top:12px">${q.options.map((o, i) => `<button class="opt" data-o="${i}">${esc(o)}</button>`).join('')}</div>`}
      <div id="fb1" class="fb" hidden></div>
      <button class="btn" id="next1" hidden style="margin-top:12px">${round.i === total - 1 ? T('See results') : T('Next →')}</button>`;
    if (q.audio) { playSeq(q.audio); document.getElementById('replay').onclick = () => playSeq(q.audio); }
    box.querySelectorAll('.clip').forEach(c => c.onclick = () => playSeq([q.clips[+c.dataset.c]]));
    const done = (ok, given, correct, msg) => {
      round.i++;
      if (ok) round.score++; else round.missed.push({ q: `${name} — ${q.reveal}`, given, correct });
      const fb = document.getElementById('fb1');
      fb.hidden = false; fb.className = 'fb ' + (ok ? 'good' : 'bad');
      fb.innerHTML = (msg || ((ok ? T('✓ Correct — ') : T('✗ Not quite. The correct answer is: ')) + esc(q.reveal))) + ' ' + (q.after ? playBtn(q.after[0]) : '') + (q.detail || '');
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
        done(r.ok, inp.value.trim(), q.accept[0], (r.ok ? T('✓ Correct — ') + esc(q.accept[0]) : esc(r.msg)));
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
      ${round.missed.length ? `<p class="muted">${T('Missed:')}</p><ul>${round.missed.map(m => `<li>${esc(m.q)}</li>`).join('')}</ul>` : ''}
      <button class="btn" id="again">${T('Play again')}</button>`;
    document.getElementById('again').onclick = () => runRound(box, name, make, onFinish, total);
    onFinish(round.score, round.missed);
  };
  ask();
}

// ---------- Grammar check ----------
const FORMATS = { mixed: T('Mixed'), mc: T('Multiple choice'), fix: T('Type the fix'), audio: T('Listen & choose') };

function grammarQuestion(g, fmt) {
  const meaning = `<div class="meaning">${T('Meaning: “{m}”', { m: esc(g.en) })}</div>`;
  const why = `<div class="why">${esc(g.x)}</div>`;
  if (fmt === 'fix') {
    return { prompt: `${T('This has a mistake — type it correctly:')}<span class="big">${esc(g.bad[0])}</span>${meaning}`,
             typed: true, accept: [g.ok, ...g.alt], after: [g.ok], reveal: g.ok, detail: why };
  }
  const opts = shuffle([g.ok, ...g.bad]);
  if (fmt === 'audio') {
    const letters = opts.map((_, i) => 'ABC'[i]);
    return { prompt: `${T('Listen to each clip. Which one is grammatically correct?')}${meaning}`, clips: opts, options: letters,
             answer: opts.indexOf(g.ok), after: [g.ok], reveal: g.ok,
             detail: why + `<ul class="clip-list">${opts.map((t, i) => `<li>${t === g.ok ? '✅' : '❌'} <b>${letters[i]}:</b> ${esc(t)}</li>`).join('')}</ul>` };
  }
  return { prompt: `${T('Which is grammatically correct?')}${meaning}`, options: opts, answer: opts.indexOf(g.ok), after: [g.ok], reveal: g.ok, detail: why };
}

function grammarPane(pane, w, p) {
  const best = p.grammar_attempts ? T(' Best so far: {a}/{b}.', { a: p.grammar_best, b: p.grammar_total }) : '';
  pane.innerHTML = `<p class="muted">${T('Is it grammatically correct? 10 questions per round in three formats.')}${best}</p>
    <div class="card">
      <div class="muted" style="font-size:.85rem;margin-bottom:6px">${T('Format')}</div>
      <div class="row drill-modes">${Object.entries(FORMATS).map(([k, n]) => `<button class="btn ghost" data-fmt="${k}">${n}</button>`).join('')}</div>
      <div class="muted" style="font-size:.85rem;margin:10px 0 6px">${T('Questions from')}</div>
      <div class="row"><label><input type="radio" name="scope" value="week" checked> ${T('This week only')}</label>
      ${w.week > 1 ? `<label><input type="radio" name="scope" value="review"> ${T('Review weeks 1–{n}', { n: w.week })}</label>` : ''}</div>
    </div>
    <div id="gbox" class="card" hidden style="margin-top:12px"></div>`;
  const box = document.getElementById('gbox');
  pane.querySelectorAll('[data-fmt]').forEach(b => b.onclick = () => {
    const fmt = b.dataset.fmt;
    pane.querySelectorAll('[data-fmt]').forEach(x => x.classList.toggle('active', x === b));
    const review = pane.querySelector('input[name=scope]:checked').value === 'review';
    const pool = shuffle(review ? C.weeks.filter(x => x.week >= 1 && x.week <= w.week).flatMap(x => x.grammar) : w.grammar);
    const label = `${FORMATS[fmt]}${review ? T(' (review)') : ''}`;
    runRound(box, T('Grammar — {l}', { l: label }), i => grammarQuestion(pool[i % pool.length], fmt === 'mixed' ? pick(['mc', 'fix', 'audio']) : fmt),
      (score, missed) => send({ type: 'grammar', week: w.week, label, score, total: 10, missed }, T('Grammar score saved to Obsidian')));
  });
}

// ---------- R Trill Lab ----------
function slowBtn(text) {
  const f = AUDIO['slow:' + text];
  return f ? `<button class="play" data-a="media/${f}" title="${T('Slow')}" aria-label="${T('Slow')}: ${esc(text)}">🐢</button>` : '';
}

function rrLab() {
  const L = C.rr_lab;
  let n = 0;
  const row = t => `<div class="speak-row"><span><span class="speak-text">${esc(t)}</span>${L.say[t] && L.say[t] !== t ? `<div class="say-syl">${esc(L.say[t])}</div>` : ''}</span>
    <span class="row">${playBtn(t)}${slowBtn(t)}<button class="rec" data-i="${n}" title="${T('Record')}">🎙</button><button class="mine" data-i="${n++}" title="${T('Play my recording')}" disabled>${T('▶ Me')}</button></span></div>`;
  app.innerHTML = `
    <div class="muted"><a href="#/">${T('← Home')}</a> · <a href="#/week/0/lesson">${T('Week 0')}</a></div>
    <h1>${T('🌀 R Trill Lab')}</h1>
    <p class="prose">${inline(L.intro)}</p>
    <div class="card"><h2 style="margin-top:0">${T('Your daily 5 minutes')}</h2><ol class="prose">${L.routine.map(r => `<li>${inline(r)}</li>`).join('')}</ol>
      <div class="row vault-only"><select id="tech">${L.techniques.map(t => `<option>${esc(t.name)}</option>`).join('')}<option>${T('Mixed / full routine')}</option></select>
      <input type="number" id="rr-min" value="5" min="1" max="60" style="width:70px"> ${T('min')}
      <button class="btn" id="rr-log">${T('Log today\'s practice')}</button></div>
      <p class="muted" style="margin:8px 0 0;font-size:.85rem">${T('🔊 normal speed · 🐢 slow · 🎙 record yourself · ▶ hear yourself.')}<span class="vault-only">${T(' Logged practice goes to your Obsidian Study Log.')}</span></p></div>
    <h2>${T('Techniques — try them all')}</h2>
    ${L.techniques.map(t => `<div class="card tech"><h3 style="margin-top:0">${esc(t.name)}</h3>
      <p class="muted">${inline(t.why)}</p><ol class="prose">${t.steps.map(x => `<li>${inline(x)}</li>`).join('')}</ol>
      ${t.say.map(row).join('')}</div>`).join('')}
    <h2>${T('Practice ladder')}</h2><p class="muted">${T('Move up a stage when the current one feels easy.')}</p>
    ${L.ladder.map(st => `<div class="card tech"><h3 style="margin-top:0">${esc(st.stage)}</h3>${st.words.map(row).join('')}</div>`).join('')}
    <h2>${T('Tongue twisters')}</h2><div class="card">${L.twisters.map(row).join('')}</div>
    <h2>${T('Troubleshooting')}</h2><div class="card prose">${L.troubleshooting.map(([q, a]) => `<p><strong>${esc(q)}</strong><br>${esc(a)}</p>`).join('')}</div>`;
  wireRecorder(app);
  document.getElementById('rr-log').onclick = async () => {
    const minutes = parseInt(document.getElementById('rr-min').value, 10);
    if (!(minutes > 0)) return toast(T('Enter minutes'));
    await send({ type: 'session', minutes, note: 'R trill practice — ' + document.getElementById('tech').value }, T('Trill practice logged'));
  };
}

function guide(id) {
  const g = (C.guides || []).find(g => g.id === id);
  if (!g) return (location.hash = '#/');
  app.innerHTML = `<div class="muted"><a href="#/">${T('← Home')}</a></div><h1>${g.icon} ${esc(T(g.title))}</h1>
    <p class="muted" style="font-size:.9rem">${T('Tap 🔊 next to any Spanish phrase to hear it.')}</p><div class="prose">${md(g.md)}</div>`;
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

// One Vocabulary Bank word, w = [English, Spanish, what to say instead, "spain"|"also"], sorted out for display:
// es = the word to learn (Latin American first), other = the Spain-side word Quizlet gave, if any. null-safe for odd rows.
function bankWord(w) {
  const [en, es, instead, kind] = w;
  if (/^— vulgar/.test(instead || '')) return { es, en, clip: spoken(es), lang: 'es-ES', vulgar: true, add: '' };
  if (instead) {
    const add = instead.replace(/\s*\(.*$/, '');
    return { es: instead, en, clip: spoken(instead), other: es, kind: kind === 'also' ? 'also' : 'spain', rude: /\bcoger\b/.test(es), add };
  }
  const m = es.match(LATAM_TAG);
  if (m) return { es: m[1], en, clip: spoken(m[1]), other: m[2], kind: 'spain', add: spoken(m[1]) };
  return { es, en, clip: spoken(es), add: es };
}
const today = () => new Date().toLocaleDateString('en-CA');  // YYYY-MM-DD, local time
const isKnown = b => ((state && state.flash) || {})[b.es]?.box >= 2;

function bankCard(w, topic, extra = '') {
  const b = bankWord(w), pills = [];
  if (b.other) pills.push(b.kind === 'also'
    ? `<span class="pill latam">${T('🌎 also Latin America: ')}${esc(b.other)} ${sayBtn(spoken(b.other))}</span>`
    : `<span class="pill spain">${T('🇪🇸 Spain: ')}${esc(b.other)} ${sayBtn(spoken(b.other), 'es-ES')}</span>`);
  if (b.vulgar) pills.push(`<span class="pill spain">${T('🇪🇸 Spain')}</span><span class="pill tip">${T('🔞 vulgar')}</span>`);
  if (b.rude) pills.push(`<span class="pill tip">${T('⚠️ rude in Mexico')}</span>`);
  if (isKnown(b)) pills.push(`<span class="pill known">${T('✅ known')}</span>`);
  const add = b.add ? `<button class="add vault-only" data-es="${attr(b.add)}" data-en="${attr(b.en)}" data-topic="${attr(topic)}" title="${T('Add to my Vocab')}">➕</button>` : '';
  return `<div class="wcard${b.vulgar ? ' dim' : ''}"><div class="es">${artWord(b.es)} ${sayBtn(b.clip, b.lang)}</div><div class="en">${esc(b.en)}</div>
    ${pills.length || extra ? `<div class="pills">${pills.join('')}${extra}</div>` : ''}${add}</div>`;
}
const bankGrid = (words, topic) => `<div class="wgrid">${words.map(w => bankCard(w, topic)).join('')}</div>`;

app.addEventListener('click', e => {
  const b = e.target.closest('button.add');
  if (b) send({ type: 'vocab', es: b.dataset.es, en: b.dataset.en, topic: b.dataset.topic }, T('Added “{w}” to Vocab', { w: b.dataset.es }));
});

async function vocab(id) {
  app.innerHTML = `<p class="muted">${T('Loading vocabulary…')}</p>`;
  let Q;
  try { Q = await loadQuizlet(); } catch { app.innerHTML = `<p>${T('Couldn\'t load the vocabulary list.')}</p>`; return; }
  const count = f => f.sets.reduce((a, s) => a + s.words.length, 0);
  const total = Q.reduce((a, f) => a + count(f), 0);
  const f = Q.find(f => f.id === id);
  const head = `<p class="muted wintro">${T('From the Quizlet class “Mastering Spanish Vocabulary”. The Latin American word comes first —')}
      <span class="pill spain">${T('🇪🇸 Spain')}</span> ${T('or')} <span class="pill latam">${T('🌎 also Latin America')}</span> ${T('shows the word Quizlet gave.')}
      <span class="art m">el / los</span> <span class="art f">la / las</span><span class="vault-only">${T(' · ➕ adds to My Notes/Vocab.md')}</span></p>
    <div class="wtools"><input type="search" id="vq" placeholder="${T('Search English or Spanish…')}"></div>`;
  if (!f) {
    app.innerHTML = `<div class="muted"><a href="#/">${T('← Home')}</a></div><h1>${T('📚 Vocabulary Bank')}</h1>${head}
      <div id="vres"></div>
      <div class="grid" id="vgrid">${Q.map(f => `<a class="card week-card" href="#/vocab/${f.id}">
        <div class="num">${T('{n} words', { n: count(f) })}</div><div class="t">${f.id}. ${esc(f.title)}</div></a>`).join('')}</div>
      <p class="muted" style="font-size:.9rem">${T('{n} words in {m} topics.', { n: total.toLocaleString(), m: Q.length })}</p>`;
    const all = Q.flatMap(f => f.sets.flatMap(s => s.words.map(w => ({ w, f, key: fold(w.join(' ')) }))));
    document.getElementById('vq').oninput = e => {
      const q = fold(e.target.value.trim());
      document.getElementById('vgrid').hidden = !!q;
      const hits = q ? all.filter(x => x.key.includes(q)) : [];
      document.getElementById('vres').innerHTML = !q ? '' : !hits.length ? `<p class="muted">${T('No matches.')}</p>`
        : `${hits.length > 200 ? `<p class="muted">${T('Showing 200 of {n} — keep typing to narrow it down.', { n: hits.length })}</p>` : ''}
          <div class="wgrid">${hits.slice(0, 200).map(x => bankCard(x.w, x.f.title, `<a class="pill tip" href="#/vocab/${x.f.id}">${esc(x.f.title)}</a>`)).join('')}</div>`;
    };
    return;
  }
  const i = Q.indexOf(f), prev = Q[i - 1], next = Q[i + 1];
  const summary = (s, k) => {
    const words = s.words.map(bankWord), known = words.filter(isKnown).length;
    return `<span class="vt">${esc(s.title)}</span>
      <span class="vcount">${T('{n} words', { n: s.words.length })}${known ? T(' · ✅ {k} known', { k: known }) : ''}</span>
      <button class="btn ghost" data-flash="${k}">${T('🎴 Flashcards')}</button>`;
  };
  app.innerHTML = `<div class="muted"><a href="#/">${T('← Home')}</a> · <a href="#/vocab">${T('📚 Vocabulary Bank')}</a></div>
    <h1>${f.id}. ${esc(f.title)}</h1>${head}
    <div class="row vtop"><button class="btn" data-flash="all">${T('🎴 Flashcards: whole topic')}</button>
      <button class="btn ghost" id="vopen">${T('Open all')}</button></div>
    <div id="vres"></div>
    <div id="vbody">${f.sets.map((s, k) => `<details class="vset" data-k="${k}"><summary>${summary(s, k)}</summary><div class="vgrid-slot"></div></details>`).join('')}</div>
    <div class="row" style="justify-content:space-between;margin-top:16px">
      ${prev ? `<a class="btn ghost" href="#/vocab/${prev.id}">← ${esc(prev.title)}</a>` : '<span></span>'}
      ${next ? `<a class="btn ghost" href="#/vocab/${next.id}">${esc(next.title)} →</a>` : ''}</div>`;
  const body = document.getElementById('vbody');
  const fill = d => { const slot = d.querySelector('.vgrid-slot'); if (!slot.innerHTML) slot.innerHTML = bankGrid(f.sets[+d.dataset.k].words, f.title); };
  const refresh = () => body.querySelectorAll('.vset').forEach(d => {  // after flashcards: update ✅ counts and card badges
    d.querySelector('summary').innerHTML = summary(f.sets[+d.dataset.k], d.dataset.k);
    const slot = d.querySelector('.vgrid-slot');
    if (slot.innerHTML) { slot.innerHTML = ''; fill(d); }
  });
  body.addEventListener('toggle', e => { if (e.target.open) fill(e.target); }, true);
  app.querySelector('.vtop').onclick = body.onclick = e => {
    const fb = e.target.closest('[data-flash]');
    if (!fb) return;
    e.preventDefault();  // a button inside <summary> would otherwise also open/close the set
    const k = fb.dataset.flash;
    const cards = (k === 'all' ? f.sets.flatMap(s => s.words) : f.sets[+k].words).map(bankWord);
    flashcards(k === 'all' ? f.title : `${f.title} › ${f.sets[+k].title}`, cards, refresh);
  };
  let allOpen = false;
  document.getElementById('vopen').onclick = e => {
    allOpen = !allOpen;
    body.querySelectorAll('.vset').forEach(d => { d.open = allOpen; });
    e.target.textContent = allOpen ? T('Close all') : T('Open all');
  };
  document.getElementById('vq').oninput = e => {
    const q = fold(e.target.value.trim());
    body.hidden = !!q;
    const hits = q ? f.sets.flatMap(s => s.words).filter(w => fold(w.join(' ')).includes(q)) : [];
    document.getElementById('vres').innerHTML = !q ? '' : hits.length ? bankGrid(hits, f.title) : `<p class="muted">${T('No matches.')}</p>`;
  };
}

// 🎴 Flashcards: up to 20 cards, words that are due first. Tap (or Space) to flip, then "Still learning" / "I know it"
// (keys 1 / 2, or swipe left / right). Missed cards come back once at the end of the round. Results go to the vault.
function flashcards(title, cards, onDone) {
  const F = (state && state.flash) || {};
  const pool = cards.filter(b => b && !b.vulgar);
  const due = pool.filter(b => !F[b.es] || (F[b.es].due || '') <= today());
  const deck = shuffle(due.length ? due : pool).slice(0, 20).map(b => ({ b, again: false }));
  const results = new Map();
  let i = 0, flipped = false, enFirst = false;
  try { enFirst = localStorage.getItem('flash-en-first') === '1'; } catch {}
  const ov = document.createElement('div');
  ov.className = 'flash-ov';
  ov.innerHTML = `<div class="flash-box" role="dialog" aria-label="${T('Flashcards')}">
    <div class="flash-top"><b>${esc(title)}</b><button class="fc-x" title="${T('Close (Esc)')}">✕</button></div>
    <div class="flash-bar"><div></div></div><div class="flash-n muted"></div>
    <div class="fcard" tabindex="0"><div class="fin"><div class="face front"></div><div class="face back"></div></div></div>
    <div class="fc-btns"><button class="btn ghost" data-r="0">${T('😕 Still learning')}</button><button class="btn" data-r="1">${T('✅ I know it')}</button></div>
    <div class="flash-foot muted"><label><input type="checkbox" id="fc-en"${enFirst ? ' checked' : ''}> ${T('English first')}</label>
      <span>${T('Space flip · 1 still learning · 2 know it')}</span></div>
    ${due.length ? '' : `<p class="muted" style="text-align:center;margin:4px 0 0">${T('Nothing due — practicing the whole set.')}</p>`}</div>`;
  document.body.appendChild(ov);
  const $ = q => ov.querySelector(q), card = $('.fcard');
  const sideEs = b => `<div class="big">${artWord(b.es)}</div>${sayBtn(b.clip)}`;
  const sideEn = b => `<div class="big en">${esc(b.en)}</div>${b.other ? `<div class="pills"><span class="pill ${b.kind === 'also' ? 'latam' : 'spain'}">${b.kind === 'also' ? T('🌎 also Latin America') : T('🇪🇸 Spain')}: ${esc(b.other)}</span></div>` : ''}${b.note ? `<div class="pills">${notePills(b.note)}</div>` : ''}`;
  const show = () => {
    const { b } = deck[i];
    flipped = false;
    card.classList.remove('flipped', 'go-l', 'go-r');
    $('.front').innerHTML = (enFirst ? sideEn(b) : sideEs(b)) + `<div class="hint">${T('tap to flip')}</div>`;
    $('.back').innerHTML = enFirst ? sideEs(b) : sideEn(b);
    $('.fc-btns').classList.remove('on');
    $('.flash-n').textContent = `${i + 1} / ${deck.length}`;
    $('.flash-bar div').style.width = `${100 * i / deck.length}%`;
    card.focus({ preventScroll: true });
  };
  const flip = () => {
    flipped = !flipped;
    card.classList.toggle('flipped', flipped);
    $('.fc-btns').classList.toggle('on', flipped);
    if (flipped && enFirst) $('.back .play')?.click();  // hear the Spanish as it's revealed
  };
  const answer = known => {
    if (!flipped) return;
    const c = deck[i];
    if (!results.has(c.b.es)) results.set(c.b.es, { es: c.b.es, en: c.b.en, known });  // first answer is what counts
    if (!known && !c.again) deck.push({ b: c.b, again: true });
    card.classList.add(known ? 'go-r' : 'go-l');
    setTimeout(() => (++i < deck.length ? show() : finish()), 180);
  };
  const close = () => { document.removeEventListener('keydown', key); ov.remove(); };
  const finish = async () => {
    const r = [...results.values()], knew = r.filter(x => x.known).length, still = r.filter(x => !x.known);
    $('.flash-bar div').style.width = '100%';
    $('.flash-box').innerHTML = `<div class="flash-top"><b>${esc(title)}</b><button class="fc-x">✕</button></div>
      <div class="fdone"><div class="big">${knew === r.length ? '🎉' : '💪'} ${knew} / ${r.length}</div><p class="muted">${T('you knew on the first try')}</p>
      ${still.length ? `<div class="fstill"><b>${T('Still learning')}</b>${still.map(x => `<div>${esc(x.es)} — <span class="muted">${esc(x.en)}</span></div>`).join('')}</div>` : ''}
      <div class="row" style="justify-content:center"><button class="btn" id="fc-again">${T('Another round')}</button><button class="btn ghost fc-x">${T('Done')}</button></div></div>`;
    $('#fc-again').onclick = () => { close(); flashcards(title, cards, onDone); };
    ov.querySelectorAll('.fc-x').forEach(b => b.onclick = close);
    await send({ type: 'flash', set: title, results: r }, PUBLIC ? '' : T('Flashcards saved to Obsidian'));
    onDone && onDone();
  };
  const key = e => {
    if (e.key === 'Escape') return close();
    if (!$('.fcard')) return;
    if (e.key === ' ' || e.key === 'Enter') { e.preventDefault(); flip(); }
    else if (e.key === '1' || e.key === 'ArrowLeft') answer(false);
    else if (e.key === '2' || e.key === 'ArrowRight') answer(true);
  };
  document.addEventListener('keydown', key);
  ov.onclick = e => { if (e.target === ov || e.target.closest('.fc-x')) close(); };
  card.onclick = e => { if (swiped) swiped = false; else if (!e.target.closest('.play')) flip(); };
  ov.querySelectorAll('[data-r]').forEach(b => b.onclick = () => answer(b.dataset.r === '1'));
  $('#fc-en').onchange = e => { enFirst = e.target.checked; try { localStorage.setItem('flash-en-first', enFirst ? '1' : '0'); } catch {} show(); };
  let x0 = null, swiped = false;  // swipe on phones, once the card is flipped
  card.onpointerdown = e => { x0 = e.clientX; };
  card.onpointerup = e => { if (x0 !== null && flipped && Math.abs(e.clientX - x0) > 70) { swiped = true; answer(e.clientX > x0); } x0 = null; };
  show();
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
// 🇲🇽 / 🇺🇸 switch in the header (i18n.js); also translates the bits of index.html
document.documentElement.lang = LANG;
document.title = T('Spanish Course');
document.querySelector('.brand span').textContent = T('· Latin American Spanish');
{
  const b = document.getElementById('lang');
  b.textContent = LANG === 'es' ? '🇺🇸 English' : '🇲🇽 Español';
  b.title = LANG === 'es' ? 'Switch the site to English' : 'Cambiar el sitio a español';
  b.onclick = () => setLang(LANG === 'es' ? 'en' : 'es');
}
loadState().then(route);
