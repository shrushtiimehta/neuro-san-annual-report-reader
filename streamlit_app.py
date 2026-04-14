# Copyright © 2025 Cognizant Technology Solutions Corp, www.cognizant.com.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# END COPYRIGHT

import json
import time

import requests
import streamlit as st

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Cognizant 2024 Annual Report Explorer",
    page_icon="🔵",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Constants ─────────────────────────────────────────────────────────────────
NEURO_SAN_BASE_URL = "http://localhost:8080/api/v1"
AGENT_SIMPLE = "annual_report_reader"
AGENT_MULTI  = "multiagent_annual_report_reader"

MSG_AI             = 4
MSG_AGENT          = 100
MSG_AGENT_FRAMEWORK = 101
MSG_AGENT_TOOL_RESULT = 103
MSG_AGENT_PROGRESS = 104

# Map string type names to their integer constants
_TYPE_NAME_TO_INT = {
    "AI": MSG_AI,
    "AGENT": MSG_AGENT,
    "AGENT_FRAMEWORK": MSG_AGENT_FRAMEWORK,
    "AGENT_TOOL_RESULT": MSG_AGENT_TOOL_RESULT,
    "AGENT_PROGRESS": MSG_AGENT_PROGRESS,
}

def _normalize_msg_type(raw) -> int:
    """Accept int, string name, or unknown and return the int constant."""
    if isinstance(raw, int):
        return raw
    if isinstance(raw, str):
        return _TYPE_NAME_TO_INT.get(raw, 0)
    return 0

# Label + colour per message type for the log panel
MSG_META = {
    MSG_AI:               ("AI",       "#58a6ff"),
    MSG_AGENT:            ("AGENT",    "#e3b341"),
    MSG_AGENT_FRAMEWORK:  ("FINAL",    "#3fb950"),
    MSG_AGENT_TOOL_RESULT:("TOOL",     "#bc8cff"),
    MSG_AGENT_PROGRESS:   ("PROGRESS", "#8b949e"),
}

# ── Session state ─────────────────────────────────────────────────────────────
if "logs"         not in st.session_state: st.session_state.logs         = []
if "final_answer" not in st.session_state: st.session_state.final_answer = ""

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

