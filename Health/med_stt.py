from typing import List
from phi.tools import Toolkit
from phi.utils.log import logger
import pyttsx3
import speech_recognition as sr
from phi.agent import Agent
from phi.model.google import Gemini
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class SpeechTools(Toolkit):
    def __init__(self):
        super().__init__(name="speech_tools")
        self.register(self.capture_speech)
        self.register(self.say_text)

    def capture_speech(self) -> str:
        """Capture speech from the microphone and convert it to text."""
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening... Please speak now.")
            try:
                # Adjust for ambient noise and record audio
                recognizer.adjust_for_ambient_noise(source)
                audio_data = recognizer.listen(source, timeout=5)
                # Recognize speech using Google Web Speech API
                text = recognizer.recognize_google(audio_data)
                return text
            except sr.UnknownValueError:
                return "Sorry, I couldn't understand that."
            except sr.RequestError as e:
                return f"Speech Recognition error: {e}"

    def say_text(self, text: str):
        """Convert text to speech."""
        try:
            engine = pyttsx3.init()
            engine.say(text)
            engine.runAndWait()
            engine.stop()  # Ensure the event loop stops
        except RuntimeError:
            print("Text-to-speech engine is already running. Skipping speech.")


# Initialize the Medical Agent
medical_agent = Agent(
    name="Medical Agent",
    model=Gemini(id="gemini-2.0-flash-exp"),
    description=(
        "You are an assistant that provides personalized health insights and wellness suggestions. "
        "Your task is to analyze health data provided by the user and offer actionable recommendations. "
        "Focus on promoting long-term health and well-being while addressing specific concerns."
    ),
    instructions=[
        "1. When given daily health activity data (e.g., steps, heart rate, sleep patterns, calories burned):",
        "   - Analyze the trends and patterns in the data.",
        "   - Provide 3 personalized recommendations for improving overall health based on the data.",
        "   - Highlight any anomalies or noteworthy observations.",
        "2. If the user provides specific health goals (e.g., weight loss, stress reduction, improved sleep):",
        "   - Offer a 5-step action plan tailored to those goals.",
        "   - Incorporate relevant health metrics from the user's data.",
        "   - Suggest tools, exercises, or techniques that align with the goals.",
        "3. If the user reports any symptoms or concerns:",
        "   - List potential causes or triggers for the symptoms.",
        "   - Advise when to consult a healthcare professional based on the severity or persistence of the symptoms.",
        "   - Share practical self-care tips to alleviate the symptoms if appropriate.",
        "4. Format the response in Markdown with the following sections:",
        "   - **Overview of Health Data Trends** (if applicable).",
        "   - **Personalized Recommendations**.",
        "   - **Action Plan for Health Goals** (if goals are provided).",
        "   - **Symptom Insights and Advice** (if symptoms are reported).",
        "5. If no relevant insights can be provided, mention that clearly and suggest alternative approaches."
    ],
    show_tool_calls=True,
    markdown=True,
    add_datetime_to_instructions=True,
)

def main():
    print("Welcome to the Medical Assistant!")
    speech_tools = SpeechTools()
    while True:
        print("\nOptions:")
        print("1. Type your question")
        print("2. Speak your question")
        print("3. Exit")

        choice = input("Enter your choice (1/2/3): ").strip()
        if choice == "1":
            # User types a question
            user_input = input("Type your question: ")
        elif choice == "2":
            # User speaks a question
            user_input = speech_tools.capture_speech()
            print(f"You said: {user_input}")
        elif choice == "3":
            print("Exiting. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")
            continue

        # Process input and get response from the Medical Agent
        if user_input and "Sorry" not in user_input:
            response = medical_agent.run(user_input)
            print("\nMedical Agent Response:")
            print(response.content)

            # Speak the response
            speech_tools.say_text(response.content)

if __name__ == "__main__":
    main()
