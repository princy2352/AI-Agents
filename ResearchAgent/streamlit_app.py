import sys
import os
from dotenv import load_dotenv
env_path = "/Users/princypatel/Desktop/ML Projects/AI-Agents/ResearchAgent/.env"  # Replace with your actual path
load_dotenv(dotenv_path=env_path)# Access the token
# Add the project root to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from phi.agent import Agent
from phi.model.openai import OpenAIChat
from phi.model.google import Gemini 
from phi.tools.duckduckgo import DuckDuckGo
from phi.tools.youtube_tools import YouTubeTools
from phi.tools.github import GithubTools
from phi.model.groq import Groq
from ResearchAgent.app_constants import SYSTEM_PROMPT, INSTRUCTIONS

from phi.playground import Playground, serve_playground_app
import streamlit as st
github_token = st.secrets["GITHUB_ACCESS_TOKEN"]
#github_token = os.getenv("GITHUB_ACCESS_TOKEN")
api_key= st.secrets['GOOGLE_API_KEY']
@st.cache_resource
def get_agent():
    return Agent(
        name="Coding Research Agent",
        model=Gemini(id="gemini-2.0-flash-exp",api_key=api_key),
        #model=OpenAIChat(id="gpt-4o"),
        tools=[GithubTools(access_token=github_token), YouTubeTools(),DuckDuckGo()],
        description= SYSTEM_PROMPT,
        instructions=INSTRUCTIONS,
        
        show_tool_calls=True,
        markdown=True,
        add_datetime_to_instructions=True,
    )

# Function to analyze a coding topic
def analyze_topic(agent, topic):
    agent= get_agent()
    with st.spinner(f"Searching for results on '{topic}'..."):
        try:
            response = agent.run(topic)
            return response.content.strip()
        except Exception as e:
            return f"An error occurred: {e}"

# Streamlit app
def main():
    st.title("🤖 Coding Research Assistant")
    st.markdown("Enter a coding topic to get GitHub repositories and YouTube videos related to it.")

    agent = get_agent()

# Create a form for input and submission
    with st.form(key="search_form"):
        topic = st.text_input("Enter a coding topic:", placeholder="e.g., Machine Learning, Web Development")
        submit_button = st.form_submit_button("Search")

    # Check if the form was submitted
    if submit_button and topic.strip():
        # Display results
        results = analyze_topic(agent, topic)
        if results:
            st.markdown(results)
        else:
            st.error("No results found for the given topic.")
    elif submit_button and not topic.strip():
        st.error("Please enter a valid topic.")

if __name__ == "__main__":
    st.set_page_config(
        page_title="Coding Research Assistant",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    main()


    