[data-testid="stAppViewContainer"] { background:#EEF2FF; font-family:'Inter',sans-serif; }
[data-testid="stHeader"]            { background:transparent; }
[data-testid="stMainBlockContainer"]{ padding-top:1.5rem; }
[data-testid="stColumn"]            { background:transparent !important; }

/* Keep alert/warning/error boxes visible */
[data-testid="stAlert"],
div[role="alert"],
.stAlert,
.element-container .stAlert {
    background:#fff8e1 !important;
    border:1px solid #f9a825 !important;
    border-radius:8px !important;
    color:#5d4037 !important;
}
[data-testid="stAlert"] p,
[data-testid="stAlert"] span,
div[role="alert"] p,
div[role="alert"] span {
    color:#5d4037 !important;
}

/* ── Hero ── */
.hero {
    background: linear-gradient(135deg,#0033A0 0%,#001B5E 55%,#001435 100%);
    border-radius:20px; padding:2.6rem 3rem 2rem;
    margin-bottom:1.6rem; color:white; position:relative; overflow:hidden;
    box-shadow:0 8px 32px rgba(0,51,160,.25);
}
.hero::before {
    content:""; position:absolute; right:-80px; top:-80px;
    width:360px; height:360px; border-radius:50%;
    background:rgba(255,255,255,.045);
}
.hero::after {
    content:""; position:absolute; left:-40px; bottom:-100px;
    width:260px; height:260px; border-radius:50%;
    background:rgba(77,166,213,.08);
}
.hero-eyebrow { font-size:.7rem; font-weight:700; letter-spacing:2px;
    text-transform:uppercase; opacity:.6; margin:0 0 .5rem; }
.hero-title   { font-size:2.3rem; font-weight:700; letter-spacing:-.8px;
    margin:0 0 .45rem; line-height:1.15; }
.hero-title span { color:#7AB8F5; }
.hero-sub     { font-size:.98rem; opacity:.75; margin:0 0 1.6rem;
    max-width:560px; line-height:1.6; }
.hero-tags    { display:flex; gap:.5rem; flex-wrap:wrap; }
.hero-tag {
    display:inline-block; background:rgba(255,255,255,.1);
    border:1px solid rgba(255,255,255,.2); border-radius:6px;
    padding:.2rem .7rem; font-size:.7rem; font-weight:600;
    letter-spacing:.8px; text-transform:uppercase;
}

/* ── Stat cards ── */
.stat-row {
    display:grid; grid-template-columns:repeat(6,1fr);
    gap:.85rem; margin-bottom:1.6rem;
}
.stat-card {
    background:white; border-radius:14px; padding:1rem 1.1rem .9rem;
    border-bottom:3px solid #0033A0;
    box-shadow:0 2px 10px rgba(0,51,160,.07); transition:transform .15s;
}
.stat-card:hover { transform:translateY(-2px); }
.stat-card .val { font-size:1.5rem; font-weight:700; color:#0033A0; line-height:1.1; }
.stat-card .lbl { font-size:.67rem; color:#6b7280; text-transform:uppercase;
    letter-spacing:.5px; margin-top:.25rem; font-weight:500; }

/* ── Widget labels — covers both text input and selectbox ── */
label,
[data-testid="stWidgetLabel"],
[data-testid="stWidgetLabel"] p,
[data-testid="stWidgetLabel"] span,
[data-testid="stTextInput"]  label,
[data-testid="stSelectbox"]  label,
.stTextInput label,
.stSelectbox label {
    color:#0033A0 !important; font-weight:700 !important; font-size:1.1rem !important;
}

/* ── Text input ── */
[data-testid="stTextInput"] input {
    border-radius:10px !important; border:1.5px solid #C7D2FE !important;
    font-size:.95rem !important; padding:.6rem 1rem !important;
    background:white !important; color:#111827 !important;
}
[data-testid="stTextInput"] input:focus {
    border-color:#0033A0 !important;
    box-shadow:0 0 0 3px rgba(0,51,160,.1) !important;
}

/* ── Selectbox ── */
[data-testid="stSelectbox"] > div > div,
[data-baseweb="select"] > div {
    border-radius:10px !important; border:1.5px solid #C7D2FE !important;
    background:white !important;
}
[data-baseweb="select"] span,
[data-baseweb="select"] div,
[data-testid="stSelectbox"] span { color:#111827 !important; }

/* ── Button ── */
[data-testid="stButton"] > button {
    border-radius:10px !important; font-weight:600 !important;
    font-size:.95rem !important;
    background:linear-gradient(135deg,#0033A0 0%,#0047CC 100%) !important;
    color:white !important; border:none !important;
    box-shadow:0 3px 14px rgba(0,51,160,.35) !important;
    transition:all .15s ease !important;
}
[data-testid="stButton"] > button:hover {
    background:linear-gradient(135deg,#002880 0%,#003BB8 100%) !important;
    box-shadow:0 5px 20px rgba(0,51,160,.45) !important;
    transform:translateY(-1px) !important; color:white !important;
}

/* ── Log panel ── */
.log-panel {
    background:#0d1117; border-radius:14px; padding:0;
    box-shadow:0 4px 20px rgba(0,0,0,.35);
    border:1px solid #30363d; overflow:hidden;
    font-family:'JetBrains Mono','Fira Code','Courier New',monospace;
}
.log-header {
    background:#161b22; padding:.7rem 1rem;
    border-bottom:1px solid #30363d;
    display:flex; align-items:center; gap:.6rem;
}
.log-header-dot { width:10px; height:10px; border-radius:50%; }
.log-header-title {
    color:#8b949e; font-size:.72rem; font-weight:600;
    letter-spacing:1px; text-transform:uppercase; margin-left:.2rem;
}
.log-body {
    padding:.8rem 1rem; height:520px; overflow-y:auto;
    font-size:.72rem; line-height:1.6;
}
.log-body::-webkit-scrollbar { width:5px; }
.log-body::-webkit-scrollbar-track { background:#0d1117; }
.log-body::-webkit-scrollbar-thumb { background:#30363d; border-radius:3px; }
.log-entry { margin-bottom:.45rem; word-break:break-word; }
.log-ts    { color:#484f58; margin-right:.4rem; }
.log-badge {
    display:inline-block; border-radius:4px; padding:.05rem .4rem;
    font-size:.65rem; font-weight:700; margin-right:.45rem;
    letter-spacing:.4px;
}
.log-text  { color:#cdd9e5; }
.log-empty { color:#484f58; font-style:italic; }

/* ── Section heading (matches widget label size) ── */
h4 {
    color:#0033A0 !important; font-weight:700 !important; font-size:1.35rem !important;
}

/* ── Footer ── */
.footer {
    text-align:center; color:#9ca3af; font-size:.75rem;
    padding:1.4rem 0 .6rem; letter-spacing:.3px;
}
</style>
""", unsafe_allow_html=True)

# ── Helpers ───────────────────────────────────────────────────────────────────

def get_agent_name() -> str:
    return AGENT_MULTI if "Multi-agent" in agent_choice else AGENT_SIMPLE


def check_server_health(agent: str) -> bool:
    try:
        r = requests.get(f"{NEURO_SAN_BASE_URL}/{agent}/function", timeout=5)
        return r.status_code == 200
    except requests.exceptions.RequestException:
        return False


def stream_neuro_san(url_input: str, agent: str):
    url = f"{NEURO_SAN_BASE_URL}/{agent}/streaming_chat"
    payload = {
        "user_message": {"text": (
            f"Here is my LinkedIn profile: {url_input} — "
            "what does Cognizant's annual report cover that relates to my background?"
        )},
        "chat_filter": {"chat_filter_type": "MAXIMAL"},
    }
    with requests.post(url, json=payload, stream=True, timeout=None) as resp:
        resp.raise_for_status()
        for raw_line in resp.iter_lines():
            if not raw_line:
                continue
            try:
                data = json.loads(raw_line)
            except json.JSONDecodeError:
                continue
            if err := data.get("error"):
                raise RuntimeError(err)
            response = data.get("response", data)
            raw_type = response.get("type")
            # Normalize type: server may send int (101) or string ("AGENT_FRAMEWORK")
            msg_type = _normalize_msg_type(raw_type)
            text = (response.get("text") or "").strip()
            if text:
                yield msg_type, text


def render_log_panel(placeholder, logs: list):
    """Render the log panel HTML into the given st.empty() placeholder."""
    if not logs:
        body = '<div class="log-empty">Waiting for agent activity…</div>'
    else:
        rows = []
        for entry in logs:
            mtype  = entry["type"]
            label, colour = MSG_META.get(mtype, ("MSG", "#8b949e"))
            ts     = entry["ts"]
            text   = entry["text"][:300] + ("…" if len(entry["text"]) > 300 else "")
            # escape HTML and $ (Streamlit renders $...$ as LaTeX)
            text = (text.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
                        .replace("$","&#36;"))
            rows.append(
                f'<div class="log-entry">'
                f'<span class="log-ts">{ts}</span>'
                f'<span class="log-badge" style="background:{colour}22;color:{colour}">{label}</span>'
                f'<span class="log-text">{text}</span>'
                f'</div>'
            )
        body = "\n".join(rows)
        # auto-scroll script
        body += """
<script>
  var lb = document.querySelector('.log-body');
  if(lb) lb.scrollTop = lb.scrollHeight;
</script>"""

    html = f"""
<div class="log-panel">
  <div class="log-header">
    <div class="log-header-dot" style="background:#ff5f57"></div>
    <div class="log-header-dot" style="background:#febc2e"></div>
    <div class="log-header-dot" style="background:#28c840"></div>
    <span class="log-header-title">Agent Network Logs</span>
  </div>
  <div class="log-body">{body}</div>
</div>"""
    placeholder.markdown(html, unsafe_allow_html=True)


# ── Full-width top section ────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <div class="hero-eyebrow">Cognizant Technology Solutions</div>
  <div class="hero-title">2024 Annual Report <span>Explorer</span></div>
  <div class="hero-sub">
    Enter a LinkedIn profile URL and receive a personalized summary of
    Cognizant's 2024 Annual Report — curated to your industry and seniority.
  </div>
  <div class="hero-tags">
    <span class="hero-tag">Powered by Neuro SAN Studio</span>
    <span class="hero-tag">AI Multi-Agent</span>
    <span class="hero-tag">2024 Annual Report</span>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="stat-row">
  <div class="stat-card"><div class="val">$19.7B</div><div class="lbl">FY 2024 Revenue</div></div>
  <div class="stat-card"><div class="val">2%</div><div class="lbl">Revenue Growth</div></div>
  <div class="stat-card"><div class="val">336,800</div><div class="lbl">Associates Worldwide</div></div>
  <div class="stat-card"><div class="val">$27.1B</div><div class="lbl">Record TCV Bookings</div></div>
  <div class="stat-card"><div class="val">29</div><div class="lbl">Large Deals Won</div></div>
  <div class="stat-card"><div class="val">230K+</div><div class="lbl">Associates Trained in AI</div></div>
</div>
""", unsafe_allow_html=True)

# ── Two-column split: main | log panel ───────────────────────────────────────
main_col, log_col = st.columns([2, 1], gap="large")

# ── Right: log panel (rendered before main so placeholder exists) ─────────────
with log_col:
    log_placeholder = st.empty()
    render_log_panel(log_placeholder, st.session_state.logs)

# ── Left: input + results ─────────────────────────────────────────────────────
with main_col:
    col_url, col_mode, col_btn = st.columns([5, 2, 1])
    with col_url:
        linkedin_url = st.text_input(
            "LinkedIn Profile URL",
            placeholder="https://www.linkedin.com/in/your-profile/",
        )
    with col_mode:
        agent_choice = st.selectbox(
            "Agent mode",
            options=["Standard (faster)", "Multi-agent (thorough)"],
            index=1,
            help="Multi-agent uses 10 parallel section researchers.",
        )
    with col_btn:
        st.markdown("<div style='margin-top:1.72rem'></div>", unsafe_allow_html=True)
        analyze_clicked = st.button("Analyze Profile", type="primary", use_container_width=True)

    st.markdown(
        "<h4 style='color:#0033A0;margin:0.3rem 0 0.2rem;font-size:1.35rem'>Your Personalized Report Summary</h4>",
        unsafe_allow_html=True,
    )
    st.divider()
    result_placeholder = st.empty()

    # Show last answer if available
    if st.session_state.final_answer and not analyze_clicked:
        escaped = st.session_state.final_answer.replace("$", "&#36;")
        result_placeholder.markdown(
            f'<div style="background:white;color:#111;padding:1.5rem 2rem;'
            f'border-radius:12px;box-shadow:0 2px 10px rgba(0,0,0,.07);'
            f'line-height:1.7;font-size:.95rem;">{escaped}</div>',
            unsafe_allow_html=True,
        )

# ── Streaming logic ───────────────────────────────────────────────────────────
if analyze_clicked:
    if not linkedin_url or not linkedin_url.startswith("http"):
        with main_col:
            st.warning("Please enter a valid LinkedIn profile URL (starting with https://).")
        st.stop()

    # Clear previous run
    st.session_state.logs = []
    st.session_state.final_answer = ""
    result_placeholder.empty()

    agent = get_agent_name()

    with main_col:
        with st.spinner("Connecting to Neuro SAN server…"):
            is_up = check_server_health(agent)
        if not is_up:
            st.error(
                "Cannot reach the Neuro SAN server at `localhost:8080`. "
                "Start it with:\n\n```bash\npython -m run --server-only\n```"
            )
            st.stop()

        status_box = st.status("Processing your profile…", expanded=True)

    start = time.time()

    try:
        for msg_type, text in stream_neuro_san(linkedin_url, agent):
            ts = time.strftime("%H:%M:%S")

            # Always log every message
            st.session_state.logs.append({"type": msg_type, "text": text, "ts": ts})
            render_log_panel(log_placeholder, st.session_state.logs)

            if msg_type == MSG_AGENT_FRAMEWORK:
                st.session_state.final_answer = text
                # Escape $ to prevent Streamlit from rendering LaTeX math
                escaped = text.replace("$", "&#36;")
                result_placeholder.markdown(
                    f'<div style="background:white;color:#111;padding:1.5rem 2rem;'
                    f'border-radius:12px;box-shadow:0 2px 10px rgba(0,0,0,.07);'
                    f'line-height:1.7;font-size:.95rem;">{escaped}</div>',
                    unsafe_allow_html=True,
                )
                with main_col:
                    with status_box:
                        st.markdown("✅ Final answer received.")

            else:
                pass  # All non-final messages go to the log panel only

    except requests.exceptions.ConnectionError:
        with main_col:
            st.error("Lost connection to the Neuro SAN server mid-stream.")
    except requests.exceptions.Timeout:
        with main_col:
            st.error("Request timed out. Try again shortly.")
    except requests.exceptions.HTTPError as exc:
        with main_col:
            st.error(f"Server returned an error: {exc}")
    except RuntimeError as exc:
        msg = str(exc)
        with main_col:
            if "agent tool path" in msg.lower() or "pythonpath" in msg.lower():
                st.error(
                    f"**Server configuration error:** `{msg}`\n\n"
                    "Restart the server from the project root:\n\n"
                    "```bash\nsource venv/bin/activate\npython -m run --server-only\n```"
                )
            else:
                st.error(f"Server error: {msg}")
    except Exception as exc:  # pylint: disable=broad-except
        with main_col:
            st.error(f"Unexpected error: {exc}")
    else:
        elapsed = time.time() - start
        with main_col:
            status_box.update(
                label=f"Done — completed in {elapsed:.0f}s",
                state="complete", expanded=False,
            )
            if not st.session_state.final_answer:
                st.warning("Agent finished but returned no final answer. Check server logs.")

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    Cognizant Technology Solutions · 2024 Annual Report ·
    Powered by <strong>Neuro SAN Studio</strong>
</div>
""", unsafe_allow_html=True)
