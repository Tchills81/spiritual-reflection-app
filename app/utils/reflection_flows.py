import streamlit as st
import time
from ui.response_engine import save_reflection
from datetime import datetime

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

evening_sequences = {
    "Gratitude": [
        "What are three things you’re grateful for today?",
        "Was there a moment that brought you unexpected joy?",
        "How might you carry this gratitude into tomorrow?"
    ],
    "Release": [
        "Is there anything you’d like to let go of from today?",
        "What emotions surfaced that you didn’t fully process?",
        "How can you offer yourself closure tonight?"
    ],
    "Rest": [
        "What does rest mean to you right now?",
        "Is there a ritual that helps you transition into sleep?",
        "What intention would you like to set for your dreams?"
    ],
    "Reflection": [
        "What did today teach you?",
        "Were there any moments that felt especially meaningful?",
        "How has this day shaped your emotional landscape?"
    ]
}


weekly_sequences = {
    "Growth": [
        "What personal growth did you notice this week?",
        "Was there a challenge that helped you evolve?",
        "What intention will guide your growth next week?"
    ],
    "Connection": [
        "Who did you feel most connected to this week?",
        "Was there a moment of emotional resonance with someone?",
        "How might you deepen those connections moving forward?"
    ],
    "Purpose": [
        "Did your actions this week align with your deeper purpose?",
        "What felt meaningful or fulfilling?",
        "Is there a purpose you’d like to recommit to next week?"
    ],
    "Balance": [
        "How well did you balance work, rest, and reflection?",
        "Was there a moment you felt truly centered?",
        "What adjustments could help you feel more balanced next week?"
    ]
}


def get_reflection_mode_by_time():
    now = datetime.now().hour
    if 5 <= now < 12:
        return "daily"       # Morning
    elif 12 <= now < 18:
        return "guided"      # Afternoon
    elif 18 <= now < 22:
        return "evening"     # Evening wind-down
    else:
        return "weekly"      # Late night or weekend review




mode_sequences = {
    "guided": guided_sequences,
    "daily": daily_sequences,
    "evening": evening_sequences,
    "weekly": weekly_sequences
}

def get_prompt_sequence(theme: str, mode: str = "guided") -> list:
    return mode_sequences.get(mode, {}).get(theme, ["What would you like to reflect on today?"])



def run_guided_reflection_flow(
    theme,
    tone,
    prompts,
    source="Chat",
    reflection_type="Guided Journey",
    form_key_prefix="guided",
    state_key_prefix="guided",
    mode="guided",
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
        st.rerun()



from ui.incons import ambient_track_map
def play_ambient_music(tone):
    track_path = ambient_track_map.get(tone)
    if track_path:
        audio_file = open(track_path, 'rb')
        audio_bytes = audio_file.read()
        st.audio(audio_bytes, format='audio/wav', start_time=0, autoplay=True)




def  playAmbient():
    # Initialize session state for the audio player's visibility
    if 'show_audio' not in st.session_state:
        st.session_state.show_audio = False

    # A container that we will fill or empty
    audio_container = st.empty()

    #Create a toggle button to control visibility
    col1, col2 = st.columns([1, 10])
    with col1:
        st.toggle("Play Ambient Sound", value=st.session_state.show_audio, key="audio_toggle")

    # The URL for the ambient sound stream
    ambient_stream_url = "app/audios/gentle_piano.mp3"
    # Logic to show or hide the audio player
    if st.session_state.audio_toggle:
    # Use the container to place the audio player
        with audio_container:
         st.audio(ambient_stream_url, format="audio/wav", autoplay=True, loop=True)
    else:
    # Clear the container to remove the audio player
       audio_container.empty()

# Add some other content to the page
    with col2:
       st.write("Toggle the switch to start or stop the ambient sound.")
       st.info("This sound is streamed from iloveradio.mp3 and will play automatically when the switch is on.")