import streamlit as st
import pandas as pd

from datetime import datetime, timedelta

from utils.dummy_data import generate_dummy_journal
from utils.milestone_utils  import detect_reflection_milestones  

from ui.response_engine import (
    generate_affirmation, 
    save_reflection,
    generate_reflection,
    ResponseComposer
    )
from utils.reflection_summary_engine import ReflectionSummaryEngine
from utils.reflection_flows import (
    run_guided_reflection_flow,
    get_reflection_mode_by_time,
    get_prompt_sequence, 
    mode_sequences, 
    weekly_sequences,
    play_ambient_music,
    )


from ui.incons import(
    ambient_track_map, 
    mood_icon_map,
    affirmation_map
    )
from utils.themes import get_themes_by_mode, get_themes_with_icons

import re

def clean_tone(tone_str):
    return re.sub(r"[^\w\s]", "", tone_str).strip()


def clean_theme(theme_str):
    # Remove emoji and extra spaces
    return re.sub(r"[^\w\s]", "", theme_str).strip()




from ui.incons import tone_icon_map, theme_icon_map
import plotly.express as px

def plot_journal_entries(df):
    import plotly.express as px
    from datetime import datetime, timedelta
    import pandas as pd

    # Clean theme and tone
    df["clean_theme"] = df["theme"].apply(clean_theme)
    df["clean_tone"] = df["tone"].apply(clean_tone)

    # Initialize engine
    engine = ReflectionSummaryEngine(st.session_state["journal_entries"])
    advice = engine.generate_advice()
    timeline = engine.get_timeline()
    tone = engine.get_top_tone()

    # Icon maps
    tone_icon_map = {
        "Gentle": "🌸", "Empowering": "🔥", "Neutral": "🌿", "Philosophical": "🧠", "Unspecified": "❔"
    }
    theme_icon_map = {
        "Forgiveness": "💗", "Resilience": "🛡️", "Spirituality": "✨",
        "Healing": "🌊", "Identity": "🧬", "Growth": "🌱", "Courage": "🦁", "Unspecified": "❔"
    }
    affirmation_map = {
        "Gentle": "You are enough, just as you are.",
        "Empowering": "Your strength is your compass.",
        "Neutral": "Your presence brings balance.",
        "Philosophical": "Your thoughts illuminate the path.",
        "Unspecified": "Your journey matters."
    }

    # Tone over time scatter
    st.markdown("### 📊 Emotional Insights")
    st.caption("Your tone journey across saved reflections.")
    tone_chart = px.scatter(
        df,
        x="timestamp",
        y="clean_tone",
        color="clean_tone",
        title="🧭 Tone Over Time",
        labels={"timestamp": "Date", "clean_tone": "Tone"},
        height=300
    )
    st.plotly_chart(tone_chart, use_container_width=True)

    # Frequency counts
    theme_counts = df["clean_theme"].value_counts().reset_index()
    tone_counts = df["clean_tone"].value_counts().reset_index()
    theme_counts.columns = ["Theme", "Count"]
    tone_counts.columns = ["Tone", "Count"]

    theme_counts["Theme"] = theme_counts["Theme"].apply(lambda t: f"{theme_icon_map.get(t, '')} {t}")
    tone_counts["Tone"] = tone_counts["Tone"].apply(lambda t: f"{tone_icon_map.get(t, '')} {t}")

    # Side-by-side charts
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 🌱 Theme Frequency")
        theme_chart = px.bar(theme_counts, x="Theme", y="Count", color="Theme", height=300)
        st.plotly_chart(theme_chart, use_container_width=True)

    with col2:
        st.markdown("### 🎼 Tone Frequency")
        tone_chart = px.bar(tone_counts, x="Tone", y="Count", color="Tone", height=300)
        st.plotly_chart(tone_chart, use_container_width=True)

    # Most common theme
    if not theme_counts.empty:
        top_theme = theme_counts.iloc[0]["Theme"]
        icon = theme_icon_map.get(top_theme.split(" ")[-1], "❔")
        st.caption(f"🧘 Your reflections lean toward {icon} **{top_theme}** this week.")
    else:
        st.caption("🧘 No reflections yet—your journey begins here.")

    # Clickable theme launch
    st.markdown("### 🧭 Begin a New Journey")
    st.caption("Tap a theme to start a guided reflection.")

    top_themes = theme_counts["Theme"].head(5)

    for theme in top_themes:
        raw_theme = theme.split(" ", 1)[-1]  # Strip emoji if present
        icon = theme_icon_map.get(raw_theme, "❔")
        label = f"{icon} {raw_theme}"

        if st.button(label, key=f"start_{raw_theme}"):
        # 🔍 Find source from journal entries
           journal = st.session_state.get("journal_entries", [])
           matching_entries = [e for e in journal if e.get("theme") == raw_theme]
           source = matching_entries[-1]["source"] if matching_entries else "Reflection"
           st.caption(f"🧭 Starting a guided journey on **{raw_theme}** from your last {source} entry.")

        # 🧭 Launch guided journey
           st.session_state["selected_theme"] = raw_theme
           st.session_state["mode"] = "guided"
           st.session_state["step"] = 0
           st.session_state["journey_history"] = []

           st.session_state["reflection_context"] = {
            "theme": raw_theme,
            "tone": engine.get_top_tone(),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "source": source
         }

        # 🗂 Route to correct tab
           st.session_state["active_tab"] = source
           st.rerun()




    # Emotional timeline
    st.markdown("### 📅 Emotional Timeline")
    st.caption("Tone shifts across your recent reflections.")
    try:
        df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
        df = df.dropna(subset=["timestamp"])
        df["date"] = df["timestamp"].dt.date

        cutoff = datetime.now().date() - timedelta(days=7)
        recent_df = df[df["date"] >= cutoff]

        timeline_df = recent_df.groupby(["date", "clean_tone"]).size().reset_index(name="Count")
        pivot_df = timeline_df.pivot(index="date", columns="clean_tone", values="Count").fillna(0)

        if pivot_df.empty:
            st.caption("📅 Not enough data to show emotional shifts—here’s a tone snapshot instead.")
            st.bar_chart(df["clean_tone"].value_counts())
        else:
            st.line_chart(pivot_df)
    except Exception as e:
        st.caption("📅 Timeline unavailable—your reflections will appear here as they grow.")
        st.write("⚠️ Debug info (optional):", str(e))

    # Reflective guidance
    st.markdown("### 🧠 Reflective Guidance")
    st.caption("Gentle advice based on your recent tone and theme patterns.")
    st.markdown(f"""
        <div style='background-color:#f9f9f9; padding:12px; border-radius:10px'>
        <strong>📅 {timeline}</strong><br>
        <em>💬 {advice}</em>
        </div>
    """, unsafe_allow_html=True)

    affirmation = affirmation_map.get(tone, "Your journey matters.")
    st.markdown(f"🌟 _{affirmation}_")



