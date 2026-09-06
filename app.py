import streamlit as st
import google.generativeai as genai

st.title("🏡 Real Estate Caption Generator")
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-3.6-flash')

# New Platform Selector
platform = st.selectbox("Choose the platform:", ["Instagram", "Facebook", "LinkedIn", "TikTok"])

# Existing Tone Selector
tone = st.selectbox("Choose the caption tone:", ["Professional", "Fun & Energetic", "Urgent (Just Listed!)", "Luxury & Exclusive"])

details = st.text_input("Enter property details (e.g., 3 bed, pool, downtown):")

if st.button("Generate Caption") and details:
    # Upgraded Prompt to include the platform
    prompt = f"Act as an expert real estate copywriter. Write a {tone} social media caption specifically optimized for {platform} about this property: {details}. Include relevant formatting, emojis, and hashtags suited for {platform}."
    
    st.write(model.generate_content(prompt).text)
