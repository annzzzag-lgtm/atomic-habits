import streamlit as st
import datetime
import random

# Set up page configuration
st.set_page_config(
    page_title="Atomic Habits Daily Companion",
    page_icon="⚛️",
    layout="centered"
)

# ----------------------------------------------------
# DATA SOURCE: Book Frameworks, Tips, and Action Items
# ----------------------------------------------------
ATOMIC_DATA = [
    {
        "day": 1,
        "theme": "Identity-Based Habits",
        "tip": "Focus on who you wish to become, not what you want to achieve. Your identity emerges out of your habits. Every action is a vote for the type of person you want to become.",
        "tasks": [
            "Write down the identity you want to reinforce today (e.g., 'I am a healthy person', 'I am a writer').",
            "Cast one small 'vote' for that identity today (e.g., drinking a glass of water, writing one sentence)."
        ]
    },
    {
        "day": 2,
        "theme": "The 1st Law: Make It Obvious (Cue)",
        "tip": "Many of our bad habits are built on hidden cues. Use a Habit Scorecard to look at your daily routines and become aware of your current behaviors before changing them.",
        "tasks": [
            "Track your morning routine step-by-step on a piece of paper.",
            "Mark each habit with '+' for positive, '-' for negative, or '=' for neutral."
        ]
    },
    {
        "day": 3,
        "theme": "Habit Stacking",
        "tip": "One of the best ways to build a new habit is to identify a current habit you already do each day and stack your new behavior on top. Formula: After [CURRENT HABIT], I will [NEW HABIT].",
        "tasks": [
            "Fill out the formula: 'After I [pour my morning coffee/brush my teeth], I will [meditate for 1 min / do 5 pushups].'",
            "Execute your new stacked habit immediately when the cue happens."
        ]
    },
    {
        "day": 4,
        "theme": "Environment Design",
        "tip": "Environment is the invisible hand that shapes human behavior. Make the cues of good habits obvious and visible in your environment, and hide the cues of bad habits.",
        "tasks": [
            "Place an object related to a good habit in plain sight (e.g., a book on your pillow, a water bottle on your desk).",
            "Move a distraction out of sight (e.g., put your phone in another room while working)."
        ]
    },
    {
        "day": 5,
        "theme": "The 2nd Law: Make It Attractive (Craving)",
        "tip": "Temptation bundling pairs an action you want to do with an action you need to do. This leverages dopamine spikes to make hard habits more attractive.",
        "tasks": [
            "Identify one thing you *need* to do today and pair it with something you *want* to do (e.g., only listen to a favorite podcast while folding laundry)."
        ]
    },
    {
        "day": 6,
        "theme": "The 3rd Law: Make It Easy (Response)",
        "tip": "Human behavior follows the Law of Least Effort. We naturally gravitate toward the option that requires the least amount of work. Reduce friction for your good habits.",
        "tasks": [
            "Prime your environment for tomorrow's habit (e.g., lay out your workout clothes tonight, prep your breakfast ahead of time)."
        ]
    },
    {
        "day": 7,
        "theme": "The Two-Minute Rule",
        "tip": "When you start a new habit, it should take less than two minutes to do. A habit must be established before it can be improved. Scale it down down to make it impossible to skip.",
        "tasks": [
            "Scale down a big habit to under 2 minutes (e.g., 'Read for 1 hour' becomes 'Read 1 page').",
            "Perform that 2-minute version today and *stop* right when the timer hits 2 minutes."
        ]
    },
    {
        "day": 8,
        "theme": "The 4th Law: Make It Satisfying (Reward)",
        "tip": "What is immediately rewarded is repeated. What is immediately punished is avoided. Use immediate, artificial rewards to stay motivated while waiting for long-term delays.",
        "tasks": [
            "Create an immediate reward for completing a difficult habit today (e.g., checking off an item, transferring $5 to a vacation fund after a workout)."
        ]
    },
    {
        "day": 9,
        "theme": "Never Miss Twice",
        "tip": "Missing once is an accident. Missing twice is the start of a new bad habit. The first mistake is never what ruins you. It is the spiral of repeated mistakes that follows.",
        "tasks": [
            "If you fall off track with a habit today, commit to a 'micro-version' of it immediately to keep the streak alive.",
            "Write down your plan to prevent a double-miss tomorrow."
        ]
    },
    {
        "day": 10,
        "theme": "Goldilocks Rule & Reflection",
        "tip": "The Goldilocks Rule states that humans experience peak motivation when working on tasks of just manageable difficulty—not too hard, not too easy. Keep adjusting your habits to stay in the zone.",
        "tasks": [
            "Evaluate your current habits: Are any too hard (causing anxiety) or too easy (causing boredom)?",
            "Slightly adjust one habit to match your current skill level perfectly."
        ]
    }
]

