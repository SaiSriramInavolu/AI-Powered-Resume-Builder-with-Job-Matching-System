import os
from langgraph.graph import StateGraph, END
from core.resume_parser import parse_pdf_resume
from core.jd_parser import parse_text_job_description
from core.matcher import match_resume_to_jd
from core.scorer import score_match
from typing import TypedDict, Any
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from PIL import Image
from io import BytesIO
from core.resume_generator import ResumeGenerator

class GraphState(TypedDict):
    resume_file: Any
    jd_text: str
    resume_data: dict
    jd_data: dict
    similarity_score: float
    final_score: float
    google_api_key: str
    enhancement_suggestions: str
    user_prompt: str # Added for resume generation
    generated_resume_latex: str # Added for resume generation


def resume_parser_node(state: GraphState):
    print("---PARSING RESUME---")
    resume_file = state["resume_file"]
    resume_data = parse_pdf_resume(resume_file)
    return {"resume_data": resume_data}


def jd_parser_node(state: GraphState):
    print("---PARSING JOB DESCRIPTION---")
    jd_text = state["jd_text"]
    jd_data = parse_text_job_description(jd_text)
    return {"jd_data": jd_data}


def matcher_node(state: GraphState):
    print("---MATCHING RESUME TO JOB DESCRIPTION---")
    resume_text = state["resume_data"]["text"]
    jd_text = state["jd_data"]["text"]
    similarity_score = match_resume_to_jd(resume_text, jd_text)
    return {"similarity_score": similarity_score}


def scorer_node(state: GraphState):
    print("---SCORING MATCH---")
    resume_data = state["resume_data"]
    jd_data = state["jd_data"]
    similarity_score = state["similarity_score"]
    final_score = score_match(resume_data, jd_data, similarity_score)
    return {"final_score": final_score, "resume_data": resume_data, "jd_data": jd_data}


def content_enhancement_node(state: GraphState):
    print("---GENERATING CONTENT ENHANCEMENT SUGGESTIONS---")

    api_key = state.get("google_api_key") or os.getenv("GOOGLE_API_KEY")

    if not api_key:
        return {"enhancement_suggestions": "Google API Key not provided. Skipping content enhancement."}

    llm = ChatGoogleGenerativeAI(google_api_key=api_key, model="gemini-2.5-flash")
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful AI assistant that provides suggestions to improve a resume based on a job description."),
        ("user", "Resume:\n{resume_text}\n\nJob Description:\n{jd_text}\n\nProvide specific suggestions to enhance the resume to better match the job description. Focus on skill gaps, keyword optimization, and relevant experience. Format your suggestions as a markdown list.")
    ])
    chain = prompt | llm

    response = chain.invoke({
        "resume_text": state["resume_data"]["text"],
        "jd_text": state["jd_data"]["text"]
    })
    return {"enhancement_suggestions": response.content}

def resume_generation_node(state: GraphState):
    print("---GENERATING RESUME WITH GEMINI AI---")
    user_prompt = state.get("user_prompt")

    if not user_prompt:
        return {"generated_resume_latex": "No user prompt provided for resume generation."}

    resume_generator = ResumeGenerator()
    resume_data = resume_generator.generate_resume_content_with_gemini(user_prompt)
    generated_resume_latex = resume_generator.generate_resume(resume_data, output_format="latex")

    return {"generated_resume_latex": generated_resume_latex}

def create_graph():
    workflow = StateGraph(GraphState)

    workflow.add_node("resume_parser", resume_parser_node)
    workflow.add_node("jd_parser", jd_parser_node)
    workflow.add_node("matcher", matcher_node)
    workflow.add_node("scorer", scorer_node)
    workflow.add_node("content_enhancement", content_enhancement_node)
    workflow.add_node("resume_generation", resume_generation_node) # New node for resume generation

    workflow.add_edge("resume_parser", "jd_parser")
    workflow.add_edge("jd_parser", "matcher")
    workflow.add_edge("matcher", "scorer")
    workflow.add_edge("scorer", "content_enhancement")
    workflow.add_edge("content_enhancement", END)

    
    workflow.add_edge("resume_generation", END)

    workflow.set_entry_point("resume_parser")

    return workflow


def get_graph_image(workflow):
    graph = workflow.get_graph()
    # Set graphviz attributes for better visualization
    graph.graph_attr['rankdir'] = 'LR'  # Left to right layout
    graph.graph_attr['nodesep'] = '0.8' # Increase separation between nodes in the same rank
    graph.graph_attr['ranksep'] = '1.5' # Increase separation between ranks
    graph.graph_attr['size'] = '10,8'   # Set a reasonable size for the output image
    graph.graph_attr['dpi'] = '150'     # Increase DPI for better resolution

    # Output as SVG for scalability
    svg_content = graph.draw(format='svg').decode('utf-8')
    return svg_content