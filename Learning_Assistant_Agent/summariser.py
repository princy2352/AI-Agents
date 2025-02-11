import streamlit as st
from agno.agent import Agent
from agno.tools.firecrawl import FirecrawlTools
from dotenv import load_dotenv
load_dotenv()

def get_firecrawl_agent():
    # Retrieve the Firecrawler API key from session state.
    firecrawler_api_key = st.session_state.get("firecrawler_api_key", "")
    if not firecrawler_api_key.strip():
        st.error("Firecrawler API key is required.")
        st.stop()
    # If the Firecrawl tool accepts an api_key parameter, pass it here.
    return Agent(
        tools=[FirecrawlTools(scrape=False, crawl=True, api_key=firecrawler_api_key)],
        show_tool_calls=True,
        markdown=True
    )

def summarize_url(url):
    """Return a summary for the given URL using Firecrawl tools."""
    try:
        agent_firecrawl = get_firecrawl_agent()
        response = agent_firecrawl.run(f"Summarize this {url}")
        return response.content
    except Exception as e:
        return f"Error: {e}"

def get_summary_page(url=None):
    st.header("URL Summary")
    if url is not None:
        if url.strip():
            with st.spinner("Summarizing URL..."):
                summary = summarize_url(url)
            st.markdown("### Summary Result:")
            st.markdown(summary)
            return summary
        else:
            st.error("Please enter a valid URL.")
            return ""
    else:
        url = st.text_input("Enter a URL to summarize:", "https://arxiv.org/pdf/1811.06341v1", key="url_input")
        if st.button("Summarize URL", key="summarize_url_btn"):
            if url.strip():
                with st.spinner("Summarizing URL..."):
                    summary = summarize_url(url)
                st.markdown("### Summary Result:")
                st.markdown(summary)
                return summary
            else:
                st.error("Please enter a valid URL.")
                return ""
