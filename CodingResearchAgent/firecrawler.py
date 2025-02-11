from agno.agent import Agent
from agno.tools.firecrawl import FirecrawlTools
from dotenv import load_dotenv
load_dotenv()
agent = Agent(tools=[FirecrawlTools(scrape=False, crawl=True)], show_tool_calls=True, markdown=True)
agent.print_response("Summarize this https://arxiv.org/pdf/1811.06341v1")
