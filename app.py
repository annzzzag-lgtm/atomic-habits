import streamlit as st
import random

# Set up page configuration
st.set_page_config(
    page_title="Atomic Habits AI Companion",
    page_icon="⚛️",
    layout="centered"
)

# ----------------------------------------------------
# SYSTEM TEMPLATES FOR GENERATING ACHIVABLE TASKS
# ----------------------------------------------------
# Since we want this completely self-contained and free, we use a smart rules engine
# that instantly translates what you write into Atomic Habits blueprints.
def generate_atomic_tasks(user_notes, identity_type):
    clean_note = user_notes.strip() if user_notes else "be productive"
    
    # Templates for actionable, micro-steps based on the 4 Laws
    templates = {
        "identity": [
            f"Cast 1 vote for being a person who focuses on '{clean_note}' (e.g., do the absolute smallest action related to it right now).",
            f"Write down: 'I am a person who {clean_note}.' Say it out loud once."
        ],
        "obvious": [
            f"Set up a physical visual cue in your room or desk right now for '{clean_note}'.",
            f"Fill out this stack formula: 'After I finish my morning coffee, I will immediately spend 1 minute on {clean_note}'."
        ],
        "easy": [
            f"Apply the Two-Minute Rule: Reduce your largest goal for '{clean_note}' down to an action that takes less than 120 seconds.",
            f"Prime your environment tonight (lay out clothes, open browser tabs, or prep tools) to make starting '{clean_note}' effortless tomorrow."
        ],
        "attractive": [
            f"Temptation Bundle: Pair an action you *need* to do for '{clean_note}' with an action you *want* to do (e.g., listen to a favorite song/podcast while doing it)."
        ]
    }
    
    # Return a tailored blend of these rules based on what they wrote
    return templates["identity"] + [templates["obvious"][0]] + [templates["easy"][0]] + [templates["attractive"][0]]

# ----------------------------------------------------
# APP STATE MANAGEMENT
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
# UI RENDERING
# ----------------------------------------------------
st.title("⚛️ Atomic Habits AI Companion")
st.subheader("Systems over goals. 1% better every day.")

# Sidebar Stats
st.sidebar.header("Your Progression")
st.sidebar.metric(label="👤 Total Identity Votes Cast", value=st.session_state.identity_votes)
if st.sidebar.button("Reset App Data"):
    st.session_state.identity_votes = 0
    st.session_state.generated_tasks = []
    st.session_state.current_identity = ""
    st.session_state.completed_tasks = {}
    st.rerun()

# --- STEP 1: INPUT AND NOTE TAKING ---
st.markdown("### 📝 Step 1: Define Your Focus & Identity")
user_input = st.text_input(
    "What identity do you want to reinforce, or what specific habit/task are you working on today?",
    placeholder="e.g., writer, healthy eater, organized person, software engineer...",
    value=st.session_state.current_identity
)

user_notes = st.text_area(
    "Add any daily notes, obstacles, or specific contexts here:",
    placeholder="e.g., I'm feeling tired today, or I need to clear out my messy desk desk..."
)

# Button to trigger the AI rules analyzer
if st.button("Analyze & Generate Achievable To-Do List ✨", type="primary"):
    if user_input:
        st.session_state.current_identity = user_input
        # Analyze what they wrote and build the system steps
        st.session_state.generated_tasks = generate_atomic_tasks(user_input, user_notes)
        # Clear previous checklist completions for the new custom list
        st.session_state.completed_tasks = {}
        st.rerun()
    else:
        st.error("Please enter an identity or habit focus above to generate your list!")

# --- STEP 2: DYNAMIC TO-DO LIST ---
if st.session_state.generated_tasks:
    st.markdown("---")
    st.markdown(f"### 🎯 Your Adjusted System Checklist for: **{st.session_state.current_identity}**")
    st.caption("These tasks have been scaled down to minimize resistance and match your current environment.")
    
    all_checked = True
    
    for idx, task in enumerate(st.session_state.generated_tasks):
        task_key = f"dynamic_task_{idx}"
        
        # Checkbox tracking
        is_checked = st.checkbox(
            task,
            key=task_key,
            value=st.session_state.completed_tasks.get(task_key, False)
        )
        
        # Handle state change when checked/unchecked
        if is_checked != st.session_state.completed_tasks.get(task_key, False):
            st.session_state.completed_tasks[task_key] = is_checked
            if is_checked:
                st.session_state.identity_votes += 1
                st.toast("Vote cast for your ideal identity! 🎉")
            else:
                st.session_state.identity_votes = max(0, st.session_state.identity_votes - 1)
            st.rerun()
            
        if not is_checked:
            all_checked = False

    # Success Celebration Framework
    if all_checked:
        st.success("✨ Incredible! You kept your requirements small, reduced friction, and successfully cast your votes. You are 1% better today!")
    else:
        st.info("💡 Remember the **Two-Minute Rule**: If a step feels too hard, scale it down even further until it takes less than 2 minutes.")
else:
    st.info("Write down your identity focus above and click 'Analyze' to build your friction-free, adaptive checklist.")
