import streamlit as st
import google.generativeai as genai

# --- הגדרת העמוד ---
st.set_page_config(page_title="PostFlow AI", page_icon="🚀", layout="wide")

# --- עיצוב CSS ---
st.markdown("""
<style>
    .stApp { background-color: #0E1117; color: white; }
    .stTextArea textarea { background-color: #1E1E1E; color: white; }
    .stButton>button { background-color: #7C3AED; color: white; border-radius: 10px; height: 50px; }
</style>
""", unsafe_allow_html=True)

st.title("🚀 PostFlow")
st.caption("הפוך מחשבות גולמיות לפוסטים ויראליים בשניות")

# --- בדיקת מפתח (החלק החשוב) ---
# המערכת בודקת אם יש מפתח ב"כספת" של השרת
if "GOOGLE_API_KEY" in st.secrets:
    api_key = st.secrets["GOOGLE_API_KEY"]
else:
    # אם אין, מבקשים מהמשתמש (למקרה שאתה בודק מקומית)
    api_key = st.sidebar.text_input("הכנס מפתח Gemini API", type="password")

# --- מסך ראשי ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("💡 הרעיון שלך")
    platform = st.selectbox("לאיזו פלטפורמה?", ["LinkedIn", "Twitter/X Thread", "Instagram Caption", "Facebook"])
    tone = st.selectbox("איזה סגנון?", ["מקצועי ורציני", "ויראלי וקצבי", "מצחיק ושנון", "סיפורי ורגשי"])
    raw_idea = st.text_area("שפוך כאן את המחשבות שלך...", height=200)
    generate_btn = st.button("צור קסם ✨")

with col2:
    st.subheader("📝 התוצאה")
    result_container = st.empty()
    
    if generate_btn:
        if not api_key:
            st.error("חסר מפתח API! יש להגדיר אותו ב-Secrets בשרת.")
        elif not raw_idea:
            st.warning("לא כתבת שום רעיון...")
        else:
            try:
                with st.spinner('ה-AI כותב עבורך...'):
                    genai.configure(api_key=api_key)
                    # שימוש במודל 1.5 Pro החזק
                    model = genai.GenerativeModel('gemini-1.5-pro')
                    
                    prompt = f"""
                    You are an expert social media ghostwriter.
                    Platform: {platform}
                    Tone: {tone}
                    User's raw thought: "{raw_idea}"
                    Task: Rewrite this into a perfect, engaging post in Hebrew.
                    Add emojis, line breaks, and hashtags.
                    """
                    
                    response = model.generate_content(prompt)
                    result_container.success("הפוסט מוכן!")
                    st.text_area("העתק מכאן:", value=response.text, height=400)
            except Exception as e:
                st.error(f"שגיאה: {str(e)}")
