import streamlit as st
from agno.agent import Agent
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.youtube import YouTubeTools
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
def get_youtube_agent():
    api_key = st.session_state.get("api_key", "")
    model_name = st.session_state.get("model_name")
    model_instance = get_model_instance(model_name, api_key)
    
    return Agent(
        name="Youtube Agent",
        model=model_instance,
        tools=[DuckDuckGoTools(),YouTubeTools() ],
        description=["You are a coding assistant that retrieves top YouTube videos given topics.",  
                    "Your task is to find the top 10 related YouTube videos about the given topic, prioritizing informative, highly-rated, and recent content.",  
                    ],
                     instructions=["""
                      - Find the top 10 related YouTube videos about the given topic.
    - Prioritize videos that are:
        - Informative,
        - Highly rated,
        - Recent.
Always include sources.                                    """],
        show_tool_calls=True,
        markdown=True,
    )

def get_youtube_research(topic):
    agent = get_youtube_agent()
    response = agent.run(topic)
    return response.content


def youtube_page(topic):
    st.subheader("YouTube Videos")
    if topic.strip():
        with st.spinner("Fetching YouTube videos..."):
            query = f"List the top 10 YouTube videos about '{topic}' along with brief descriptions and links."
            result = get_youtube_research(query)
        st.markdown(result)
    else:
        st.error("Please enter a valid topic.")
