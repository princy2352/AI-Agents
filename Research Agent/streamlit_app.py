from phi.agent import Agent
from phi.model.openai import OpenAIChat
from phi.tools.duckduckgo import DuckDuckGo
from phi.tools.youtube_tools import YouTubeTools
from phi.tools.github import GithubTools
from dotenv import load_dotenv
from phi.playground import Playground, serve_playground_app
import streamlit as st
load_dotenv()
@st.cache_resource
def get_agent():
    return Agent(
        name="Coding Research Agent",
        model=OpenAIChat(id="gpt-4o"),
        tools=[GithubTools(), YouTubeTools(),DuckDuckGo()],
        description=(
            "You are an assistant that provides insights into coding-related topics. "
            "Your task is to retrieve the top 5 GitHub repositories and top 5 YouTube videos "
            "related to the requested coding topic. Provide the results in a clear Markdown format."
        ),
        instructions=[
            "1. When given a coding-related topic, search for the top 5 GitHub repositories using the GitHub tool.",
            "   - Evaluate repositories based on stars, relevance, and quality of content.",
            "   - Provide the repository name, description, star count, and a link to the repository.",
            "2. Search for the top 5 related YouTube videos using the YouTube tool.",
            "   - Focus on videos that are informative, highly rated, and recent.",
            "   - Provide the video title, creator/channel name, video length, and a link to the video.",
            "3. If no relevant links are found for either GitHub or YouTube, mention that clearly in the response.",
            "4. Format your response in Markdown with separate sections for GitHub repositories and YouTube videos.",
        ],
        
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

    # Input field for the coding topic
    topic = st.text_input("Enter a coding topic:", placeholder="e.g., Machine Learning, Web Development")

    if st.button("Search"):
        if topic.strip():
            # Display results
            results = analyze_topic(agent, topic)
            if results:
                st.markdown(results)
            else:
                st.error("No results found for the given topic.")
        else:
            st.error("Please enter a valid topic.")

if __name__ == "__main__":
    st.set_page_config(
        page_title="Coding Research Assistant",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    main()