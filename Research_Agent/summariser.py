# firecrawler.py
import streamlit as st
from agno.agent import Agent
from agno.tools.firecrawl import FirecrawlTools
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

agent_firecrawl = Agent(
    tools=[FirecrawlTools(scrape=False, crawl=True)], 
    show_tool_calls=True, 
    markdown=True
)

def summarize_url(url):
    """Return a summary for the given URL using Firecrawl tools."""
    try:
        response = agent_firecrawl.run(f"Summarize this {url}")
        return response.content
    except Exception as e:
        return f"Error: {e}"

def firecrawl_page():
    st.subheader("Direct URL Summary")
    # Use a form container as in your original code
    with st.form(key="firecrawl_form"):
        url = st.text_input("Enter a URL to summarize:", "https://arxiv.org/pdf/1811.06341v1")
        submit_button = st.form_submit_button("Summarize URL")
    
    if submit_button:
        if url.strip():
            with st.spinner("Summarizing URL..."):
                summary = summarize_url(url)
            st.markdown("### URL Summary:")
            st.markdown(summary)
        else:
            st.error("Please enter a valid URL.")