# streamlit_app.py
import streamlit as st
from agno.agent import Agent
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.youtube import YouTubeTools
from agno.tools.github import GithubTools
from agno.models.google import Gemini
from dotenv import load_dotenv
from app_constants import SYSTEM_PROMPT, INSTRUCTIONS

# Load environment variables
load_dotenv()

@st.cache_resource
def get_coding_agent():
    # Retrieve secrets from st.secrets
    github_token = st.secrets['GITHUB_ACCESS_TOKEN']
    api_key = st.secrets['GOOGLE_API_KEY']
    return Agent(
        name="Coding Research Agent",
        model=Gemini(id="gemini-2.0-flash-exp", api_key=api_key),
        tools=[GithubTools(access_token=github_token), YouTubeTools(), DuckDuckGoTools()],
        description = SYSTEM_PROMPT,
        instructions = INSTRUCTIONS,
        show_tool_calls=True,
        markdown=True,
    )

def get_coding_research(topic):
    agent = get_coding_agent()
    response = agent.run(topic)
    return response.content

def github_page(topic):
    st.subheader("GitHub Repositories")
    if topic.strip():
        with st.spinner("Fetching GitHub repositories..."):
            # Query modified to be specific about GitHub repos
            query = f"List the top GitHub repositories for the topic '{topic}' along with brief descriptions and links."
            result = get_coding_research(query)
        st.markdown(result)
    else:
        st.error("Please enter a valid topic.")

def youtube_page(topic):
    st.subheader("YouTube Videos")
    if topic.strip():
        with st.spinner("Fetching YouTube videos..."):
            # Query modified for YouTube videos
            query = f"List the top 10 YouTube videos about '{topic}' along with brief descriptions and links."
            result = get_coding_research(query)
        st.markdown(result)
    else:
        st.error("Please enter a valid topic.")