import streamlit as st
from phi.agent import Agent
from phi.model.openai import OpenAIChat
from phi.tools.duckduckgo import DuckDuckGo
from phi.tools.youtube_tools import YouTubeTools
from phi.tools.github import GithubTools
from dotenv import load_dotenv
from phi.playground import Playground, serve_playground_app

load_dotenv()

coding_research_agent = Agent(
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
# Streamlit app setup
st.title("Coding Research Agent")
st.write(
    "An AI-powered assistant to fetch top GitHub repositories and YouTube videos for coding topics."
)

# Input field for query
query = st.text_input("Enter a coding-related topic:", "")

if st.button("Search"):
    if query.strip():
        with st.spinner("Fetching results..."):
            response = coding_research_agent.run(query)
            st.markdown(response.result, unsafe_allow_html=True)
    else:
        st.error("Please enter a valid topic to search!")

""""
app = Playground(agents=[coding_research_agent]).get_app()

if __name__ == "__main__":
    serve_playground_app("research_agent:app", reload=True)"""

#coding_research_agent.print_response("Transformers", stream=True)