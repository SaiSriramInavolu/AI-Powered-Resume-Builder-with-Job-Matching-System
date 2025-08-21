import streamlit as st
import os
from dotenv import load_dotenv
import pandas as pd
import plotly.express as px
import graphviz # Import graphviz

# Import functions from the new library file
from core.agent_functions import create_graph, get_graph_representation

# Import functions from core and app/utils
from core.resume_generator import create_pdf_resume
from app.utils import save_match_result, load_match_results, logger

load_dotenv() # Load environment variables at the application start

st.set_page_config(layout="wide")
st.title("✨ AI-Powered Resume Matcher & Builder ✨")
st.subheader("Find the perfect candidate, or the perfect job!")

# Sidebar for navigation
st.sidebar.title("Navigation")
page_selection = st.sidebar.radio(
    "Go to",
    ["Resume Matcher", "Resume Builder", "Workflow Visualization", "Analytics Dashboard"]
)

# Initialize google_api_key in session state if it's not already there
if 'google_api_key' not in st.session_state:
    st.session_state.google_api_key = os.getenv("GOOGLE_API_KEY", "")

# --- Resume Matcher Page ---
if page_selection == "Resume Matcher":
    st.header("AI-Powered Resume Matcher")

    google_api_key = st.session_state.google_api_key

    col1, col2 = st.columns(2)

    with col1:
        st.header("Upload Resume")
        uploaded_resumes = st.file_uploader("Upload Resume", type=["pdf"], accept_multiple_files=True)

    with col2:
        st.header("Paste Job Description")
        job_description = st.text_area("Description", height=300)

    # Initialize session state for results
    if 'all_match_results_session' not in st.session_state:
        st.session_state.all_match_results_session = None
    if 'df_results_session' not in st.session_state:
        st.session_state.df_results_session = None

    if st.button("Match Resumes", use_container_width=True):
        if job_description and uploaded_resumes:
            all_match_results = []
            st.subheader("Processing Resumes...")
            progress_bar = st.progress(0)
            status_text = st.empty()

            for i, uploaded_resume in enumerate(uploaded_resumes):
                status_text.text(f"Matching {uploaded_resume.name} ({i+1}/{len(uploaded_resumes)})...")
                progress_bar.progress((i + 1) / len(uploaded_resumes))

                with st.spinner(f"Matching {uploaded_resume.name}... ✨"):
                    workflow = create_graph()
                    compiled_workflow = workflow.compile()

                    graph_input = {"resume_file": uploaded_resume, "jd_text": job_description}
                    if google_api_key:
                        graph_input["google_api_key"] = google_api_key

                    output = compiled_workflow.invoke(graph_input)
                    final_score = float(output.get("final_score", 0.0))

                all_match_results.append({
                    "Resume Name": uploaded_resume.name,
                    "Match Score": final_score,
                    "Resume Skills": ", ".join(output.get("resume_data", {}).get("skills", [])),
                    "JD Skills": ", ".join(output.get("jd_data", {}).get("skills", [])),
                    "Common Skills": ", ".join(sorted(set(output.get("resume_data", {}).get("skills", [])).intersection(set(output.get("jd_data", {}).get("skills", []))))),
                    "Resume Keywords": ", ".join(output.get("resume_data", {}).get("keywords", [])),
                    "JD Keywords": ", ".join(output.get("jd_data", {}).get("keywords", [])),
                    "Common Keywords": ", ".join(sorted(set(output.get("resume_data", {}).get("keywords", [])).intersection(set(output.get("jd_data", {}).get("keywords", []))))),
                    "Enhancement Suggestions": output.get("enhancement_suggestions", "N/A"),
                    "Timestamp": pd.Timestamp.now().isoformat()
                })
                save_match_result(
                    {
                        "timestamp": pd.Timestamp.now().isoformat(),
                        "final_score": final_score,
                        "resume_skills": output.get("resume_data", {}).get("skills", []),
                        "jd_skills": output.get("jd_data", {}).get("skills", []),
                        "enhancement_suggestions": output.get(
                            "enhancement_suggestions", "N/A"
                        ),
                    }
                )
            status_text.text("Pairwise matching complete!")

            if all_match_results:
                df_results = pd.DataFrame(all_match_results)
                df_results = df_results.sort_values(by="Match Score", ascending=False).reset_index(drop=True)
                
                st.session_state.all_match_results_session = all_match_results
                st.session_state.df_results_session = df_results
            else:
                st.session_state.all_match_results_session = None
                st.session_state.df_results_session = None
        else:
            st.error("Please upload at least one resume and a job description.")

    # Display results if available in session state
    if st.session_state.df_results_session is not None:
        df_results = st.session_state.df_results_session # Use the cached DataFrame

        st.subheader("Comparison Results")

        num_best_resumes = st.number_input(
            "Show top N matching resumes:",
            min_value=1,
            max_value=len(df_results),
            value=min(5, len(df_results)), # Default to 5 or max available
            step=1,
            key="num_best_resumes_input" # Add a key to prevent warning
        )
        
        st.dataframe(df_results.head(num_best_resumes).drop(columns=["Enhancement Suggestions", "Timestamp"]))

        st.subheader("Detailed Analysis and Suggestions")
        for idx, row in df_results.head(num_best_resumes).iterrows():
            st.markdown(f"### {row['Resume Name']} (Score: {row['Match Score']:.2%})")
            with st.expander("See Detailed Analysis"):
                st.write("**Resume Skills:**", row["Resume Skills"])
                st.write("**Job Description Skills:**", row["JD Skills"])
                st.write("**Common Skills:**", row["Common Skills"])
                st.write("---")
                st.write("**Resume Keywords:**", row["Resume Keywords"])
                st.write("**JD Keywords:**", row["JD Keywords"])
                st.write("**Common Keywords:**", row["Common Keywords"])
            
            if google_api_key and row["Enhancement Suggestions"] != "N/A":
                st.subheader("Content Enhancement Suggestions")
                st.markdown(row["Enhancement Suggestions"])
            st.markdown("---")
    elif st.session_state.all_match_results_session is None and st.session_state.df_results_session is None:
        logger.info("No match results in session. Prompting user to upload and match.")
        st.info("Upload resumes and job description, then click 'Match Resumes' to see results.")

