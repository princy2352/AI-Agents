from phi.agent import Agent
from phi.tools.duckduckgo import DuckDuckGo
from phi.tools.crawl4ai_tools import Crawl4aiTools

# Create the agent with the required tools
agent = Agent(
    tools=[
        DuckDuckGo(),  # Search engine tool
        Crawl4aiTools(max_length=None),  # Web crawling tool
    ],
    description="An AI job search agent to find job descriptions for specific roles at specified companies.",
    instructions=[
        "Given a keyword for a job role and a company name by the user, "
        "use DuckDuckGo to search for job postings or career pages related to the company and role.",
        "Extract and crawl the complete job description from the most relevant results using Crawl4ai.",
        "Ensure the search results are relevant and provide detailed job descriptions.",
    ],
    show_tool_calls=True,
    debug_mode=True,
)

# Example query
response = agent.print_response(
    "Find job description for 'Machine Learning Engineer' role at 'TESLA'",
    markdown=True,
)
print(response)
