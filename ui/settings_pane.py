# ui/settings_pane.py

import streamlit as st

def display_settings(conversation_memory_config):
    """
    Displays the settings pane in the Streamlit sidebar to adjust conversation memory settings.
    This includes an explanatory dropdown about why summarization is necessary and how the 
    configuration affects the context provided to agents in the pipeline.
    """
    # Sidebar Header
    st.sidebar.header("Conversation Memory Settings")

    # Explanatory Dropdown
    with st.sidebar.expander("Why are these settings important?", expanded=False):
        st.write("""
        Large Language Model (LLM) APIs, such as OpenAI's GPT models, are stateless by design. 
        This means they do not inherently retain memory of prior interactions beyond what is 
        explicitly included in the input to each request.

        To ensure that agents in the pipeline maintain relevant context from past interactions, 
        we generate a summarized trail of conversations and reports. This summary is fed back to 
        the agents, allowing them to "remember" key points and respond effectively while staying 
        within token limits.

        The settings below allow you to control the length of this summarization:
        - **Number of messages**: Determines how many recent conversation messages (both user 
          and assistant messages) are included in the summary. Higher values provide more 
          context but may risk exceeding token limits.
        - **Number of reports**: Specifies how many recent reports or results are included in the 
          summarized context for agents. Adjust this based on the depth of insights required.
        """)

    # Number of Messages to Summarize
    num_messages = st.sidebar.number_input(
        "Number of messages to include in summary",
        min_value=1,
        max_value=10,
        value=conversation_memory_config.num_messages,
        step=1,
        help="This sets the number of recent messages (user and assistant) included in the summarization. Adjust for optimal context."
    )

    # Number of Reports to Summarize
    num_reports = st.sidebar.number_input(
        "Number of reports to include in summary",
        min_value=1,
        max_value=10,
        value=conversation_memory_config.num_reports,
        step=1,
        help="This sets the number of recent reports included in the summarization. Adjust based on context needs."
    )

    # Update the configuration with user inputs
    conversation_memory_config.set_num_messages(num_messages)
    conversation_memory_config.set_num_reports(num_reports)
