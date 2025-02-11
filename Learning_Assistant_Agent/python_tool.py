"""from agno.agent import Agent
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

"""

from youtubesearchpython import VideosSearch

def get_top_youtube_videos(query, max_results=5):
    videos_search = VideosSearch(query, limit=max_results)
    results = videos_search.result()["result"]

    video_list = []
    for video in results:
        title = video['title']
        views = video['viewCount']['text']
        link = video['link']
        video_list.append(f"- **{title}** ({views}) 🔗 [Watch here]({link})")

    return video_list


topic = "Python machine learning"
videos = get_top_youtube_videos(topic)
if videos:
    print("### YouTube Videos:\n" + "\n".join(videos))
else:
    print("No relevant YouTube videos found.")
