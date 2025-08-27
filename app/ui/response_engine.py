
def generate_affirmation(text, tone, theme):
    # Simple placeholder logic
    if tone == "Gentle":
        return "You are allowed to feel deeply and heal slowly."
    elif tone == "Empowering":
        return "You have the strength to rise and reshape your path."
    elif tone == "Philosophical":
        return "This moment holds meaning—let it unfold with grace."
    else:
        return "You are present, and that is enough."

from datetime import datetime

from datetime import datetime

def save_reflection(
    tone,
    theme,
    text,
    journal_entries,
    source="Chat",
    reflection_type="Conversational Insight",
    mood="Unspecified",
    length="Unspecified"
):
    entry = {
        "text": text,
        "tone": tone,
        "theme": theme,
        "mood": mood,
        "length": length,
        "source": source,
        "reflection_type": reflection_type,
        "timestamp": datetime.now().isoformat()
    }
    journal_entries.append(entry)
    return journal_entries






import random

def generate_reflection(tone, theme, length, backend):
    # Tone variants
    base = {
        "Gentle": [
            "You are allowed to feel deeply and heal slowly.",
            "Gentleness is a strength, not a weakness.",
            "Your emotions are valid, and your pace is sacred."
        ],
        "Empowering": [
            "You have the strength to rise and reshape your path.",
            "Your courage is the foundation of your transformation.",
            "You are capable of rewriting your story."
        ],
        "Philosophical": [
            "This moment holds meaning—let it unfold with grace.",
            "Existence is layered—each breath a quiet revelation.",
            "Time is a mirror; growth reflects inward and outward."
        ],
        "Neutral": [
            "You are present, and that is enough.",
            "This moment simply is—no need to change it.",
            "Stillness is a valid state of being."
        ]
    }

    # Theme variants
    theme_addon = {
        "Growth": [
            "Each step forward is part of your evolution.",
            "Growth is quiet, steady, and deeply personal.",
            "You are becoming more of who you truly are."
        ],
        "Forgiveness": [
            "Letting go is a gift you give yourself.",
            "Forgiveness is a bridge to inner peace.",
            "Release is not weakness—it’s wisdom."
        ],
        "Resilience": [
            "You’ve weathered storms—your roots run deep.",
            "Resilience is built in the quiet moments.",
            "You are still standing, and that is powerful."
        ],
        "Courage": [
            "Bravery is choosing to show up, even when it’s hard.",
            "Courage is not loud—it’s persistent.",
            "You face the unknown with open eyes."
        ],
        "Unspecified": [""]
    }

    length_map = {
        "Short": 1,
        "Medium": 2,
        "Long": 3
    }

    tone_variants = base.get(tone, [""])
    theme_variants = theme_addon.get(theme, [""])
    multiplier = length_map.get(length, 1)

    # Compose reflection with varied, shuffled segments
    segments = []
    for _ in range(multiplier):
        segments.append(random.choice(tone_variants))
        segments.append(random.choice(theme_variants))

    # Optional: remove accidental duplicates
    unique_segments = []
    for s in segments:
        if s and s not in unique_segments:
            unique_segments.append(s)

    return " ".join(unique_segments)


import random

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import random

