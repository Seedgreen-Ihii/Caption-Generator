import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Real Estate Caption Generator", page_icon="🏡")
st.title("🏡 Real Estate Caption Generator")

# Initialize session state to track free generations
if "generation_count" not in st.session_state:
    st.session_state.generation_count = 0

FREE_LIMIT = 3

# List of authorized buyer emails (manually add buyer emails here)
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
        # Unlimited generations for paid users
        prompt = f"Act as an expert real estate copywriter. Write a {tone} social media caption specifically optimized for {platform} about this property: {details}. Include relevant formatting, emojis, and hashtags suited for {platform}."
        with st.spinner("Generating caption..."):
            st.write(model.generate_content(prompt).text)
            
    elif remaining_free > 0:
        # Allow generation for trial users and increment the counter
        prompt = f"Act as an expert real estate copywriter. Write a {tone} social media caption specifically optimized for {platform} about this property: {details}. Include relevant formatting, emojis, and hashtags suited for {platform}."
        with st.spinner("Generating caption..."):
            st.write(model.generate_content(prompt).text)
            st.session_state.generation_count += 1
            st.rerun()  # Refresh app to instantly update the remaining count
            
    else:
        # Block user if trial is finished
        st.error("Trial limit reached! Please buy lifetime access or log in via the sidebar.")
