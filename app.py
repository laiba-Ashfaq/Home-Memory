import os, io, html
from datetime import datetime
import streamlit as st
from PIL import Image
import core

st.set_page_config(page_title="HomeMemory", page_icon=":material/home:")
os.makedirs("uploads", exist_ok=True)
ss = st.session_state
for k, v in {"dark": False, "mood": "idle", "msg": None, "chat": []}.items():
    ss.setdefault(k, v)
NAME = "friend"  # change to your name

LIGHT = dict(bg="#EDE4F1", bg2="#F9E9EE", surface="#FBF8FD", s2="#F0E7F6", text="#2A2133", muted="#7C6F8A",
             p="#7A5AA6", p2="#A783D4", accent="#2FB8A3", border="#E2D6EA", shadow="rgba(90,60,130,.14)")
DARK = dict(bg="#16111E", bg2="#1E1830", surface="#201A2C", s2="#2B2339", text="#F2EBFA", muted="#A99DB8",
            p="#B59AEA", p2="#7A5AA6", accent="#4FD6C0", border="#33293F", shadow="rgba(0,0,0,.5)")
P = DARK if ss.dark else LIGHT

CSS = """
.stApp{background:radial-gradient(900px 500px at 0% -10%,var(--bg2),transparent 60%),var(--bg);}
#MainMenu,footer,[data-testid="stToolbar"],[data-testid="stDecoration"]{display:none}
[data-testid="stHeader"]{background:transparent}
.block-container{max-width:860px;padding-top:1rem;padding-bottom:4rem}
.stApp,.stApp p,.stApp label,.stApp span,.stApp li,.stApp h1,.stApp h2,.stApp h3{color:var(--text)}
.stApp,.stApp p,.stApp label,.stApp li,.stApp h1,.stApp h2,.stApp h3,.stApp input,.stApp textarea,.stApp button{font-family:'Trebuchet MS','Segoe UI',system-ui,sans-serif}
[data-testid="stIconMaterial"]{font-family:'Material Symbols Rounded'!important}
.stTabs [role="tablist"]{gap:14px!important;background:var(--surface)!important;padding:8px 10px!important;border-radius:999px!important;border:1px solid var(--border)!important;box-shadow:0 6px 20px var(--shadow);overflow-x:auto}
.stApp [role="tab"]{border-radius:999px!important;padding:10px 24px!important;margin:0!important;height:auto!important;background:transparent!important;border:0!important;border-bottom:0!important;box-shadow:none!important;transition:all .2s}
.stApp [role="tab"]:hover{background:var(--s2)!important}
.stApp [role="tab"][aria-selected="true"]{background:linear-gradient(135deg,var(--p),var(--p2))!important;box-shadow:0 8px 20px var(--shadow)!important;transform:translateY(-1px)}
.stApp [role="tab"][aria-selected="true"],.stApp [role="tab"][aria-selected="true"] *{color:#fff!important}
.stApp [role="tab"] p{margin:0!important;font-weight:600}
.stApp [data-baseweb="tab-highlight"],.stApp [data-baseweb="tab-border"],.stApp [role="tablist"]>div[aria-hidden="true"]{display:none!important;height:0!important;background:transparent!important}
.stButton>button,.stFormSubmitButton>button{background:linear-gradient(135deg,var(--p),var(--p2));border:0;border-radius:14px;padding:.55rem 1.3rem;box-shadow:0 8px 20px var(--shadow)}
.stButton>button p,.stFormSubmitButton>button p{color:#fff!important;font-weight:600}
.stTextInput input,.stTextArea textarea,[data-baseweb="select"]>div{background:var(--surface)!important;color:var(--text)!important;border:1px solid var(--border)!important;border-radius:14px!important}
[data-testid="stFileUploader"] section{background:var(--surface);border:2px dashed var(--p2);border-radius:18px}
[data-testid="stFileUploader"] section *{color:var(--text)!important}
[data-testid="stFileUploader"] button{background:linear-gradient(135deg,var(--p),var(--p2))!important;border:0!important;border-radius:12px!important}
[data-testid="stFileUploader"] button,[data-testid="stFileUploader"] button *{color:#fff!important}
[data-baseweb="input"],[data-baseweb="base-input"],[data-baseweb="textarea"]{background:var(--surface)!important;border-radius:14px!important}
.stTextInput input,.stTextArea textarea{-webkit-text-fill-color:var(--text)!important;caret-color:var(--text)}
.stTextInput input::placeholder,.stTextArea textarea::placeholder{color:var(--muted)!important;-webkit-text-fill-color:var(--muted)!important;opacity:1}
.stTextInput input:focus,.stTextArea textarea:focus{border-color:var(--p2)!important;box-shadow:0 0 0 3px var(--shadow)!important}
.card{background:var(--surface);border:1px solid var(--border);border-radius:22px;padding:16px 20px;box-shadow:0 10px 30px var(--shadow);margin-bottom:12px}
.hero{display:flex;align-items:center;gap:18px;flex-wrap:wrap}
.card.hero h1{margin:0;font-family:'Fredoka','Trebuchet MS',sans-serif;font-weight:700;font-size:2.5rem;letter-spacing:.5px;color:var(--p);line-height:1.1}
.speech{margin-top:8px;display:inline-block;background:var(--s2);border:1px solid var(--border);padding:9px 14px;border-radius:16px 16px 16px 4px}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px;margin:6px 0 12px}
.grid .card{margin:0}.n{font-family:'Fredoka','Trebuchet MS',sans-serif;font-size:2.2rem;font-weight:700;color:var(--p)}.l{color:var(--muted);font-size:.85rem}
.chip{display:inline-block;padding:4px 12px;border-radius:999px;background:var(--s2);border:1px solid var(--border);margin:3px;font-size:.82rem}
.bubble{padding:11px 16px;border-radius:18px;margin:8px 0;max-width:88%;line-height:1.5;border:1px solid var(--border);width:fit-content}
.bubble.user{margin-left:auto;background:linear-gradient(135deg,var(--p),var(--p2));color:#fff;border-bottom-right-radius:5px}
.bubble.bot{background:var(--surface);border-bottom-left-radius:5px;box-shadow:0 6px 18px var(--shadow)}
.dots{display:inline-flex;gap:5px;padding:5px 2px}.dots i{width:9px;height:9px;border-radius:50%;background:var(--accent);animation:bn 1.2s infinite ease-in-out}
.dots i:nth-child(2){animation-delay:.15s}.dots i:nth-child(3){animation-delay:.3s}
@keyframes bn{0%,60%,100%{transform:translateY(0);opacity:.4}30%{transform:translateY(-7px);opacity:1}}
.pill{padding:3px 10px;border-radius:999px;font-size:.8rem;font-weight:700}
.pill.red{background:rgba(230,70,90,.18);color:#e0455a}.pill.amber{background:rgba(240,170,60,.2);color:#c98412}.pill.green{background:rgba(47,184,163,.2);color:#1f9482}
.memo{width:118px;height:138px;flex:none}.memo .body{animation:fl 3s ease-in-out infinite}
@keyframes fl{0%,100%{transform:translateY(0)}50%{transform:translateY(-6px)}}
.memo .eye{transform-box:fill-box;transform-origin:center;animation:bk 4s infinite}
@keyframes bk{0%,92%,100%{transform:scaleY(1)}95%{transform:scaleY(.1)}}
.memo .ant{animation:gl 2s infinite}@keyframes gl{0%,100%{opacity:1}50%{opacity:.35}}
.memo .arm{transform-box:fill-box;transform-origin:left center}
.memo.idle .arm{animation:wv 1.4s ease-in-out 3}
@keyframes wv{0%,100%{transform:rotate(0)}30%{transform:rotate(-40deg)}60%{transform:rotate(15deg)}}
.memo.thinking .eyes{animation:lk 1.2s infinite}.memo.thinking .ant{animation:gl .5s infinite}
@keyframes lk{0%,100%{transform:translateX(-3px)}50%{transform:translateX(3px)}}
.memo.happy .body{animation:jp .6s ease 3}@keyframes jp{0%,100%{transform:translateY(0)}40%{transform:translateY(-16px)}}
.memo.happy .mouth{transform-box:fill-box;transform-origin:center;transform:scaleY(1.7)}
.memo.confused .body{transform-origin:60px 126px;animation:tl 1.2s ease-in-out infinite}
@keyframes tl{0%,100%{transform:rotate(-4deg)}50%{transform:rotate(4deg)}}
.memo.confused .mouth{transform-box:fill-box;transform-origin:center;transform:scaleY(-1)}
@media (prefers-reduced-motion:reduce){.memo *,.dots i{animation:none!important}}
"""


