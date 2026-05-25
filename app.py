import streamlit as st
import ollama
import speech_recognition as sr
import pdfplumber
import time

st.set_page_config(page_title="Clirix · Your Thinking Layer", page_icon="C", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=JetBrains+Mono:wght@300;400;500&family=Outfit:wght@300;400;500;600&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html, body, [class*="css"], .stApp { font-family: 'Outfit', sans-serif; background-color: #080c14 !important; color: #c8d4e8; height: 100vh; overflow: hidden; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 !important; max-width: 100% !important; overflow: hidden; height: 100vh; }
section[data-testid="stSidebar"] { display: none; }
.stDeployButton, div[data-testid="stToolbar"] { display: none; }
.stTextInput { padding: 0 8px; }
.topbar-container { display: flex; align-items: center; justify-content: space-between; padding: 0 20px; background: #0d1220; border-bottom: 1px solid #1a2540; height: 52px; }
.topbar-logo { display:flex; align-items:center; gap:8px; font-family:'Syne',sans-serif; font-weight:800; font-size:0.95rem; color:#e0eaff; letter-spacing:0.02em; }
.topbar-logo-hex { width:28px; height:28px; background:linear-gradient(135deg,#4f8ef7 0%,#7b5cf0 100%); clip-path:polygon(50% 0%,100% 25%,100% 75%,50% 100%,0% 75%,0% 25%); display:flex; align-items:center; justify-content:center; font-size:0.6rem; color:white; font-weight:700; }
.topbar-title { color:#7a8aaa; font-size:0.78rem; font-weight:400; margin-left:4px; }
.topbar-right { display:flex; align-items:center; gap:16px; }
.topbar-badge { font-family:'JetBrains Mono',monospace; font-size:0.7rem; color:#4f8ef7; background:#0d1e3a; border:1px solid #1e3a6e; border-radius:6px; padding:3px 10px; }
.topbar-avatar { width:28px; height:28px; background:linear-gradient(135deg,#7b5cf0,#4f8ef7); border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:0.65rem; color:white; font-weight:700; }

div[data-testid="column"]:nth-of-type(1) { background:#0a0f1c; border-right:1px solid #131c30; display:flex; flex-direction:column; align-items:center; padding:16px 0; min-height:calc(100vh - 52px); }
div[data-testid="column"]:nth-of-type(1) .stButton > button { width:40px !important; height:40px !important; border-radius:10px !important; display:flex; align-items:center; justify-content:center; font-size:1rem !important; color:#3a4a6a !important; background:transparent !important; border:none !important; transition:all 0.2s !important; padding:0 !important; }
div[data-testid="column"]:nth-of-type(1) .stButton > button:hover { background:#111b30 !important; color:#7ab0ff !important; }
div[data-testid="column"]:nth-of-type(1) .stButton > button[data-testid="baseButton-primary"] { background:#111b30 !important; color:#7ab0ff !important; position:relative; }
div[data-testid="column"]:nth-of-type(1) .stButton > button[data-testid="baseButton-primary"]::before { content:''; position:absolute; left:0; top:10px; bottom:10px; width:3px; background:#4f8ef7; border-radius:0 3px 3px 0; }

.chat-header { padding:14px 20px 10px; border-bottom:1px solid #111b2a; display:flex; align-items:center; gap:10px; }
.chat-header-title { font-family:'Syne',sans-serif; font-size:0.9rem; font-weight:700; color:#d0ddf5; }
.chat-header-sub { font-size:0.72rem; color:#3a4e70; margin-top:1px; }
.doc-pill { margin-left:auto; background:#0d1e3a; border:1px solid #1e3a6e; border-radius:20px; padding:3px 10px 3px 7px; display:flex; align-items:center; gap:5px; font-size:0.7rem; color:#4f8ef7; font-family:'JetBrains Mono',monospace; }

.messages { padding:20px 20px 10px; display:flex; flex-direction:column; gap:16px; min-height:200px; max-height:calc(100vh - 200px); overflow-y:auto; scrollbar-width:thin; scrollbar-color:#1a2540 transparent; }
.messages::-webkit-scrollbar { width:6px; }
.messages::-webkit-scrollbar-track { background:transparent; }
.messages::-webkit-scrollbar-thumb { background:#1a2540; border-radius:3px; }
.msg-row { display:flex; gap:10px; align-items:flex-start; }
.msg-row.user { flex-direction:row-reverse; }
.msg-avatar { width:30px; height:30px; border-radius:8px; display:flex; align-items:center; justify-content:center; font-size:0.7rem; font-weight:700; flex-shrink:0; }
.msg-avatar.ai { background:linear-gradient(135deg,#111b30,#1a2a4a); border:1px solid #1e3060; color:#4f8ef7; }
.msg-avatar.user { background:linear-gradient(135deg,#7b5cf0,#4f8ef7); color:white; }
.msg-bubble { max-width:75%; padding:10px 14px; border-radius:4px 14px 14px 14px; font-size:0.855rem; line-height:1.65; color:#b8ccee; background:#0d1525; border:1px solid #151f35; }
.msg-bubble.user { border-radius:14px 4px 14px 14px; background:#0f1e40; border-color:#1e3a6e; color:#c8d8f5; }
.msg-meta { font-size:0.65rem; color:#2a3a5a; margin-top:5px; font-family:'JetBrains Mono',monospace; }
.msg-bubble.user + .msg-meta { text-align:right; }
.source-tag { display:inline-flex; align-items:center; gap:4px; background:#091525; border:1px solid #1a3050; border-radius:6px; padding:3px 8px; font-size:0.65rem; color:#3a6090; font-family:'JetBrains Mono',monospace; margin-top:6px; }

.inputbar { padding:16px 24px 20px; background:#0a0f1c; border-top:1px solid #111b2a; margin-bottom:12px; }

.panel-section { padding:14px 20px 10px 16px; border-bottom:1px solid #111b2a; }
div[data-testid="column"]:nth-of-type(3) { overflow-y:auto; max-height:calc(100vh - 52px); padding-right:8px; scrollbar-width:thin; scrollbar-color:#1a2540 transparent; padding-bottom: 20px; }
div[data-testid="column"]:nth-of-type(3)::-webkit-scrollbar { width:6px; }
div[data-testid="column"]:nth-of-type(3)::-webkit-scrollbar-track { background:transparent; }
div[data-testid="column"]:nth-of-type(3)::-webkit-scrollbar-thumb { background:#1a2540; border-radius:3px; }
.panel-label { font-size:0.65rem; font-weight:600; letter-spacing:0.1em; text-transform:uppercase; color:#2a3a5a; margin-bottom:10px; font-family:'JetBrains Mono',monospace; }
.panel-label span { color:#4f8ef7; }
.model-row { display:flex; align-items:center; gap:8px; background:#0d1525; border:1px solid #151f35; border-radius:8px; padding:7px 12px; margin-top:8px; }
.model-dot { width:6px; height:6px; border-radius:50%; background:#22c55e; }
.model-name { font-family:'JetBrains Mono',monospace; font-size:0.72rem; color:#6a88b8; flex:1; }
.concept-card { background:#0d1525; border:1px solid #151f35; border-left:3px solid #4f8ef7; border-radius:0 8px 8px 0; padding:9px 11px; margin-bottom:8px; }
.concept-card:hover { border-left-color:#7b5cf0; }
.concept-title { font-size:0.75rem; font-weight:600; color:#a0b8e0; margin-bottom:3px; font-family:'Syne',sans-serif; }
.concept-body { font-size:0.7rem; color:#4a5e80; line-height:1.5; }

.welcome { display:flex; flex-direction:column; align-items:center; justify-content:center; gap:12px; padding:60px 40px; text-align:center; opacity:1; }
.welcome-hex { width:52px; height:52px; background:linear-gradient(135deg,#1a2a4a,#0d1525); border:1px solid #1e3060; clip-path:polygon(50% 0%,100% 25%,100% 75%,50% 100%,0% 75%,0% 25%); display:flex; align-items:center; justify-content:center; font-size:1.4rem; }
.welcome-title { font-family:'Syne',sans-serif; font-size:1rem; font-weight:700; color:#a0bce0; text-align:center; }
.welcome-sub { font-size:0.75rem; color:#6a85b0; line-height:1.6; text-align:center; }

.stTextInput > div > div > input { background:transparent !important; border:none !important; color:#c8d4e8 !important; font-family:'Outfit',sans-serif !important; font-size:0.85rem !important; padding:0 !important; box-shadow:none !important; }
.stTextInput > div { background:transparent !important; border:none !important; box-shadow:none !important; }
.stTextInput > label { display:none !important; }

.stButton > button { background:linear-gradient(135deg,#1e3a6e,#2a4a8e) !important; color:#7ab0ff !important; border:1px solid #2a4a80 !important; border-radius:8px !important; font-family:'Outfit',sans-serif !important; font-size:0.78rem !important; padding:6px 14px !important; font-weight:500 !important; transition:all 0.2s !important; }
.stButton > button:hover { background:linear-gradient(135deg,#254880,#3060a8) !important; color:#b0d0ff !important; }

.stSelectbox > label { display:none !important; }
.stSelectbox > div > div { background:#0d1525 !important; border:1px solid #151f35 !important; border-radius:8px !important; color:#6a88b8 !important; font-family:'JetBrains Mono',monospace !important; font-size:0.72rem !important; }

.stFileUploader > label { display:none !important; }
.stFileUploader > div { background:#0d1525 !important; border:1px dashed #1a2a44 !important; border-radius:8px !important; }
.stFileUploader p { font-size:0.72rem !important; color:#3a5070 !important; }

.stRadio > label { display:none !important; }
</style>
""", unsafe_allow_html=True)

# ── Helpers ──────────────────────────────────────────────────────────────────
def extract_pdf_text(f):
    txt = ""
    with pdfplumber.open(f) as pdf:
        for p in pdf.pages:
            t = p.extract_text()
            if t: txt += t + "\n"
    return txt

def chunk_text(text, size=700, overlap=80):
    words = text.split()
    chunks, i = [], 0
    while i < len(words):
        chunks.append(" ".join(words[i:i+size]))
        i += size - overlap
    return chunks

def retrieve(query, chunks, k=3):
    qw = set(query.lower().split())
    scored = sorted(chunks, key=lambda c: len(qw & set(c.lower().split())), reverse=True)
    return [c for c in scored[:k] if len(qw & set(c.lower().split())) > 0]

TONES = {
    "Formal":     "Respond in a professional, formal tone with complete sentences.",
    "Casual":     "Respond in a friendly, casual conversational tone.",
    "ELI5":       "Explain as if talking to a 5-year-old. Use simple words.",
    "Bullets":    "Always respond in concise bullet points only.",
    "Technical":  "Respond with technical depth and correct terminology.",
}

def build_sys(tone, has_doc):
    base = TONES.get(tone, list(TONES.values())[0])
    if has_doc:
        base += "\n\nAnswer ONLY from the provided document context. If not found, say so."
    return base

def record_voice():
    r = sr.Recognizer()
    r.energy_threshold = 50
    r.dynamic_energy_threshold = False
    with sr.Microphone(device_index=2) as src:
            st.toast("Listening... speak now!", icon="🎤")
            try:
                audio = r.record(src, duration=5)
                text = r.recognize_google(audio)
                st.toast(f"Heard: {text}", icon="✅")
                return text
            except sr.UnknownValueError:
                st.toast("Could not understand audio.", icon="⚠️")
                return ""
            except Exception as e:
                st.toast(f"Error: {str(e)}", icon="⚠️")
                return ""

def stream_resp(msgs, model):
    stream = ollama.chat(model=model, messages=msgs, stream=True)
    for chunk in stream:
        yield chunk["message"]["content"]

# ── State ────────────────────────────────────────────────────────────────────
for k, v in [("messages",[]),("doc_chunks",[]),("doc_name",None),("active_tone","Formal"),("active_page","Chat"),("pending_query",None)]:
    if k not in st.session_state: st.session_state[k] = v

def submit_chat():
    q = st.session_state.chat_input.strip()
    if q:
        st.session_state.pending_query = q
        st.session_state.messages.append({"role": "user", "content": q, "source": None})
        st.session_state.chat_input = ""

try:
    models_res = ollama.list()
    model_list = [m["name"] for m in models_res.get("models", [])] if isinstance(models_res, dict) else [m.model for m in models_res.models]
    if not model_list:
        model_list = ["No local models found"]
except Exception:
    model_list = ["mistral","llama3","phi3","gemma"]

# ── TOP BAR ──────────────────────────────────────────────────────────────────
from streamlit_option_menu import option_menu
t1, t2, t3 = st.columns([0.2, 0.6, 0.2])
with t1:
    st.markdown("""
    <div style="height:52px; display:flex; align-items:center; padding-left:20px;">
      <div class="topbar-logo"><div class="topbar-logo-hex">C</div>Clirix<span class="topbar-title">Your Thinking Layer</span></div>
    </div>""", unsafe_allow_html=True)
with t2:
    st.session_state.active_page = option_menu(
        None, ["Chat", "Library", "Knowledge", "Analytics"], 
        icons=['chat', 'folder', 'book', 'bar-chart'], 
        menu_icon="cast", default_index=["Chat", "Library", "Knowledge", "Analytics"].index(st.session_state.active_page), orientation="horizontal",
        styles={
            "container": {"padding": "0!important", "background-color": "transparent", "margin-top": "6px"},
            "icon": {"color": "#556080", "font-size": "14px"}, 
            "nav-link": {"font-size": "13px", "text-align": "center", "margin":"0px", "--hover-color": "#111b30", "color": "#556080", "font-family": "Outfit"},
            "nav-link-selected": {"background-color": "#111b30", "color": "#a0c0ff", "border": "1px solid #1e3060", "font-weight": "400"},
        }
    )
with t3:
    st.markdown("""
    <div style="height:52px; display:flex; align-items:center; justify-content:flex-end; padding-right:20px; gap:16px;">
      <div class="topbar-badge">⬡ local inference</div>
      <div class="topbar-avatar">CX</div>
    </div>""", unsafe_allow_html=True)

# ── COLUMNS ──────────────────────────────────────────────────────────────────
c_nav, c_main, c_right = st.columns([0.045, 0.615, 0.34])

# Default — overwritten inside c_main when on Chat page
voice_btn = False

with c_nav:
    if st.button("💬", type="primary" if st.session_state.active_page == "Chat" else "secondary", help="Chat"): st.session_state.active_page = "Chat"; st.rerun()
    if st.button("📁", type="primary" if st.session_state.active_page == "Library" else "secondary", help="Library"): st.session_state.active_page = "Library"; st.rerun()
    if st.button("🧠", type="primary" if st.session_state.active_page == "Knowledge" else "secondary", help="Knowledge"): st.session_state.active_page = "Knowledge"; st.rerun()
    if st.button("📊", type="primary" if st.session_state.active_page == "Analytics" else "secondary", help="Analytics"): st.session_state.active_page = "Analytics"; st.rerun()
    st.markdown("<div style='flex:1; min-height: 200px;'></div>", unsafe_allow_html=True)
    if st.button("❓", type="secondary", help="Help"): pass

with c_main:
    if st.session_state.active_page != "Chat":
        st.markdown(f"""
        <div class="welcome" style="padding-top:100px;">
          <div class="welcome-hex">{'📁' if st.session_state.active_page=='Library' else '🧠' if st.session_state.active_page=='Knowledge' else '📊'}</div>
          <div class="welcome-title">{st.session_state.active_page} Area</div>
          <div class="welcome-sub">This section is functionally separated now.<br>You are no longer in the Chat view.</div>
        </div>""", unsafe_allow_html=True)
    else:
        doc_label = st.session_state.doc_name or "No document loaded"
        st.markdown(f"""
        <div class="chat-header">
          <div>
            <div class="chat-header-title">New Chat</div>
            <div class="chat-header-sub">Ask anything · Voice enabled · Document aware</div>
          </div>
          <div class="doc-pill">📎 {doc_label}</div>
        </div>""", unsafe_allow_html=True)
    
        # Messages
        st.markdown('<div class="messages">', unsafe_allow_html=True)
        if not st.session_state.messages:
            st.markdown("""
            <div class="welcome">
              <div class="welcome-hex">⬡</div>
              <div class="welcome-title">Ask Clirix anything</div>
              <div class="welcome-sub">Type or speak your question.<br>Upload a PDF to chat with your documents.</div>
            </div>""", unsafe_allow_html=True)
        else:
            for msg in st.session_state.messages:
                role = msg["role"]
                av = "⬡" if role=="assistant" else "U"
                av_cls = "ai" if role=="assistant" else "user"
                row_cls = "" if role=="assistant" else "user"
                bub_cls = "" if role=="assistant" else "user"
                src_html = '<div class="source-tag">📎 Doc context used</div>' if msg.get("source") else ""
                content = msg["content"].replace("<","&lt;").replace(">","&gt;")
                st.markdown(
                    f'<div class="msg-row {row_cls}">'
                    f'<div class="msg-avatar {av_cls}">{av}</div>'
                    f'<div>'
                    f'<div class="msg-bubble {bub_cls}">{content}</div>'
                    f'{src_html}'
                    f'<div class="msg-meta">{time.strftime("%H:%M")}</div>'
                    f'</div></div>',
                    unsafe_allow_html=True
                )
    
        # Input
        st.markdown('<div class="inputbar">', unsafe_allow_html=True)
        inp1, inp2, inp3 = st.columns([0.76, 0.11, 0.13])
        with inp1:
            if "prefill" in st.session_state and st.session_state.prefill:
                st.session_state.chat_input = st.session_state.pop("prefill")
            st.text_input("q", placeholder="Ask Clirix anything...", key="chat_input", label_visibility="collapsed", on_change=submit_chat)
        with inp2:
            voice_btn = st.button("🎤 Rec", key="voice")
        with inp3:
            st.button("Send ➤", key="send", type="primary", on_click=submit_chat)
        st.markdown('</div>', unsafe_allow_html=True)

with c_right:
    with st.container(height=750, border=False):
        # Model
        st.markdown('<div class="panel-section"><div class="panel-label"><span>⬡</span> Model</div>', unsafe_allow_html=True)
        sel_model = st.selectbox("m", model_list, label_visibility="collapsed")
        st.markdown(f'<div class="model-row"><div class="model-dot"></div><div class="model-name">{sel_model}</div><span style="font-size:0.62rem;color:#2a4060;font-family:\'JetBrains Mono\',monospace">LOCAL</span></div></div>', unsafe_allow_html=True)
    
        # Tone
        st.markdown('<div class="panel-section"><div class="panel-label"><span>◈</span> Response Tone</div>', unsafe_allow_html=True)
        tone = st.radio("t", list(TONES.keys()), index=list(TONES.keys()).index(st.session_state.active_tone), label_visibility="collapsed")
        st.session_state.active_tone = tone
        st.markdown('</div>', unsafe_allow_html=True)
    
        # Document
        st.markdown('<div class="panel-section"><div class="panel-label"><span>📎</span> Document</div>', unsafe_allow_html=True)
        upfile = st.file_uploader("f", type=["pdf"], label_visibility="collapsed")
        if upfile:
            if st.session_state.doc_name != upfile.name:
                with st.spinner("Indexing..."):
                    raw = extract_pdf_text(upfile)
                    st.session_state.doc_chunks = chunk_text(raw)
                    st.session_state.doc_name = upfile.name
                st.success(f"✅ {len(st.session_state.doc_chunks)} chunks")
        else:
            st.session_state.doc_chunks = []
            st.session_state.doc_name = None
        st.markdown('</div>', unsafe_allow_html=True)
    
        # Contextual notes
        st.markdown('<div class="panel-section"><div class="panel-label"><span>💡</span> Contextual Notes</div>', unsafe_allow_html=True)
        ai_msgs = [m for m in st.session_state.messages if m["role"]=="assistant"]
        if ai_msgs:
            preview = " ".join(ai_msgs[-1]["content"].split()[:25])
            st.markdown(f'<div class="concept-card"><div class="concept-title">Last Response</div><div class="concept-body">{preview}…</div></div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="concept-card"><div class="concept-title">🎙️ Voice Input</div><div class="concept-body">Click mic and speak. Google STT transcribes your query automatically.</div></div>
        <div class="concept-card"><div class="concept-title">📄 Document Chat</div><div class="concept-body">Upload a PDF. Clirix chunks and retrieves relevant context per query.</div></div>
        <div class="concept-card"><div class="concept-title">🎭 Tone Control</div><div class="concept-body">Each tone modifies the system prompt sent to the local model.</div></div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
        if st.button("🗑️ Reset Chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()

# ── Voice ─────────────────────────────────────────────────────────────────────
if voice_btn:
    spoken = record_voice()
    if spoken:
        st.session_state.pending_query = spoken
        st.session_state.messages.append({"role": "user", "content": spoken, "source": None})
        st.toast(f"✅ Heard: {spoken}", icon="🎤")
        st.rerun()

# ── Send ──────────────────────────────────────────────────────────────────────
if st.session_state.pending_query:
    query = st.session_state.pending_query
    st.session_state.pending_query = None  # Reset so it only runs once!
    
    source_used = None
    ctx = ""
    if st.session_state.doc_chunks:
        hits = retrieve(query, st.session_state.doc_chunks)
        if hits:
            ctx = "\n\n---\nDocument context:\n" + "\n\n".join(hits)
            source_used = hits[0]

    sys_p = build_sys(st.session_state.active_tone, bool(st.session_state.doc_chunks))
    o_msgs = [{"role":"system","content":sys_p}]
    for m in st.session_state.messages[:-1][-8:]:
        o_msgs.append({"role":m["role"],"content":m["content"]})
    o_msgs.append({"role":"user","content":query+ctx})

    with st.spinner(""):
        if sel_model == "No local models found":
            full = "⚠️ No local model is available. Please pull a model using `ollama pull mistral` in your terminal."
            st.session_state.messages.append({"role":"assistant","content":full,"source":source_used})
            st.rerun()
            
        full = ""
        ph = st.empty()
        try:
            for tok in stream_resp(o_msgs, sel_model):
                full += tok
                ph.markdown(f'<div class="msg-row"><div class="msg-avatar ai">⬡</div><div><div class="msg-bubble">{full}▌</div><div class="msg-meta">typing…</div></div></div>', unsafe_allow_html=True)
        except Exception as e:
            full = f"⚠️ Generation error: {str(e)}"
        ph.empty()

    st.session_state.messages.append({"role":"assistant","content":full,"source":source_used})
    st.rerun()