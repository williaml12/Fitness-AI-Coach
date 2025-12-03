# import streamlit as st
# import google.generativeai as genai

# # -----------------------
# # 🔑 Configure Gemini API
# # -----------------------
# api_key = st.secrets["GOOGLE_API_KEY"]
# genai.configure(api_key=api_key)

# # model = genai.GenerativeModel("gemini-1.5-flash")
# model = genai.GenerativeModel("gemini-2.5-flash")

# # -----------------------
# # 🌟 Page Config
# # -----------------------
# st.set_page_config(
#     page_title="AI Resume Reviewer",
#     page_icon="📄",
#     layout="wide"
# )

# # -----------------------
# # 🎯 Header Section
# # -----------------------
# st.markdown("""
# <h1 style='text-align:center; margin-bottom:0;'>📄 AI Resume Reviewer</h1>
# <p style='text-align:center; font-size:18px; color:gray;'>
# Upload your resume and get industry-ready feedback powered by Google Gemini.
# </p>
# """, unsafe_allow_html=True)

# st.write("---")

# # -----------------------
# # 💡 About the Project
# # -----------------------
# with st.expander("💡 About the Project", expanded=True):
#     st.markdown("""
# **AI Resume Reviewer** simplifies your resume improvement process using generative AI:

# - Analyzes your resume content  
# - Identifies strengths & weaknesses  
# - Suggests improvements for clarity, relevance, and professionalism  
# - Gives tips tailored to your target job or industry  
# - No downloads or coding required — upload and get instant feedback  
#     """)

# st.write("---")

# # -----------------------
# # 📤 Upload Resume
# # -----------------------
# st.subheader("📤 Upload Your Resume")

# uploaded_file = st.file_uploader(
#     "Upload your resume (PDF or TXT)",
#     type=["pdf", "txt"]
# )

# # -----------------------
# # 🎯 Job Context Input
# # -----------------------
# st.subheader("🎯 Target Job / Industry")

# job_title = st.text_input("Job Title")
# job_description = st.text_area(
#     "Job Description / Requirements",
#     height=150,
#     placeholder="Paste job description or describe the role you're targeting..."
# )

# st.write("---")

# # -----------------------
# # 🔍 Analyze Button
# # -----------------------
# if st.button("🔍 Analyze My Resume", type="primary"):
#     if not uploaded_file:
#         st.error("Please upload your resume first.")
#     else:
#         with st.spinner("Analyzing your resume with Gemini... ⏳"):

#             # Read uploaded file
#             resume_text = uploaded_file.read().decode("utf-8", errors="ignore")

#             # Prompt to Gemini
#             prompt = f"""
# You are an expert resume reviewer. Analyze the following resume and give clear, structured feedback.

# Resume Content:
# {resume_text}

# Job Target:
# - Job Title: {job_title}
# - Job Description / Requirements: {job_description}

# Please provide analysis in the following format:

# 1. **Overall Summary**
# 2. **Strengths**
# 3. **Weaknesses**
# 4. **Suggestions for Improvement**
# 5. **ATS Optimization Tips**
# 6. **Job Target Alignment Assessment**
# 7. **Rewrite Suggestions (Bullet Points / Summary / Skills)**

# Make the feedback detailed, actionable, and easy to follow.
# """

#             response = model.generate_content(prompt)

#         # Display response
#         st.subheader("📊 Resume Analysis Report")
#         st.markdown(response.text)

#         st.success("Done! Scroll up to view your report.")

# # -----------------------
# # 📌 Footer
# # -----------------------
# st.write("---")
# st.markdown(
#     "<p style='text-align:center; color:gray;'>Built with ❤️ using Streamlit + Google Gemini</p>",
#     unsafe_allow_html=True
# )











import streamlit as st
import google.generativeai as genai
from io import BytesIO
from PyPDF2 import PdfReader
from docx import Document
import json
import re

# -----------------------
# Configure Gemini API
# -----------------------
api_key = st.secrets.get("GOOGLE_API_KEY", None)
if not api_key:
    st.error("Missing Google API key in st.secrets['GOOGLE_API_KEY']. Add it and redeploy.")
    st.stop()

genai.configure(api_key=api_key)
# model = genai.GenerativeModel("gemini-1.5-flash")  # adjust model if needed
model = genai.GenerativeModel("gemini-2.5-flash")

# -----------------------
# Page config
# -----------------------
st.set_page_config(page_title="AI Resume Reviewer", page_icon="📄", layout="wide")

