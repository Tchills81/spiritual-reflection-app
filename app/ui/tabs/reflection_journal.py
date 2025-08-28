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
from ui.incons import tone_icon_map, theme_icon_map, CAPTION_ICONS
from ui.response_engine import generate_affirmation
from streamlit_extras.stylable_container import stylable_container
from ui.tabs.styles import styled_audio_button, styled_text_area, styled_icon_button, styled_caption

# 🔹 Utility functions
def clean_tone(tone_str):
    return re.sub(r"[^\w\s]", "", tone_str).strip()

def clean_theme(theme_str):
    return re.sub(r"[^\w\s]", "", theme_str).strip()

def save_reflection(tone, theme, text, journal_entries, mood="Unspecified", source="Reflection", reflection_type="Freeform"):
    new_entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "tone": tone,
        "theme": theme,
        "text": text.strip(),
        "mood": mood,
        "source": source,
        "reflection_type": reflection_type
    }
    return journal_entries + [new_entry]

# 🔹 Chart and summary rendering
def plot_journal_entries(df):
    df["clean_theme"] = df["theme"].apply(clean_theme)
    df["clean_tone"] = df["tone"].apply(clean_tone)

    # 🔹 Frequency counts
    theme_counts = df["clean_theme"].value_counts().reset_index()
    tone_counts = df["clean_tone"].value_counts().reset_index()
    theme_counts.columns = ["Theme", "Count"]
    tone_counts.columns = ["Tone", "Count"]

    # 🔹 Icon labels
    theme_counts["Theme"] = theme_counts["Theme"].apply(lambda t: f"{theme_icon_map.get(t, '')} {t}")
    tone_counts["Tone"] = tone_counts["Tone"].apply(lambda t: f"{tone_icon_map.get(t, '')} {t}")

    # 🔹 Charts with distinct palettes
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 🌱 Theme Frequency")
        theme_fig = px.bar(
            theme_counts,
            x="Theme",
            y="Count",
            color="Theme",
            title="Theme Frequency",
            color_discrete_sequence=px.colors.qualitative.Pastel1
        )
        st.plotly_chart(theme_fig, use_container_width=True)

    with col2:
        st.markdown("### 🎼 Tone Frequency")
        tone_fig = px.bar(
            tone_counts,
            x="Tone",
            y="Count",
            color="Tone",
            title="Tone Frequency",
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        st.plotly_chart(tone_fig, use_container_width=True)

    # 🔹 Top theme summary
    if not theme_counts.empty:
        top_theme = theme_counts.iloc[0]["Theme"]
        raw_theme = top_theme.split(" ", 1)[-1]
        icon = theme_icon_map.get(raw_theme, "❔")
        st.caption(f"🧘 Your reflections lean toward {icon} **{raw_theme}** this week.")
    else:
        

        st.caption("🧘 No reflections yet—your journey begins here.")


def render_export_summary(tab_key):
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("📤 Export Journal", key=f"{tab_key}_journal"):
            df = pd.DataFrame(st.session_state["journal_entries"])
            st.dataframe(df)
    with col2:
        if st.button("🧠 Generate Summary", key=f"{tab_key}_summary"):
            engine = ReflectionSummaryEngine(st.session_state["journal_entries"])
            st.markdown("#### 🧠 Emotional Summary & Guidance")
            st.markdown(f"""
                <div style='background-color:#f0f8ff; padding:12px; border-radius:10px'>
                {engine.generate_summary()}
                </div>
            """, unsafe_allow_html=True)
            st.markdown("#### 🏁 Reflection Milestones")
            milestones = detect_reflection_milestones(st.session_state["journal_entries"])
            if milestones:
                for m in milestones:
                    st.markdown(f"- {m}")
            else:
                st.info("No milestones yet—your journey is just beginning.")

def render_tab():
    st.markdown("_Capture your thoughts, moods, and affirmations in a space that listens._")
    st.caption("This space helps you explore your emotional journey through tone, theme, and guided insights.")

    with st.expander("🧭 How to Use This Space", expanded=False):
        st.markdown("""
        - **📊 Emotional Insights**: See how your tone and themes evolve over time.
        - **🌱 Theme Frequency**: Discover which themes you return to most often.
        - **🧭 Begin a New Journey**: Tap into recurring themes to start a guided reflection.
        - **📅 Emotional Timeline**: Track shifts in tone across your recent reflections.
        - **🧠 Reflective Guidance**: Receive gentle advice based on your emotional patterns.
        - **📖 Dialogue Journal**: Review your saved reflections and emotional history.
        """)

    st.session_state.setdefault("journal_entries", [])
    st.session_state.setdefault("reflection", "")

    entries = st.session_state["journal_entries"]
    if entries:
        df = pd.DataFrame(entries).sort_values("timestamp")
        plot_journal_entries(df)

    from ui.tabs.styles import styled_selectbox

    mood = styled_selectbox("How are you feeling right now?", ["Calm", "Anxious", "Grateful", "Reflective", "Heavy"], key="mood_select")
    tone = styled_selectbox("Hello a tone for your reflection:", ["Gentle", "Empowering", "Philosophical", "Neutral"], key="tone_select")
    theme_label = styled_selectbox("What theme best fits your moment?", get_themes_with_icons("guided"), key="theme_select")
    theme = theme_label.split(" ", 1)[-1]
    

    reflection_text = styled_text_area("Write your reflection here...", key="journal_reflection", height=200)

    st.markdown("___")  # subtle horizontal line


    # ✨ Generate Affirmation
    if styled_icon_button("generate_affirmation", key_suffix="tab1_generate"):
        affirmation = generate_affirmation(reflection_text, tone, theme)
        st.session_state["affirmation"] = affirmation
        st.markdown(f"### {tone_icon_map[tone]} Your Affirmation\n_{affirmation}_")
        play_ambient_music(tone)
        #st.caption("Now that your affirmation is ready, you can listen or save it below.")
        icon = CAPTION_ICONS.get("audio_hint", "🔘")
        styled_caption(f"{icon} Now that your affirmation is ready, you can listen or save it below.", key_suffix="audio_hint")
    else:
        # Always display affirmation if it exists
        if "affirmation" in st.session_state:
           st.markdown(f"### {tone_icon_map[tone]} Your Affirmation\n_{st.session_state['affirmation']}_")


    st.markdown("___")  # subtle horizontal line
   


    # 🔊 Play + 💾 Save (side by side)
    if "affirmation" in st.session_state:
        # Reserve space for audio playback to prevent layout shift
        audio_slot = st.empty()

        col1, col2 = st.columns([1, 1])

    

        with col1:
             if styled_audio_button("play_affirmation", st.session_state["affirmation"], "tab1_play"):
               
               styled_caption("🔊 Playing your affirmation...", key_suffix="audio_caption")


        with col2:
            if styled_icon_button("save", key_suffix="tab1_save"):
                if reflection_text.strip():
                    journal = st.session_state.get("journal_entries", [])
                    updated_journal = save_reflection(
                        tone=tone,
                        theme=theme,
                        text=reflection_text,
                        journal_entries=journal,
                        mood=mood,
                        source="Inner Compass",
                        reflection_type="Guided Reflection"
                    )
                    st.session_state["journal_entries"] = updated_journal
                    st.toast("📝 Reflection saved to journal.")
                else:
                    st.warning("Reflection cannot be empty.")


      


