import streamlit as st
from PIL import Image
import io

# ---------------------------- PAGE CONFIG ----------------------------
st.set_page_config(
    page_title="AI Resume Reviewer",
    page_icon="📝",
    layout="wide"
)

# ---------------------------- HEADER ----------------------------
st.title("📝 AI Resume Reviewer")
st.subheader("Upload your resume and describe your target job — get instant, AI-powered feedback.")

st.markdown("""
Welcome to the **AI Resume Reviewer!**  
Upload your resume *and* provide context about your **target job or industry**  
(such as job title, job description, and key requirements).

I’ll analyze your resume and provide:

- ✔️ Content quality & clarity analysis  
- ✔️ Formatting and structure feedback  
- ✔️ ATS-readiness scoring  
- ✔️ Alignment with job requirements  
- ✔️ Specific improvement recommendations  

You can also ask **follow-up questions** after the analysis.
""")

st.markdown("---")

# ---------------------------- INPUT SECTION ----------------------------

col1, col2 = st.columns([1.2, 1])

with col1:
    st.header("📄 Upload Your Resume")
    uploaded_file = st.file_uploader("Upload PDF or DOCX", type=["pdf", "docx"])

with col2:
    st.header("🎯 Target Job Information")
    job_title = st.text_input("Job Title (e.g., Software Engineer, Data Analyst)")
    job_description = st.text_area("Job Description / Key Responsibilities")
    job_requirements = st.text_area("Required Skills / Qualifications")

st.markdown("---")

# ---------------------------- ANALYSIS BUTTON ----------------------------

if uploaded_file and job_title:
    if st.button("🔍 Analyze My Resume"):
        with st.spinner("Analyzing your resume... This may take a few seconds."):

            # ----------------------------
            # PLACE YOUR AI MODEL HERE
            # Example mock result for demo
            # ----------------------------
            mock_result = {
                "overall_score": "82%",
                "summary": "Your resume is strong but can be improved for better ATS scoring and clarity.",
                "content_feedback": [
                    "Add more quantifiable achievements.",
                    "Your experience section is strong but could use better action verbs.",
                    "Skills section is missing a few industry-standard keywords."
                ],
                "formatting_feedback": [
                    "Consider using consistent bullet styles.",
                    "Margins and spacing can be improved for readability."
                ],
                "alignment_feedback": [
                    "Matches 70% of the required skills.",
                    "Consider highlighting projects relevant to the target job."
                ],
            }

        # ---------------------------- RESULTS SECTION ----------------------------
        st.success("Resume analysis complete!")

        st.header("📊 Overall Evaluation")
        st.metric(label="Resume Score", value=mock_result["overall_score"])

        st.subheader("🧠 Summary")
        st.write(mock_result["summary"])

        st.subheader("📝 Content Feedback")
        for item in mock_result["content_feedback"]:
            st.write(f"- {item}")

        st.subheader("🎨 Formatting Feedback")
        for item in mock_result["formatting_feedback"]:
            st.write(f"- {item}")

        st.subheader("🎯 Job Alignment Feedback")
        for item in mock_result["alignment_feedback"]:
            st.write(f"- {item}")

        st.markdown("---")

        # ---------------------------- FOLLOW-UP QUESTIONS ----------------------------
        st.header("💬 Ask Follow-Up Questions")
        follow_up = st.text_input("Ask anything (e.g., 'How can I improve my summary?')")
        if st.button("Ask"):
            st.info("Follow-up answer will go here. (Connect to your model.)")

else:
    st.info("Please upload your resume and enter at least the job title to continue.")

# ---------------------------- FOOTER ----------------------------
st.markdown("---")
st.caption("Built with Streamlit · AI Resume Reviewer · 2025")
