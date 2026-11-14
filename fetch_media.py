#!/usr/bin/env python3
"""Download photos (Wikimedia Commons) and generate audio (Microsoft neural TTS, es-MX)
into the vault's Media/ folder, and record everything in media.json.

    .venv/bin/python fetch_media.py images              # download chosen photos
    .venv/bin/python fetch_media.py candidates [week]   # contact sheets of top results to review
    .venv/bin/python fetch_media.py audio               # generate missing audio clips
Then run: python3 build.py --force
"""
import asyncio
import hashlib
import html
import json
import re
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

from build import COURSE, REFERENCE, VAULT, daily_words, drill_texts, grammar_texts, rr_texts, spell_texts

HERE = Path(__file__).resolve().parent
MEDIA = VAULT / "Media"
MANIFEST = HERE / "media.json"
UA = "SpanishCourseLocal/1.0 (personal study site; contact: local)"
VOICE, RATE = "es-MX-DaliaNeural", "-10%"
API = "https://commons.wikimedia.org/w/api.php"


def load_manifest():
    return json.loads(MANIFEST.read_text()) if MANIFEST.exists() else {"images": {}, "audio": {}}


def save_manifest(m):
    MANIFEST.write_text(json.dumps(m, ensure_ascii=False, indent=1), encoding="utf-8")


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    for attempt in range(6):
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                data = r.read()
            time.sleep(0.5)  # be polite to Wikimedia
            return data
        except urllib.error.HTTPError as e:
            if e.code != 429 or attempt == 5:
                raise
            time.sleep(5 * (attempt + 1))


def commons(params, width=960):
    # Wikimedia only serves standard thumbnail widths cheaply (see https://w.wiki/GHai)
    params = {"action": "query", "format": "json", "prop": "imageinfo",
              "iiprop": "url|extmetadata|mime|size", "iiurlwidth": width, **params}
    pages = json.loads(get(API + "?" + urllib.parse.urlencode(params))).get("query", {}).get("pages", {})
    pages = sorted(pages.values(), key=lambda p: p.get("index", 0))
    return [p for p in pages if p.get("imageinfo") and p["imageinfo"][0]["mime"] in ("image/jpeg", "image/png", "image/webp")]


def search(q, n, width=960):
    return commons(width=width, params={"generator": "search", "gsrsearch": f"{q} filetype:bitmap", "gsrnamespace": 6, "gsrlimit": n * 3})[:n]


def by_title(title, width=960):
    return commons({"titles": title}, width)


def strip_html(s):
    return html.unescape(re.sub(r"<[^>]+>", "", s or "")).strip()


def save_image(page, key):
    info = page["imageinfo"][0]
    meta = info.get("extmetadata", {})
    out = MEDIA / "img" / f"{key}.jpg"
    out.parent.mkdir(parents=True, exist_ok=True)
    raw = out.with_suffix(".src")
    url = info["thumburl"]
    if info.get("width", 10**6) <= 960:  # small original: use the largest standard thumbnail below it
        width = next(w for w in (500, 330, 250, 120) if w < info["width"])
        url = by_title(page["title"], width)[0]["imageinfo"][0]["thumburl"]
    raw.write_bytes(get(url))
    subprocess.run(["magick", str(raw), "-resize", "800x600>", "-quality", "82", str(out)], check=True)
    raw.unlink()
    return {"file": f"img/{key}.jpg", "title": page["title"], "source": info["descriptionurl"],
            "artist": strip_html(meta.get("Artist", {}).get("value"))[:120] or "Unknown",
            "license": strip_html(meta.get("LicenseShortName", {}).get("value")) or "see source"}


def images():
    m = load_manifest()
    pins = json.loads((HERE / "photo_pins.json").read_text()) if (HERE / "photo_pins.json").exists() else {}
    for w in COURSE:
        for i, ph in enumerate(w["photos"]):
            key = f"{w['id']}-{i + 1}"
            want = pins.get(key) or ph.get("pin")
            have = m["images"].get(key)
            if have and have.get("query") == ph["q"] and (not want or have["title"] == want):
                continue
            pages = by_title(want) if want else search(ph["q"], 1)
            if not pages:
                print(f"  ✗ {key}: no result for {want or ph['q']!r}")
                continue
            m["images"][key] = {**save_image(pages[0], key), "query": ph["q"]}
            print(f"  ✓ {key}: {pages[0]['title']}")
            save_manifest(m)


