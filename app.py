import streamlit as st
from resume_analyzer import extract_text_from_pdf, extract_text_from_docx, analyze_resume
from linkedin_scraper import scrape_linkedin_jobs
from job_matcher import extract_skills_from_analysis, recommend_keywords
from job_storage import store_jobs_csv, store_jobs_mysql   # ⭐ NEW IMPORT

st.set_page_config(page_title="Intelligent Career Recommendation Platform", layout="wide")

# -------------------------
# CUSTOM UI STYLING
# -------------------------

st.markdown("""
<style>

.stApp{
background: linear-gradient(135deg,#0f2027,#203a43,#2c5364);
color:white;
}

.hero{
text-align:center;
padding:20px;
margin-bottom:20px;
}

.glow{
font-size:48px;
font-weight:bold;
background: linear-gradient(90deg,#00dbde,#fc00ff);
-webkit-background-clip:text;
-webkit-text-fill-color:transparent;
animation: glowMove 6s linear infinite;
}

@keyframes glowMove{
0%{background-position:0%}
100%{background-position:200%}
}

.subtitle{
font-size:18px;
opacity:0.85;
margin-top:10px;
}

section[data-testid="stSidebar"]{
background: rgba(0,0,0,0.65);
}

.stButton>button{
background: linear-gradient(45deg,#00c6ff,#0072ff);
color:white;
border-radius:10px;
border:none;
font-weight:bold;
padding:10px 18px;
transition:0.3s;
}

.stButton>button:hover{
background: linear-gradient(45deg,#0072ff,#00c6ff);
transform:scale(1.05);
}

.card{
background:rgba(255,255,255,0.08);
padding:25px;
border-radius:14px;
box-shadow:0px 5px 25px rgba(0,0,0,0.5);
backdrop-filter: blur(12px);
margin-bottom:20px;
}

.job-card{
background:rgba(0,0,0,0.65);
padding:22px;
border-radius:14px;
margin-bottom:22px;
box-shadow:0px 6px 20px rgba(0,0,0,0.5);
transition:0.3s;
border-left:4px solid #22c55e;
}

.job-card:hover{
transform:translateY(-6px);
box-shadow:0px 10px 30px rgba(0,0,0,0.7);
}

[data-testid="metric-container"]{
background:rgba(255,255,255,0.08);
padding:15px;
border-radius:10px;
box-shadow:0px 4px 15px rgba(0,0,0,0.4);
}

</style>
""", unsafe_allow_html=True)

# -------------------------
# HERO HEADER
# -------------------------

st.markdown("""
<div class="hero">

<h1 class="glow">🚀 Intelligent Career Recommendation Platform</h1>

<p class="subtitle">
AI-Powered Resume Analysis • Smart Career Prediction • Live Job Recommendations
</p>

</div>
""", unsafe_allow_html=True)

# -------------------------
# SESSION STATES
# -------------------------

if "users" not in st.session_state:
    st.session_state.users = {}

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user_email" not in st.session_state:
    st.session_state.user_email = None

if "username" not in st.session_state:
    st.session_state.username = None

if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None

if "analysis_score" not in st.session_state:
    st.session_state.analysis_score = None


# -------------------------
# LOGIN / REGISTER
# -------------------------

if not st.session_state.logged_in:

    menu = st.sidebar.radio("Menu", ["Login", "Register"])

    if menu == "Register":

        st.subheader("Create New Account")

        username = st.text_input("Full Name")
        new_email = st.text_input("Email")
        new_password = st.text_input("Password", type="password")

        if st.button("Register"):

            if new_email in st.session_state.users:
                st.error("User already exists!")

            else:

                st.session_state.users[new_email] = {
                    "password": new_password,
                    "username": username
                }

                st.success("Registration Successful! Please Login.")

    elif menu == "Login":

        st.subheader("Login to Continue")

        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if st.button("Login"):

            if (
                email in st.session_state.users
                and st.session_state.users[email]["password"] == password
            ):

                st.session_state.logged_in = True
                st.session_state.user_email = email
                st.session_state.username = st.session_state.users[email]["username"]

                st.success("Login Successful")
                st.rerun()

            else:
                st.error("Invalid Credentials")


