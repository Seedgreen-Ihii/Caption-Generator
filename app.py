import streamlit as st
import google.generativeai as genai
from supabase import create_client, Client

st.set_page_config(page_title="Real Estate Caption Generator", page_icon="🏡")
st.title("🏡 Real Estate Caption Generator")

# --- 1. CONNECT TO SUPABASE DATABASE ---
@st.cache_resource
def init_supabase() -> Client:
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)

supabase = init_supabase()

FREE_LIMIT = 3
# Initialize session state for memory
if "last_caption" not in st.session_state:
    st.session_state.last_caption = ""
# --- 2. MANDATORY USER IDENTIFICATION ---
st.markdown("### Step 1: Enter your email to start")
user_email = st.text_input("Enter your email address:").strip().lower()

if not user_email:
    st.info("👆 Please enter your email above to access the caption generator.")
    st.stop()

# --- 3. FETCH OR CREATE USER RECORD ---
# Query Supabase for this specific email
response = supabase.table("user_trials").select("*").eq("email", user_email).execute()
user_data = response.data

if not user_data:
    # New User: Create record in database
    new_user = {"email": user_email, "generations_used": 0, "is_paid": False}
    supabase.table("user_trials").insert(new_user).execute()
    generations_used = 0
    is_paid_user = False
else:
    # Existing User: Fetch persistent record
    generations_used = user_data[0]["generations_used"]
    is_paid_user = user_data[0]["is_paid"]

remaining_free = FREE_LIMIT - generations_used

# --- 4. STATUS BANNERS ---
if is_paid_user:
    st.success("✅ **Lifetime Access Active** (Unlimited Generations)")
elif remaining_free > 0:
    st.caption(f"🎁 **Free Trial Active:** You have **{remaining_free} of {FREE_LIMIT}** free generations remaining.")
else:
    st.warning("🔒 **Trial Expired:** You have used all 3 of your free trial generations.")
    st.markdown("### Unlock Unlimited Access for $7")
    st.markdown("[👉 **Click Here to Buy Lifetime Access for $7**](https://doleeseed.gumroad.com/l/lxdlsf)")

# --- 5. APP INTERFACE ---
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-3.6-flash')

platform = st.selectbox("Choose the platform:", ["Instagram", "Facebook", "LinkedIn", "TikTok"])
tone = st.selectbox("Choose the caption tone:", ["Professional", "Fun & Energetic", "Urgent (Just Listed!)", "Luxury & Exclusive"])
details = st.text_input("Enter property details (e.g., 3 bed, pool, downtown):")

master_prompt = f"""
Act as a world-class real estate copywriter and digital marketing strategist. 
Write a highly engaging, conversion-optimized {tone} social media caption specifically for {platform} about this property: {details}.

Strictly follow these rules:
1. Hook: Start with a powerful, scroll-stopping opening line.
2. Framework: Use the AIDA framework (Attention, Interest, Desire, Action).
3. SEO: Seamlessly integrate high-ranking real estate search keywords.
4. Action: End with a highly compelling Call to Action (CTA).
5. Formatting: Use excellent spacing, relevant emojis, and targeted hashtags.
"""

# --- 6. GENERATION LOGIC WITH PERSISTENT COUNTER ---
if st.button("Generate Caption"):
    if not details:
        st.warning("Please enter property details first!")
    elif is_paid_user:
        with st.spinner("Generating caption..."):
            # Save to memory, then refresh
            st.session_state.last_caption = model.generate_content(master_prompt).text
            st.rerun()
    elif remaining_free > 0:
        with st.spinner("Generating caption..."):
            # Save to memory
            st.session_state.last_caption = model.generate_content(master_prompt).text
            
            # Increment and update the database permanently
            new_count = generations_used + 1
            supabase.table("user_trials").update({"generations_used": new_count}).eq("email", user_email).execute()
            
            # Refresh to update the counter banner
            st.rerun()
    else:
        st.error("Trial limit reached for this email! Please buy lifetime access to continue.")

# --- 7. DISPLAY THE GENERATED CAPTION ---
if st.session_state.last_caption:
    st.success("✨ Here is your caption:")
    st.write(st.session_state.last_caption)
