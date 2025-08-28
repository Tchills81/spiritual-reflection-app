from collections import Counter
from datetime import datetime
from ui.incons import tone_icon_map, theme_icon_map, mood_icon_map

#Aggregate journal data, generate insights, and compose tone-aware summaries and advice.

class ReflectionSummaryEngine:
    def __init__(self, entries):
        self.entries = entries
        self.tone_counts = Counter()
        self.theme_counts = Counter()
        self.mood_counts = Counter()
        self.timestamps = []

        self._aggregate()

    def _aggregate(self):
        for entry in self.entries:
            self.tone_counts[entry.get("tone", "Unspecified")] += 1
            self.theme_counts[entry.get("theme", "Unspecified")] += 1
            self.mood_counts[entry.get("mood", "Unspecified")] += 1
            ts = entry.get("timestamp")
            if ts:
                self.timestamps.append(ts)

    def get_top_tone(self):
        return self.tone_counts.most_common(1)[0][0] if self.tone_counts else "Unspecified"

    def get_top_theme(self):
        return self.theme_counts.most_common(1)[0][0] if self.theme_counts else "Unspecified"

    def get_top_mood(self):
        return self.mood_counts.most_common(1)[0][0] if self.mood_counts else "Unspecified"

    def generate_summary(self):
        tone = self.get_top_tone()
        theme = self.get_top_theme()
        mood = self.get_top_mood()

        tone_icon = tone_icon_map.get(tone, "❔")
        theme_icon = theme_icon_map.get(theme, "❔")
        mood_icon = mood_icon_map.get(mood, "❔")

        return (
              f"{tone_icon} Your reflections often carry a **{tone}** tone, "
              f"with themes like {theme_icon} **{theme}** appearing most frequently. "
              f"{mood_icon} You've expressed a mood of **{mood}**, suggesting a season of emotional depth.\n\n"
              f"🧭 You might consider exploring a guided journey on *{theme}*, "
              f"or reflecting on how your tone of *{tone}* has shaped your recent entries."
            )

    def generate_advice(self):
        tone = self.get_top_tone()
        theme = self.get_top_theme()

        advice_map = {
            "Gentle": "Consider embracing moments of stillness and self-compassion.",
            "Empowering": "Channel your inner strength to overcome challenges.",
            "Resilient": "Reflect on past triumphs to fuel your current journey.",
            "Spiritual": "Deepen your connection with your spiritual practices.",
            "Growth": "Set small, achievable goals to foster continuous growth.",
            "Healing": "Allow yourself the time and space needed for healing.",
            "Courage": "Face your fears with bravery and an open heart.",
            "Forgiveness": "Release grudges to find peace within yourself.",
            "Gratitude": "Cultivate a daily practice of gratitude to enhance joy.",
            "Release": "Let go of what no longer serves you to make room for new blessings.",
            "Rest": "Prioritize rest and rejuvenation in your daily routine.",
            "Reflection": "Take time to reflect on your journey and lessons learned.",
            "Connection": "Nurture relationships that uplift and support you.",
            "Purpose": "Align your actions with your deeper sense of purpose.",
            "Balance": "Strive for harmony between different aspects of your life."
        }

        return advice_map.get(tone, "Embrace the journey of self-discovery with an open heart.")
    def get_timeline(self):
        if not self.timestamps:
            return "No entries yet."

        dates = [datetime.fromisoformat(ts) for ts in self.timestamps]
        start_date = min(dates).strftime("%Y-%m-%d")
        end_date = max(dates).strftime("%Y-%m-%d")

        return f"Entries from {start_date} to {end_date}"
    
    def to_dataframe(self):
        import pandas as pd
        return pd.DataFrame(self.entries)