# -------------------------
# DASHBOARD
# -------------------------

else:

    st.sidebar.title("👤 User Panel")
    st.sidebar.write(f"Logged in as **{st.session_state.username}**")

    if st.sidebar.button("🚪 Logout"):

        st.session_state.logged_in = False
        st.session_state.user_email = None
        st.session_state.username = None
        st.session_state.analysis_result = None
        st.session_state.analysis_score = None
        st.rerun()

    st.success(f"Hey {st.session_state.username} 👋")
    st.markdown("---")

    st.header("📄 Upload Resume")

    uploaded_file = st.file_uploader("Upload PDF or DOCX", type=["pdf", "docx"])

    if uploaded_file is not None:

        if uploaded_file.type == "application/pdf":
            resume_text = extract_text_from_pdf(uploaded_file)
        else:
            resume_text = extract_text_from_docx(uploaded_file)

        if st.button("🚀 Analyze Resume"):

            with st.spinner("Analyzing Resume..."):
                result, score = analyze_resume(resume_text)

            st.session_state.analysis_result = result
            st.session_state.analysis_score = score

    if st.session_state.analysis_result:

        result = st.session_state.analysis_result
        score = st.session_state.analysis_score

        lines = result.split("\n")
        cleaned_lines = [line for line in lines if "Resume Score" not in line]
        cleaned_result = "\n".join(cleaned_lines)

        st.markdown("## 📊 Resume Analysis Dashboard")

        col1, col2 = st.columns([1,3])

        with col1:
            st.metric("Resume Score", f"{score}/10")

        with col2:
            st.progress(min(score/10,1.0))

        st.markdown(f"""<div class="card">{cleaned_result}</div>""", unsafe_allow_html=True)

        st.download_button(
            label="📥 Download Analysis Report",
            data=f"Resume Score: {score}/10\n\n{cleaned_result}",
            file_name="resume_analysis_report.txt",
            mime="text/plain"
        )

        st.header("💼 AI Job Recommendations")

        skills = extract_skills_from_analysis(cleaned_result)
        keywords = recommend_keywords(skills)

        st.markdown("### 🎯 Recommended Career Paths")

        for k in keywords:
            st.markdown(f"• **{k}**")

        if st.button("🔎 Search Job Recommendations"):

            with st.spinner("Fetching matching jobs..."):

                all_jobs = []

                for role in keywords:

                    jobs = scrape_linkedin_jobs(role)

                    for j in jobs:
                        j["role"] = role
                        all_jobs.append(j)

                # ⭐ STORE JOBS
                store_jobs_csv(all_jobs)
                store_jobs_mysql(all_jobs)

            if len(all_jobs) == 0:

                st.warning("No matching jobs found.")

            else:

                st.subheader("🔥 Top Job Matches")

                shown = 0

                for job in all_jobs:

                    if shown >= 10:
                        break

                    st.markdown(
                        f"""
                        <div class="job-card">

                        <h3 style="color:#4ade80;">{job['title']}</h3>

                        <b>🏢 Company:</b> {job['company']} <br>
                        <b>📍 Location:</b> {job['location']}

                        <h4 style="color:#facc15;margin-top:10px;">📄 Job Description</h4>

                        <p style="font-size:14px;">
                        {job['description']}
                        </p>

                        <a href="{job['url']}" target="_blank"
                        style="background:#22c55e;color:white;padding:8px 15px;text-decoration:none;border-radius:6px;font-weight:bold;">
                        🚀 Apply Now
                        </a>

                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    shown += 1

                st.markdown("### 🎯 Personalized Career Recommendation")

                best_role = keywords[0]

                st.write(f"""
Based on your **resume analysis**, your strongest career path appears to be **{best_role}**.

**Recommendation**

• Build advanced projects related to **{best_role}**  
• Learn **Cloud (AWS / Azure)**  
• Improve **DSA & System Design**  
• Contribute to **GitHub projects**
""")