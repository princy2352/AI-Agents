import streamlit as st
from agno.agent import Agent
from agno.tools.arxiv import ArxivTools
from agno.models.google import Gemini
from agno.models.openai import OpenAIChat
from dotenv import load_dotenv
load_dotenv()

def get_model_instance(model_name, api_key):
    if not api_key.strip():
        st.error("🔑 API key is required.")
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
        
        description = ['You are a specialized academic research assistant that discovers and analyzes relevant papers from arXiv. You focus on finding papers that provide significant value to the users research topic.'],
        instructions=[
            "Search for 10 research papers with these criteria:",
    "1. Direct relevance to the topic in title or abstract",
    "2. Preference for papers with high citation counts and recent publication dates",
    "3. Focus on influential work in the field",
    
    "For each paper, format the output as follows:",
    
    "📄 **[PAPER TITLE]**\n",
    "👥 Authors: [Names of authors]\n",
    "📅 Published: [Publication Date]\n",
    "🔍 Citations: [Citation Count if available]\n",
    "💡 Key Findings:\n",
    "   • [3-4 bullet points of main contributions]\n",
    "📚 Summary: [2-3 sentences from abstract highlighting key insights]\n",
    "🔗 Link: [Paper URL]\n",
    
    "---",  # Separator between papers
    
    "Additional Guidelines:",
    "• Present papers in order of relevance and impact",
    "• Include a mix of foundational and recent papers",
    "• Highlight practical applications and methodologies",
    "• Ensure summaries are accessible to the target audience"
]
    )

def search_arxiv(query, model_name):
    api_key = st.session_state.get("api_key", "")
    agent = get_arxiv_agent(model_name, api_key)
    response = agent.run(f"Search arXiv for '{query}'")
    return response.content

def arxiv_page(topic):
    
    st.markdown("""
        <style>
        .overview-card {
            padding: 20px;
            border-radius: 10px;
            background-color: #f8f9fa;
            margin: 10px 0;
            border-left: 4px solid #0066cc;
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.title("📚 Research Papers")
    
    


    if topic.strip():
        with st.spinner("🔍 Searching ArXiv..."):
            model_name = st.session_state.get("model_name")
            result = search_arxiv(topic, model_name)
        st.markdown(result, unsafe_allow_html=True)
    else:
        st.error("Please enter a valid topic for research papers.")
    
    