def render_reflection_journal():

    import pandas as pd
    
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



    if "journal_entries" not in st.session_state:
       st.session_state["journal_entries"] = []

    if "reflection" not in st.session_state:
       st.session_state["reflection"] = ""




    entries = st.session_state.get("journal_entries", [])
    if entries:
       df = pd.DataFrame(entries)
       df["timestamp"] = pd.to_datetime(df["timestamp"])
       df = df.sort_values("timestamp")
       plot_journal_entries(df)


    # Mood selector
    mood = st.selectbox("How are you feeling right now?", ["Calm", "Anxious", "Grateful", "Reflective", "Heavy"])

    # Tone selector
    tone = st.selectbox("Choose a tone for your reflection:", ["Gentle", "Empowering", "Philosophical", "Neutral"])

    # Theme selector
    #theme = st.selectbox("What theme best fits your moment?", get_themes_by_mode("guided"))

    theme_label = st.selectbox("What theme best fits your moment?", get_themes_with_icons("guided"))
    theme = theme_label.split(" ", 1)[-1]


    # Reflection input
    reflection_text = st.text_area("Write your reflection here...", height=200)

    if st.button("✨ Generate Affirmation", key="tab1_generate"):
       affirmation = generate_affirmation(reflection_text, tone, theme)
       st.session_state["affirmation"] = affirmation
       
      # st.markdown(f"### {tone_icon_map[tone]} Affirmation")
       st.markdown(f"### {tone_icon_map[tone]} Your Affirmation\n_{affirmation}_")
       
       play_ambient_music(tone)
       


    if "affirmation" in st.session_state:
        if st.button("### 🔊 Play Affirmation", key="tab1_play"):
          audio_buffer = play_audio(st.session_state["affirmation"])
          
          st.audio(audio_buffer, format="audio/wav", autoplay=True)
    

    # Reflection preview
    if reflection_text.strip():
        #st.caption("📝 Reflection Preview")
       # st.markdown(f"_{reflection_text}_")
        st.markdown(f"### {tone_icon_map[tone]} Your Reflection\n_{reflection_text}_")
          
    
    else:
        st.warning("No reflection entered yet.")

            


    # Save reflection
    if st.button("### 💾 Save Reflection", key="tab1_save"):
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

    # Display saved reflections (always visible if entries exist)
    if "journal_entries" in st.session_state and st.session_state["journal_entries"]:
        st.markdown("### 📖 Dialogue Journal")
        st.caption("A living archive of your emotional and spiritual journey.")

        st.caption(f"🗂 {len(st.session_state['journal_entries'])} reflections saved")

        for entry in reversed(st.session_state["journal_entries"]):
            mood = entry.get("mood", "Unspecified")
            tone = entry.get("tone", "Unspecified")
            theme = entry.get("theme", "Unspecified")

            tone_icon = tone_icon_map.get(tone, "❔")
            theme_icon = theme_icon_map.get(theme, "❔")
            mood_icon = mood_icon_map.get(mood, "❔")
            
            st.caption(f"""
            **🕒 {entry['timestamp']}**  
            _Mood:_ {mood_icon} {mood}" | 🧭 Tone: {tone_icon} {tone} | 🌱 Theme: {theme_icon} {theme}  
            > {entry['text']}
            """)
            st.markdown("---")



    
    import pandas as pd
    renderExportJournalSummary(pd, "tab1")

    




