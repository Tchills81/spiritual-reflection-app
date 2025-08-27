
from utils.reflection_flows import guided_sequences, daily_sequences, evening_sequences, weekly_sequences
from ui.incons import theme_icon_map

def get_themes_by_mode(mode="guided"):

    if mode == "guided":
        return sorted(guided_sequences.keys())
    elif mode == "daily":
        return sorted(daily_sequences.keys())
    elif mode == "evening":
        return sorted(evening_sequences.keys())
    elif mode == "weekly":
        return sorted(weekly_sequences.keys())
    else:
        return ["Unspecified"]

def get_themes_with_icons(mode="guided"):
    themes = get_themes_by_mode(mode)
    return [f"{theme_icon_map.get(t, '')} {t}" for t in themes]




