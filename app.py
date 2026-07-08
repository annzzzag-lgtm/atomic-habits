import streamlit as st

# ----------------------------------------------------
# PREMIUM APP CONFIGURATION
# ----------------------------------------------------
st.set_page_config(
    page_title="Atomic Systems Pro",
    page_icon="⚛️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom Premium CSS (Clean typography, glassmorphic cards, modern input styling)
st.markdown("""
    <style>
    /* Global App Background & Font Settings */
    .stApp {
        background: linear-gradient(180deg, #0F172A 0%, #020617 100%);
    }
    html, body, [data-testid="stWidgetLabel"] p {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
        color: #E2E8F0 !important;
    }
    
    /* Premium Glassmorphic Cards */
    .metric-card {
        background: rgba(30, 41, 59, 0.45);
        backdrop-filter: blur(8px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.2);
    }
    
    /* Clean custom headers */
    .main-title {
        font-size: 2.2rem;
        font-weight: 800;
        background: linear-gradient(90deg, #F59E0B 0%, #D97706 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -0.05em;
        margin-bottom: 5px;
    }
    .section-header {
        font-size: 1.25rem;
        font-weight: 600;
        color: #F8FAFC;
        margin-top: 15px;
        margin-bottom: 10px;
        letter-spacing: -0.02em;
    }
    
    /* Modern Checkbox Overrides */
    div[data-testid="stCheckbox"] {
        background: rgba(30, 41, 59, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 10px;
        padding: 12px 16px;
        margin-bottom: 8px;
        transition: all 0.2s ease;
    }
    div[data-testid="stCheckbox"]:hover {
        background: rgba(30, 41, 59, 0.6);
        border-color: rgba(245, 158, 11, 0.3);
    }
    </style>
""", unsafe_allow_html=True)

# ----------------------------------------------------
# SYSTEM TEMPLATES FOR GENERATING TASKS
# ----------------------------------------------------
def generate_atomic_tasks(user_notes, identity_type):
    clean_note = user_notes.strip() if user_notes else "execute intentionally"
    
    templates = {
        "identity": [
            f"Cast an identity vote: Perform the absolute smallest friction-free action aligned with being a '{clean_note}'.",
            f"Affirm your system: Mentally confirm your baseline statement: 'I am a person who prioritizes {clean_note}.'"
        ],
        "obvious": [
            f"Optimize environment architecture: Position a highly visible physical cue for '{clean_note}' in your immediate line of sight.",
            f"Formulate implementation intention: Map out exactly *when* and *where* you will trigger this habit today."
        ],
        "easy": [
            f"Apply the Two-Minute Rule: Compress your primary action for '{clean_note}' into an operational step requiring under 120 seconds.",
            f"Friction reduction: Eliminate one digital or environmental obstacle that stands between you and starting '{clean_note}'."
        ]
    }
    return [templates["identity"][0], templates["obvious"][0], templates["easy"][0], templates["easy"][1]]

# ----------------------------------------------------
# STATE MANAGEMENT
# ----------------------------------------------------
if "identity_votes" not in st.session_state:
    st.session_state.identity_votes = 0
if "generated_tasks" not in st.session_state:
    st.session_state.generated_tasks = []
if "current_identity" not in st.session_state:
    st.session_state.current_identity = ""
if "completed_tasks" not in st.session_state:
    st.session_state.completed_tasks = {}

# ----------------------------------------------------
# HEADER & METRIC HERO SECTION
# ----------------------------------------------------
col_title, col_metric = st.columns([2, 1])

with col_title:
    st.markdown('<div class="main-title">ATOMIC SYSTEMS</div>', unsafe_allow_html=True)
    st.markdown('<p style="color: #94A3B8; font-size: 0.95rem; margin-top:-5px;">Compounding 1% gains daily • Built on James Clear Frameworks</p>', unsafe_allow_html=True)

with col_metric:
    # A professional, elegant card display for your stats
    st.markdown(f"""
        <div class="metric-card" style="padding: 10px 15px; text-align: center; margin-bottom: 0;">
            <span style="color: #94A3B8; font-size: 0.75rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em;">Identity Votes</span>
            <h2 style="color: #F59E0B; margin: 0; font-size: 1.8rem; font-weight: 700;">{st.session_state.identity_votes}</h2>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ----------------------------------------------------
# INPUT INTERFACE
# ----------------------------------------------------
st.markdown('<div class="section-header">🧬 Define System Architecture</div>', unsafe_allow_html=True)

user_input = st.text_input(
    "Target Identity Focus",
    placeholder="e.g., Deep Work Focused Engineer, Intentional Writer, High-Performance Athlete...",
    value=st.session_state.current_identity,
    label_visibility="collapsed"
)

user_notes = st.text_area(
    "Daily Constraints / Contextual Notes",
    placeholder="List daily obstacles or environmental friction points here (e.g., packed schedule, energy low)...",
    height=80
)

# Custom styled action button
if st.button("Calibrate System Steps →", use_container_width=True, type="primary"):
    if user_input:
        st.session_state.current_identity = user_input
        st.session_state.generated_tasks = generate_atomic_tasks(user_input,
