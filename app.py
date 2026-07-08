# ----------------------------------------------------
# INPUT INTERFACE
# ----------------------------------------------------
st.markdown('<div class="section-header">🧬 Define System Architecture</div>', unsafe_allow_html=True)

user_input = st.text_input(
    "Target Identity Focus",
    placeholder="e.g., Deep Work Focused Engineer, Intentional Writer...",
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
        st.session_state.generated_tasks = generate_atomic_tasks(user_notes, user_input)
        st.session_state.completed_tasks = {}
        st.rerun()
    else:
        st.error("Operational target required. Please input a target identity focus.")