# if modularized

def renderExportJournalSummary(pd, tab):
    col1, col2 = st.columns([1, 1])

    with col1:
        if st.button("📤 Export Journal", key=f"{tab}_journal"):
            df = pd.DataFrame(st.session_state["journal_entries"])
            st.dataframe(df)

    with col2:
        if st.button("🧠 Generate Summary", key=f"{tab}_summary"):
            engine = ReflectionSummaryEngine(st.session_state["journal_entries"])
            st.markdown("#### 🧠 Emotional Summary & Guidance")
            st.caption("A gentle overview of your recent reflections—tone, theme, and mood insights.")
            st.markdown(f"""
                <div style='background-color:#f0f8ff; padding:12px; border-radius:10px'>
                {engine.generate_summary()}
                </div>
            """, unsafe_allow_html=True)

            # 🎉 Reflection Milestones
            st.markdown("#### 🏁 Reflection Milestones")
            journal = st.session_state.get("journal_entries", [])
            milestones = detect_reflection_milestones(journal)

            if milestones:
                st.caption("These are emotional patterns your reflections have quietly revealed.")
                for m in milestones:
                    st.markdown(f"- {m}")
            else:
                st.info("No milestones yet—your journey is just beginning.")





def render_tab2(tone, theme, length, backend):
    import pandas as pd
    st.markdown("_Let the assistant guide you into deeper insight._")

    # Developer tool: dummy journal generator
    if st.button("🧪 Generate Dummy Journal Data"):
        st.session_state["journal_entries"] = generate_dummy_journal()
        st.success("Dummy journal data generated for the past 7 days.")
        st.rerun()

    # Weekly chaining section
    render_weekly_chaining()

    # Layout: Reflection Generator + Tone-Based Filtering side by side
    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("### 🧠 Generate a New Reflection")

        tone = st.selectbox("Choose a tone:", ["Gentle", "Empowering", "Philosophical", "Neutral"], index=0)
        theme_label = st.selectbox("Explore your weekly journey:", get_themes_with_icons("weekly"))
        theme = theme_label.split(" ", 1)[-1]
        length = st.radio("Reflection length:", ["Short", "Medium", "Long"], index=0)
        backend = st.selectbox("Choose backend:", ["Auto", "Simple", "Advanced"], index=0)

        if "reflection" not in st.session_state:
            st.session_state["reflection"] = ""

        if st.button("🧠 Generate Reflection", key="tab2_generate"):
            reflection = generate_reflection(tone, theme, length, backend)
            st.session_state["reflection"] = reflection
            st.markdown(f"### {tone_icon_map[tone]} Your Reflection\n_{reflection}_")
            play_ambient_music(tone)

        if "reflection" in st.session_state and st.session_state["reflection"]:
            if st.button("🔊 Play Reflection", key="tab2_play"):
                audio_buffer = play_audio(st.session_state["reflection"])
                st.audio(audio_buffer, format="audio/wav", autoplay=True)

        if st.button("💾 Save Reflection", key="tab2_save"):
            journal = st.session_state.get("journal_entries", [])
            reflection = st.session_state["reflection"]
            updated_journal = save_reflection(
                tone=tone,
                theme=theme,
                text=reflection,
                journal_entries=journal,
                source="Emotional Landscape",
                reflection_type="Weekly Summary"
            )
            st.session_state["journal_entries"] = updated_journal
            st.toast("📝 Reflection saved to journal.")

    with col2:
        st.markdown("### 🎨 Filter Reflections by Tone")
        tones = ["Gentle", "Empowering", "Philosophical", "Neutral"]
        selected_tone = st.selectbox("Select tone to explore:", tones)

        filtered = [
            e for e in st.session_state.get("journal_entries", [])
            if e.get("tone") == selected_tone
        ]

        if filtered:
            for entry in reversed(filtered[:3]):  # Show top 3 for brevity
                st.caption(f"""
                🕒 {entry['timestamp']}  
                🌱 Theme: {entry.get('theme', 'Unspecified')}  
                > {entry['text']}
                """)
                st.markdown("---")
        else:
            st.info(f"No reflections found with tone: {selected_tone}")

    # Full journal viewer
    if "journal_entries" in st.session_state and st.session_state["journal_entries"]:
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

    renderExportJournalSummary(pd, "tab2")





