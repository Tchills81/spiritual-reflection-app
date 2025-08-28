import streamlit as st
from datetime import datetime
from io import BytesIO
from gtts import gTTS

from utils.reflection_flows import get_prompt_sequence, run_guided_reflection_flow, play_ambient_music
from ui.response_engine import generate_affirmation, save_reflection
from ui.incons import tone_icon_map, theme_icon_map, mood_icon_map
from utils.themes import get_themes_with_icons
from ui.tabs.styles import  styled_timeline_block
import pandas as pd


def play_audio(text: str) -> BytesIO:
    audio_buffer = BytesIO()
    gTTS(text).write_to_fp(audio_buffer)
    audio_buffer.seek(0)
    return audio_buffer

  # 👈 ensure this is imported

def render_tab():
    st.markdown("## 🌅 Daily Reflection")
    st.caption("Begin your day with intention and emotional clarity.")

    # 🔹 Session state setup
    st.session_state.setdefault("journal_entries", [])
    st.session_state.setdefault("daily_reflection", "")
    st.session_state.setdefault("daily_reflections", [])
    st.session_state.setdefault("daily_step", 0)
    st.session_state.setdefault("daily_reflection_text", "")
    st.session_state.setdefault("daily_reflection_affirmation", "")

    # 🔹 Tone + Theme selection
    tone = st.selectbox("Choose a tone", ["Gentle", "Empowering", "Neutral", "Philosophical"], key="daily_tone")
    theme_label = st.selectbox("Choose a theme", get_themes_with_icons("daily"), key="daily_theme")
    theme = theme_label.split(" ", 1)[-1]

    # 🔹 Prompt sequence
    prompts = get_prompt_sequence(theme, mode="daily")

    run_guided_reflection_flow(
        theme=theme,
        tone=tone,
        prompts=prompts,
        source="Rhythms of the Day",
        reflection_type="Morning Reflection",
        form_key_prefix="daily_reflection",
        state_key_prefix="daily_reflection"
    )

    # 🔹 Affirmation playback
    if not st.session_state["daily_reflection_affirmation"] and st.button("✨ Generate Affirmation", key="daily_affirmation"):
        affirmation = generate_affirmation(prompts[0], tone=tone, theme=theme)
        st.session_state["daily_reflection_affirmation"] = affirmation
        st.markdown(f"### {tone_icon_map[tone]} Your Affirmation\n_{affirmation}_")
        play_ambient_music(tone)

    if st.session_state["daily_reflection_affirmation"]:
        if st.button("🔊 Play Affirmation", key="daily_play"):
            audio_buffer = play_audio(st.session_state["daily_reflection_affirmation"])
            st.audio(audio_buffer, format="audio/wav", autoplay=True)

    # 🔹 Save logic
    if st.session_state["daily_reflection_text"].strip():
        st.markdown(f"### {tone_icon_map[tone]} Your Reflection\n_{st.session_state['daily_reflection_text']}_")

        if st.button("💾 Save Reflection", key="daily_save"):
            updated_journal = save_reflection(
                tone=tone,
                theme=theme,
                text=st.session_state["daily_reflection_text"],
                journal_entries=st.session_state["journal_entries"],
                mood="Unspecified",
                source="Rhythms of the Day",
                reflection_type="Morning Reflection"
            )
            st.session_state["journal_entries"] = updated_journal
            st.toast("📝 Reflection saved to journal.")
    else:
        st.warning("No reflection entered yet.")

    # 🔹 Journal display
    if st.session_state["journal_entries"]:
        st.markdown("### 📖 Dialogue Journal")
        st.caption(f"🗂 {len(st.session_state['journal_entries'])} reflections saved")

        for i, entry in enumerate(reversed(st.session_state["journal_entries"])):
            tone = entry.get("tone", "Unspecified")
            theme = entry.get("theme", "Unspecified")
            mood = entry.get("mood", "Unspecified")
            source = entry.get("source", "Daily")
            reflection_type = entry.get("reflection_type", "Morning Reflection")
            text = entry.get("text", "No reflection text available.")
            date = entry.get("timestamp", pd.Timestamp.now())

            # Emotionally styled block
            styled_timeline_block(
                tone=tone,
                theme=theme,
                date=pd.to_datetime(date).strftime("%b %d, %Y"),
                text=text,
                key_suffix=f"daily_{i}"
            )

            # Original metadata preserved
            tone_icon = tone_icon_map.get(tone, "❔")
            theme_icon = theme_icon_map.get(theme, "❔")
            mood_icon = mood_icon_map.get(mood, "❔")

            st.caption(f"""
            🕒 {pd.to_datetime(date).strftime('%H:%M %p')}  
            _Mood:_ {mood_icon} {mood} | 🧭 Tone: {tone_icon} {tone} | 🌱 Theme: {theme_icon} {theme}
            """)
            st.caption(f"📍 Source: {source} | 🧠 Type: {reflection_type}")
            st.markdown("---")
