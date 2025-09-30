import streamlit as st
from agno.agent import Agent
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.youtube import YouTubeTools
from agno.tools.github import GithubTools
from agno.models.openai import OpenAIChat
from agno.models.google import Gemini
from dotenv import load_dotenv
load_dotenv()

def get_model_instance(model_name, api_key):
    if not api_key.strip():
        st.error("Main API key is required for model access.")
        st.stop()
    if model_name == "Gemini (Google)":
        return Gemini(id="gemini-2.0-flash-exp", api_key=api_key)
    elif model_name == "OpenAI (GPT-4)":
        return OpenAIChat(id="gpt-4", api_key=api_key)
    else:
        st.error("Invalid model selected.")
        st.stop()

@st.cache_resource
def get_coding_agent():
    github_token = st.secrets['GITHUB_ACCESS_TOKEN']
    api_key = st.session_state.get("api_key", "")
    model_name = st.session_state.get("model_name")
    model_instance = get_model_instance(model_name, api_key)
    
    return Agent(
        name="Coding Research Agent",
        model=model_instance,
        tools=[GithubTools(access_token=github_token), YouTubeTools(), DuckDuckGoTools()],
        description = [
    "You are a specialized code repository curator who identifies the most valuable and well-maintained GitHub projects, focusing on code quality, community engagement, and practical implementation.",
    "Your goal is to find repositories that offer both learning value and production-ready solutions."
],
instructions = [
    "Search for GitHub repositories using these evaluation criteria:",
    "1. Primary Metrics:",
    "   • Direct relevance to the topic",
    "   • Active maintenance (recent commits)",
    "   • Community engagement level",
    "   • Documentation quality",
    
    "For each repository, format the output as follows:",
    
    "💻 **[REPOSITORY NAME]** \n",
    "📋 Description: [Clear, concise description] \n",
    "📊 Stats: \n",
    "   • ⭐ Stars: [count] \n",
    "   • 🔄 Forks: [count] \n",
    
    "📚 Key Features: \n",
    "   • [3-4 main features or capabilities] \n",
    "🔧 Tech Stack: [Main technologies used] \n",
    "📖 Documentation: [Documentation quality: Excellent/Good/Basic] \n",
    "🔗 Link: [Repository URL] \n",
    
    "---",  # Separator between repositories
    
    "Additional Considerations:",
    "• Ensure repositories are actively maintained",
    "• Check for comprehensive README files",
    "• Verify presence of example code or demos",
    "• Consider issue response times and community support",
    
    "Present the top 10 repositories sorted by overall value (combination of stars, activity, and relevance).",
    
    "If no relevant repositories are found, state:",
    "❌ No relevant GitHub repositories found for this topic."
    "Make sure the font isn't too large."
],
        
        markdown=True,
    )

def get_coding_research(topic):
    agent = get_coding_agent()
    response = agent.run(topic)
    return response.content

def github_page(topic):
    st.markdown("""
        <style>
        .repo-card {
            padding: 20px;
            border-radius: 10px;
            background-color: #f8f9fa;
            margin: 15px 0;
            border: 1px solid #ddd;
        }
        .repo-stats {
            display: flex;
            gap: 20px;
            margin-top: 10px;
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.title("💻 GitHub Repositories")
    if topic.strip():
        with st.spinner("Fetching GitHub repositories..."):
            query = f"List the top GitHub repositories for the topic '{topic}' along with brief descriptions and links."
            result = get_coding_research(query)
        st.markdown(result)
    else:
        st.error("Please enter a valid topic.")


