import streamlit as st
import pandas as pd
import plotly.express as px
from collections import Counter

from ui.incons import tone_icon_map, theme_icon_map, MILESTONE_MICROCOPY, TONE_COLORS
from utils.milestone_utils import detect_milestones
from ui.tabs.styles import styled_badge, styled_caption, styled_timeline_block


def render_tab():
    st.markdown("## 📘 Journey Summary")
    st.markdown("_Your emotional landscape, milestones, and reflections in one place._")

    journal = st.session_state.get("journal_entries", [])
    if not journal:
        st.info("No reflections yet—your journey summary will appear here once you begin.")
        return

    df = pd.DataFrame(journal)

    # 🛡️ Ensure 'date' column exists
    if "date" not in df.columns:
        st.warning("Your reflections don’t include timestamps yet. Tone evolution and timeline features will be limited.")
        df["date"] = pd.Timestamp.now()

    df["date"] = pd.to_datetime(df["date"])
    df["date_str"] = df["date"].dt.strftime("%Y-%m-%d")

    # 🔹 Animated Tone Evolution Chart
    tone_time_counts = df.groupby(["date_str", "tone"]).size().reset_index(name="Frequency")
    tone_time_counts["Tone"] = tone_time_counts["tone"].apply(lambda t: f"{tone_icon_map.get(t, '')} {t}")

    tone_color_map = {
        f"{tone_icon_map.get(t)} {t}": TONE_COLORS.get(t, "#999999")
        for t in df["tone"].unique()
    }

    tone_fig = px.bar(
        tone_time_counts,
        x="Tone",
        y="Frequency",
        color="Tone",
        animation_frame="date_str",
        title="Tone Evolution Over Time",
        color_discrete_map=tone_color_map
    )
    st.plotly_chart(tone_fig, use_container_width=True)

    # 🔹 Dynamic Caption for Top Tone
    top_tone_raw = df["tone"].value_counts().idxmax()
    top_tone_icon = tone_icon_map.get(top_tone_raw, "")
    st.caption(f"{top_tone_icon} You’ve reflected most often with a **{top_tone_raw}** tone—emotionally attuned and resonant.")

    # 🔹 Theme Frequency Chart
    theme_counts = df["theme"].value_counts().reset_index()
    theme_counts.columns = ["Theme", "Frequency"]
    theme_counts["Theme"] = theme_counts["Theme"].apply(lambda t: f"{theme_icon_map.get(t, '')} {t}")

    theme_fig = px.bar(
        theme_counts,
        x="Theme",
        y="Frequency",
        color="Theme",
        title="Theme Frequency",
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    st.plotly_chart(theme_fig, use_container_width=True)

    # 🔹 Summary Block
    top_theme_raw = theme_counts.iloc[0]["Theme"].split(" ", 1)[-1] if not theme_counts.empty else "your reflections"
    summary_text = f"You've reflected with depth and warmth. Themes of {top_theme_raw.lower()} have guided your journey."
    st.markdown(f"""
        <div style='background-color:#f0f8ff; padding:16px; border-radius:12px; font-size:16px'>
            <span style='font-size:24px'>🌱</span> {summary_text}
        </div>
    """, unsafe_allow_html=True)

    # 🔹 Milestone Detection
    milestones = detect_milestones(journal)
    if milestones:
        tone_count = len(set(df["tone"]))
        total_reflections = len(journal)
        st.markdown("### 🏁 Milestones Reached")
        st.caption(f"Milestone triggered by {total_reflections} reflections across {tone_count} tones.")

        theme_counts_raw = Counter([entry["theme"] for entry in journal])
        top_theme, top_count = theme_counts_raw.most_common(1)[0]
        theme_icon = theme_icon_map.get(top_theme, "🛡️")
        st.markdown(f"{theme_icon} You’ve explored **{top_theme}** in {top_count} reflections.")

        milestone_icons = {
            "First Reflection": "📝",
            "Tone Shift": "🎭",
            "Theme Cluster": "🌿",
            "Export Ready": "📦"
        }

        cols = st.columns(len(milestones))
        for i, milestone in enumerate(milestones):
            icon = milestone_icons.get(milestone, "🏁")
            with cols[i]:
                styled_badge(label=milestone, icon=icon, key_suffix=f"milestone_{i}")
                tone = st.session_state.get("tone", "Neutral")
                caption = MILESTONE_MICROCOPY.get(milestone, {}).get(tone, "")
                if caption:
                    styled_caption(caption, key_suffix=f"{milestone}_caption")
    else:
        st.info("No milestones yet—your journey is just beginning.")

    # 🔹 Reflection Timeline
    st.markdown("### 🧭 Reflection Timeline")
    df_sorted = df.sort_values(by="date")
    for i, row in df_sorted.iterrows():
        styled_timeline_block(
            tone=row["tone"],
            theme=row["theme"],
            date=pd.to_datetime(row["date"]).strftime("%b %d, %Y"),
            text=row.get("text", "No reflection text available."),
            key_suffix=f"timeline_{i}"
        )
