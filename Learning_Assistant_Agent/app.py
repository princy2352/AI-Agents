import streamlit as st
from dotenv import load_dotenv
load_dotenv()

# Import our module functions
from overview import get_summary
from research_papers import arxiv_page
from blogs import medium_page
from github_tool import github_page
from youtube_tool import youtube_page

def main():
    st.set_page_config(page_title="Learning Assistant Agent", layout="wide")
    st.title("Research Assistant")
    
    # Main area: Topic input field
    topic_input = st.text_input("Enter a topic to research:", "AI Agents")
    st.session_state["topic"] = topic_input  # Save the topic in session state
    
    # Sidebar: API key for the main model, model selection, and Firecrawler API key
    with st.sidebar:
        st.header("Configuration")
        selected_model = st.selectbox("Select AI Model for summarization:", ["Gemini (Google)", "OpenAI (GPT-4)"])
        api_key_input = st.text_input("Enter API Key for model access (required):", type="password")
        firecrawler_api_key_input = st.text_input("Enter Firecrawler API Key (required):", type="password")
        
        st.session_state["api_key"] = api_key_input
        st.session_state["model_name"] = selected_model
        st.session_state["firecrawler_api_key"] = firecrawler_api_key_input
        
        if not api_key_input.strip():
            st.error("Main API key is required. Please enter your API key.")
        if not firecrawler_api_key_input.strip():
            st.error("Firecrawler API key is required. Please enter your Firecrawler API key.")
    
    # Stop further processing if any required key is missing.
    if not st.session_state.get("api_key", "").strip() or not st.session_state.get("firecrawler_api_key", "").strip():
        st.stop()
    
    # Proceed if a topic is entered
    if topic_input.strip():
        st.header(f"Topic: {topic_input}")
        col1, col2, col3, col4, col5 = st.columns(5)
        
        # Overview: Get a high-level summary using summary.py
        if col1.button("Overview"):
            with st.spinner("Generating overview summary..."):
                summary = get_summary(topic_input)
            st.markdown("### Overview")
            st.markdown(summary)
        
        if col2.button("Get Research Papers"):
            arxiv_page(topic_input)
        if col3.button("Get Relevant Blogs"):
            medium_page(topic_input)
        if col4.button("Get GitHub Repos"):
            github_page(topic_input)
        if col5.button("Get YouTube Videos"):
            youtube_page(topic_input)
        
        
    else:
        st.info("Please enter a topic to begin.")

if __name__ == "__main__":
    main()
