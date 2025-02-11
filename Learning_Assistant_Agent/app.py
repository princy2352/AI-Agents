import streamlit as st
from dotenv import load_dotenv
from overview import get_summary
from research_papers import arxiv_page
from blogs import medium_page
from github_tool import github_page
from youtube_tool import youtube_page

def set_page_config():
    st.set_page_config(
        page_title="Learning Assistant AI",
        page_icon="🎓",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS
    st.markdown("""
        <style>
        .main {
            padding: 2rem;
        }
        .stButton>button {
            width: 100%;
            padding: 1rem;
            border-radius: 10px;
        }
        .css-1d391kg {
            padding: 2rem;
        }
        .stTextInput>div>div>input {
            padding: 1rem;
        }
        </style>
    """, unsafe_allow_html=True)

def sidebar_config():
    with st.sidebar:
        
        st.header("⚙️ Configuration")
        
        # Model Selection with info
        st.subheader("Model Selection")
        model_info = {
            "Gemini (Google)": "",
            "OpenAI (GPT-4)": ""
        }
        selected_model = st.selectbox(
            "Select AI Model",
            options=list(model_info)
        )
        st.info(model_info[selected_model])
        
        # API Keys with validation
        st.subheader("API Configuration")
        api_key = st.text_input("Main API Key", type="password", help="Enter your API key for the selected model")
        firecrawler_key = st.text_input("Firecrawler API Key", type="password", help="Required for blog search functionality")
        
        if not api_key.strip() or not firecrawler_key.strip():
            st.warning("⚠️ Both API keys are required for full functionality")
        
        # Save to session state
        st.session_state.update({
            "api_key": api_key,
            "model_name": selected_model,
            "firecrawler_api_key": firecrawler_key
        })
        
        st.markdown("---")

def main_content():
    st.title("🎓 Learning Assistant AI")
    st.markdown("Your intelligent research companion powered by AI")
    
    # Topic input with example
    topic = st.text_input(
        "What would you like to learn about?",
        placeholder="e.g., Machine Learning, Python Programming, Data Science",
        help="Enter any topic you want to research"
    )
    
    if topic.strip():
        st.session_state["topic"] = topic
        
        # Service selection with improved layout
        st.markdown("### Select the type of resource")
        
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            overview_btn = st.button(
                "📝 Overview",
                help="Get a concise overview of the topic"
            )
            
        with col2:
            papers_btn = st.button(
                "📚 Research Papers",
                help="Find academic papers from ArXiv"
            )
            
        with col3:
            blogs_btn = st.button(
                "📰 Blogs",
                help="Discover relevant blog posts"
            )
            
        with col4:
            github_btn = st.button(
                "💻 GitHub",
                help="Find related repositories"
            )
            
        with col5:
            youtube_btn = st.button(
                "🎥 YouTube",
                help="Watch educational videos"
            )
        
        # Progress tracking
        if any([overview_btn, papers_btn, blogs_btn, github_btn, youtube_btn]):
            progress = st.progress(0)
            status = st.empty()
            
        # Handle button clicks
        if overview_btn:
            status.text("Generating overview...")
            progress.progress(50)
            summary = get_summary(topic)
            
            st.markdown(summary)
            progress.progress(100)
            status.empty()
            
        elif papers_btn:
            status.text("Searching research papers...")
            progress.progress(50)
            arxiv_page(topic)
            progress.progress(100)
            status.empty()
            
        elif blogs_btn:
            status.text("Finding relevant blogs...")
            progress.progress(50)
            medium_page(topic)
            progress.progress(100)
            status.empty()
            
        elif github_btn:
            status.text("Searching GitHub repositories...")
            progress.progress(50)
            github_page(topic)
            progress.progress(100)
            status.empty()
            
        elif youtube_btn:
            status.text("Finding YouTube videos...")
            progress.progress(50)
            youtube_page(topic)
            progress.progress(100)
            status.empty()
            
    else:
        # Example topics showcase
        st.info("👋 Welcome! Try searching for topics like:")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.code("Machine Learning")
        with col2:
            st.code("Web Development")
        with col3:
            st.code("Data Science")



def main():
    set_page_config()
    sidebar_config()
    main_content()

if __name__ == "__main__":
    main()