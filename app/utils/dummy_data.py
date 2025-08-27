from datetime import datetime, timedelta
import random
import streamlit as st

themes = ["Growth", "Forgiveness", "Resilience", "Healing", "Courage", "Connection", "Purpose"]
tones = ["Gentle", "Empowering", "Reflective", "Still", "Philosophical"]
sources = ["Inner Compass", "Emotional Landscape", "Soul Exchange", "Rhythms of the Day"]

def generate_dummy_journal(days=7, entries_per_day=2):
    journal = []
    now = datetime.now()
    for i in range(days):
        day = now - timedelta(days=i)
        for _ in range(entries_per_day):
            entry = {
                "theme": random.choice(themes),
                "tone": random.choice(tones),
                "mood": random.choice(["Calm", "Hopeful", "Tender", "Centered"]),
                "text": f"Reflection on {day.strftime('%A')} about {random.choice(themes)}.",
                "timestamp": day.strftime("%Y-%m-%d %H:%M:%S"),
                "source": random.choice(sources),
                "reflection_type": "Guided Reflection"
            }
            journal.append(entry)
    return journal



def generate_milestone_test_data():
    from datetime import datetime, timedelta
    import random

    themes = ["Growth", "Resilience", "Resilience", "Resilience", "Healing", "Connection"]
    tones = ["Gentle", "Gentle", "Empowering", "Reflective", "Empowering", "Still", "Philosophical"]
    moods = ["Calm", "Hopeful", "Tender", "Centered"]
    sources = ["Inner Compass", "Emotional Landscape", "Soul Exchange", "Rhythms of the Day"]

    journal = []
    now = datetime.now()

    for i in range(12):  # 12 entries to trigger Export Ready
        day = now - timedelta(days=i)
        entry = {
            "theme": random.choice(themes),
            "tone": random.choice(tones),
            "mood": random.choice(moods),
            "text": f"Test reflection {i+1} on {day.strftime('%A')}.",
            "timestamp": day.strftime("%Y-%m-%d %H:%M:%S"),
            "source": random.choice(sources),
            "reflection_type": "Guided Reflection"
        }
        journal.append(entry)

    return journal

