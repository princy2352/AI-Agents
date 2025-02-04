import streamlit as st
from health_agent import agent1_page
from research_agent import agent2_page

# Streamlit app interface
def main():
    st.set_page_config(page_title="AI Agents", layout="wide")

    # Sidebar navigation
    st.sidebar.title("Select an AI Agent")
    agent = st.sidebar.radio("Choose an agent", ("Medical Agent", "Coding Research Agent"))

    if agent == "Medical Agent":
        agent1_page()
    elif agent == "Coding Research Agent":
        agent2_page()

if __name__ == "__main__":
    main()
