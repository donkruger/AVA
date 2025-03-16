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

    # Keep the raw report (string) ...
    if 'risk_profile_report' not in st.session_state:
        st.session_state['risk_profile_report'] = None

    # ... and the parsed data (dictionary)
    if 'risk_profile_data' not in st.session_state:
        st.session_state['risk_profile_data'] = {}

    if 'fundamentals_report' not in st.session_state:
        st.session_state['fundamentals_report'] = None

    if 'price_chart_data' not in st.session_state:
        st.session_state['price_chart_data'] = None

    if 'radar_chart_data' not in st.session_state:
        st.session_state['radar_chart_data'] = None
    if 'radar_chart_note' not in st.session_state:
        st.session_state['radar_chart_note'] = None


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

# (Optional) Add a section for downloading the risk profile:
def display_risk_profile_download():
    """
    Displays a download button if a risk profile report is available
    in session_state['risk_profile_report'].
    """
    if st.session_state.get('risk_profile_report'):
        st.download_button(
            label="Download Risk Profile (JSON)",
            data=st.session_state['risk_profile_report'].encode('utf-8'),
            file_name="risk_profile_report.json",
            mime="application/json"
        )