class ResponseComposer:
    def __init__(self):
        self.analyzer = SentimentIntensityAnalyzer()

        self.tone_templates = {
            "Gentle": [
                "That sounds tender. Would you like to explore that feeling together?",
                "I'm here with you. What’s been weighing on your heart?",
                "It’s okay to feel this way. Let’s unpack it gently."
            ],
            "Empowering": [
                "You're sensing a shift. What’s one bold step you feel ready to take?",
                "That’s a powerful realization. What strength are you drawing on right now?",
                "You’ve come far. What’s the next move that excites you?"
            ],
            "Philosophical": [
                "That’s a deep reflection. What does this moment reveal about your values?",
                "A beautiful question. What meaning do you find in this experience?",
                "Let’s sit with that thought—what truth is emerging for you?"
            ],
            "Neutral": [
                "Tell me more—what’s been on your mind?",
                "I’m listening. What’s been unfolding for you lately?",
                "Let’s explore this together. Where would you like to begin?"
            ]
        }

    def detect_tone(self, text: str) -> str:
        lowered = text.lower()
        score = self.analyzer.polarity_scores(text)
        compound = score["compound"]

        # Keyword override
        if any(word in lowered for word in ["lost", "sad", "heavy", "tired", 
                                            "lonely", "afraid", "uncertain",
                                             "depressed",  "hopeless", "anxious",
                                            "overwhelmed", "stressed", "confused",
                                            "disappointed", "hurt", "frustrated", "spiritual", "reflective",
                                            "reflect", "reflecting", "reflection", "introspection", "introspective",
                                            "faith", "spirituality", "soul", "soulful", "soul-searching"]):
            return "Gentle"
        elif any(word in lowered for word in ["change", "breakthrough", "ready", "strong", "bold", "shift"]):
            return "Empowering"
        elif any(word in lowered for word in ["meaning", "purpose", "identity", "truth", "values"]):
            return "Philosophical"

        # VADER fallback
        if compound < -0.3:
            return "Gentle"
        elif compound > 0.3:
            return "Empowering"
        else:
            return "Neutral"

    def infer_theme(self, text: str) -> str:
        lowered = text.lower()

        forgiveness_keywords = ["forgive", "regret", "sorry", "apologize"]
        growth_keywords = ["grow", "evolve", "transform", "change"]
        resilience_keywords = ["strong", "bounce back", "bounced back", "cope", "coping", "recover", "resilient"]
        courage_keywords = ["fear", "brave", "face", "confront"]
        spirituality_keywords = ["pray", "meditate", "reflect", "faith", "spiritual", "divine", "grace", "sacred"]
        healing_keywords = ["heal", "healing", "recover", "release", "let go", "grieve"]
        identity_keywords = ["purpose", "meaning", "who i am", "identity", "truth", "values"]

        if any(word in lowered for word in forgiveness_keywords):
           return "Forgiveness"
        elif any(word in lowered for word in growth_keywords):
           return "Growth"
        elif any(word in lowered for word in resilience_keywords):
             return "Resilience"
        elif any(word in lowered for word in courage_keywords):
             return "Courage"
        elif any(word in lowered for word in spirituality_keywords):
             return "Spirituality"
        elif any(word in lowered for word in healing_keywords):
             return "Healing"
        elif any(word in lowered for word in identity_keywords):
             return "Identity"
        else:
             return "Unspecified"


    def compose_response(self, user_text: str, mode: str = "Conversational") -> dict:

        tone = self.detect_tone(user_text)
        theme = self.infer_theme(user_text)

        if mode == "Guided":
           guided_prompt = self.generate_guided_prompt(theme, tone)
           full_response = guided_prompt
        else:
            base_response = random.choice(self.tone_templates.get(tone, self.tone_templates["Neutral"]))
            follow_up = self.generate_follow_up(tone, theme)
            full_response = base_response + ("\n\n" + follow_up if follow_up else "")

        
        return {
        "response": full_response,
        "tone": tone,
        "theme": theme
        }


    def generate_follow_up(self, tone: str, theme: str) -> str:
        # Tone-based prompts
        gentle_prompts = [
            "Would you like to sit with that feeling a bit longer?",
            "It’s okay to pause here. What’s coming up for you?",
            "Would you like to write about this feeling in your journal?"
        ]
        empowering_prompts = [
            "Is there a step you feel ready to take?",
            "What’s one small move that feels doable today?",
            "Would you like to name the strength you’re drawing on?"
        ]
        philosophical_prompts = [
            "What meaning do you find in this moment?",
            "Does this reflection connect to a deeper truth for you?",
            "Would you like to explore the values behind this feeling?"
        ]

        # Theme-based prompts
        forgiveness_prompts = [
            "Is there someone—or yourself—you’re ready to forgive?",
            "Would you like to reflect on what release might feel like?",
            "Is there a moment you’d like to let go of?"
        ]
        resilience_prompts = [
            "What’s helped you bounce back before?",
            "Is there a strength you’ve leaned on in the past?",
            "Would you like to reflect on how you’ve grown through adversity?"
        ]
        spirituality_prompts = [
            "Would you like to reflect on your spiritual practice today?",
            "Is there a prayer, meditation, or ritual that brings you peace?",
            "Would you like to write about your connection to something greater?"
        ]

        healing_prompts = [
        "Would you like to reflect on what healing means to you?",
        "Is there something you’re ready to release or let go of?",
        "Would writing about this help you process it gently?"
        ]

        identity_prompts = [
        "What truth is emerging for you in this moment?",
        "Would you like to explore who you’re becoming?",
        "Is there a value or belief you’re reconnecting with?"
       ]

        

        # Priority: tone first, then theme
        if tone == "Gentle":
            return random.choice(gentle_prompts)
        elif tone == "Empowering":
            return random.choice(empowering_prompts)
        elif tone == "Philosophical":
            return random.choice(philosophical_prompts)

        if theme == "Forgiveness":
            return random.choice(forgiveness_prompts)
        elif theme == "Resilience":
            return random.choice(resilience_prompts)
        elif theme == "Spirituality":
            return random.choice(spirituality_prompts)
        elif theme == "Healing":
            return random.choice(healing_prompts)
        elif theme == "Identity":
            return random.choice(identity_prompts)

        return None
    
    def generate_guided_prompt(self, theme: str, tone: str) -> str:
        prompts = {
        "Forgiveness": [
            "Is there someone you’re ready to forgive?",
            "What would compassion toward yourself look like today?"
        ],
        "Resilience": [
            "What’s helped you bounce back before?",
            "Is there a strength you’ve rediscovered recently?"
        ],
        "Spirituality": [
            "Would you like to reflect on your spiritual practice?",
            "Is there a prayer or ritual that brings you peace?"
        ],
        "Healing": [
            "What does healing mean to you right now?",
            "Is there something you’re ready to release?"
        ],
        "Identity": [
            "Who are you becoming?",
            "What truth feels alive in you today?"
        ]
        }

        if theme in prompts:
           return random.choice(prompts[theme])
        else:
           return "What would you like to reflect on today?"





