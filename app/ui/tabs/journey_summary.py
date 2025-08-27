import streamlit as st
import pandas as pd
import plotly.express as px
from collections import Counter

from ui.incons import tone_icon_map, theme_icon_map
from utils.milestone_utils import detect_milestones

def render_tab():
    st.markdown("## 📘 Journey Summary")
    st.markdown("_Your emotional landscape, milestones, and reflections in one place._")

    journal = st.session_state.get("journal_entries", [])

    if not journal:
        st.info("No reflections yet—your journey summary will appear here once you begin.")
        return

    df = pd.DataFrame(journal)

    # 🔹 Tone Frequency
    tone_counts = df["tone"].value_counts().reset_index()
    tone_counts.columns = ["Tone", "Frequency"]
    tone_counts["Tone"] = tone_counts["Tone"].apply(lambda t: f"{tone_icon_map.get(t, '')} {t}")
    tone_fig = px.bar(
        tone_counts,
        x="Tone",
        y="Frequency",
        color="Tone",
        title="Tone Frequency",
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    st.plotly_chart(tone_fig, use_container_width=True)

    # 🔹 Theme Frequency
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
        # Trigger summary
        tone_count = len(set(df["tone"]))
        total_reflections = len(journal)
        st.markdown("### 🏁 Milestones Reached")
        st.caption(f"Milestone triggered by {total_reflections} reflections across {tone_count} tones.")

        # Theme depth summary
        theme_counts_raw = Counter([entry["theme"] for entry in journal])
        top_theme, top_count = theme_counts_raw.most_common(1)[0]
        theme_icon = theme_icon_map.get(top_theme, "🛡️")
        st.markdown(f"{theme_icon} You’ve explored **{top_theme}** in {top_count} reflections.")

        # Milestone badges with icons
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
                st.markdown(f"""
                    <div style='text-align:center; padding:8px; background-color:#e6f7ff; border-radius:8px'>
                        <span style='font-size:20px'>{icon}</span><br>
                        <strong>{milestone}</strong>
                    </div>
                """, unsafe_allow_html=True)
    else:
        st.info("No milestones yet—your journey is just beginning.")