def candidates(week=None):
    """Contact sheet per week: top 4 Commons results per photo, labeled, for picking pins."""
    out_dir = HERE / "candidates"
    out_dir.mkdir(exist_ok=True)
    for w in COURSE:
        if week and w["week"] != week:
            continue
        tiles = []
        pins = json.loads((HERE / "photo_pins.json").read_text()) if (HERE / "photo_pins.json").exists() else {}
        for i, ph in enumerate(w["photos"]):
            if f"{w['id']}-{i + 1}" in pins:  # already chosen
                continue
            for j, page in enumerate(search(ph["q"], 4, width=330)):
                f = out_dir / f"{w['id']}-{i + 1}-{j}.jpg"
                f.write_bytes(get(page["imageinfo"][0]["thumburl"]))
                tiles += ["-label", f"{i + 1}.{j} {page['title'][5:40]}", str(f)]
                (out_dir / f"{w['id']}-{i + 1}-{j}.txt").write_text(page["title"])
        if not tiles:
            continue
        sheet = out_dir / f"sheet-{w['id']}.jpg"
        subprocess.run(["montage", *tiles, "-tile", "4x", "-geometry", "260x195+4+4", "-pointsize", "11", str(sheet)], check=True)
        print(sheet)


# ---------- audio ----------
ITALIC = re.compile(r"(?<!\*)\*(?!\*)([^*\n]+?)\*(?!\*)")


def audio_texts():
    texts = []
    for w in COURSE:
        texts += ITALIC.findall(w["lesson"].replace("**", ""))
        c = w["cyber"] or {"terms": [], "examples": [], "drill": []}
        texts += [es for es, _ in c["terms"]] + [es for es, _ in c["examples"]]
        texts += [it["a"][0] for it in w["worksheet"] + c["drill"]]
        texts += [ph["es"] for ph in w["photos"]] + w.get("speak", []) + [x["es"] for x in w["say_first"]]
    for line in REFERENCE["Classroom Phrases"].splitlines():
        if line.startswith("| ") and not line.startswith("| Español"):
            texts.append(line.split("|")[1].strip())
        texts += ITALIC.findall(line) if line.startswith("- ") else []
    texts += drill_texts() + grammar_texts() + rr_texts() + ["slow:" + t for t in rr_texts()]  # slow versions for hearing the trill
    texts += [x for d in daily_words() for x in (d["es"], d["ex"])]
    seen, out = set(), []
    for t in (t.strip() for t in texts):
        if re.search(r"[a-záéíóúñ]", t, re.I) and t not in seen:
            seen.add(t)
            out.append(t)
    return out


def speakable(t):
    t = re.sub(r"\([^)]*→[^)]*\)", "", t)           # (e→ie) hints
    t = t.replace(" / ", ", ").replace("…", "")
    return re.sub(r"\s+", " ", t).strip(" ,")


def trim_spell_clips(m):
    """Cut leading/trailing silence from letter-name clips so spelled words play back-to-back quickly."""
    done = set(m.get("trimmed", []))
    trim = "silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse,apad=pad_dur=0.08"
    for t in spell_texts():
        f = m["audio"].get(t)
        if not f or f in done:
            continue
        src, tmp = MEDIA / f, MEDIA / (f + ".tmp.mp3")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(src), "-af", trim, str(tmp)], check=True)
        tmp.replace(src)
        done.add(f)
    m["trimmed"] = sorted(done)


async def gen_audio():
    import edge_tts
    m = load_manifest()
    todo = []
    for t in audio_texts():
        name = hashlib.sha1(t.encode()).hexdigest()[:12] + ".mp3"
        m["audio"][t] = f"audio/{name}"
        if not (MEDIA / "audio" / name).exists():
            todo.append((t, MEDIA / "audio" / name))
    (MEDIA / "audio").mkdir(parents=True, exist_ok=True)
    sem = asyncio.Semaphore(6)

    async def one(t, path):
        async with sem:
            for attempt in range(3):
                try:
                    slow = t.startswith("slow:")
                    await edge_tts.Communicate(speakable(t.removeprefix("slow:")), VOICE, rate="-45%" if slow else RATE).save(str(path))
                    return
                except Exception as e:  # network hiccups
                    if attempt == 2:
                        print(f"  ✗ {t!r}: {e}")
                    await asyncio.sleep(2)

    print(f"{len(m['audio'])} clips total, generating {len(todo)}…")
    await asyncio.gather(*(one(t, p) for t, p in todo))
    m["audio"] = {t: f for t, f in m["audio"].items() if (MEDIA / f).exists()}
    trim_spell_clips(m)
    save_manifest(m)
    print(f"done: {len(m['audio'])} clips")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "images":
        images()
    elif cmd == "candidates":
        candidates(int(sys.argv[2]) if len(sys.argv) > 2 else None)
    elif cmd == "audio":
        asyncio.run(gen_audio())
    else:
        print(__doc__)
