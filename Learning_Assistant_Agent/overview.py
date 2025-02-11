import streamlit as st
from agno.agent import Agent
from agno.models.google import Gemini
from agno.models.openai import OpenAIChat

def get_model_instance(model_name, api_key):
    if not api_key.strip():
        st.error("API key is required for model access.")
        st.stop()
    if model_name == "Gemini (Google)":
        return Gemini(id="gemini-2.0-flash-exp", api_key=api_key)
    elif model_name == "OpenAI (GPT-4)":
        return OpenAIChat(id="gpt-4", api_key=api_key)
    else:
        st.error("Invalid model name provided.")
        st.stop()

def get_summary_agent(model_name, api_key):
    model_instance = get_model_instance(model_name, api_key)
    return Agent(
        model=model_instance,
        show_tool_calls=True,
        markdown=True,
        description = [
    "You are an expert educational synthesizer who creates clear, structured, and comprehensive topic overviews.",
    "Your goal is to break down complex topics into digestible sections while maintaining depth and accuracy."
],
instructions = [
    "Create a structured overview of the topic following this format:",
    
    "###📚 **Topic Overview**",
    
    "🎯 Core Concept:",
    "• [2-3 sentences defining the topic clearly]",
    
    "🔑 Key Components:",
    "• [4-5 fundamental elements or principles]",
    "• Each point should be 1-2 sentences",
    
    "💡 Main Applications:",
    "• [3-4 real-world uses or implementations]",
    
    "⚡ Key Features:",
    "• [4-5 distinctive characteristics]",
    
    "🛠️ Technologies/Tools (if applicable):",
    "• [Related technologies or tools]",
    
    "📈 Current Trends:",
    "• [2-3 current developments or directions]",
    
    "🎓 Prerequisites (if any):",
    "• [Required background knowledge]",
    
    "⚠️ Important Considerations:",
    "• [2-3 critical points to remember]",
    
    "Additional Guidelines:",
    "• Keep points concise but informative",
    "• Use simple, clear language",
    "• Include both theoretical and practical aspects",
    "• Maintain logical flow between sections",
    "• Adapt depth based on topic complexity",
    
    "Format each bullet point as a complete thought that can stand alone."
]
    )

def get_summary(topic):
    st.markdown("""
        <style>
        .overview-card {
            padding: 20px;
            border-radius: 10px;
            background-color: #f8f9fa;
            margin: 10px 0;
            border-left: 4px solid #0066cc;
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.title("📚 Topic Overview")
    model_name = st.session_state.get("model_name", "Gemini (Google)")
    api_key = st.session_state.get("api_key", "")
    agent = get_summary_agent(model_name, api_key)
    response = agent.run(topic)
    return response.content