# ----------------------------------------------------
# APP STATE MANAGEMENT (Using Streamlit Session State)
# ----------------------------------------------------
if "current_day_index" not in st.session_state:
    st.session_state.current_day_index = 0

# Track completion of tasks using a dictionary keying (day, task_index)
if "completed_tasks" not in st.session_state:
    st.session_state.completed_tasks = {}

# Track total identity votes cast
if "identity_votes" not in st.session_state:
    st.session_state.identity_votes = 0

# Get current day data
day_data = ATOMIC_DATA[st.session_state.current_day_index]

# ----------------------------------------------------
# UI RENDERING
# ----------------------------------------------------
st.title("⚛️ Atomic Habits Companion")
st.subheader("Build systems, not goals. 1% better every day.")

# Sidebar Navigation
st.sidebar.header("Navigation & Stats")
selected_day = st.sidebar.selectbox(
    "Jump to Day:",
    options=[f"Day {d['day']}: {d['theme']}" for d in ATOMIC_DATA],
    index=st.session_state.current_day_index
)
# Update state index based on sidebar selection
new_index = int(selected_day.split(":")[0].replace("Day ", "")) - 1
if new_index != st.session_state.current_day_index:
    st.session_state.current_day_index = new_index
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.metric(label="👤 Total Identity Votes Cast", value=st.session_state.identity_votes)

# Reset Button
if st.sidebar.button("Reset All App Data"):
    st.session_state.completed_tasks = {}
    st.session_state.identity_votes = 0
    st.session_state.current_day_index = 0
    st.rerun()

# Main Application Block
st.markdown(f"### 📅 Day {day_data['day']}: **{day_data['theme']}**")

# Highlighted Daily Tip
st.info(f"**Daily Tip:** {day_data['tip']}")

st.markdown("#### 🎯 Today's Achievable System Tasks")
st.caption("Remember: Keep them small. Make them easy. Focus on action.")

# Render Tasks
all_checked = True
for idx, task in enumerate(day_data['tasks']):
    task_key = f"day_{day_data['day']}_task_{idx}"
    
    # Checkbox state handled via session state to persistent track across reruns
    is_checked = st.checkbox(
        task, 
        key=task_key, 
        value=st.session_state.completed_tasks.get(task_key, False)
    )
    
    # Update local memory
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

# Progress feedback
if all_checked:
    st.success("✨ Incredible work! You successfully optimized your system today. You are 1% better!")
else:
    st.warning("⏳ Complete your micro-steps above to cast your daily identity votes.")

# Day Progression Buttons
st.markdown("---")
col1, col2 = st.columns(2)

with col1:
    if st.session_state.current_day_index > 0:
        if st.button("⬅️ Previous Concept"):
            st.session_state.current_day_index -= 1
            st.rerun()

with col2:
    if st.session_state.current_day_index < len(ATOMIC_DATA) - 1:
        if st.button("Next Concept ➡️"):
            st.session_state.current_day_index += 1
            st.rerun()
    else:
        st.balloons()
        st.markdown("**🎉 You finished the initial 10-day system loop! Restart or keep iterating your environment.**")
