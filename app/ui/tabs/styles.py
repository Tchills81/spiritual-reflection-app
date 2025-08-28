from streamlit_extras.stylable_container import stylable_container
import streamlit as st
from gtts import gTTS
from io import BytesIO
from ui.incons import BUTTON_LABELS, shadow_map, tone_icon_map, TONE_COLORS



def styled_audio_button(action_key, affirmation_text, container_key):
    """
    A reusable, theme-aware audio button using BUTTON_LABELS for icon-rich labels.
    Preserves layout and ensures proper audio playback.

    Args:
        action_key (str): Key from BUTTON_LABELS dict (e.g. "play_affirmation").
        affirmation_text (str): The text to convert to speech and play.
        container_key (str): Unique key for the stylable_container.
    Returns:
        bool: True if the button was clicked.
    """
    label = BUTTON_LABELS.get(action_key, "🔘 Action")
    theme = st.session_state.get("theme_config", {})
    accent = theme.get("accent_color", "#000000")
    font = theme.get("font_family", "sans-serif")
    hover = "#FF6666"
    active = "#CC3333"

    css = f"""
        div.stButton > button {{
            background-color: {accent};
            color: white;
            border-radius: 8px;
            padding: 10px 24px;
            font-size: 16px;
            font-family: {font};
            border: none;
            transition: background-color 0.3s ease;
        }}
        div.stButton > button:hover {{
            background-color: {hover};
        }}
        div.stButton > button:active {{
            background-color: {active};
            transform: scale(0.98);
        }}
        div.stButton > button:focus {{
            box-shadow: 0 0 0 2px {accent}, 0 0 0 4px {hover};
        }}
        div.stButton {{
            text-align: center;
        }}
    """

    audio_slot = st.empty()  # Reserve space to prevent layout shift

    with stylable_container(key=f"{container_key}_container", css_styles=css):
        clicked = st.button(label, key=f"{container_key}_button")
        if clicked:
            audio_buffer = BytesIO()
            gTTS(text=affirmation_text, lang="en").write_to_fp(audio_buffer)
            audio_buffer.seek(0)
            st.audio(audio_buffer, format="audio/wav", autoplay=True)
            
        return clicked
    




def styled_tab_button(label, tab_key, current_tab, container_key):
    theme = st.session_state.get("theme_config", {})
    tone_config = st.session_state.get("tone_config", {})
    
    accent = theme.get("accent_color", "#2c6df2")
    text_color = theme.get("text_color", "#444")
    font = theme.get("font_family", "sans-serif")
    hover_color = tone_config.get("hover_color", "#f0f4ff")
    shadow = tone_config.get("shadow", "none")
    icon = tone_config.get("icon", "🔘")

    is_active = (tab_key == current_tab)

    css = f"""
        div.stButton > button {{
            background-color: transparent;
            border: none;
            color: {accent if is_active else text_color};
            font-weight: {'600' if is_active else '400'};
            text-decoration: {'underline' if is_active else 'none'};
            font-family: {font};
            font-size: 16px;
            padding: 6px 18px;
            border-radius: 4px;
            box-shadow: {shadow if is_active else 'none'};
            transition: all 0.2s ease-in-out;
        }}
        div.stButton > button:hover {{
            background-color: {hover_color};
            color: {accent};
            text-decoration: underline;
        }}
        div.stButton {{
            text-align: center;
        }}
    """

    with stylable_container(key=f"{container_key}_container", css_styles=css):
        return st.button(f"{icon} {label}", key=f"{container_key}_button")