# -----------------------
# Helper: extract text from uploaded file
# -----------------------
def extract_text_from_file(uploaded_file) -> str:
    """
    Accepts a Streamlit UploadedFile and returns extracted text.
    Supports: .pdf, .docx, .txt
    """
    name = uploaded_file.name.lower()
    uploaded_file.seek(0)
    data = uploaded_file.read()

    # Handle PDF
    if name.endswith(".pdf"):
        try:
            reader = PdfReader(BytesIO(data))
            text_pages = []
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text_pages.append(page_text)
            return "\n\n".join(text_pages).strip()
        except Exception as e:
            st.warning(f"PDF parsing error: {e}")
            return ""

    # Handle DOCX
    if name.endswith(".docx"):
        try:
            doc = Document(BytesIO(data))
            paragraphs = [p.text for p in doc.paragraphs if p.text]
            return "\n\n".join(paragraphs).strip()
        except Exception as e:
            st.warning(f"DOCX parsing error: {e}")
            return ""

    # Handle plain text
    if name.endswith(".txt"):
        try:
            return data.decode("utf-8", errors="ignore").strip()
        except Exception:
            return data.decode("latin-1", errors="ignore").strip()

    return ""

# -----------------------
# Truncate helper (avoid very long prompts)
# -----------------------
def truncate_text(text: str, max_chars: int = 30000) -> (str, bool):
    if len(text) <= max_chars:
        return text, False
    truncated = text[:max_chars]
    return truncated, True

# -----------------------
# UI
# -----------------------
st.title("📄 AI Resume Reviewer")
st.write("Upload your resume and optionally paste a job description. The app extracts text from the file, sends it to Gemini, and returns a structured analysis.")

uploaded_file = st.file_uploader("Upload resume (PDF, DOCX, TXT)", type=["pdf", "docx", "txt"])
job_title = st.text_input("Target Job Title")
job_description = st.text_area("Job Description / Requirements", height=150)

st.markdown("---")

if st.button("🔍 Analyze My Resume"):
    if not uploaded_file:
        st.error("Please upload a resume file first.")
    else:
        with st.spinner("Extracting text from your document..."):
            resume_text = extract_text_from_file(uploaded_file)

        if not resume_text:
            st.error(
                "Could not extract readable text from the uploaded file. "
                "If it's a scanned PDF/image, please OCR it first or paste the resume text manually."
            )
        else:
            # Truncate if too long and warn user
            resume_text, was_truncated = truncate_text(resume_text, max_chars=30000)
            if was_truncated:
                st.warning("Resume text was truncated to fit the model prompt (very long resume).")

            # Build prompt asking for JSON only
            prompt = f"""
You are an expert resume reviewer. Analyze the resume and produce a JSON object ONLY (no surrounding text)
with the following keys: score, summary, strengths, weaknesses, suggestions, ats_tips, alignment.

- score: a string percentage like "82%"
- summary: short paragraph
- strengths: list of short bullet items
- weaknesses: list of short bullet items
- suggestions: list of specific actionable changes
- ats_tips: list of short tips for ATS optimization
- alignment: short description of how well it matches the provided job

Resume:
{resume_text}

Job target:
Job Title: {job_title}
Job Description / Requirements:
{job_description}

Return STRICTLY valid JSON. Example:
{{"score":"80%","summary":"...","strengths":["..."],"weaknesses":["..."],"suggestions":["..."],"ats_tips":["..."],"alignment":"..."}}
"""

            # Call Gemini
            with st.spinner("Calling Gemini for analysis..."):
                try:
                    response = model.generate_content(prompt)
                    raw = response.text.strip()
                except Exception as e:
                    st.error(f"Error calling Gemini: {e}")
                    st.stop()

            # Sometimes the model returns text plus JSON; attempt to extract JSON substring
            json_text = None
            try:
                # naive search for the first JSON object in the response
                match = re.search(r"\{[\s\S]*\}\s*$", raw)
                if match:
                    json_text = match.group(0)
                else:
                    # fallback: try to find the first '{' and last '}' and slice
                    first = raw.find("{")
                    last = raw.rfind("}")
                    if first != -1 and last != -1 and last > first:
                        json_text = raw[first:last+1]
            except Exception:
                json_text = None

            if not json_text:
                st.error("Gemini did not return a JSON object. Raw output shown below for debugging.")
                st.code(raw)
            else:
                try:
                    result = json.loads(json_text)
                except Exception as e:
                    st.error(f"Failed to parse JSON from the model response: {e}")
                    st.code(json_text)
                else:
                    # Display structured results
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

                    st.subheader("🛠 Suggestions")
                    for sug in result.get("suggestions", []):
                        st.write("• " + sug)

                    st.subheader("📑 ATS Tips")
                    for tip in result.get("ats_tips", []):
                        st.write("• " + tip)

                    st.subheader("🎯 Job Alignment")
                    st.write(result.get("alignment", ""))

                    # Keep raw response hidden under expander for debugging
                    with st.expander("Raw model output (for debugging)"):
                        st.code(raw)

st.markdown("---")
st.caption("Built with Streamlit + Google Gemini")