# --- Resume Builder Page ---
elif page_selection == "Resume Builder":
    st.header("AI-Powered Resume Builder")

    # Initialize session state for lists of entries
    if 'experience_entries' not in st.session_state:
        st.session_state.experience_entries = []
    if 'education_entries' not in st.session_state:
        st.session_state.education_entries = []
    if 'project_entries' not in st.session_state:
        st.session_state.project_entries = []
    if 'certification_entries' not in st.session_state:
        st.session_state.certification_entries = []
    if 'language_entries' not in st.session_state:
        st.session_state.language_entries = []
    if 'award_entries' not in st.session_state:
        st.session_state.award_entries = []

    with st.form("resume_form"):
        name = st.text_input("Full Name")
        email = st.text_input("Email")
        phone = st.text_input("Phone")
        github = st.text_input("GitHub URL")
        linkedin = st.text_input("LinkedIn URL")
        summary = st.text_area("Summary")

        # --- Education Section ---
        with st.expander("Education", expanded=True):
            for i, entry in enumerate(st.session_state.education_entries):
                with st.container():
                    st.write(f"Education #{i + 1}")
                    entry['degree'] = st.text_input(f"Degree", key=f"edu_degree_{i}")
                    entry['university'] = st.text_input(f"University", key=f"edu_university_{i}")
                    entry['graduation_year'] = st.text_input(f"Graduation Year", key=f"edu_grad_year_{i}")
                    entry['description'] = st.text_area(f"Description (e.g., coursework, honors)", key=f"edu_desc_{i}")
                    if st.form_submit_button(f"Remove Education #{i + 1}"):
                        st.session_state.education_entries.pop(i)
                        st.rerun()
            add_edu_button_label = "Add Education" if len(st.session_state.education_entries) == 0 else "Add another Education"
            if st.form_submit_button(add_edu_button_label):
                st.session_state.education_entries.append({})
                st.rerun()

        # --- Experience Section ---
        with st.expander("Experience", expanded=True):
            for i, entry in enumerate(st.session_state.experience_entries):
                with st.container():
                    st.write(f"Experience #{i + 1}")
                    entry['title'] = st.text_input(f"Job Title", key=f"exp_title_{i}")
                    entry['company'] = st.text_input(f"Company", key=f"exp_company_{i}")
                    entry['years'] = st.text_input(f"Years (e.g., 2020-Present)", key=f"exp_years_{i}")
                    entry['description'] = st.text_area(f"Description", key=f"exp_desc_{i}")
                    if st.form_submit_button(f"Remove Experience #{i + 1}"):
                        st.session_state.experience_entries.pop(i)
                        st.rerun()
            add_exp_button_label = "Add Experience" if len(st.session_state.experience_entries) == 0 else "Add another Experience"
            if st.form_submit_button(add_exp_button_label):
                st.session_state.experience_entries.append({})
                st.rerun()

        # --- Projects Section ---
        with st.expander("Projects", expanded=True):
            for i, entry in enumerate(st.session_state.project_entries):
                with st.container():
                    st.write(f"Project #{i + 1}")
                    entry['name'] = st.text_input(f"Project Name", key=f"proj_name_{i}")
                    entry['description'] = st.text_area(f"Description", key=f"proj_desc_{i}")
                    entry['technologies'] = st.text_input(f"Technologies Used (comma-separated)", key=f"proj_tech_{i}")
                    entry['link'] = st.text_input(f"Project Link (optional)", key=f"proj_link_{i}")
                    if st.form_submit_button(f"Remove Project #{i + 1}"):
                        st.session_state.project_entries.pop(i)
                        st.rerun()
            add_proj_button_label = "Add Project" if len(st.session_state.project_entries) == 0 else "Add another Project"
            if st.form_submit_button(add_proj_button_label):
                st.session_state.project_entries.append({})
                st.rerun()

        # --- Certifications Section ---
        with st.expander("Certifications", expanded=True):
            for i, entry in enumerate(st.session_state.certification_entries):
                with st.container():
                    st.write(f"Certification #{i + 1}")
                    entry['name'] = st.text_input(f"Certification Name", key=f"cert_name_{i}")
                    entry['organization'] = st.text_input(f"Issuing Organization", key=f"cert_org_{i}")
                    entry['date_issued'] = st.text_input(f"Date Issued (e.g., Month Year)", key=f"cert_date_{i}")
                    if st.form_submit_button(f"Remove Certification #{i + 1}"):
                        st.session_state.certification_entries.pop(i)
                        st.rerun()
            add_cert_button_label = "Add Certification" if len(st.session_state.certification_entries) == 0 else "Add another Certification"
            if st.form_submit_button(add_cert_button_label):
                st.session_state.certification_entries.append({})
                st.rerun()

        # --- Languages Section ---
        with st.expander("Languages", expanded=True):
            for i, entry in enumerate(st.session_state.language_entries):
                with st.container():
                    st.write(f"Language #{i + 1}")
                    entry['language'] = st.text_input(f"Language Name", key=f"lang_name_{i}")
                    entry['proficiency'] = st.text_input(f"Proficiency (e.g., Native, Fluent, Conversational)", key=f"lang_prof_{i}")
                    if st.form_submit_button(f"Remove Language #{i + 1}"):
                        st.session_state.language_entries.pop(i)
                        st.rerun()
            add_lang_button_label = "Add Language" if len(st.session_state.language_entries) == 0 else "Add another Language"
            if st.form_submit_button(add_lang_button_label):
                st.session_state.language_entries.append({})
                st.rerun()

        # --- Awards/Honors Section ---
        with st.expander("Awards/Honors", expanded=True):
            for i, entry in enumerate(st.session_state.award_entries):
                with st.container():
                    st.write(f"Award/Honor #{i + 1}")
                    entry['name'] = st.text_input(f"Award Name", key=f"award_name_{i}")
                    entry['organization'] = st.text_input(f"Issuing Organization", key=f"award_org_{i}")
                    entry['date'] = st.text_input(f"Date (e.g., Month Year)", key=f"award_date_{i}")
                    if st.form_submit_button(f"Remove Award/Honor #{i + 1}"):
                        st.session_state.award_entries.pop(i)
                        st.rerun()
            add_award_button_label = "Add Award/Honor" if len(st.session_state.award_entries) == 0 else "Add another Award/Honor"
            if st.form_submit_button(add_award_button_label):
                st.session_state.award_entries.append({})
                st.rerun()

        skills = st.text_area("Skills (comma-separated)")

        submitted = st.form_submit_button("Generate Resume")

    if submitted:
        resume_data = {
            "name": name,
            "email": email,
            "phone": phone,
            "github": github,
            "linkedin": linkedin,
            "summary": summary,
            "experience": st.session_state.experience_entries,
            "education": st.session_state.education_entries,
            "projects": st.session_state.project_entries,
            "certifications": st.session_state.certification_entries,
            "languages": st.session_state.language_entries,
            "awards": st.session_state.award_entries,
            "skills": skills,
        }
        pdf_buffer = create_pdf_resume(resume_data)
        st.download_button(
            label="Download Resume as PDF",
            data=pdf_buffer,
            file_name=f"{(name or 'Resume').replace(' ', '_')}_Resume.pdf",
            mime="application/pdf",
        )

        

