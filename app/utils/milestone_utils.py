from collections import Counter

def detect_reflection_milestones(journal, theme_threshold=5, tone_threshold=7):
    """
    Detects emotional milestones based on theme and tone frequency.
    Returns a list of milestone strings.
    """
    themes = [e.get("theme") for e in journal if e.get("theme")]
    tones = [e.get("tone") for e in journal if e.get("tone")]

    theme_counts = Counter(themes)
    tone_counts = Counter(tones)

    milestones = []

    for theme, count in theme_counts.items():
        if count >= theme_threshold:
            milestones.append(f"🌱 You’ve explored **{theme}** in {count} reflections.")

    for tone, count in tone_counts.items():
        if count >= tone_threshold:
            milestones.append(f"🎨 Your reflections often carry a **{tone}** tone—{count} times this month.")

    return milestones


def detect_milestones(journal_entries):
    milestones = []

    if not journal_entries:
        return milestones

    # First Reflection
    if len(journal_entries) >= 1:
        milestones.append("First Reflection")

    # Tone Shift
    tones = [entry["tone"] for entry in journal_entries if "tone" in entry]
    if len(set(tones)) > 1:
        milestones.append("Tone Shift")

    # Theme Cluster
    themes = [entry["theme"] for entry in journal_entries if "theme" in entry]
    theme_freq = {t: themes.count(t) for t in set(themes)}
    clustered = [t for t, count in theme_freq.items() if count >= 3]
    if clustered:
        milestones.append("Theme Cluster")

    # Export Ready
    if len(journal_entries) >= 10:
        milestones.append("Export Ready")

    return milestones

