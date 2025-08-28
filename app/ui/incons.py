tone_icon_map = {
    "Gentle": "🍃",
    "Philosophical": "🧠",
    "Empowering": "⚡",
    "Neutral": "🌿",
    "Reflective": "🪞",
    "Grateful": "🙏",
    "Tender": "💗",
    "Resilient": "🛡️",
    "Spiritual": "✨",
    "Joyful": "😊",
    "Sad": "😢",
    "Angry": "🔥",
    "Confused": "❓",
    "Unspecified": "❔"
}


theme_icon_map = {
    "Courage": "🦁",
    "Forgiveness": "🕊️",
    "Resilience": "🛡️",
    "Healing": "💗",
    "Identity": "🧬",
    "Growth": "🌱",
    "Spirituality": "✨",
    "Gratitude": "🙏",
    "Release": "🌬️",
    "Rest": "😴",
    "Reflection": "🪞",
    "Connection": "🤝",
    "Purpose": "🎯",
    "Balance": "⚖️",
    "Unspecified": "❔"
}


source_icon_map = {
    "Chat": "💬",
    "Guided": "🌿",
    "Daily": "☀️",
    "Evening": "🌙",
    "Weekly": "📅",
    "Unspecified": "❔"
}

type_icon_map = {
    "Conversational Insight": "🧠",
    "Evening Reflection": "🌙",
    "Daily Intention": "☀️",
    "Weekly Summary": "📅",
    "Guided Journey": "🛤️",
    "Unspecified": "❔"
}


ambient_track_map = {
    "Gentle": "app/audios/gentle_piano.mp3",
    "Philosophical":"app/audios/gentle_piano.mp3",
    "Empowering": "app/audios/gentle_piano.mp3",
    "Neutral": "app/audios/gentle_piano.mp3",
    "Resilient": "app/audios/gentle_piano.mp3",
    "Spiritual": "app/audios/gentle_piano.mp3",
    "Evening": "app/audios/gentle_piano.mp3",
    "Morning": "app/audios/gentle_piano.mp3"
}


mood_icon_map = {
    "Grateful": "🙏",
    "Peaceful": "🕊️",
    "Joyful": "😊",
    "Sad": "😢",
    "Angry": "🔥",
    "Confused": "❓",
    "Hopeful": "🌅",
    "Reflective": "🪞",
    "Tender": "💗",
    "Resilient": "🛡️",
    "Anxious": "😰",
    "Neutral": "🌿",
    "Unspecified": "❔",
    "Default": "❔"
}

milestone_icons = {
    "First Reflection": "📝",
    "Tone Shift": "🎭",
    "Theme Cluster": "🌿",
    "Export Ready": "📦"
}

BUTTON_LABELS = {
    "save": "💾 Save Reflection",
    "generate_affirmation": "✨ Generate Affirmation",
    "play_affirmation": "🔊 Play Affirmation",
    "load_dummy": "🧪 Load Dummy Journal",
    "generate_milestone": "🎯 Generate Milestone Test Data",
    "export_summary": "📤 Export Journey Summary",
    "submit_form": "➡️ Submit Reflection",
    "next": "➡️ Next",
    "start_journey": "🚀 Begin Guided Journey",
    "refresh_theme": "🔄 Refresh Theme",
    "chat": "💬 Start Conversation",
    "view_summary": "📘 View Journey Summary"
}

shadow_map = {
    "Gentle": "0 2px 6px rgba(180, 180, 255, 0.3)",
    "Empowering": "0 4px 12px rgba(255, 100, 100, 0.4)",
    "Philosophical": "0 3px 8px rgba(100, 100, 100, 0.3)",
    "Neutral": "0 2px 4px rgba(150, 150, 150, 0.2)"
}

gradient_map = {
    "Gentle": "linear-gradient(135deg, #e0f7fa, #fce4ec)",
    "Empowering": "linear-gradient(135deg, #ff8a65, #ff5252)",
    "Philosophical": "linear-gradient(135deg, #cfd8dc, #eceff1)",
    "Neutral": "linear-gradient(135deg, #f5f5f5, #eeeeee)"
}

ICON_MAP = {
    "Gentle": "🌸",
    "Empowering": "🔥",
    "Philosophical": "🧠",
    "Neutral": "🌀"
}


CAPTION_ICONS = {
    "audio_hint": "🔊",
    "save_confirmation": "💾",
    "reflection_prompt": "📝",
    "theme_guidance": "🌱",
    "tone_tip": "🎭",
    "navigation_hint": "🧭",
    "error": "⚠️",
    "success": "✅",
    "info": "ℹ️"
}


BUTTON_VARIANTS = {
    "gentle": {"save": "💾 Gently Save"},
    "empowering": {"save": "💾 Lock It In"},
    "philosophical": {"save": "💾 Archive Reflection"}
}



affirmation_map = {
    "Gentle": "You are enough, just as you are.",
    "Empowering": "Your strength is your compass.",
    "Resilient": "You rise, again and again.",
}


TONE_CONFIGS = {
    "Gentle": {
        "hover_color": "#d0e6ff",
        "shadow": "0 2px 6px rgba(180, 180, 255, 0.3)",
        "icon": "🌸"
    },
    "Empowering": {
        "hover_color": "#ffe0e0",
        "shadow": "0 4px 12px rgba(255, 100, 100, 0.4)",
        "icon": "🔥"
    },
    "Philosophical": {
        "hover_color": "#e0e0e0",
        "shadow": "0 3px 8px rgba(100, 100, 100, 0.3)",
        "icon": "🧠"
    },
    "Neutral": {
        "hover_color": "#f0f0f0",
        "shadow": "0 2px 4px rgba(150, 150, 150, 0.2)",
        "icon": "🌀"
    }
}


THEME_TO_TONE = {
    "Gentle": "Gentle",
    "Empowering": "Empowering",
    "Still": "Philosophical"  # or "Neutral" if you prefer
}

MILESTONE_MICROCOPY = {
    "First Reflection": {
        "Gentle": "A soft beginning to your journey 🌸",
        "Empowering": "You’ve taken the first bold step 🔥",
        "Philosophical": "The first thought, the first echo 🧠",
        "Neutral": "Your journey begins 🌀"
    },
    # Add others similarly...
}


TONE_COLORS = {
    "Gentle": "#a3c9f1",
    "Empowering": "#ff6b6b",
    "Philosophical": "#b0b0b0",
    "Neutral": "#cccccc"
}





"""source_icon = source_icon_map.get(source, "❔")
type_icon = type_icon_map.get(reflection_type, "❔")

#st.caption(f"{source_icon} Source: {source} | {type_icon} Type: {reflection_type}")"""
