from agno.agent import Agent
from agno.tools.arxiv import ArxivTools
from agno.models.google import Gemini 
from dotenv import load_dotenv
load_dotenv()

agent = Agent(
    model=Gemini(id="gemini-2.0-flash-exp"),
    tools=[ArxivTools()], 
    show_tool_calls=True,
    instructions= 'Always include sources.')
agent.print_response("Search arxiv for 'LSTM'", markdown=True)