def get_weekly_themes(journal):
    cutoff = datetime.now() - timedelta(days=7)
    recent = [e for e in journal if pd.to_datetime(e["timestamp"]) >= cutoff]
    themes = [e.get("theme") for e in recent if e.get("theme")]
    return sorted(set(themes), key=lambda t: themes.count(t), reverse=True)

def generate_weekly_chain_prompt(theme):
   
    if theme in weekly_sequences:
        return weekly_sequences[theme]
    return [
        f"What has {theme.lower()} meant to you this week?",
        f"Is there a moment that deepened your sense of {theme.lower()}?",
        f"What intention will guide your {theme.lower()} next week?"
    ]

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
            st.session_state["selected_theme"] = top_theme
            st.session_state["mode"] = "guided"
            st.session_state["step"] = 0
            st.session_state["active_tab"] = "Rhythms of the Day"
            st.rerun()
    else:
        st.info("No reflections found from the past week.")



            
from gtts import gTTS
from io import BytesIO
import streamlit as st

def play_audio(text):
    try:
        # Create in-memory buffer
        audio_buffer = BytesIO()

        # Generate speech and write to buffer
        tts = gTTS(text)
        tts.write_to_fp(audio_buffer)

        # Reset buffer position
        audio_buffer.seek(0)

        return audio_buffer

        # Stream audio directly
        
    except Exception as e:
        st.error(f"Audio playback failed: {e}")


import time
import uuid
import streamlit as st
import time

