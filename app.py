import streamlit as st
from resume_analyzer import extract_text_from_pdf, extract_text_from_docx, analyze_resume

st.set_page_config(page_title="Intelligent Career Recommendation Platform", layout="wide")

st.title("🚀 Intelligent Career Recommendation Platform")

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


# -------------------------
# LOGIN / REGISTER
# -------------------------
if not st.session_state.logged_in:

    menu = st.sidebar.radio("Menu", ["Login", "Register"])

    # -------- REGISTER --------
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

    # -------- LOGIN --------
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
# DASHBOARD AFTER LOGIN
# -------------------------
else:

    # -------- SIDEBAR --------
    st.sidebar.title("👤 User Panel")
    st.sidebar.write(f"Logged in as **{st.session_state.username}**")

    if st.sidebar.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.session_state.user_email = None
        st.session_state.username = None
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

            # Remove score line safely
            lines = result.split("\n")
            cleaned_lines = [line for line in lines if "Resume Score" not in line]
            cleaned_result = "\n".join(cleaned_lines)

            st.markdown("---")
            st.markdown("## 📊 Resume Analysis Dashboard")

            # -------- Score Section --------
            col1, col2 = st.columns([1, 3])

            with col1:
                st.metric("Resume Score", f"{score}/10")

            with col2:
                st.progress(min(score / 10, 1.0))

            st.markdown("---")

            # -------- Analysis Display --------
            st.markdown(
                f"""
                <div style="
                    background-color:#1e1e1e;
                    padding:25px;
                    border-radius:12px;
                    box-shadow:0px 4px 15px rgba(0,0,0,0.3);
                    color:white;
                ">
                {cleaned_result}
                </div>
                """,
                unsafe_allow_html=True
            )

            st.markdown("---")

            # -------- Download Button --------
            st.download_button(
                label="📥 Download Analysis Report",
                data=f"Resume Score: {score}/10\n\n{cleaned_result}",
                file_name="resume_analysis_report.txt",
                mime="text/plain"
            )