import streamlit as st
import google.generativeai as genai

st.title("🏡 Real Estate Caption Generator")
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-3.6-flash')

details = st.text_input("Enter property details (e.g., 3 bed, pool, downtown):")
if st.button("Generate Caption") and details:
    prompt = f"Act as an expert real estate copywriter. Write an engaging Instagram caption for: {details}. Include emojis and hashtags."
    st.write(model.generate_content(prompt).text)
