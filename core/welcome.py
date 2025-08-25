import streamlit as st

def show_welcome():
    st.title("Resume Intelligence Hub 🤖")

    st.markdown("""
        ### One-stop platform for building, analyzing, and matching resumes with job descriptions.
        
        This project integrates **Resume Builder, Resume Matcher, Workflow Visualization, and Analytics Dashboard**
        into a seamless pipeline powered by **AI, NLP, and Embeddings**.
        
        🔹 Build professional ATS-friendly resumes  
        🔹 Parse & analyze resumes and job descriptions  
        🔹 Match resumes to job postings with similarity scoring  
        🔹 Visualize the end-to-end workflow  
        🔹 Track performance with an analytics dashboard  
        """)
    st.subheader("Choose where to start:")
    col1, col2 = st.columns(2)

    with col1:
        if st.button("🚀 Resume Matcher"):
            st.session_state.next_page = "Resume Matcher"
            st.rerun()

        if st.button("📝 Resume Builder"):
            st.session_state.next_page = "Resume Builder"
            st.rerun()

    with col2:
        if st.button("📊 Workflow Visualization"):
            st.session_state.next_page = "Workflow Visualization"
            st.rerun()

        if st.button("📈 Analytics Dashboard"):
            st.session_state.next_page = "Analytics Dashboard"
            st.rerun()