def M(s):
    return " ".join(x.strip() for x in s.splitlines() if x.strip())


def show(s, target=st):
    target.markdown(M(s), unsafe_allow_html=True)


def esc(t):
    return html.escape(str(t)).replace("$", "&#36;").replace("\n", "<br>")


def robot(mood):
    f = lambda c: f'style="fill:var(--{c})"'
    return f'''<svg class="memo {mood}" viewBox="0 0 120 140"><ellipse cx="60" cy="133" rx="26" ry="5" style="fill:rgba(0,0,0,.15)"/>
<g class="body"><line x1="60" y1="18" x2="60" y2="32" style="stroke:var(--p);stroke-width:4;stroke-linecap:round"/>
<circle class="ant" cx="60" cy="14" r="6" {f("accent")}/><rect x="22" y="30" width="76" height="62" rx="26" {f("p")}/>
<rect x="30" y="38" width="60" height="46" rx="20" {f("surface")}/>
<g class="eyes"><ellipse class="eye" cx="48" cy="60" rx="6" ry="8" {f("text")}/><ellipse class="eye" cx="72" cy="60" rx="6" ry="8" {f("text")}/></g>
<circle cx="40" cy="72" r="5" fill="#FF9DB5" opacity=".6"/><circle cx="80" cy="72" r="5" fill="#FF9DB5" opacity=".6"/>
<path class="mouth" d="M52 73 Q60 81 68 73" style="stroke:var(--text);stroke-width:3;fill:none;stroke-linecap:round"/>
<rect x="38" y="96" width="44" height="30" rx="14" {f("p2")}/><circle cx="60" cy="111" r="5" {f("accent")}/>
<rect class="arm" x="22" y="102" width="16" height="8" rx="4" {f("p")}/><rect class="arm" x="82" y="102" width="16" height="8" rx="4" {f("p")}/></g></svg>'''


