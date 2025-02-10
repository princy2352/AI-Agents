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
        instructions=[
            "Give an overview of the topic in concise bullet points."
        ]
    )

def get_summary(topic):
    model_name = st.session_state.get("model_name", "Gemini (Google)")
    api_key = st.session_state.get("api_key", "")
    agent = get_summary_agent(model_name, api_key)
    response = agent.run(topic)
    return response.content
