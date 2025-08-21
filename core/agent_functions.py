import os
from langgraph.graph import StateGraph, END, START
from core.resume_parser import parse_pdf_resume, parse_text_resume # Added parse_text_resume
from core.jd_parser import parse_text_job_description
from core.matcher import match_resume_to_jd
from core.scorer import score_match
from typing import TypedDict, Any
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from PIL import Image
from io import BytesIO
from app.utils import logger
from core.vector_db import VectorDB

# Initialize VectorDB
vector_db = VectorDB()

class GraphState(TypedDict):
    resume_file: Any # Keep for file uploads
    resume_text: str # New: for text input from DB
    jd_text: str
    resume_data: dict
    jd_data: dict
    similarity_score: float
    final_score: float
    google_api_key: str
    enhancement_suggestions: str


def resume_parser_node(state: GraphState):
    logger.info("---PARSING RESUME---")
    resume_data = {}
    if "resume_file" in state and state["resume_file"] is not None:
        logger.info("Parsing resume from file.")
        resume_file = state["resume_file"]
        resume_data = parse_pdf_resume(resume_file)
    elif "resume_text" in state and state["resume_text"] is not None:
        logger.info("Parsing resume from text.")
        resume_text = state["resume_text"]
        resume_data = parse_text_resume(resume_text)
    else:
        logger.error("No resume_file or resume_text provided to resume_parser_node.")
        # Return empty data or raise an error, depending on desired behavior
        return {"resume_data": {}}

    return {"resume_data": resume_data}


def jd_parser_node(state: GraphState):
    logger.info("---PARSING JOB DESCRIPTION---")
    jd_text = state["jd_text"]
    jd_data = parse_text_job_description(jd_text)
    return {"jd_data": jd_data}


def matcher_node(state: GraphState):
    logger.info("---MATCHING RESUME TO JOB DESCRIPTION---")
    resume_text = state["resume_data"]["text"]
    jd_text = state["jd_data"]["text"]
    
    # Use the vector_db's embedding model for consistency
    similarity_score = match_resume_to_jd(resume_text, jd_text, vector_db.model)
    return {"similarity_score": similarity_score}


def scorer_node(state: GraphState):
    logger.info("---SCORING MATCH---")
    resume_data = state["resume_data"]
    jd_data = state["jd_data"]
    similarity_score = state["similarity_score"]
    final_score = score_match(resume_data, jd_data, similarity_score)
    return {"final_score": final_score, "resume_data": resume_data, "jd_data": jd_data}


def content_enhancement_node(state: GraphState):
    logger.info("---GENERATING CONTENT ENHANCEMENT SUGGESTIONS---")

    api_key = state.get("google_api_key") or os.getenv("GOOGLE_API_KEY")

    if not api_key:
        logger.warning("Google API Key not provided. Skipping content enhancement.")
        return {"enhancement_suggestions": "Google API Key not provided. Skipping content enhancement."}

    llm = ChatGoogleGenerativeAI(google_api_key=api_key, model="gemini-1.5-flash")
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


def create_graph():
    workflow = StateGraph(GraphState)

    workflow.add_node("resume_parser", resume_parser_node)
    workflow.add_node("jd_parser", jd_parser_node)
    workflow.add_node("matcher", matcher_node)
    workflow.add_node("scorer", scorer_node)
    workflow.add_node("content_enhancement", content_enhancement_node)

    workflow.add_edge("resume_parser", "jd_parser")
    workflow.add_edge("jd_parser", "matcher")
    workflow.add_edge("matcher", "scorer")
    workflow.add_edge("scorer", "content_enhancement")
    workflow.add_edge("content_enhancement", END)
    workflow.add_edge(START, "resume_parser") # Explicitly add edge from START

    return workflow

def get_graph_representation(compiled_workflow):
    graph = compiled_workflow.get_graph()
    nodes = []
    edges = []

    for node_name, _ in compiled_workflow.nodes.items():
        nodes.append(node_name)

    for edge in graph.edges:
        edges.append((edge.source, edge.target))
    
    # Handle the START node explicitly
    if START in nodes:
        nodes.remove(START)
        nodes.insert(0, "_start_") # Use a string representation for START and place at beginning

    # Handle the END node explicitly
    if END in nodes:
        nodes.remove(END)
        nodes.append("_end_") # Use a string representation for END

    # Adjust edges for START and END nodes
    for i, (start, end) in enumerate(edges):
        if start == START:
            edges[i] = ("_start_", end)
        if end == END:
            edges[i] = (start, "_end_")

    return {"nodes": nodes, "edges": edges}