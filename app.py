import streamlit as st
import google.generativeai as genai

st.title("System Check 🔍")
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

st.write("Google says your API key has access to these specific models:")
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            st.write(m.name)
except Exception as e:
    st.write(f"Error: {e}")