"""def run_guided_reflection_flow(
    theme,
    tone,
    prompts,
    source="Chat",
    reflection_type="Guided Journey",
    form_key_prefix="guided",
    state_key_prefix="guided"
):
    # Namespaced session keys
    step_key = f"{state_key_prefix}_step"
    reflections_key = f"{state_key_prefix}_reflections"

    # Initialize session state
    if step_key not in st.session_state:
        st.session_state[step_key] = 0
    if reflections_key not in st.session_state:
        st.session_state[reflections_key] = []

    current_step = st.session_state[step_key]
    total_steps = len(prompts)

    # Active reflection step
    if current_step < total_steps:
        st.markdown(f"**Assistant:** {prompts[current_step]}")
        st.caption(f"Step {current_step + 1} of {total_steps}")

        with st.form(key=f"{form_key_prefix}_form"):
            user_reflection = st.text_area(
                "Your reflection:",
                key=f"{form_key_prefix}_textarea"
            )
            submitted = st.form_submit_button("Next")

        if submitted and user_reflection.strip():
            st.session_state[reflections_key].append(user_reflection)
            st.session_state[step_key] += 1
            st.rerun()

    # Final step: save and reset
    else:
        full_text = "\n\n".join(st.session_state[reflections_key])
        journal = st.session_state.get("journal_entries", [])
        updated_journal = save_reflection(
            tone=tone,
            theme=theme,
            text=full_text,
            journal_entries=journal,
            source=source,
            reflection_type=reflection_type,
            mood="Unspecified"
        )
        st.session_state["journal_entries"] = updated_journal
        st.success("🌿 Guided journey complete. Reflection saved to journal.")
        time.sleep(3)
        st.session_state[step_key] = 0
        st.session_state[reflections_key] = []
        st.rerun()"""




composer = ResponseComposer()

def render_chat_companion():
    mode = st.radio("🧘 Choose Reflection Mode", ["Conversational", "Guided"], horizontal=True)
    mood = "Unspecified"

    st.session_state["reflection_mode"] = mode
    if "reflection" not in st.session_state:
       st.session_state["reflection"] = ""

    st.markdown("_Talk through your thoughts. I'm here to listen and reflect with you._")


    if mode == "Guided":
       st.markdown("### 🌿 Guided Reflection")

       mode_key = "evening"  # or "daily", "evening", etc.
       available_themes = list(mode_sequences.get(mode_key, {}).keys())


       # Lock theme once journey begins
       theme_key = f"{mode_key}_theme"
       step_key = f"{mode_key}_step"

       if theme_key not in st.session_state or st.session_state.get(step_key, 0) == 0:
          selected_theme = st.selectbox("Choose a theme", available_themes)
          st.session_state[theme_key] = selected_theme
       else:
           selected_theme = st.session_state[theme_key]
           st.markdown(f"**Theme:** 🌱 {selected_theme}")
       tone = "Neutral"  # You can make this user-selectable later if needed


       guided_sequences = {
        "Forgiveness": [
        "Is there someone you’re ready to forgive today?",
        "What emotions arise when you think about that person or situation?",
        "How might forgiveness free you emotionally?"
        ],
        "Resilience": [
        "What challenge are you facing right now?",
        "What inner strength are you drawing on?",
        "How can you support yourself through this moment?"
        ],
        "Healing": [
        "What part of you feels tender today?",
        "Is there something you’re ready to release?",
        "What does emotional healing look like for you right now?"
        ],
       "Identity": [
        "What part of your identity feels most alive today?",
        "Are there roles or labels you’re questioning?",
        "How do you define yourself beyond external expectations?"
       ],
       # Growth and Spirituality already defined
       }


       if "guided_step" not in st.session_state:
          st.session_state["guided_step"] = 0
       if "guided_reflections" not in st.session_state:
          st.session_state["guided_reflections"] = []

       #prompts = guided_sequences.get(selected_theme, ["What would you like to reflect on today?"])
       prompts = get_prompt_sequence(selected_theme, mode=mode_key)
       run_guided_reflection_flow(selected_theme, tone, prompts, form_key_prefix="chat_guided", state_key_prefix="chat_guided")

       """ prompts = get_prompt_sequence(selected_theme, mode="guided")
       run_guided_reflection_flow(
       theme=selected_theme,
       tone=tone,
       prompts=prompts,
       source="Guided",
       reflection_type="Evening Reflection",
       mode="evening"
      )"""

       

            



    
    if mode == "Conversational":
    # Existing chat history display
    # Input form
    # Save last reflection button

      # Initialize chat history
      if "chat_history" not in st.session_state:
         st.session_state["chat_history"] = []

      # Display chat history first
      chat_container = st.container()
      with chat_container:
        for exchange in st.session_state["chat_history"]:
            tone = exchange.get("tone", "Unspecified")
            theme = exchange.get("theme", "Unspecified")
            tone_icon = tone_icon_map.get(tone, "❔")
            theme_icon = theme_icon_map.get(theme, "❔")
            mood_icon = mood_icon_map.get(mood, "❔")

            st.markdown(f"**You:** {exchange['user']}")
            st.markdown(f"*Assistant:* {exchange['ai']}")
            
            st.caption(f"_Mood:_ {mood_icon} {mood} | 🧭 Tone: {tone_icon} {tone} | 🌱 Theme: {theme_icon} {theme}")


      # Input form always at bottom
      input_container = st.container()
      with input_container:
         with st.form(key="chat_form"):
            user_input = st.text_input("Type your reflection or question...", key="chat_input")
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
         if st.session_state["chat_history"]:
            last = st.session_state["chat_history"][-1]
            if st.button("💾 Save Last Reflection to Journal"):
               journal = st.session_state.get("journal_entries", [])
               updated_journal = save_reflection(
               tone=last["tone"],
               theme=last["theme"],
               text=f"**You:** {last['user']}\n\n**Assistant:** {last['ai']}",
               journal_entries=journal,
               source="Soul Exchange",
               reflection_type="Conversational Insight"
               )
               st.session_state["journal_entries"] = updated_journal
               st.toast("📝 Reflection saved to journal.")
         if "journal_entries" in st.session_state and st.session_state["journal_entries"]:
            st.markdown("### 📖 Dialogue Journal")
            st.caption(f"🗂 {len(st.session_state['journal_entries'])} reflections saved")

            

            for entry in reversed(st.session_state["journal_entries"]):
                tone = entry.get("tone", "Unspecified")
                theme = entry.get("theme", "Unspecified")
                mood = entry.get("mood", "Unspecified")
                source = entry.get("source", "Chat")
                reflection_type = entry.get("reflection_type", "Conversational Insight")

                tone_icon = tone_icon_map.get(tone, "❔")
                theme_icon = theme_icon_map.get(theme, "❔")
                mood_icon = mood_icon_map.get(mood, "❔")

                st.caption(f"""
                **🕒 {entry['timestamp']}**  
                _Mood:_ {mood_icon} {mood} | 🧭 Tone: {tone_icon} {tone} | 🌱 Theme: {theme_icon} {theme}  
                > {entry['text']}
                """)
                st.caption(f"📍 Source: {source} | 🧠 Type: {reflection_type}")
                st.markdown("---")





