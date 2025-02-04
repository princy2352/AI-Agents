from agno.agent import Agent
from agno.tools.python import PythonTools
from agno.models.google import Gemini 
from dotenv import load_dotenv
load_dotenv()
agent = Agent(
    model=Gemini(id="gemini-2.0-flash-exp"),
    tools=[PythonTools()], 
    show_tool_calls=True,
    )
agent.print_response("Write a python script for fibonacci series and display the result till the 10th number")