MSG = {"idle": f"Hi {NAME}! I'm Memo. Show me something and I'll remember where it lives.",
       "thinking": "Hmm, let me think...", "happy": "Done! Anything else to remember?",
       "confused": "I couldn't find that. Try adding it first!"}


def hero(mood, msg=None):
    return f'<div class="card hero">{robot(mood)}<div><h1>HomeMemory</h1><div class="speech">{esc(msg or MSG[mood])}</div></div></div>'


def bubble(role, text):
    return f'<div class="bubble {role}">{esc(text)}</div>'


DOTS = '<div class="bubble bot"><div class="dots"><i></i><i></i><i></i></div></div>'

show("<style>@import url('https://fonts.googleapis.com/css2?family=Fredoka:wght@500;700&display=swap');:root{color-scheme:" + ("dark" if ss.dark else "light") + ";" + "".join(f"--{k}:{v};" for k, v in P.items()) + "}" + CSS + "</style>")
_, tg = st.columns([4, 2])
tg.button(":material/light_mode: Light" if ss.dark else ":material/dark_mode: Dark", key="theme_btn", on_click=lambda: ss.update(dark=not ss.dark))
slot = st.empty()
show(hero(ss.mood, ss.msg), slot)
ss.mood, ss.msg = "idle", None
t_home, t_add, t_ask, t_due = st.tabs([":material/home: Home", ":material/add_a_photo: Add", ":material/chat: Ask", ":material/schedule: Due soon"])

with t_home:
    s = core.stats()
    show(f'<div class="grid"><div class="card"><div class="n">{s["total"]}</div><div class="l">things remembered</div></div>'
         f'<div class="card"><div class="n">{s["soon"]}</div><div class="l">expiring in 60 days</div></div>'
         f'<div class="card"><div class="n">{len(s["cats"])}</div><div class="l">categories</div></div></div>')
    if s["cats"]:
        show('<div class="card"><b>Browse by type</b><br>' + "".join(f'<span class="chip">{esc(c["_id"])} · {c["n"]}</span>' for c in s["cats"]) + "</div>")
    else:
        show('<div class="card">Nothing here yet. Open <b>Add</b> and show Memo your first thing.</div>')
    rec = core.recent(6)
    cols = st.columns(3)
    for i, d in enumerate(rec):
        with cols[i % 3]:
            if os.path.exists(d.get("image_path", "")):
                st.image(d["image_path"])
            show(f'<div class="card"><b>{esc(d["item"])}</b><br><span class="l">{esc(d.get("user_note",""))}</span></div>')
            if st.button(":material/delete: Delete", key=f"del_{d['_id']}"):
                core.delete(str(d["_id"]))
                st.rerun()

