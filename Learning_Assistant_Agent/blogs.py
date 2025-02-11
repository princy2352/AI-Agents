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
        
        description = [
    'You are a specialized content curator who discovers high-quality blog posts and articles, focusing on credibility, readability, and practical value for the user.',
],
instructions = [
    "Search for 10 articles and blog posts using these criteria:",
    "1. High relevance to the topic",
    "2. Recent publication (preferably within last 6 months)",
    "3. Content from reputable sources and established authors",
    "4. Mix of technical depth and practical applications",
    
    "For each article, format the output as follows:",
    
    "📝 **[ARTICLE TITLE]** \n",
    "✍️ Author: [Author Name] \n",
    "📅 Published: [Publication Date] \n",
    "📌 Summary: [5-6 sentences capturing the core message] \n",
    "🔗 Source: [Article URL] \n",
    "🏢 Platform: [Publishing platform/website] \n",
    
    "---",  # Separator between articles
    
    "Additional Guidelines:",
    "• Prioritize articles with hands-on examples or case studies",
    "• Include a mix of comprehensive guides and focused topics",
    "• Verify content is accessible (not behind paywalls)",
    "• Consider reader engagement metrics when available (likes, shares)",
    
    "Present the top 10 most relevant articles, ensuring diverse perspectives and depth levels."
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
    st.markdown("""
        <style>
        .blog-card {
            padding: 20px;
            border-radius: 10px;
            background-color: #f8f9fa;
            margin: 15px 0;
            border-left: 4px solid #00ab6c;
        }
        .blog-meta {
            color: #666;
            font-size: 0.9em;
            margin: 10px 0;
        }
        </style>
    """, unsafe_allow_html=True)
    st.title("📝 Blog Articles")
    if topic.strip():
        with st.spinner("Fetching blogs..."):
            model_name = st.session_state.get("model_name")
            result = get_medium_blogs(topic,model_name)
        st.markdown(result)
        
    else:
        st.error("Please enter a valid topic for blogs.")
    
    