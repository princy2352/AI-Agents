# arxiv1.py
import streamlit as st
from agno.agent import Agent
from agno.tools.arxiv import ArxivTools
from agno.models.google import Gemini
from agno.models.openai import OpenAIChat
from dotenv import load_dotenv
from firecrawler import summarize_url  # Import the URL summarization function

# Load environment variables
load_dotenv()

# Define available models for ArXiv search (you can expand as needed)
MODELS = {
    "Gemini (Google)": Gemini(id="gemini-2.0-flash-exp"),
    "OpenAI (GPT-4)": OpenAIChat(id="gpt-4"),
}

@st.cache_resource
def get_arxiv_agent(model):
    return Agent(
        model=model,
        tools=[ArxivTools()],
        show_tool_calls=True,
        instructions=[
            "Give the title of the paper, authors, a short summary of the paper, and the link to the paper.",
            "Always include sources.",
            "Write in points. First point should be the title of the paper. Second should be the name of the authors. Third should be a short summary of the paper. Fourth should be the link to the paper."
        ]
    )

def search_arxiv(query, model_name="Gemini (Google)"):
    selected_model = MODELS[model_name]
    agent = get_arxiv_agent(selected_model)
    response = agent.run(f"Search arXiv for '{query}'")
    return response.content

def arxiv_page(topic):
    st.subheader("Research Papers")
    if topic.strip():
        with st.spinner("Searching ArXiv..."):
            result = search_arxiv(topic)
        st.markdown(result, unsafe_allow_html=True)
    else:
        st.error("Please enter a valid topic for research papers.")
    
    st.markdown("---")

    st.subheader("Or, get a summary of a research paper URL")
    url = st.text_input("Enter the URL of the research paper:", key="arxiv_url")
    if st.button("Summarize Paper URL", key="arxiv_url_btn"):
        if url.strip():
            with st.spinner("Summarizing paper..."):
                summary = summarize_url(url)
            st.markdown("### Paper Summary:")
            st.markdown(summary)
        else:
            st.error("Please enter a valid URL.")