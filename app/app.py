import streamlit as st
from ui.ui_components import render_reflection_journal, render_tab2, render_chat_companion

st.set_page_config(page_title="Spiritual Reflection App", layout="wide")

st.title("🧘 Spiritual Reflection Assistant")

tab1, tab2, tab3 = st.tabs(["Reflection Journal", "Generated Reflection", "Chat Companion"])

with tab1:
    render_reflection_journal()

with tab2:
    render_tab2(tone="Gentle", theme="Growth", length="Short", backend="Auto")

with tab3:
    render_chat_companion()
