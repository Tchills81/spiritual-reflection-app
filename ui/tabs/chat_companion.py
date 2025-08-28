import streamlit as st
from ui.response_engine import ResponseComposer, save_reflection
from utils.reflection_flows import get_prompt_sequence, run_guided_reflection_flow
from ui.incons import tone_icon_map, theme_icon_map, mood_icon_map
from utils.themes import get_themes_by_mode
from ui.tabs.styles import styled_audio_button, styled_text_area, styled_text_input, styled_timeline_block
import pandas as pd
composer = ResponseComposer()



def render_tab():
    st.markdown("## 🗣️ Chat Companion")
    st.markdown("_Talk through your thoughts. I'm here to listen and reflect with you._")

    # 🔹 Session state setup
    st.session_state.setdefault("reflection_mode", "Conversational")
    st.session_state.setdefault("reflection", "")
    st.session_state.setdefault("chat_history", [])
    st.session_state.setdefault("guided_step", 0)
    st.session_state.setdefault("guided_reflections", [])
    st.session_state.setdefault("journal_entries", [])

    mood = "Unspecified"
    mode = st.radio("🧘 Choose Reflection Mode", ["Conversational", "Guided"], horizontal=True)
    st.session_state["reflection_mode"] = mode

    # 🔹 Guided Mode
    if mode == "Guided":
        st.markdown("### 🌿 Guided Reflection")
        mode_key = "evening"
        available_themes = get_themes_by_mode(mode_key)

        theme_key = f"{mode_key}_theme"
        step_key = f"{mode_key}_step"

        if theme_key not in st.session_state or st.session_state.get(step_key, 0) == 0:
            selected_theme = st.selectbox("Choose a theme", available_themes)
            st.session_state[theme_key] = selected_theme
        else:
            selected_theme = st.session_state[theme_key]
            st.markdown(f"**Theme:** 🌱 {selected_theme}")

        tone = "Neutral"  # Optional: make this user-selectable later
        prompts = get_prompt_sequence(selected_theme, mode=mode_key)

        run_guided_reflection_flow(
            theme=selected_theme,
            tone=tone,
            prompts=prompts,
            source="Guided",
            reflection_type="Evening Reflection",
            form_key_prefix="chat_guided",
            state_key_prefix="chat_guided"
        )

    # 🔹 Conversational Mode
    if mode == "Conversational":
        st.markdown("### 💬 Conversational Reflection")

        # Display chat history
        with st.container():
            for exchange in st.session_state["chat_history"]:
                tone = exchange.get("tone", "Unspecified")
                theme = exchange.get("theme", "Unspecified")
                tone_icon = tone_icon_map.get(tone, "❔")
                theme_icon = theme_icon_map.get(theme, "❔")
                mood_icon = mood_icon_map.get(mood, "❔")

                st.markdown(f"**You:** {exchange['user']}")
                st.markdown(f"*Assistant:* {exchange['ai']}")
                st.caption(f"_Mood:_ {mood_icon} {mood} | 🧭 Tone: {tone_icon} {tone} | 🌱 Theme: {theme_icon} {theme}")

        # Input form
        with st.form(key="chat_form"):
            user_input = styled_text_input("Type your reflection or question...", key="chat_input")
            submitted = st.form_submit_button("Send")

        if submitted and user_input.strip():
            result = composer.compose_response(user_input, mode=mode)
            st.session_state["chat_history"].append({
                "user": user_input,
                "ai": result["response"],
                "tone": result["tone"],
                "theme": result["theme"]
            })
            st.rerun()

        # Save last reflection
        if st.session_state["chat_history"]:
            last = st.session_state["chat_history"][-1]
            if st.button("💾 Save Last Reflection to Journal"):
                updated_journal = save_reflection(
                    tone=last["tone"],
                    theme=last["theme"],
                    text=f"**You:** {last['user']}\n\n**Assistant:** {last['ai']}",
                    journal_entries=st.session_state["journal_entries"],
                    source="Soul Exchange",
                    reflection_type="Conversational Insight"
                )
                st.session_state["journal_entries"] = updated_journal
                st.toast("📝 Reflection saved to journal.")

        # Display saved reflections
        if st.session_state["journal_entries"]:
            st.markdown("### 📖 Dialogue Journal")
            st.caption(f"🗂 {len(st.session_state['journal_entries'])} reflections saved")

            for i, entry in enumerate(reversed(st.session_state["journal_entries"])):
                tone = entry.get("tone", "Unspecified")
                theme = entry.get("theme", "Unspecified")
                mood = entry.get("mood", "Unspecified")
                source = entry.get("source", "Chat")
                reflection_type = entry.get("reflection_type", "Conversational Insight")
                text = entry.get("text", "No reflection text available.")
                date = entry.get("timestamp", pd.Timestamp.now())

                # Emotionally styled block
                styled_timeline_block(
                    tone=tone,
                    theme=theme,
                    date=pd.to_datetime(date).strftime("%b %d, %Y"),
                    text=text,
                    key_suffix=f"chat_{i}"
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
