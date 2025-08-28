from streamlit_extras.stylable_container import stylable_container
import streamlit as st
from gtts import gTTS
from io import BytesIO
from ui.incons import BUTTON_LABELS



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
    """
    A reusable, theme-aware tab button.

    Args:
        label (str): Emoji-rich label for the tab (e.g. "📓 Reflection Journal").
        tab_key (str): Internal key for the tab (e.g. "Inner Compass").
        current_tab (str): Currently active tab key.
        container_key (str): Unique key for the stylable_container.

    Returns:
        bool: True if this tab was clicked.
    """
    theme = st.session_state.get("theme_config", {})
    accent = theme.get("accent_color", "#2c6df2")
    text_color = theme.get("text_color", "#444")
    font = theme.get("font_family", "sans-serif")

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
            transition: all 0.2s ease-in-out;
        }}
        div.stButton > button:hover {{
            background-color: #f0f4ff;
            color: {accent};
            text-decoration: underline;
        }}
        div.stButton {{
            text-align: center;
        }}
    """

    with stylable_container(key=f"{container_key}_container", css_styles=css):
        return st.button(label, key=f"{container_key}_button")



def _styled_selectbox(label, options, key, default_index=0):
    """
    A reusable, theme-aware styled selectbox.

    Args:
        label (str): Label to display above the dropdown.
        options (list): List of options to choose from.
        key (str): Unique key for the container and widget.
        default_index (int): Index of the default selected option.

    Returns:
        str: The selected option.
    """
    theme = st.session_state.get("theme_config", {})
    accent = theme.get("accent_color", "#000000")
    font = theme.get("font_family", "sans-serif")
    bg = theme.get("badge_bg", "#f0f0f0")
    text_color = theme.get("text_color", "#333")

    css = f"""
        div[data-baseweb="select"] {{
            background-color: {bg};
            border-radius: 8px;
            font-family: {font};
        }}
        label {{
            font-weight: bold;
            color: {accent};
            font-family: {font};
            font-size: 16px;
        }}
    """

    with stylable_container(key=f"{key}_container", css_styles=css):
        return st.selectbox(label, options, index=default_index, key=f"{key}_select")

import streamlit as st
from streamlit_extras.stylable_container import stylable_container

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
    
import streamlit as st
from streamlit_extras.stylable_container import stylable_container

def styled_text_area(label, key, height=180, placeholder="Let your thoughts flow..."):
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
    """
    A reusable, theme-aware styled button with emoji/icon support.

    Args:
        label (str): Button text (can include emoji).
        key (str): Unique key for the container and button.

    Returns:
        bool: True if the button was clicked.
    """
    theme = st.session_state.get("theme_config", {})
    accent = theme.get("accent_color", "#000000")
    font = theme.get("font_family", "sans-serif")

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
            background-color: #FF6666;
        }}
        div.stButton > button:active {{
            background-color: #CC3333;
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
            background-color: #FF6666;
        }}
        div.stButton > button:active {{
            background-color: #CC3333;
            transform: scale(0.98);
        }}
        div.stButton {{
            text-align: center;
        }}
    """

    with stylable_container(key=f"{key_suffix}_container", css_styles=css):
        return st.button(label, key=f"{key_suffix}_button")


def styled_caption(text, key_suffix="caption"):
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

