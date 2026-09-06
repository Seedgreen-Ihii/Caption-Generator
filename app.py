import streamlit as st
import google.generativeai as genai

st.title("🏡 Real Estate Caption Generator")
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-3.6-flash')

# New Dropdown Menu
tone = st.selectbox("Choose the caption tone:", ["Professional", "Fun & Energetic", "Urgent (Just Listed!)", "Luxury & Exclusive"])

details = st.text_input("Enter property details (e.g., 3 bed, pool, downtown):")

if st.button("Generate Caption") and details:
    # Updated Prompt
    prompt = f"Act as an expert real estate copywriter. Write a {tone} Instagram caption for: {details}. Include emojis and hashtags."
    
    st.write(model.generate_content(prompt).text)
