import streamlit as st
import requests
import json

# Set the URL of your Flask app
FLASK_APP_URL = "http://localhost:5000"  # This will work when running locally

st.title("Pet Care Q&A")

# Question input
question = st.text_input("Enter your question about pet care:")

if st.button("Ask"):
    if question:
        # Send POST request to /question endpoint
        response = requests.post(f"{FLASK_APP_URL}/question", json={"question": question})
        
        if response.status_code == 200:
            result = response.json()
            st.write("Answer:", result["answer"])
            
            # Store conversation_id in session state
            st.session_state.conversation_id = result["conversation_id"]
            
            # Display feedback buttons
            col1, col2 = st.columns(2)
            with col1:
                if st.button("👍 Helpful"):
                    feedback_response = requests.post(f"{FLASK_APP_URL}/feedback", 
                                                      json={"conversation_id": st.session_state.conversation_id, "feedback": 1})
                    if feedback_response.status_code == 200:
                        st.success("Thank you for your feedback!")
            with col2:
                if st.button("👎 Not Helpful"):
                    feedback_response = requests.post(f"{FLASK_APP_URL}/feedback", 
                                                      json={"conversation_id": st.session_state.conversation_id, "feedback": -1})
                    if feedback_response.status_code == 200:
                        st.success("Thank you for your feedback!")
        else:
            st.error("An error occurred while processing your question.")
    else:
        st.warning("Please enter a question.")

# Instructions for running the app
st.sidebar.header("How to use")
st.sidebar.write("""
1. Enter your pet care question in the text box.
2. Click 'Ask' to get an answer.
3. Provide feedback on the answer using the thumbs up or down buttons.
""")

# Information about the app
st.sidebar.header("About")
st.sidebar.write("""
This app uses AI to answer your pet care questions. 
It's connected to a database of pet care information to provide accurate and helpful responses.
""")
