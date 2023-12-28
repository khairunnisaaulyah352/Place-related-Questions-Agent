import streamlit as st
import google.generativeai as genai
import random
from api import api

# Configure the API key
genai.configure(api_key=api)

# Set default parameters
defaults = {
    'model': 'models/text-bison-001',
    'temperature': 0.25,
    'candidate_count': 1,
    'top_k': 40,
    'top_p': 0.95,
}

# Add a header image about places
header_image = "places.jpg"
st.image(header_image, caption='Places Around the World',
         use_column_width=True, width=300)

st.title('Place-related Questions Agent')
st.write('Ask me anything related to a place, and I will generate a response!')

# Add a dropdown for selecting a country
countries = ["Asia", "Africa", "North America",
             "South America", "Antartica", "Europe", "Australia"]
selected_country = st.selectbox("Select a Country:", countries)

# Initialize conversation history in session state
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []

# Initialize reporting information in session state
if 'reporting_info' not in st.session_state:
    st.session_state.reporting_info = {"name": "", "email": ""}

# Initialize search history in session state
if 'search_history' not in st.session_state:
    st.session_state.search_history = []

# Create a text input for the user's question about a place
question = st.text_input("Ask me anything about a place:")

# When the 'Generate Response' button is pressed, generate the response
if st.button('Generate Response'):
    if selected_country != "Select Country":
        question += f" in {selected_country}"

    response = genai.generate_text(
        **defaults,
        prompt=question
    )

    # Display the response
    st.write("Response:")
    st.info(response.result)

    # Update the conversation history in session state
    st.session_state.conversation_history.append(f"You: {question}")
    st.session_state.conversation_history.append(f"Agent: {response.result}")

    # Update the search history in session state
    st.session_state.search_history.append(question)

# Varied list of suggested places based on search history
suggested_places = list(set(st.session_state.search_history))

# Button to suggest a place based on history
if st.button('Suggest a Place Based on History'):
    if suggested_places:
        # Generate a random place suggestion from the history
        suggested_place = random.choice(suggested_places)
        st.write(
            f"I suggest you go to {suggested_place} based on your search history!")
    else:
        st.write(
            "No search history available. Start searching to get personalized suggestions.")

# Display the conversation history in the sidebar
st.sidebar.title("Conversation History")
for entry in st.session_state.conversation_history:
    st.sidebar.text(entry)

# Button to clear conversation history
if st.sidebar.button('Clear Conversation History'):
    st.session_state.conversation_history = []

# Reporting feature
st.sidebar.title("Report an Issue")
report_name = st.sidebar.text_input("Your Name:")
report_email = st.sidebar.text_input("Your Email:")
report_issue_button = st.sidebar.button("Report Issue")

if report_issue_button:
    # Update reporting information in session state
    st.session_state.reporting_info["name"] = report_name
    st.session_state.reporting_info["email"] = report_email

    # You can add additional reporting logic here, such as sending an email or storing the report.

    st.sidebar.success("Issue reported successfully! Thank you.")
