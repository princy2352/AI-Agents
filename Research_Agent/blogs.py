# medium.py
import streamlit as st
from agno.agent import Agent
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.models.google import Gemini
from dotenv import load_dotenv
from agno.tools.crawl4ai import Crawl4aiTools
from firecrawler import summarize_url  # For URL summarization

# Load environment variables
load_dotenv()

search_agent = Agent(
    tools=[DuckDuckGoTools()],
    model=Gemini(id="gemini-2.0-flash-exp"),
)

crawl_agent = Agent(
    tools=[Crawl4aiTools(max_length=None)], 
    show_tool_calls=True,
    instructions=[
        "Scrape blogs of the topic given by the user from https://medium.com",
        "Give the links of the top 10 recent articles from Medium of the topic provided by the user.",
        "Sort the articles in terms of relevance and content.",
        "Always include sources."
    ]
)

agent_team_medium = Agent(
    model=Gemini(id="gemini-2.0-flash-exp"),
    team=[search_agent, crawl_agent],
    instructions=[
        "First, summarize the given topic in 500 words.",
        "Then, list relevant Medium blogs with links about that topic.",
        "Always include sources."
    ],
)

def get_medium_blogs(topic):
    response = agent_team_medium.run(topic)
    return response.content

def medium_page(topic):
    st.header("Medium Blogs")
    if topic.strip():
        with st.spinner("Fetching Medium blogs..."):
            result = get_medium_blogs(topic)
        st.markdown(result)
    else:
        st.error("Please enter a valid topic for Medium blogs.")
    
    st.markdown("---")
    st.subheader("Or, summarize a Medium blog URL")
    url = st.text_input("Enter the URL of the Medium blog:", key="medium_url")
    if st.button("Summarize Medium Blog URL", key="medium_url_btn"):
        if url.strip():
            with st.spinner("Summarizing blog..."):
                summary = summarize_url(url)
            st.markdown("### Blog Summary:")
            st.markdown(summary)
        else:
            st.error("Please enter a valid URL.")