def styled_selectbox(label, options, key, default_index=0):
    """
    A reusable, theme-aware styled selectbox with more robust selectors.
    """
    # Assuming 'theme_config' is correctly managed in your session state
    theme = st.session_state.get("theme_config", {})
    accent = theme.get("accent_color", "#FF4B4B")
    font = theme.get("font_family", "sans-serif")
    bg = theme.get("badge_bg", "#F0F2F6")
    text_color = theme.get("text_color", "#262730")

    css = f"""
        /* Style the selectbox's label */
        label[for="{key}_select-label"] {{
            font-weight: bold;
            color: {accent};
            font-family: {font};
            font-size: 16px;
        }}

        /* Target the main selectbox container using data-testid */
        div[data-testid="stSelectbox"] {{
            border-radius: 8px;
            font-family: {font};
        }}
        
        /* Style the visible input area of the selectbox */
        div[data-testid="stSelectbox"] > div:first-child > div[data-baseweb="select"] > div:first-child {{
            background-color: {bg};
            border-radius: 8px;
            font-family: {font};
            color: {text_color};
            border: 1px solid #ccc;
        }}

        /* Style the dropdown list that appears on click */
        div[data-baseweb="menu"] ul {{
            background-color: {bg};
            border-radius: 8px;
            font-family: {font};
            color: {text_color};
        }}

        /* Hover effect for options in the dropdown list */
        div[data-baseweb="menu"] li:hover {{
            background-color: #e6f7ff !important;
            color: {accent} !important;
        }}
        
        /* Ensure the text color of the options is correct */
        div[data-baseweb="menu"] li > div {{
            color: {text_color} !important;
        }}
        
        /* Handle color of the selected option when dropdown is open */
        div[data-baseweb="menu"] li[aria-selected="true"] > div {{
            color: {accent} !important;
        }}
    """
    
    with stylable_container(key=f"{key}_container", css_styles=css):
        return st.selectbox(label, options, index=default_index, key=f"{key}_select")




def styled_text_input(label, key, placeholder="Type here..."):
    tone_config = st.session_state.get("tone_config", {})
    shadow = tone_config.get("shadow", "none")
    hover_color = tone_config.get("hover_color", "#FF6666")
    """
    A reusable, theme-aware styled text input.

    Args:
        label (str): Label to display above the input.
        key (str): Unique key for the container and input.
        placeholder (str): Placeholder text inside the input.

    Returns:
        str: The user's input.
    """
    theme = st.session_state.get("theme_config", {})
    accent = theme.get("accent_color", "#000000")
    font = theme.get("font_family", "sans-serif")
    bg = theme.get("badge_bg", "#f0f0f0")
    text_color = theme.get("text_color", "#333")

    css = f"""
        input[type="text"] {{
            background-color: {bg};
            color: {text_color};
            border-radius: 8px;
            padding: 10px;
            font-size: 15px;
            font-family: {font};
            border: 1px solid {accent};
            transition: background-color 0.3s ease;
            box-shadow: {shadow};
        }}
        label {{
            font-weight: bold;
            color: {accent};
            font-family: {font};
            font-size: 16px;
        }}
    """

    with stylable_container(key=f"{key}_container", css_styles=css):
        return st.text_input(label, placeholder=placeholder, key=f"{key}_input")


def styled_text_area(label, key, height=180, placeholder="Let your thoughts flow..."):
    tone_config = st.session_state.get("tone_config", {})
    shadow = tone_config.get("shadow", "none")
    hover_color = tone_config.get("hover_color", "#FF6666")
    """
    A reusable, theme-aware styled text area for journaling or reflection.

    Args:
        label (str): Label to display above the input.
        key (str): Unique key for the container and input.
        height (int): Height of the text area.
        placeholder (str): Placeholder text inside the input.

    Returns:
        str: The user's input.
    """
    theme = st.session_state.get("theme_config", {})
    accent = theme.get("accent_color", "#000000")
    font = theme.get("font_family", "sans-serif")
    bg = theme.get("badge_bg", "#f0f0f0")
    text_color = theme.get("text_color", "#333")

    css = f"""
        textarea {{
            background-color: {bg};
            color: {text_color};
            border-radius: 10px;
            padding: 12px;
            font-size: 15px;
            font-family: {font};
            border: 1px solid {accent};
            transition: background-color 0.3s ease;
            box-shadow: {shadow};
        }}
        label {{
            font-weight: bold;
            color: {accent};
            font-family: {font};
            font-size: 16px;
        }}
    """

    with stylable_container(key=f"{key}_container", css_styles=css):
        return st.text_area(label, height=height, placeholder=placeholder, key=f"{key}_input")



  # 👈 reuse your existing component

