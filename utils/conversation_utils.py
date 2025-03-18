# utils/conversation_utils.py

import re
import streamlit as st

class ConversationManager:
    """
    💬 ConversationManager Class - Conversation Handling for Advisory App
    ---------------------------------------------------------------------
    Technical Overview:
    The ConversationManager class manages the flow of dialogue between the user and AgentZero. It combines 
    user input, optional report summaries, and risk profile reports to generate a coherent assistant response. 
    The conversation method retrieves the latest risk profile report, if available, and passes relevant context 
    to AgentZero to generate a response. The response is then cleaned, stored in session state, and displayed 
    on the interface, ensuring continuity and consistency in user interactions. This class helps centralize 
    dialogue management, facilitating clear communication within the app.

    In Simple Terms:
    The ConversationManager is like the chat handler. It takes what the user says, combines it with any extra 
    information like risk reports, and gets a response from AgentZero. This response is cleaned up, saved to 
    the chat history, and shown to the user, making sure the conversation feels smooth and on-topic.

    Attributes:
    - None specific to this class; it relies on session state for data storage.

    Methods:
    - conversation: Manages the chat flow by combining user input, reports, and agent responses, cleaning 
      the output, and saving it to the chat history for seamless interaction.
    """

    def __init__(self, agent_zero, agent_summarizer, num_messages=3, num_reports=3):
        self.agent_zero = agent_zero
        self.agent_summarizer = agent_summarizer
        self.num_messages = num_messages
        self.num_reports = num_reports

    def conversation(self, user_input, **kwargs):
        """
        Handles the chat flow by combining user input with context and generating a response from AgentZero.

        Parameters:
        - user_input (str): The user's input to the system.
        - kwargs (dict): Optional additional arguments such as:
          - report_summaries: List of past report summaries.
          - risk_profile_report: The latest risk profile report.
          - fundamentals_report: Fundamentals report of a stock.
          - price_chart_note: Notes from the price chart.

        Returns:
        - str: The assistant's response.
        """
        # Summarize conversation history
        conversation_summary = self.agent_summarizer.summarize_conversation(
            st.session_state['conversation_history'],
            num_messages=self.num_messages
        )

        # Summarize reports if provided
        report_summaries = kwargs.get('report_summaries', [])
        if 'report_summaries' in st.session_state:
            report_summaries.extend(st.session_state['report_summaries'])

        reports_summary = self.agent_summarizer.summarize_reports(
            report_summaries,
            num_reports=self.num_reports
        ) if report_summaries else None

        # Extract additional context from kwargs
        risk_profile_report = kwargs.get('risk_profile_report')
        fundamentals_report = kwargs.get('fundamentals_report')
        price_chart_note = kwargs.get('price_chart_note')

        radar_chart_note = kwargs.get('radar_chart_note', None)

        # Generate assistant response with summarized context
        assistant_response = self.agent_zero.generate_response(
            user_input,
            conversation_summary=conversation_summary,
            reports_summary=reports_summary,
            risk_profile_report=risk_profile_report,
            fundamentals_report=fundamentals_report,
            price_chart_note=price_chart_note,
            radar_chart_note=radar_chart_note
        )

        # Clean up the response
        assistant_response = re.sub(r"[\n\n]+", "\n\n", assistant_response).strip()
        st.session_state['messages'].append({"role": "assistant", "content": assistant_response})
        with st.chat_message("assistant"):
            st.markdown(assistant_response)

        # Append Agent Zero's response to conversation history
        st.session_state['conversation_history'].append({"role": "assistant", "content": assistant_response})

        return assistant_response
