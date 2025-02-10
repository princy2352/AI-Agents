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
        description=["You are a coding assistant that retrieves top GitHub repositories for software development topics.",  
                    "Your task is to provide the top 10 relevant GitHub repositories related to the given topic, focusing on their quality and popularity."],
        instructions=["""
                      1. Evaluate repositories based on: 
                        - Relevance to the topic  
                        - Star count (popularity),
                      2. Provide the following information for each repository:
                        - Repository Name,  
                        - A brief description about the repository,  
                        - Star count (include a ⭐ emoji after the star count),  
                        - Link to the repository.

                      Formatting:  
                        - Use bullet points for each repository.
                        - If no relevant repositories are found, clearly state:  
                            "No relevant GitHub repositories found." """],
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
            query = f"List the top GitHub repositories for the topic '{topic}' along with brief descriptions and links."
            result = get_coding_research(query)
        st.markdown(result)
    else:
        st.error("Please enter a valid topic.")


