import google.generativeai as genai
import docx2txt
import PyPDF2

api_key = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-pro")


# ---------------------------- PAGE CONFIG ----------------------------
st.set_page_config(
    page_title="AI Resume Reviewer",
    page_icon="📝",
    layout="wide"
)

# ---------------------------- HERO SECTION ----------------------------
st.markdown("""
<style>
.hero {
    background-color: #f5f7fa;
    padding: 50px;
    border-radius: 20px;
    text-align: center;
    margin-bottom: 30px;
}
.card {
    background-color: white;
    padding: 25px;
    border-radius: 20px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    margin: 10px;
}
.section {
    padding-top: 20px;
    padding-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
    <h1 style='font-size: 48px; margin-bottom: 5px;'>📝 AI Resume Reviewer</h1>
    <h3 style='color: #555;'>Instant, AI-powered resume feedback — no downloads, no coding.</h3>
</div>
""", unsafe_allow_html=True)

# ---------------------------- ABOUT SECTION ----------------------------
st.markdown("""
<div class="section">
<h2>💡 About the Project</h2>
<p style='font-size: 18px; line-height: 1.6;'>
AI Resume Reviewer simplifies the resume review process by using advanced <b>generative AI</b> to:
</p>

<ul style='font-size: 17px; line-height: 1.7;'>
<li>🔍 Analyze your resume content</li>
<li>⭐ Identify strengths and weaknesses</li>
<li>🛠️ Offer tailored suggestions to enhance clarity, relevance, and professionalism</li>
<li>🎯 Provide tips for targeting specific industries or roles</li>
</ul>

<p style='font-size: 17px; margin-top: 10px;'>
No downloads or coding required — just upload your resume and get **instant feedback**.
</p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ---------------------------- FEATURE CARDS ----------------------------
st.subheader("✨ What This Tool Can Do")

col_a, col_b, col_c = st.columns(3)

with col_a:
    st.markdown("""
    <div class="card">
        <h3>📄 Content Analysis</h3>
        <p>Examines clarity, tone, keyword usage, and storytelling quality.</p>
    </div>
    """, unsafe_allow_html=True)

with col_b:
    st.markdown("""
    <div class="card">
        <h3>📊 Strengths & Weaknesses</h3>
        <p>Shows what stands out and what needs improvement.</p>
    </div>
    """, unsafe_allow_html=True)

with col_c:
    st.markdown("""
    <div class="card">
        <h3>🎯 Job Alignment</h3>
        <p>Checks how well your resume matches a target role or job description.</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ---------------------------- INPUT SECTION ----------------------------
st.header("📥 Upload Your Resume")

col1, col2 = st.columns([1.1, 1])

with col1:
    uploaded_file = st.file_uploader("Upload your resume (PDF or DOCX)", type=["pdf", "docx"])

with col2:
    st.subheader("🎯 Target Job Information")
    job_title = st.text_input("Target Job Title")
    job_description = st.text_area("Job Description")
    job_requirements = st.text_area("Required Skills / Qualifications")

st.markdown("---")

# ---------------------------- ANALYSIS ----------------------------
if uploaded_file and job_title:
    if st.button("🔍 Analyze My Resume"):
        with st.spinner("Analyzing your resume with Google Gemini AI..."):

            # Extract resume text
            resume_text = extract_text_from_file(uploaded_file)

            if not resume_text.strip():
                st.error("Could not extract text from file. Make sure it is a valid PDF or DOCX.")
                st.stop()

            # Create the prompt for Gemini
            prompt = f"""
You are an expert resume reviewer.

Analyze the resume content below and evaluate it for clarity, structure, relevance, and alignment 
with the target job information.

Return your response in clean structured JSON with these keys only:
- score (0–100%)
- summary
- strengths (list)
- weaknesses (list)
- alignment (description)

--------------------
RESUME CONTENT:
{resume_text}

--------------------
TARGET JOB TITLE: {job_title}

JOB DESCRIPTION:
{job_description}

JOB REQUIREMENTS:
{job_requirements}
"""

            # Call Gemini
            response = model.generate_content(prompt)
            cleaned = response.text.strip()

            # Convert AI JSON to Python dict
            import json
            try:
                result = json.loads(cleaned)
            except:
                st.error("Gemini returned an invalid response. Print raw output below:")
                st.code(cleaned)
                st.stop()

        # ----------- DISPLAY RESULTS -----------
        st.success("Resume analysis complete!")

        st.header("📊 Results Overview")
        st.metric("Resume Score", result.get("score", "N/A"))

        st.subheader("🧠 Summary")
        st.write(result.get("summary", ""))

        st.subheader("⭐ Strengths")
        for s in result.get("strengths", []):
            st.write("• " + s)

        st.subheader("⚠️ Weaknesses")
        for w in result.get("weaknesses", []):
            st.write("• " + w)

        st.subheader("🎯 Job Alignment")
        st.write(result.get("alignment", ""))

        st.markdown("---")

        # ---------------- FOLLOW-UP ----------------
        st.header("💬 Ask a Follow-Up Question")
        q = st.text_input("Example: How can I improve my skills section?")
        if st.button("Ask"):
            follow_resp = model.generate_content(
                f"Follow-up question:\n{q}\n\nHere is the previous resume evaluation:\n{result}"
            )
            st.info(follow_resp.text)

else:
    st.info("Please upload your resume and enter a target job title to proceed.")


# ---------------------------- FOOTER ----------------------------
st.markdown("---")
st.caption("Built with ❤️ using Streamlit · AI Resume Reviewer · 2025")