# --- Workflow Visualization Page ---
elif page_selection == "Workflow Visualization":
    st.header("LangGraph Workflow Visualization")
    workflow = create_graph()
    compiled_workflow = workflow.compile()
    graph_representation = get_graph_representation(compiled_workflow)

    # Define node descriptions and colors for a unique and cool look
    node_descriptions = {
        "_start_": "The entry point of the workflow.",
        "resume_parser": "Extracts structured data from PDF resumes.",
        "jd_parser": "Extracts key information from text-based job descriptions.",
        "matcher": "Compares resumes against job descriptions to find similarities.",
        "scorer": "Provides a score indicating the compatibility between a resume and a job description.",
        "content_enhancement": "Offers AI-driven suggestions to improve a resume's alignment with a job description.",
        "_end_": "The end point of the workflow."
    }

    # Enhanced color palette and styling
    node_styles = {
        "_start_": {"shape": "circle", "fillcolor": "#8BC34A", "style": "filled", "fontcolor": "#FFFFFF", "width": "0.8", "height": "0.8"}, # Green
        "resume_parser": {"shape": "box", "fillcolor": "#FFEB3B", "style": "filled", "fontcolor": "#333333"}, # Yellow
        "jd_parser": {"shape": "box", "fillcolor": "#03A9F4", "style": "filled", "fontcolor": "#FFFFFF"}, # Blue
        "matcher": {"shape": "box", "fillcolor": "#FF9800", "style": "filled", "fontcolor": "#FFFFFF"}, # Orange
        "scorer": {"shape": "box", "fillcolor": "#9C27B0", "style": "filled", "fontcolor": "#FFFFFF"}, # Purple
        "content_enhancement": {"shape": "box", "fillcolor": "#00BCD4", "style": "filled", "fontcolor": "#FFFFFF"}, # Cyan
        "_end_": {"shape": "circle", "fillcolor": "#F44336", "style": "filled", "fontcolor": "#FFFFFF", "width": "0.8", "height": "0.8"} # Red
    }

    dot = graphviz.Digraph(comment='LangGraph Workflow', graph_attr={'rankdir': 'LR', 'bgcolor': '#F8F8F8', 'fontname': 'Helvetica'})

    # Add nodes
    for node_name in graph_representation["nodes"]:
        label = node_name.replace('_', ' ').title()
        description = node_descriptions.get(node_name, "No description available.")
        style = node_styles.get(node_name, node_styles["resume_parser"]) # Default to resume_parser style
        dot.node(node_name, label, tooltip=description, **style)
    
    # Add edges
    for start_node, end_node in graph_representation["edges"]:
        dot.edge(str(start_node), str(end_node))

    st.graphviz_chart(dot)

# --- Analytics Dashboard Page ---
elif page_selection == "Analytics Dashboard":
    st.header("Match Analytics Dashboard")
    results = load_match_results()
    if results:
        df = pd.DataFrame(results)
        df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
        df = df.sort_values(by="timestamp", ascending=False)

        st.subheader("Match Score Distribution")
        fig = px.histogram(df, x="final_score", nbins=10, title="Distribution of Match Scores")
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("Match Scores Over Time")
        fig = px.line(df, x="timestamp", y="final_score", title="Match Scores Over Time")
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("Recent Match Results")
        st.dataframe(df.head())
    else:
        st.info("No match results yet. Run some matches to see analytics!")