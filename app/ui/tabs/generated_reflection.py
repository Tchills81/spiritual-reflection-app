import streamlit as st
import pandas as pd
import re
from datetime import datetime, timedelta
from io import BytesIO
from gtts import gTTS
import plotly.express as px

from utils.themes import get_themes_with_icons
from utils.reflection_summary_engine import ReflectionSummaryEngine
from utils.reflection_flows import play_ambient_music
from utils.milestone_utils import detect_reflection_milestones
from ui.incons import tone_icon_map, theme_icon_map, mood_icon_map, affirmation_map
from ui.response_engine import generate_affirmation
from ui.response_engine import generate_reflection
from gtts import gTTS
from io import BytesIO
from ui.response_engine import generate_reflection, save_reflection
# Optional: export and summary
from ui.tabs.reflection_journal import render_export_summary

def get_weekly_themes(journal):
    cutoff = datetime.now() - timedelta(days=7)
    recent = [e for e in journal if pd.to_datetime(e["timestamp"]) >= cutoff]
    themes = [e.get("theme") for e in recent if e.get("theme")]
    return sorted(set(themes), key=lambda t: themes.count(t), reverse=True)

# 🔹 Weekly chaining prompt generator
def generate_weekly_chain_prompt(theme):
    return [
        f"What has {theme.lower()} meant to you this week?",
        f"Is there a moment that deepened your sense of {theme.lower()}?",
        f"What intention will guide your {theme.lower()} next week?"
    ]

# 🔹 Weekly chaining renderer
def render_weekly_chaining():
    st.markdown("## 🔄 Weekly Journey Chaining")
    journal = st.session_state.get("journal_entries", [])
    weekly_themes = get_weekly_themes(journal)

    if weekly_themes:
        top_theme = weekly_themes[0]
        icon = theme_icon_map.get(top_theme, "❔")
        st.caption(f"Your reflections this week centered around {icon} **{top_theme}**.")
        st.markdown(f"🌿 This week, your reflections echoed with **{top_theme}**. Let’s gently continue that journey.")
        count = sum(1 for e in journal if e.get("theme") == top_theme)
        st.caption(f"🗂 {count} reflections explored **{top_theme}** this week.")

        prompts = generate_weekly_chain_prompt(top_theme)
        affirmation = generate_affirmation(prompts[0], theme=top_theme, tone="Gentle")
        st.markdown(f"💬 *Affirmation:* {affirmation}")

        for i, prompt in enumerate(prompts):
            st.markdown(f"**{i+1}.** {prompt}")

        tones = [e["tone"] for e in journal if e.get("theme") == top_theme]
        tone_summary = ", ".join(sorted(set(tones)))
        st.caption(f"Your reflections on **{top_theme}** carried tones of {tone_summary}.")

        if st.button("🧭 Begin Weekly Reflection", key="weekly_launch"):
            st.session_state.update({
                "selected_theme": top_theme,
                "mode": "guided",
                "step": 0,
                "active_tab": "Rhythms of the Day"
            })
            st.rerun()
    else:
        st.info("No reflections found from the past week.")

def render_tab():
    st.markdown("## 🌈 Generated Reflection")
    st.markdown("_Let the assistant guide you into deeper insight._")

    # Developer tool: dummy journal generator
    if st.button("🧪 Generate Dummy Journal Data"):
        from utils.dummy_data import generate_dummy_journal
        st.session_state["journal_entries"] = generate_dummy_journal()
        st.success("Dummy journal data generated for the past 7 days.")
        st.rerun()

    # Weekly chaining section
    render_weekly_chaining()

    # Layout: Reflection Generator + Tone-Based Filtering side by side
    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("### 🧠 Generate a New Reflection")

        tone = st.selectbox("Choose a tone:", ["Gentle", "Empowering", "Philosophical", "Neutral"], key="tab2_tone")
        theme_label = st.selectbox("Explore your weekly journey:", get_themes_with_icons("weekly"), key="tab2_theme")
        theme = theme_label.split(" ", 1)[-1]
        length = st.radio("Reflection length:", ["Short", "Medium", "Long"], index=0, key="tab2_length")
        backend = st.selectbox("Choose backend:", ["Auto", "Simple", "Advanced"], index=0, key="tab2_backend")

        st.session_state.setdefault("reflection", "")

        if st.button("🧠 Generate Reflection", key="tab2_generate"):
            reflection = generate_reflection(tone, theme, length, backend)
            st.session_state["reflection"] = reflection
            st.markdown(f"### {tone_icon_map[tone]} Your Reflection\n_{reflection}_")
            play_ambient_music(tone)

        if st.session_state["reflection"]:
            if st.button("🔊 Play Reflection", key="tab2_play"):
                audio_buffer = play_audio(st.session_state["reflection"])
                st.audio(audio_buffer, format="audio/wav", autoplay=True)

            if st.button("💾 Save Reflection", key="tab2_save"):
                journal = st.session_state.get("journal_entries", [])
                updated_journal = save_reflection(
                    tone=tone,
                    theme=theme,
                    text=st.session_state["reflection"],
                    journal_entries=journal,
                    source="Emotional Landscape",
                    reflection_type="Weekly Summary"
                )
                st.session_state["journal_entries"] = updated_journal
                st.toast("📝 Reflection saved to journal.")

    with col2:
        st.markdown("### 🎨 Filter Reflections by Tone")
        selected_tone = st.selectbox("Select tone to explore:", ["Gentle", "Empowering", "Philosophical", "Neutral"], key="tab2_filter")

        filtered = [
            e for e in st.session_state.get("journal_entries", [])
            if e.get("tone") == selected_tone
        ]

        if filtered:
            for entry in reversed(filtered[:3]):
                st.caption(f"""
                🕒 {entry['timestamp']}  
                🌱 Theme: {entry.get('theme', 'Unspecified')}  
                > {entry['text']}
                """)
                st.markdown("---")
        else:
            st.info(f"No reflections found with tone: {selected_tone}")

    # Full journal viewer
    if st.session_state["journal_entries"]:
        st.markdown("### 📖 Dialogue Journal")
        st.caption("A living archive of your emotional and spiritual journey.")

        for entry in reversed(st.session_state["journal_entries"]):
            tone = entry.get("tone", "Unspecified")
            theme = entry.get("theme", "Unspecified")
            length = entry.get("length", "Unspecified")

            tone_icon = tone_icon_map.get(tone, "❔")
            theme_icon = theme_icon_map.get(theme, "❔")

            st.caption(f"""
            **🕒 {entry['timestamp']}**  
            🧭 Tone: {tone_icon} {tone} | 🌱 Theme: {theme_icon} {theme} | 📏 Length: {length}  
            > {entry['text']}
            """)
            st.markdown("---")

        
        render_export_summary("tab2")




def play_audio(text: str) -> BytesIO:
    """
    Converts text to speech and returns an in-memory audio buffer.
    """
    audio_buffer = BytesIO()
    tts = gTTS(text)
    tts.write_to_fp(audio_buffer)
    audio_buffer.seek(0)
    return audio_buffer