def styled_reflection_form(form_key_prefix="daily"):
    tone_config = st.session_state.get("tone_config", {})
    shadow = tone_config.get("shadow", "none")
    hover_color = tone_config.get("hover_color", "#FF6666")
    """
    A reusable, theme-aware form for capturing user reflections.

    Args:
        form_key_prefix (str): Unique prefix for form and input keys.

    Returns:
        tuple: (submitted: bool, user_reflection: str)
    """
    with st.form(key=f"{form_key_prefix}_form"):
        user_reflection = styled_text_area(
            label="📝 Your reflection",
            key=f"{form_key_prefix}_textarea",
            height=180,
            placeholder="Let your thoughts flow..."
        )
        submitted = st.form_submit_button("Next")

    return submitted, user_reflection

import streamlit as st
from streamlit_extras.stylable_container import stylable_container

def styled_button(label, key):
    theme = st.session_state.get("theme_config", {})
    tone_config = st.session_state.get("tone_config", {})
    
    accent = theme.get("accent_color", "#000000")
    font = theme.get("font_family", "sans-serif")
    shadow = tone_config.get("shadow", "none")
    hover_color = tone_config.get("hover_color", "#FF6666")
    active_color = tone_config.get("active_color", "#CC3333")  # Optional

    css = f"""
        div.stButton > button {{
            background-color: {accent};
            color: white;
            border-radius: 8px;
            padding: 10px 24px;
            font-size: 16px;
            font-family: {font};
            border: none;
            transition: background-color 0.3s ease;
            box-shadow: {shadow};
        }}
        div.stButton > button:hover {{
            background-color: {hover_color};
        }}
        div.stButton > button:active {{
            background-color: {active_color};
            transform: scale(0.98);
        }}
        div.stButton {{
            text-align: center;
        }}
    """

    with stylable_container(key=f"{key}_container", css_styles=css):
        return st.button(label, key=f"{key}_button")




def styled_icon_button(action_key, key_suffix):


    """
    A reusable, theme-aware button using emoji-rich labels from BUTTON_LABELS.

    Args:
        action_key (str): Key from BUTTON_LABELS dict (e.g. "save", "generate_affirmation").
        key_suffix (str): Unique suffix to ensure button key uniqueness.

    Returns:
        bool: True if the button was clicked.
    """

    
    label = BUTTON_LABELS.get(action_key, "🔘 Action")
    theme = st.session_state.get("theme_config", {})
    accent = theme.get("accent_color", "#000000")
    font = theme.get("font_family", "sans-serif")

    tone_config = st.session_state.get("tone_config", {})
    
    font = theme.get("font_family", "sans-serif")
    shadow = tone_config.get("shadow", "none")
    hover_color = tone_config.get("hover_color", "#FF6666")
    active_color = tone_config.get("active_color", "#CC3333")  # Optional

    css = f"""
        div.stButton > button {{
            background-color: {accent};
            color: white;
            border-radius: 8px;
            padding: 10px 24px;
            font-size: 16px;
            font-family: {font};
            border: none;
            transition: background-color 0.3s ease;
            box-shadow: {shadow};
        }}
        div.stButton > button:hover {{
            background-color: {hover_color};
        }}
        div.stButton > button:active {{
            background-color: {active_color};
            transform: scale(0.98);
        }}
        div.stButton {{
            text-align: center;
        }}
    """

    with stylable_container(key=f"{key_suffix}_container", css_styles=css):
        return st.button(label, key=f"{key_suffix}_button")


