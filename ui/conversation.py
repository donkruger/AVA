# ui/conversation.py

import streamlit as st

def initialize_conversation():
    """
    Initializes the conversation history and reports in session state.
    """
    if 'messages' not in st.session_state:
        st.session_state['messages'] = []
        st.session_state['messages'].append({"role": "assistant", "content": "Hi, how can I help you today?"})

    if 'conversation_history' not in st.session_state:
        st.session_state['conversation_history'] = []

    if 'risk_profile_report' not in st.session_state:
        st.session_state['risk_profile_report'] = None

    if 'fundamentals_report' not in st.session_state:
        st.session_state['fundamentals_report'] = None

    if 'price_chart_data' not in st.session_state:
        st.session_state['price_chart_data'] = None

def display_conversation():
    """
    Displays the conversation history in the Streamlit app.
    """
    for message in st.session_state['messages']:
        if message['role'] == 'user':
            with st.chat_message("user"):
                st.markdown(message['content'])
        else:
            with st.chat_message("assistant"):
                st.markdown(message['content'])

def get_user_input():
    """
    Captures user input from the chat input box.

    Returns:
        str: The user's input message.
    """
    return st.chat_input("Type your message...")