with t_add:
    up = st.file_uploader("Photo (camera or gallery)", type=["jpg", "jpeg", "png"])
    note = st.text_input("Short note", placeholder="spare keys, top drawer, bedroom")
    if up and st.button(":material/auto_awesome: Read photo"):
        img = Image.open(up).convert("RGB")
        img.thumbnail((1024, 1024))
        buf = io.BytesIO()
        img.save(buf, "JPEG")
        path = f"uploads/{datetime.now():%Y%m%d_%H%M%S}.jpg"
        img.save(path)
        show(hero("thinking", "Reading your photo..."), slot)
        wait = st.empty()
        show(DOTS, wait)
        ss.fields, ss.path, ss.note = core.extract(buf.getvalue(), note), path, note
        wait.empty()
        ss.mood, ss.msg = "happy", "Got it! Check the details below."
        st.rerun()
    if "fields" in ss:
        f = ss.fields
        st.image(ss.path, width=240)
        cat = f.get("category") if f.get("category") in core.CATEGORIES else "other"
        f["category"] = st.selectbox("Category", core.CATEGORIES, index=core.CATEGORIES.index(cat))
        f["item"] = st.text_input("Item", f.get("item", ""))
        f["location_hint"] = st.text_input("Where is it?", f.get("location_hint") or ss.note)
        f["text_found"] = st.text_area("Text found (numbers, Wi-Fi name...)", f.get("text_found", ""))
        f["expiry_date"] = st.text_input("Expiry date (YYYY-MM-DD, optional)", f.get("expiry_date", ""))
        if st.button(":material/check_circle: Save to memory"):
            core.save(f, ss.note, ss.path)
            del ss["fields"]
            ss.mood, ss.msg = "happy", "Saved! I'll remember that."
            st.rerun()

with t_ask:
    with st.form("ask_form", clear_on_submit=True):
        q = st.text_input("Ask Memo", placeholder="Where are my spare keys?")
        go = st.form_submit_button(":material/send: Ask")
    if go and q.strip():
        show(hero("thinking", "Searching my memory..."), slot)
        pending = st.empty()
        show(bubble("user", q) + DOTS, pending)
        try:
            ans, hits = core.ask(q)
        except Exception as e:
            pending.empty()
            st.error(f"Search failed: {e}. Check Ollama is running and the Atlas vector index is Active.")
            st.stop()
        top = hits[0] if hits else {}
        ss.chat.append({"q": q, "a": ans or "I couldn't find that yet. Add it with a photo and a short note.",
                        "img": top.get("image_path"), "score": top.get("score")})
        ss.mood = "happy" if ans else "confused"
        ss.msg = None
        st.rerun()
    for m in reversed(ss.chat):
        show(bubble("user", m["q"]) + bubble("bot", m["a"]))
        if m["score"]:
            show(f'<span class="chip">match {m["score"]:.0%}</span>')
        if m["img"] and os.path.exists(m["img"]):
            st.image(m["img"], width=220, caption="Source photo")

with t_due:
    days = st.slider("Show items expiring within (days)", 7, 365, 60)
    items = core.due_soon(days)
    if not items:
        show('<div class="card">Nothing expiring soon. Memo will flag medicines and documents here.</div>')
    for d in items:
        left = (d["expiry_date"] - datetime.now()).days
        cls, tag = ("red", "Expired") if left < 0 else (("amber", f"{left} days left") if left < 30 else ("green", f"{left} days left"))
        show(f'<div class="card"><b>{esc(d["item"])}</b> <span class="chip">{esc(d["category"])}</span> '
             f'<span class="pill {cls}">{tag}</span><br><span class="l">Expires {d["expiry_date"]:%d %b %Y}</span></div>')
