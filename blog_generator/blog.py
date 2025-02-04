import json
from typing import Optional, Iterator

from pydantic import BaseModel, Field
from phi.model.google import Gemini        
from phi.agent import Agent
from phi.workflow import Workflow, RunResponse, RunEvent
from phi.storage.workflow.sqlite import SqlWorkflowStorage
from phi.tools.duckduckgo import DuckDuckGo
from phi.utils.pprint import pprint_run_response
from phi.utils.log import logger
from dotenv import load_dotenv

load_dotenv()
import os
api_key = os.getenv('GOOGLE_API_KEY')
class NewsArticle(BaseModel):
    title: str = Field(..., description="Title of the article.")
    url: str = Field(..., description="Link to the article.")
    summary: Optional[str] = Field(..., description="Summary of the article if available.")


class SearchResults(BaseModel):
    articles: list[NewsArticle]


class BlogPostGenerator(Workflow):
    searcher: Agent = Agent(
        model=Gemini(id="gemini-2.0-flash-exp", api_key=api_key),

        tools=[DuckDuckGo()],
        instructions=[
        "You're a professional research assistant for digital content creation.",
        "Given a topic, search for recent (last 6 months) high-quality articles from authoritative sources",
        "Evaluate articles based on:",
        "- Relevance to core topic",
        "- Author credibility (industry experts, reputable publications)",
        "- Engagement metrics (shares, comments)",
        "- Depth of analysis",
        "Return 5 articles that offer diverse perspectives while maintaining high quality.",
        "Prioritize sources like: Medium articles, industry blogs, academic papers, and verified news outlets."
    ],
        response_model=SearchResults,
    )

    writer: Agent = Agent(
    model=Gemini(id="gemini-2.0-flash-exp", api_key=api_key),
    instructions=[
        "You are a senior editor at Medium specializing in viral content creation. Follow these instructions precisely:",
        "### Blog Post Requirements",
        "1. **Title**: Use power words + curiosity gap (e.g., 'The Untold Truth About...').",
        "2. **Introduction**: Start with a surprising statistic or anecdote. Use the PAS framework (Problem-Agitate-Solve).",
        "3. **Body**:",
        "   - Divide into 3-5 subsections with H3 headers.",
        "   - Use bullet points for lists.",
        "   - Include at least one case study or real-world application.",
        "4. **Conclusion**:",
        "   - Summarize key insights.",
        "   - End with a thought-provoking question + CTA (e.g., 'What's your take? Comment below').",
        "5. **Style Guidelines**:",
        "   - Flesch-Kincaid grade level 8-10.",
        "   - Use active voice (80%+ of sentences).",
        "   - Limit industry jargon to 10%.",
        "6. **SEO Optimization**:",
        "   - Include primary keyword in H1 and 2-3 H2s.",
        "   - Add latent semantic indexing keywords naturally.",
        "7. **Sources**:",
        "   - Hyperlink to original articles using [relevant anchor text].",
        "   - Never invent sources. Omit if unavailable.",
        "8. **Formatting**:",
        "   - 1500-2000 words total.",
        "   - Add emojis in section headers (➡️, 🔍, 💡).",
        "   - Use Medium's signature purple highlights for key quotes.",
        "### Output Format",
        "Your output must follow this exact structure:",
        "```markdown",
        "# [Catchy Title with Power Words]",
        "➡️ **Introduction**",
        "[Start with a surprising statistic or anecdote. Use PAS framework.]",
        "🔍 **Section 1: [Subsection Title]**",
        "[Content with bullet points, case studies, and hyperlinks.]",
        "💡 **Section 2: [Subsection Title]**",
        "[Content with bullet points, case studies, and hyperlinks.]",
        "➡️ **Conclusion**",
        "[Summarize key insights. End with a thought-provoking question + CTA.]",
        "```",
        "### Important Notes",
        "- Do not deviate from this structure.",
        "- Use emojis in headers as specified.",
        "- Always include hyperlinks to sources.",
    ],
)

    def run(self, topic: str, use_cache: bool = True) -> Iterator[RunResponse]:
        logger.info(f"Generating a blog post on: {topic}")

        # Use the cached blog post if use_cache is True
        if use_cache and "blog_posts" in self.session_state:
            logger.info("Checking if cached blog post exists")
            for cached_blog_post in self.session_state["blog_posts"]:
                if cached_blog_post["topic"] == topic:
                    logger.info("Found cached blog post")
                    yield RunResponse(
                        run_id=self.run_id,
                        event=RunEvent.workflow_completed,
                        content=cached_blog_post["blog_post"],
                    )
                    return

        # Step 1: Search the web for articles on the topic
        num_tries = 0
        search_results: Optional[SearchResults] = None
        # Run until we get a valid search results
        while search_results is None and num_tries < 3:
            try:
                num_tries += 1
                searcher_response: RunResponse = self.searcher.run(topic)
                if (
                    searcher_response
                    and searcher_response.content
                    and isinstance(searcher_response.content, SearchResults)
                ):
                    logger.info(f"Searcher found {len(searcher_response.content.articles)} articles.")
                    search_results = searcher_response.content
                else:
                    logger.warning("Searcher response invalid, trying again...")
            except Exception as e:
                logger.warning(f"Error running searcher: {e}")

        # If no search_results are found for the topic, end the workflow
        if search_results is None or len(search_results.articles) == 0:
            yield RunResponse(
                run_id=self.run_id,
                event=RunEvent.workflow_completed,
                content=f"Sorry, could not find any articles on the topic: {topic}",
            )
            return

        # Step 2: Write a blog post
        logger.info("Writing blog post")
        # Prepare the input for the writer
        writer_input = {
            "topic": topic,
            "articles": [v.model_dump() for v in search_results.articles],
        }
        # Run the writer and yield the response
        yield from self.writer.run(json.dumps(writer_input, indent=4), stream=True)

        # Save the blog post in the session state for future runs
        if "blog_posts" not in self.session_state:
            self.session_state["blog_posts"] = []
        self.session_state["blog_posts"].append({"topic": topic, "blog_post": self.writer.run_response.content})


# The topic to generate a blog post on
topic = "AI Agents vs AI Models"

# Create the workflow
generate_blog_post = BlogPostGenerator(
    session_id=f"generate-blog-post-on-{topic}",
    storage=SqlWorkflowStorage(
        table_name="generate_blog_post_workflows",
        db_file="tmp/workflows.db",
    ),
)

# Run workflow
blog_post: Iterator[RunResponse] = generate_blog_post.run(topic=topic, use_cache=True)

# Print the response
pprint_run_response(blog_post, markdown=True)
