import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from io import BytesIO
from fpdf import FPDF

from src.parse_resume import extract_text_from_pdf
from src.extract_keywords import extract_keywords
from src.save_to_snowflake import save_resume_analysis
from src.compare_with_jobs import (
    get_industries,
    get_roles_for_industry,
    get_keywords_for_role,
    compare_keywords,
    compare_with_custom_jd
)
from src.fetch_from_snowflake import fetch_saved_analytics
from src.suggest_feedback import generate_feedback  # ✅ New AI suggestion module

st.set_page_config(page_title="Resume Analyzer", page_icon="📄", layout="wide")

# Sidebar navigation
st.sidebar.title("📊 Navigation")
page = st.sidebar.radio("Go to", ["Resume Analyzer", "Dashboard"])

if page == "Resume Analyzer":
    st.title("📄 Resume Analytics Tool")

    mode = st.radio("Choose Analysis Mode", ["Select Job Role", "Upload Job Description"])

    selected_industry = ""
    selected_job_role = ""
    result = None
    match_score = 0
    matched_keywords = []
    missing_keywords = []

    # Responsive layout for industry/job role or JD upload
    col1, col2 = st.columns([1, 1])
    with col1:
        if mode == "Select Job Role":
            selected_industry = st.selectbox("Select Industry", get_industries())
            selected_job_role = st.selectbox("Select Job Role", get_roles_for_industry(selected_industry))
        else:
            uploaded_jd_file = st.file_uploader("Upload Job Description (PDF or TXT)", type=["pdf", "txt"])
    with col2:
        uploaded_resume = st.file_uploader("Upload Your Resume (PDF)", type="pdf")

    if uploaded_resume:
        resume_text = extract_text_from_pdf(uploaded_resume)
        resume_keywords = extract_keywords(resume_text)

        if mode == "Select Job Role":
            job_keywords = get_keywords_for_role(selected_industry, selected_job_role)
            result = compare_keywords(resume_keywords, job_keywords)
        else:
            if uploaded_jd_file:
                jd_text = extract_text_from_pdf(uploaded_jd_file) if uploaded_jd_file.type == "application/pdf" else uploaded_jd_file.read().decode("utf-8")
                result = compare_with_custom_jd(resume_keywords, jd_text)
            else:
                st.warning("⚠️ Please upload your job description file.")
                st.stop()

        match_score = result["match_score"]
        matched_keywords = result["matched_keywords"]
        missing_keywords = result["missing_keywords"]

        st.success(f"✅ Match Score: {match_score}%")
        st.markdown("**✅ Matched Keywords:**")
        st.write(", ".join(matched_keywords) if matched_keywords else "None")

        st.markdown("**❌ Missing Keywords:**")
        st.write(", ".join(missing_keywords) if missing_keywords else "None")

        # 📄 Downloadable PDF Report
        def generate_pdf_report():
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt="Resume Analysis Report", ln=True, align="C")
            pdf.ln(10)
            pdf.cell(200, 10, txt=f"Match Score: {match_score}%", ln=True)
            pdf.multi_cell(0, 10, txt=f"\nMatched Keywords:\n{', '.join(matched_keywords)}")
            pdf.multi_cell(0, 10, txt=f"\nMissing Keywords:\n{', '.join(missing_keywords)}")

            pdf_str = pdf.output(dest='S').encode('latin1')  # fpdf outputs string, encode to bytes
            return pdf_str

        # Responsive columns for download button and AI feedback button + output
        col1, col2 = st.columns([1, 2])
        with col1:
            st.download_button(
                label="📥 Download PDF Report",
                data=generate_pdf_report(),
                file_name="resume_analysis_report.pdf",
                mime="application/pdf"
            )
        with col2:
            if st.button("🧠 Get AI Feedback"):
                feedback = generate_feedback(match_score, matched_keywords, missing_keywords)
                st.markdown("### 💡 AI Feedback")
                st.write(feedback)

        user_email = st.text_input("📧 Enter your email (optional to save to Snowflake)")

        if st.button("💾 Save to Snowflake") and user_email:
            save_resume_analysis(
                user_email,
                selected_industry if mode == "Select Job Role" else "Custom",
                selected_job_role if mode == "Select Job Role" else "Custom",
                match_score,
                matched_keywords,
                missing_keywords
            )
            st.success("✅ Resume analysis saved to Snowflake!")

elif page == "Dashboard":
    st.title("📈 Dashboard - Saved Resume Analytics")

    data = fetch_saved_analytics()

    if data.empty:
        st.warning("⚠️ No saved resume analytics found.")
        st.stop()

    # Sidebar Filters with compact columns for better mobile UI
    st.sidebar.markdown("### 🔍 Filters")
    email_filter, industry_filter = st.sidebar.columns(2)
    with email_filter:
        email_filter_val = st.selectbox("Filter by Email", ["All"] + sorted(data["USER_EMAIL"].unique().tolist()))
    with industry_filter:
        industry_filter_val = st.selectbox("Filter by Industry", ["All"] + sorted(data["INDUSTRY"].unique().tolist()))
    job_filter = st.sidebar.selectbox("Filter by Job Role", ["All"] + sorted(data["JOB_ROLE"].unique().tolist()))
    min_score, max_score = st.sidebar.slider("Match Score Range", 0, 100, (0, 100))

    # Apply filters
    filtered_data = data[
        ((data["USER_EMAIL"] == email_filter_val) | (email_filter_val == "All")) &
        ((data["INDUSTRY"] == industry_filter_val) | (industry_filter_val == "All")) &
        ((data["JOB_ROLE"] == job_filter) | (job_filter == "All")) &
        (data["MATCH_SCORE"].between(min_score, max_score))
    ]

    # Show filtered results
    st.subheader("📋 Filtered Resume Entries")
    st.dataframe(filtered_data, use_container_width=True)

    # Visualize Match Score Distribution
    st.subheader("📊 Match Score Distribution")
    fig, ax = plt.subplots()
    ax.hist(filtered_data["MATCH_SCORE"], bins=10, color="skyblue", edgecolor="black")
    ax.set_xlabel("Match Score")
    ax.set_ylabel("Number of Resumes")
    ax.set_title("Distribution of Resume Match Scores")
    st.pyplot(fig)