import random
def generate_daily_prompt(theme: str, tone: str) -> str:
    prompts = {
        "Spirituality": [
            "What truth feels alive in you this morning?",
            "Is there a ritual or prayer you’d like to begin your day with?"
        ],
        "Growth": [
            "What intention would you like to carry today?",
            "Is there a small step you feel ready to take?"
        ],
        "Resilience": [
            "What strength are you drawing on today?",
            "How will you care for yourself if challenges arise?"
        ],
        "Healing": [
            "What does emotional healing look like for you today?",
            "Is there something you’re ready to release?"
        ]
    }
    return random.choice(prompts.get(theme, ["What would you like to reflect on today?"]))


def render_daily_reflection():
   st.markdown("### 🌅 Daily Reflection")
   st.caption("Begin your day with intention and emotional clarity.")

   theme = st.selectbox("Choose a theme", ["Spirituality", "Growth", "Resilience", "Healing"])
   tone = st.selectbox("Choose a tone", ["Gentle", "Empowering", "Neutral", "Philosophical"])
   daily_sequences = {
    "Spirituality": [
        "What truth feels alive in you this morning?",
        "Is there a ritual or prayer you’d like to begin your day with?",
        "How does this connect to your deeper sense of purpose?"
    ],
    "Growth": [
        "What intention would you like to carry today?",
        "Is there a small step you feel ready to take?",
        "What might support you in staying committed to that step?"
    ],
    "Resilience": [
        "What strength are you drawing on today?",
        "How will you care for yourself if challenges arise?",
        "What does resilience look like in your daily rhythm?"
    ],
    "Healing": [
        "What does emotional healing look like for you today?",
        "Is there something you’re ready to release?",
        "What gentle action could support your healing today?"
    ]
 }
   """prompts = get_prompt_sequence(theme, mode="daily")
   run_guided_reflection_flow(
    theme=theme,
    tone=tone,
    prompts=prompts,
    source="Daily",
    reflection_type="Evening Reflection",
    mode="evening"
   )"""

   #prompts = daily_sequences.get(theme, ["What intention would you like to set today?"])
   prompts = get_prompt_sequence(theme, mode="daily")
   run_guided_reflection_flow(theme, tone, prompts, source="Rhythms of the Day", reflection_type="Morning Reflection", form_key_prefix="daily_reflection", state_key_prefix="daily_reflection")
    


