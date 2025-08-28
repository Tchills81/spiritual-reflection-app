import streamlit as st

from app.ui.tabs.reflection_journal import render_tab as render_reflection_journal
from app.ui.tabs.generated_reflection import render_tab as render_tab2
from app.ui.tabs.chat_companion import render_tab as render_chat_companion
from app.ui.tabs.daily_reflection import render_tab as render_daily_reflection
from app.ui.tabs.journey_summary import render_tab as render_journey_summary

from app.utils.dummy_data import generate_dummy_journal
from app.utils.theme_config import THEMES
from app.ui.tabs.styles import styled_tab_button
from app.ui.incons import TONE_CONFIGS, THEME_TO_TONE

# 🌿 Page setup
st.set_page_config(page_title="Spiritual Reflection App", layout="centered")

# 🎨 Theme Initialization
if "active_theme" not in st.session_state:
    st.session_state["active_theme"] = "Gentle"
    st.session_state["theme_config"] = THEMES["Gentle"]
    st.session_state["tone"] = THEME_TO_TONE.get("Gentle", "Neutral")
    st.session_state["tone_config"] = TONE_CONFIGS.get(st.session_state["tone"], TONE_CONFIGS["Neutral"])

theme_choice = st.sidebar.selectbox(
    "🎨 Choose Theme",
    options=list(THEMES.keys()),
    index=list(THEMES.keys()).index(st.session_state["active_theme"])
)

if theme_choice != st.session_state["active_theme"]:
    st.session_state["active_theme"] = theme_choice
    st.session_state["theme_config"] = THEMES[theme_choice]
    st.session_state["tone"] = THEME_TO_TONE.get(theme_choice, "Neutral")
    st.session_state["tone_config"] = TONE_CONFIGS.get(st.session_state["tone"], TONE_CONFIGS["Neutral"])
    st.rerun()

active_theme = st.session_state["theme_config"]

# 🧘 Header
st.markdown(f"""
    <div style='background-color:{active_theme["bg_color"]}; padding:20px; border-radius:12px; text-align:center'>
        <h1 style='color:{active_theme["accent_color"]}; font-family:{active_theme["font_family"]};'>
            🧘 Spiritual Reflection Assistant
        </h1>
        <p style='font-size:18px; color:{active_theme["text_color"]}; font-family:{active_theme["font_family"]};'>
            A space to reflect, restore, and reconnect.
        </p>
    </div>
""", unsafe_allow_html=True)

# 🧪 Sidebar Controls
st.sidebar.markdown(f"""
    <div style='padding:12px; background-color:{active_theme["badge_bg"]}; border-radius:10px; margin-bottom:12px'>
        <label style='font-weight:bold; color:{active_theme["accent_color"]}; font-family:{active_theme["font_family"]};'>
            🧪 Load Test Data
        </label>
    </div>
""", unsafe_allow_html=True)

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

if "active_tab" not in st.session_state:
    st.session_state["active_tab"] = "Inner Compass"

active_tab = st.session_state["active_tab"]

# 🔄 Render styled tab buttons horizontally
cols = st.columns(len(tab_map))
for i, (label, tab_key) in enumerate(tab_map.items()):
    with cols[i]:  # 👈 ensures horizontal layout
        if styled_tab_button(label, tab_key, active_tab, container_key=f"tab_{i}"):
            st.session_state["active_tab"] = tab_key
            st.rerun()

# 🧭 Tab context
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
