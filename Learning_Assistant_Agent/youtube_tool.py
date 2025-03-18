import streamlit as st
from agno.agent import Agent
from agno.tools.googlesearch import GoogleSearchTools
from agno.tools.youtube import YouTubeTools
from agno.models.openai import OpenAIChat
from agno.models.google import Gemini
"""from dotenv import load_dotenv
load_dotenv()"""

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
        tools=[GoogleSearchTools(),YouTubeTools() ],
        description = [
            "You are a specialized educational content curator who identifies high-quality YouTube videos by accessing them through official YouTube API and tools.",
            "Your goal is to find verified, accessible videos that provide clear, accurate learning content."],
    instructions = [
    "Search for and verify YouTube videos using these steps:",
    "1. IMPORTANT: Only include videos with valid youtube.com or youtu.be URLs",
    "2. Verify each video URL before including it",
    "3. Format URLs as 'https://www.youtube.com/watch?v=[VIDEO_ID]'",
    
    "For each verified video, format the output as follows:",
    
    "🎥 **[VIDEO TITLE]** \n",
    "👤 Creator: [Channel Name] \n",
    
    
    "📝 Content Overview: \n",
    "   • [3-4 key topics covered] \n",
    
    "💡 Highlights: \n",
    "   • Teaching style \n",
    "   • Practical examples \n",
    "   • Visual aids/demonstrations \n",
    
    "🎯 Best for: [Beginner/Intermediate/Advanced]",
    "🔗 Link: [Video URL]",
    
    "---",  # Separator between videos
    
    "Quality Control Guidelines:",
    "• Double-check all URLs for validity",
    "• Ensure videos are publicly accessible",
    "• Verify videos are not shorts, livestreams, or premieres",
    "• Confirm videos are in English (or requested language)",
    
    "IMPORTANT URL RULES:",
    "1. Only use full YouTube URLs (https://www.youtube.com/watch?v=)",
    "2. Do not include playlist parameters",
    "3. Do not include timestamp parameters",
    "4. Do not include channel URLs",
    "5. Verify each URL exists before including it"
],
        
        markdown=True,
    )

def get_youtube_research(topic):
    agent = get_youtube_agent()
    response = agent.run(topic)
    return response.content


def youtube_page(topic):
    st.markdown("""
        <style>
        .video-card {
            padding: 20px;
            border-radius: 10px;
            background-color: #f8f9fa;
            margin: 15px 0;
            border: 1px solid #ddd;
        }
        .video-stats {
            color: #666;
            font-size: 0.9em;
            margin: 10px 0;
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.title("🎥 YouTube Videos")
    if topic.strip():
        with st.spinner("Fetching YouTube videos..."):
            query = f"List the top YouTube videos about '{topic}' along with brief descriptions and links."
            result = get_youtube_research(query)
        st.markdown(result)
    else:
        st.error("Please enter a valid topic.")