#from milestone_utils import detect_reflection_milestones
#from summary_engine import ReflectionSummaryEngine  # Adjust if needed

import streamlit as st
import plotly.express as px

import streamlit as st
import pandas as pd
import plotly.express as px

def render_journey_summary():
    st.markdown("## 📘 Journey Summary")
    st.markdown("_Your emotional landscape, milestones, and reflections in one place._")

    # 🔹 Sample tone/theme counts
    tone_counts = {"Gentle": 5, "Bold": 3, "Reflective": 7}
    theme_counts = {"Growth": 6, "Resilience": 4, "Connection": 5}

    # 🔹 Tone Frequency Chart with distinct colors
    tone_df = pd.DataFrame({
        "Tone": list(tone_counts.keys()),
        "Frequency": list(tone_counts.values())
    })
    tone_fig = px.bar(
        tone_df,
        x="Tone",
        y="Frequency",
        color="Tone",
        title="Tone Frequency",
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    st.plotly_chart(tone_fig, use_container_width=True)

    # 🔹 Theme Frequency Chart with distinct colors
    theme_df = pd.DataFrame({
        "Theme": list(theme_counts.keys()),
        "Frequency": list(theme_counts.values())
    })
    theme_fig = px.bar(
        theme_df,
        x="Theme",
        y="Frequency",
        color="Theme",
        title="Theme Frequency",
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    st.plotly_chart(theme_fig, use_container_width=True)

    # 🔹 Styled Summary Block
    summary_text = "You've reflected with depth and warmth. Themes of growth and connection have guided your journey."
    st.markdown(f"""
        <div style='background-color:#f0f8ff; padding:16px; border-radius:12px; font-size:16px'>
            <span style='font-size:24px'>🌱</span> {summary_text}
        </div>
    """, unsafe_allow_html=True)

    # 🔹 Milestone Badges
    milestones = ["First Reflection", "Tone Shift", "Theme Cluster", "Export Ready"]
    cols = st.columns(len(milestones))
    for i, milestone in enumerate(milestones):
        with cols[i]:
            st.markdown(f"""
                <div style='text-align:center; padding:8px; background-color:#e6f7ff; border-radius:8px'>
                    <span style='font-size:20px'>🏁</span><br>
                    <strong>{milestone}</strong>
                </div>
            """, unsafe_allow_html=True)




import plotly.express as px

import pandas as pd
import plotly.express as px

def render_tone_theme_chart(tone_counts, theme_counts):
    # 🔹 Tone Chart
    tone_df = pd.DataFrame({
        "Tone": list(tone_counts.keys()),
        "Frequency": list(tone_counts.values())
    })
    tone_fig = px.bar(
        tone_df,
        x="Tone",
        y="Frequency",
        color="Tone",  # ✅ Assigns distinct colors
        title="Tone Frequency",
        color_discrete_sequence=px.colors.qualitative.Set2  # Optional: soft palette
    )
    st.plotly_chart(tone_fig, use_container_width=True)

    # 🔹 Theme Chart
    theme_df = pd.DataFrame({
        "Theme": list(theme_counts.keys()),
        "Frequency": list(theme_counts.values())
    })
    theme_fig = px.bar(
        theme_df,
        x="Theme",
        y="Frequency",
        color="Theme",  # ✅ Assigns distinct colors
        title="Theme Frequency",
        color_discrete_sequence=px.colors.qualitative.Set3  # Optional: varied palette
    )
    st.plotly_chart(theme_fig, use_container_width=True)



def render_milestones(milestones):
    cols = st.columns(len(milestones))
    for i, milestone in enumerate(milestones):
        with cols[i]:
            st.markdown(f"""
                <div style='text-align:center; padding:8px; background-color:#e6f7ff; border-radius:8px'>
                    <span style='font-size:20px'>🏁</span><br>
                    <strong>{milestone}</strong>
                </div>
            """, unsafe_allow_html=True)





