import streamlit as st
from agno.agent import Agent
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.models.google import Gemini
from agno.models.openai import OpenAIChat
from dotenv import load_dotenv
from agno.tools.crawl4ai import Crawl4aiTools

load_dotenv()

def get_model_instance(model_name, api_key):
    
    if not api_key.strip():
        st.error("API key is required.")
        st.stop()
    if model_name == "Gemini (Google)":
        return Gemini(id="gemini-2.0-flash-exp", api_key=api_key)
    elif model_name == "OpenAI (GPT-4)":
        return OpenAIChat(id="gpt-4", api_key=api_key)
    else:
        st.error("Invalid model selected.")
        st.stop()

def get_blog_agent(model_name, api_key):
    model_instance = get_model_instance(model_name, api_key)
    return Agent(
        model=model_instance,
        tools=[DuckDuckGoTools(), Crawl4aiTools()],
        
        description = ['You are an agent that searches for blogs posts and articles related to given topic.'],
        instructions=[
            "Fetch the most recent articles and blogs posts related to topic given by the user.",
            "List the links for the top 10 relevant articles along with a summary of each.",
            "Ensure the list is sorted by relevance.",
            "Include source links for each article."
        ]
    )

def get_medium_blogs(topic,model_name):
    api_key = st.session_state.get("api_key", "")
    # Retrieve the Firecrawler API key from session state for the crawling tool.
    firecrawler_api_key = st.session_state.get("firecrawler_api_key", "")
    if not firecrawler_api_key.strip():
        st.error("Firecrawler API key is required.")
        st.stop()

    else:
        agent = get_blog_agent(model_name, api_key)
    response = agent.run(topic)
    return response.content

def medium_page(topic):
    st.subheader("Blogs")
    if topic.strip():
        with st.spinner("Fetching blogs..."):
            model_name = st.session_state.get("model_name")
            result = get_medium_blogs(topic,model_name)
        st.markdown(result)
        
    else:
        st.error("Please enter a valid topic for blogs.")
    
    