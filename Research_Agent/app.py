# app.py
import streamlit as st
from dotenv import load_dotenv
load_dotenv()

# Import page functions from your modules
from arxiv1 import arxiv_page
from medium import medium_page
from streamlit_app import github_page, youtube_page
from firecrawler import firecrawl_page
from agno.agent import Agent
from agno.models.google import Gemini
from agno.models.openai import OpenAIChat

# Define available models for summarization
MODELS = {
    "Gemini (Google)": Gemini(id="gemini-2.0-flash-exp"),
    "OpenAI (GPT-4)": OpenAIChat(id="gpt-4"),
}

def get_summary_agent(model):
    """Return an agent that summarizes the topic using the selected model."""
    return Agent(
        model=model,
        show_tool_calls=True,
        markdown=True,
        instructions=[
            "Summarize the topic in a few concise bullet points. Provide an overview of what it is and what it is used for."
        ]
    )

def get_summary(topic, model):
    agent = get_summary_agent(model)
    response = agent.run(topic)
    return response.content

def main():
    st.set_page_config(page_title="AI Research & Content Assistant", layout="wide")
    st.title("AI Research & Content Assistant")
    
    # Use session state to store the topic and summary so they don’t refresh on button clicks.
    if "topic" not in st.session_state:
        st.session_state.topic = ""
    if "summary" not in st.session_state:
        st.session_state.summary = ""
    if "model_name" not in st.session_state:
        st.session_state.model_name = list(MODELS.keys())[0]

    # Sidebar: Topic input and model selection (only once)
    with st.sidebar:
        st.header("Generate Topic Summary")
        topic_input = st.text_input("Enter a topic:", st.session_state.topic or "AI Agents")
        selected_model_name = st.selectbox("Select AI Model for summarization:", list(MODELS.keys()), index=list(MODELS.keys()).index(st.session_state.model_name))
        generate_summary = st.button("Generate Summary")
        
        # Save selections in session state
        st.session_state.topic = topic_input
        st.session_state.model_name = selected_model_name

        if generate_summary and topic_input.strip():
            with st.spinner("Generating summary..."):
                summary = get_summary(topic_input, MODELS[selected_model_name])
            st.session_state.summary = summary
            st.success("Summary generated!")

    # Main content area
    st.header("Topic Summary")
    if st.session_state.summary:
        st.markdown(st.session_state.summary)
    else:
        st.info("Please use the sidebar to generate a topic summary.")

    st.markdown("## Choose an Option:")
    col1, col2, col3, col4, col5 = st.columns(5)

    if col1.button("Research Papers"):
        # Call arxiv_page without regenerating summary
        arxiv_page(st.session_state.topic)
    if col2.button("Medium Blogs"):
        medium_page(st.session_state.topic)
    if col3.button("GitHub Repos"):
        github_page(st.session_state.topic)
    if col4.button("YouTube Videos"):
        youtube_page(st.session_state.topic)
    if col5.button("Direct URL Summary"):
        firecrawl_page()

if __name__ == "__main__":
    main()