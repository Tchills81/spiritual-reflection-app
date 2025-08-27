import streamlit as st

from ui.tabs.reflection_journal import render_tab as render_reflection_journal
from ui.tabs.generated_reflection import render_tab as render_tab2
from ui.tabs.chat_companion import render_tab as render_chat_companion
from ui.tabs.daily_reflection import render_tab as render_daily_reflection
from ui.tabs.journey_summary import render_tab as render_journey_summary

from utils.dummy_data import generate_dummy_journal

# 🌿 Page setup
st.set_page_config(page_title="Spiritual Reflection App", layout="centered")

# 🧘 Header
st.markdown("<br>", unsafe_allow_html=True)
st.title("🧘 Spiritual Reflection Assistant")
st.markdown("_A space to reflect, restore, and reconnect._")
st.markdown("<br>", unsafe_allow_html=True)

# 🧪 Dummy data trigger
if st.sidebar.button("🧪 Load Dummy Journal"):
    st.session_state["journal_entries"] = generate_dummy_journal()
    st.toast("Dummy journal loaded for testing.")
    st.rerun()
if st.sidebar.button("🎯 Generate Milestone Test Data"):
    from utils.dummy_data import generate_milestone_test_data
    st.session_state["journal_entries"] = generate_milestone_test_data()
    st.toast("Milestone test data loaded.")
    st.rerun()


# 🧭 Tab mapping with emojis
tab_map = {
    "📓 Reflection Journal": "Inner Compass",
    "🌈 Generated Reflection": "Emotional Landscape",
    "💬 Chat Companion": "Soul Exchange",
    "🕊️ Daily Reflection": "Rhythms of the Day",
    "📘 Journey Summary": "Journey Summary"
}

# Initialize default tab
if "active_tab" not in st.session_state:
    st.session_state["active_tab"] = "Inner Compass"

# 🔄 Custom tab bar with styling
tab_labels = list(tab_map.keys())
active_tab = st.session_state["active_tab"]
cols = st.columns(len(tab_labels))

for i, label in enumerate(tab_labels):
    tab_key = tab_map[label]
    is_active = (tab_key == active_tab)

    button_style = f"""
        <style>
        div[data-testid="column-{i}"] button {{
            background-color: transparent;
            border: none;
            color: {'#2c6df2' if is_active else '#444'};
            font-weight: {'600' if is_active else '400'};
            text-decoration: {'underline' if is_active else 'none'};
            transition: all 0.2s ease-in-out;
        }}
        div[data-testid="column-{i}"] button:hover {{
            color: #2c6df2;
            text-decoration: underline;
        }}
        </style>
    """
    st.markdown(button_style, unsafe_allow_html=True)

    if cols[i].button(label):
        st.session_state["active_tab"] = tab_map[label]
        st.rerun()

# Optional: display current tab context
st.caption(f"🧭 You’re exploring: **{st.session_state['active_tab']}**")

# ✅ Render tab content
if st.session_state["active_tab"] == "Inner Compass":
    render_reflection_journal()
elif st.session_state["active_tab"] == "Emotional Landscape":
    render_tab2()
elif st.session_state["active_tab"] == "Soul Exchange":
    render_chat_companion()
elif st.session_state["active_tab"] == "Rhythms of the Day":
    render_daily_reflection()
elif st.session_state["active_tab"] == "Journey Summary":
    render_journey_summary()