def styled_caption(text, key_suffix="caption"):
    tone_config = st.session_state.get("tone_config", {})
    shadow = tone_config.get("shadow", "none")
    hover_color = tone_config.get("hover_color", "#FF6666")
    """
    A reusable, theme-aware caption component.

    Args:
        text (str): The caption text to display.
        key_suffix (str): Unique key suffix for stylable_container.
    """
    theme = st.session_state.get("theme_config", {})
    font = theme.get("font_family", "sans-serif")
    color = theme.get("caption_color", "#777")
    size = theme.get("caption_size", "13px")

    css = f"""
        div.stMarkdown {{
            font-family: {font};
            font-size: {size};
            color: {color};
            font-style: italic;
            margin-top: 4px;
            margin-bottom: 8px;
            text-color:#FF0000
        }}
    """

    with stylable_container(key=f"{key_suffix}_container", css_styles=css):
        st.markdown(text)


def styled_text_block(text, key_suffix="text_block"):

    tone_config = st.session_state.get("tone_config", {})
    shadow = tone_config.get("shadow", "none")
    hover_color = tone_config.get("hover_color", "#FF6666")

    """
    A reusable, theme-aware text block component.

    Args:
        text (str): The text to display.
        key_suffix (str): Unique key suffix for stylable_container.
    """
    theme = st.session_state.get("theme_config", {})
    font = theme.get("font_family", "sans-serif")
    color = theme.get("text_color", "#333")
    size = theme.get("text_size", "16px")

    css = f"""
        div.stMarkdown {{
            font-family: {font};
            font-size: {size};
            color: {color};
            line-height: 1.6;
            margin-top: 12px;
            margin-bottom: 12px;
        }}
    """

    with stylable_container(key=f"{key_suffix}_container", css_styles=css):
        st.markdown(text)


def styled_badge(label, icon="🏁", key_suffix="badge"):
    theme = st.session_state.get("theme_config", {})
    tone_config = st.session_state.get("tone_config", {})

    badge_bg = theme.get("badge_bg", "#e6f7ff")
    accent = theme.get("accent_color", "#2c6df2")
    font = theme.get("font_family", "sans-serif")
    shadow = tone_config.get("shadow", "none")
    hover = tone_config.get("hover_color", "#f0f0f0")

    css = f"""
        div.stMarkdown {{
            background-color: {badge_bg};
            color: {accent};
            font-family: {font};
            font-size: 15px;
            padding: 10px;
            border-radius: 10px;
            text-align: center;
            box-shadow: {shadow};
            transition: all 0.4s ease;
            animation: fadeIn 0.8s ease-in-out;
        }}
        div.stMarkdown:hover {{
            background-color: {hover};
        }}
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(10px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
    """

    with stylable_container(key=f"{key_suffix}_container", css_styles=css):
        st.markdown(f"{icon}<br><strong>{label}</strong>", unsafe_allow_html=True)




def styled_timeline_block(tone, theme, date, text, key_suffix="timeline"):
    """
    A reusable, tone-aware timeline block for reflections or dialogue entries.

    Args:
        tone (str): Emotional tone (e.g. "Gentle", "Empowering").
        theme (str): Thematic label (e.g. "Resilience").
        date (str): Date string (e.g. "Aug 28, 2025").
        text (str): Reflection or dialogue content.
        key_suffix (str): Unique key suffix for stylable_container.
    """
    tone_config = st.session_state.get("tone_config", {})
    theme_config = st.session_state.get("theme_config", {})
    icon = tone_icon_map.get(tone, "🌀")
    color = TONE_COLORS.get(tone, "#999")
    font = theme_config.get("font_family", "sans-serif")

    css = f"""
        div.stMarkdown {{
            margin-bottom: 20px;
            padding: 12px;
            border-left: 4px solid {color};
            background-color: #f9f9f9;
            border-radius: 8px;
            font-family: {font};
            animation: fadeIn 0.6s ease-in-out;
        }}
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(10px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
    """

    with stylable_container(key=f"{key_suffix}_container", css_styles=css):
        st.markdown(f"""
            <div style='font-size:18px; font-weight:bold;'>{icon} {tone} | {theme}</div>
            <div style='font-size:14px; color:#555;'>{date}</div>
            <div style='margin-top:8px; font-size:15px;'>{text}</div>
        """, unsafe_allow_html=True)


