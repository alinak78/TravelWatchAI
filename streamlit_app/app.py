import streamlit as st
from skyscanner_api import _api_key

st.set_page_config(
    page_title="TravelWatch AI",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

/* Sidebar */
[data-testid="stSidebar"] {
    background: #ffffff;
    border-right: 1px solid #f0f0f0;
    padding-top: 0;
}
[data-testid="stSidebar"] > div:first-child { padding: 0; }

/* Remove default padding */
.block-container { padding: 2rem 2.5rem 2rem 2.5rem !important; }

/* Main background */
[data-testid="stAppViewContainer"] { background: #f5f5f5; }
[data-testid="stAppViewContainer"] > .main { background: #f5f5f5; }

/* Main content white card */
.main-content {
    background: #ffffff;
    border-radius: 16px;
    padding: 32px 36px;
    min-height: 90vh;
}

/* Cards */
.tw-card {
    background: #ffffff;
    border: 1px solid #ebebeb;
    border-radius: 12px;
    padding: 18px 20px;
}
.tw-card-sm {
    background: #ffffff;
    border: 1px solid #ebebeb;
    border-radius: 10px;
    padding: 12px 16px;
}

/* Badges */
.badge-buy {
    background: #1a56db;
    color: #fff;
    border-radius: 999px;
    padding: 3px 10px;
    font-size: 12px;
    font-weight: 600;
    display: inline-block;
}
.badge-wait {
    background: #6b7280;
    color: #fff;
    border-radius: 999px;
    padding: 3px 10px;
    font-size: 12px;
    font-weight: 600;
    display: inline-block;
}

/* Section label */
.sec-label {
    font-size: 12px;
    color: #9ca3af;
    margin-bottom: 6px;
    font-weight: 500;
}

/* Nav item active */
.nav-active {
    background: #f3f4f6;
    border-radius: 8px;
    font-weight: 600;
}

/* Button overrides */
.stButton > button {
    border-radius: 8px;
    font-family: 'Inter', sans-serif;
    font-weight: 500;
}
.stButton > button[kind="primary"] {
    background: #1a56db;
    border: none;
    color: white;
}

/* Input fields */
.stSelectbox > div, .stTextInput > div, .stDateInput > div, .stNumberInput > div {
    border-radius: 8px;
}

/* Radio buttons */
div[data-testid="stRadio"] > div {
    border: 1px solid #ebebeb;
    border-radius: 10px;
    padding: 8px 12px;
    margin-bottom: 4px;
}
</style>
""", unsafe_allow_html=True)

# ── Session state ─────────────────────────────────────────────────────────────
@st.cache_data(ttl=3600)
def generate_initial_watches():
    """Start empty so every watch is based on a live Skyscanner lookup."""
    if not _api_key():
        st.warning(
            "Skyscanner prices unavailable — set RAPIDAPI_KEY in your environment "
            "or .streamlit/secrets.toml to enable live pricing.",
            icon="⚠️",
        )
    return []

if "watches" not in st.session_state:
    st.session_state.watches = generate_initial_watches()
if "selected_watch_id" not in st.session_state:
    st.session_state.selected_watch_id = None
if "currency" not in st.session_state:
    st.session_state.currency = "USD"
if "price_alert" not in st.session_state:
    st.session_state.price_alert = "On"
if "page" not in st.session_state:
    st.session_state.page = "Dashboard"
if "ml_section" not in st.session_state:
    st.session_state.ml_section = "Model Evaluation"


def _go_to(page, ml_section=None):
    st.session_state.page = page
    if ml_section is not None:
        st.session_state.ml_section = ml_section
    st.rerun()

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    # Logo
    st.markdown("""
    <div style='padding: 28px 20px 20px 20px; border-bottom: 1px solid #f0f0f0;'>
        <div style='display:flex; align-items:center; gap:8px;'>
            <span style='font-size:22px;'>🪁</span>
            <span style='font-size:17px; font-weight:700; color:#111;'>TravelWatch AI</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='padding: 16px 12px 8px 12px;'>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:11px; font-weight:600; color:#9ca3af; letter-spacing:0.08em; margin-bottom:8px;'>MENU</div>", unsafe_allow_html=True)

    main_pages = [
    ("🏠", "Dashboard", "Dashboard"),
    ("🤖", "AI Agent", "AI Agent"),
    ("📊", "ML Insights", "ML Insights"),
]

    dashboard_pages = {"Dashboard", "Add New Watch", "See All", "Task Detail", "Compare"}

    for icon, label, target_page in main_pages:
        active = st.session_state.page == target_page

        if target_page == "Dashboard":
            active = st.session_state.page in dashboard_pages

        if st.button(
            f"{icon}  {label}",
            key=f"nav_{label}",
            use_container_width=True,
            type="primary" if active else "secondary",
        ):
            _go_to(target_page)

    st.markdown("</div>", unsafe_allow_html=True)

    # Settings at bottom
    st.markdown("<div style='position:absolute; bottom:0; left:0; right:0; padding:16px 12px; border-top:1px solid #f0f0f0;'>", unsafe_allow_html=True)
    if st.button(
        "⚙️  Settings",
        key="nav_Settings",
        use_container_width=True,
        type="primary" if st.session_state.page == "Settings" else "secondary",
    ):
        st.session_state.page = "Settings"
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# ── Page router ───────────────────────────────────────────────────────────────
page = st.session_state.page

if page == "Dashboard":
    from views.dashboard import render
elif page == "Add New Watch":
    from views.add_watch import render
elif page == "Task Detail":
    from views.task_detail import render
elif page == "See All":
    from views.see_all import render
elif page == "Compare":
    from views.compare import render
elif page == "ML Insights":
    from views.ml_insights import render
elif page == "View Data":
    from views.view_data import render
elif page == "Settings":
    from views.settings import render
elif page == "AI Agent":
    from views.ai_agent import render
else:
    from views.dashboard import render

render()
