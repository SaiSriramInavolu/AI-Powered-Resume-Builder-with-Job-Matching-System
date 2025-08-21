import streamlit as st
import json
import os
import logging

RESULTS_FILE = "match_results.json"

# Configure logging
log_file = "app.log"
logging.basicConfig(
    level=logging.INFO, # Default level for console output
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler() # Also log to console
    ]
)

logger = logging.getLogger(__name__)

def load_css(file_name: str):
    """Loads a CSS file into the Streamlit app."""
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def save_match_result(result: dict):
    results = []
    if os.path.exists(RESULTS_FILE):
        with open(RESULTS_FILE, "r") as f:
            try:
                results = json.load(f)
            except json.JSONDecodeError:
                logger.warning(f"Could not decode JSON from {RESULTS_FILE}. Starting with empty results.")
                results = []
    results.append(result)
    try:
        with open(RESULTS_FILE, "w") as f:
            json.dump(results, f, indent=4)
    except IOError as e:
        logger.error(f"Could not write to {RESULTS_FILE}: {e}")


def load_match_results():
    if os.path.exists(RESULTS_FILE):
        with open(RESULTS_FILE, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                logger.warning(f"Could not decode JSON from {RESULTS_FILE}. Returning empty results.")
                return []
    return []