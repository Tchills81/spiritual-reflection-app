import streamlit as st
import pandas as pd
import re
from datetime import datetime, timedelta
from io import BytesIO
from gtts import gTTS
import plotly.express as px

from utils.themes import get_themes_with_icons
from utils.reflection_summary_engine import ReflectionSummaryEngine
from utils.reflection_flows import play_ambient_music
from utils.milestone_utils import detect_reflection_milestones
from ui.incons import tone_icon_map, theme_icon_map, mood_icon_map, affirmation_map
from ui.response_engine import generate_affirmation