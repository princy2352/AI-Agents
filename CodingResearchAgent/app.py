from dotenv import load_dotenv

load_dotenv()
from flask import Flask, render_template, request, jsonify
from phi.agent import Agent
from phi.model.google import Gemini
from phi.tools.duckduckgo import DuckDuckGo
from phi.tools.youtube_tools import YouTubeTools
from phi.tools.github import GithubTools
from app_constants import SYSTEM_PROMPT, INSTRUCTIONS
import os
api_key = os.getenv('GOOGLE_API_KEY')


app = Flask(__name__)

# Initialize the agent
def get_agent():
    return Agent(
        name="Coding Research Agent",
        model=Gemini(id="gemini-2.0-flash-exp",api_key=api_key),
        tools=[GithubTools(), YouTubeTools(), DuckDuckGo()],
        description=SYSTEM_PROMPT,
        instructions=INSTRUCTIONS,
        show_tool_calls=True,
        markdown=True,
        add_datetime_to_instructions=True,
    )

# Function to analyze a coding topic
def analyze_topic(agent, topic):
    try:
        response = agent.run(topic)
        return response.content.strip()
    except Exception as e:
        return f"An error occurred: {e}"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    topic = request.form.get('topic')
    if not topic or not topic.strip():
        return jsonify({"error": "Please enter a valid topic."}), 400

    agent = get_agent()
    results = analyze_topic(agent, topic.strip())
    return jsonify({"results": results})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
