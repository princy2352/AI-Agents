import streamlit as st
from agno.agent import Agent
from agno.tools.arxiv import ArxivTools
from agno.models.google import Gemini
from agno.models.openai import OpenAIChat
from dotenv import load_dotenv
from summariser import get_summary_page  # For URL summarization
load_dotenv()

def get_model_instance(model_name, api_key):
    if not api_key.strip():
        st.error("API key is required.")
        st.stop()
    if model_name == "Gemini (Google)":
        return Gemini(id="gemini-2.0-flash-exp", api_key=api_key)
    elif model_name == "OpenAI (GPT-4)":
        return OpenAIChat(id="gpt-4", api_key=api_key)

@st.cache_resource
def get_arxiv_agent(model_name, api_key):
    model_instance = get_model_instance(model_name, api_key)
    return Agent(
        model=model_instance,
        tools=[ArxivTools()],
        
        description = ['You are an agent that searches arXiv for research papers related to given topic. Your focus is on matching the paper’s title and abstract/content to the topic, not the author names.'],
        instructions=[
            "Fetch research papers where the title or abstract/content directly relates to the user's topic.",
            "Do not consider a paper relevant if the match is solely due to the author names.",
            "For each paper, provide the title, the names of the authors, a short summary of the paper (preferably from the abstract), and a link to the paper.",
            "Ensure that the paper's title and abstract are clearly related to the topic provided.",
            "Write the output in bullet points: the first bullet is the title, the second is the authors, the third is the summary, and the fourth is the link."
        ]
    )

def search_arxiv(query, model_name):
    api_key = st.session_state.get("api_key", "")
    agent = get_arxiv_agent(model_name, api_key)
    response = agent.run(f"Search arXiv for '{query}'")
    return response.content

def arxiv_page(topic):
    st.subheader("Research Papers")
    if topic.strip():
        with st.spinner("Searching ArXiv..."):
            model_name = st.session_state.get("model_name")
            result = search_arxiv(topic, model_name)
        st.markdown(result, unsafe_allow_html=True)
    else:
        st.error("Please enter a valid topic for research papers.")
    
    