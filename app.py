import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Real Estate Caption Generator", page_icon="🏡")
st.title("🏡 Real Estate Caption Generator")

# Initialize session states for memory
if "generation_count" not in st.session_state:
    st.session_state.generation_count = 0
if "last_caption" not in st.session_state:
    st.session_state.last_caption = ""

FREE_LIMIT = 3

# List of authorized buyer emails
AUTHORIZED_EMAILS = [
    "buyer1@gmail.com",
    "realtorjohn@yahoo.com",
    "test@example.com"
]

# --- SIDEBAR: PAID MEMBER LOGIN ---
st.sidebar.header("Paid Member Access")
user_email = st.sidebar.text_input("Already bought? Enter your email:").strip().lower()

is_paid_user = user_email in [e.lower() for e in AUTHORIZED_EMAILS]

if is_paid_user:
    st.sidebar.success("✅ Lifetime Access Active")
elif user_email:
    st.sidebar.error("❌ Email not on paid list.")
    st.sidebar.markdown("[Buy Lifetime Access ($7)](https://doleeseed.gumroad.com/l/lxdlsf)")
else:
    st.sidebar.info("Already purchased? Enter your buyer email above to unlock unlimited access.")


# --- MAIN APP LOGIC ---
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-3.6-flash')

platform = st.selectbox("Choose the platform:", ["Instagram", "Facebook", "LinkedIn", "TikTok"])
tone = st.selectbox("Choose the caption tone:", ["Professional", "Fun & Energetic", "Urgent (Just Listed!)", "Luxury & Exclusive"])
details = st.text_input("Enter property details (e.g., 3 bed, pool, downtown):")

# --- THE SUPERCHARGED PROMPT ---
master_prompt = f"""
Act as a world-class real estate copywriter and digital marketing strategist. 
Write a highly engaging, conversion-optimized {tone} social media caption specifically for {platform} about this property: {details}.

Strictly follow these rules:
1. Hook: Start with a powerful, scroll-stopping opening line.
2. Framework: Use the AIDA framework (Attention, Interest, Desire, Action) to build emotional connection and highlight unique selling propositions.
3. SEO: Seamlessly integrate high-ranking real estate search keywords relevant to the property.
4. Action: End with a highly compelling Call to Action (CTA) that drives immediate inquiries, clicks, or DMs.
5. Formatting: Use excellent spacing, relevant emojis, and highly targeted hashtags suited for {platform}'s algorithm.
"""

# Calculate remaining free generations
remaining_free = FREE_LIMIT - st.session_state.generation_count

# Show free trial status banner for non-paid users
if not is_paid_user:
    if remaining_free > 0:
        st.caption(f"🎁 **Free Trial Active:** You have **{remaining_free} of {FREE_LIMIT}** free generations remaining.")
    else:
        st.warning("🔒 You've used all 3 of your free trial generations!")
        st.markdown("### Unlock Unlimited Access for $7")
        st.write("Get instant, lifetime access to generate unlimited captions for any property, platform, or tone.")
        st.markdown("[👉 **Click Here to Buy Lifetime Access for $7**](https://doleeseed.gumroad.com/l/lxdlsf)")


# --- GENERATE BUTTON LOGIC ---
if st.button("Generate Caption"):
    if not details:
        st.warning("Please enter property details first!")
        
    elif is_paid_user:
        with st.spinner("Generating high-converting caption..."):
            st.session_state.last_caption = model.generate_content(master_prompt).text
            st.rerun() 
            
    elif remaining_free > 0:
        with st.spinner("Generating high-converting caption..."):
            st.session_state.last_caption = model.generate_content(master_prompt).text
            st.session_state.generation_count += 1
            st.rerun() 
            
    else:
        st.error("Trial limit reached! Please buy lifetime access or log in via the sidebar.")

# --- DISPLAY THE GENERATED CAPTION ---
if st.session_state.last_caption:
    st.success("✨ Here is your caption:")
    st.write(st.session_state.last_caption)
