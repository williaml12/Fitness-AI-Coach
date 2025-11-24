import streamlit as st
from PIL import Image
import io

# Page config
st.set_page_config(
    page_title="ResumeCraft AI – Your Smart Resume Reviewer",
    page_icon=":rocket:",
    layout="wide",
)

# --- Header / Hero Section ---
# Optional background image
try:
    hero_img = Image.open("hero_background.jpg")
    st.image(hero_img, use_column_width=True)
except Exception:
    pass

st.title("ResumeCraft AI")
st.subheader("Your Smart Resume Reviewer")
st.markdown("""
Upload your resume and get instant feedback on structure, content, and ATS-friendliness.
""")

# ―― Feature / Info Section ――
st.markdown("---")
col1, col2, col3 = st.columns(3)

with col1:
    st.header("📄 Upload")
    st.write("Simply drag & drop your resume (PDF or DOCX).")

with col2:
    st.header("🔍 Analyze")
    st.write("Our AI reviews your resume for clarity, relevance, and formatting.")

with col3:
    st.header("✅ Improve")
    st.write("Receive actionable suggestions to make your resume stand out.")

st.markdown("---")

# ―― Upload Section ――
uploaded_file = st.file_uploader("Choose your resume file", type=["pdf","docx"])

if uploaded_file is not None:
    # Show preview or file info
    file_details = {"filename": uploaded_file.name, "filetype": uploaded_file.type, "filesize": uploaded_file.size}
    st.write(file_details)
    
    if st.button("🎯 Review My Resume"):
        with st.spinner("Analyzing your resume..."):
            # Your model logic here: e.g., parse the file, run AI model
            # result = analyse_resume(uploaded_file)
            # For demo let's mock:
            result = {
                "Overall Score": "78%",
                "Strengths": ["Clear summary section", "Relevant keywords matched"],
                "Areas to Improve": ["Add quantifiable achievements", "Shorter bullet points"],
                "ATS Friendly": "Yes"
            }
            
        st.success("Analysis complete!")
        
        # ―― Result Display ――
        st.header("🔍 Your Review")
        st.subheader("Overall Score")
        st.metric(label="", value=result["Overall Score"])
        
        st.subheader("Strengths")
        for s in result["Strengths"]:
            st.write("• " + s)
        
        st.subheader("Areas to Improve")
        for a in result["Areas to Improve"]:
            st.write("• " + a)
        
        st.subheader("ATS Friendly Check")
        st.write(result["ATS Friendly"])

# ―― Footer Section ――
st.markdown("---")
st.write("Built with ♥ using Streamlit and AI. © 2025 Your Company Name")
