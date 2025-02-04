import streamlit as st
from phi.agent import Agent
from phi.model.openai import OpenAIChat
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize the Medical Agent
medical_agent = Agent(
    name="Medical Agent",
    model=OpenAIChat(id="gpt-4o"),
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

# Streamlit app interface
def main():
    st.title("Medical Agent Health Assistant")
    
    # User inputs
    st.header("Enter your health data and symptoms")
    
    # Text inputs
    health_data = st.text_area(
        "Enter your health data (e.g., steps, heart rate, sleep patterns, etc.):",
        "ActiveEnergyBurned 0.074 Cal AppleWalkingSteadiness 0.871677 % BasalEnergyBurned Cal 19.324"
    )
    
    goals = st.text_input("Enter your health goals:", "I want to stay healthy.")
    symptoms = st.text_area("Enter any symptoms you're experiencing:", "I have started feeling lethargic and irritable.")
    
    if st.button("Get Recommendations"):
        # Generate the response using the agent
        input_text = f"Health Data: {health_data}\nGoals: {goals}\nSymptoms: {symptoms}"
        response = medical_agent.run(input_text)
        
        # Display response
        st.markdown("### Medical Recommendations:")
        st.markdown(response.content)

# Run the app
if __name__ == "__main__":
    main()
