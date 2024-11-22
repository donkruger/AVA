"""
This is the main entry point of the AVA application. It sets up the Streamlit app and orchestrates the interaction between the user and the various agents in the RAG pipeline. Specifically, it:

- Initializes the Streamlit interface, including API key input and model selection for each agent.
- Sets up configuration using the Singleton pattern from `configs.config`.
- Instantiates the agents (`AgentZero`, `AgentOne`, `AgentTwo`) and utility managers (`ConversationManager`, `ResearchManager`, `RiskProfileManager`).
- Manages conversation history and session state using `st.session_state`.
- Processes user inputs and directs them through the appropriate agents using the Chain of Responsibility pattern.
- Ensures seamless interaction between the user interface and the backend logic.

**Updates:**

- Enhanced model selection to include both GPT and Claude models.
- Improved UI to request the appropriate API keys based on the selected models.
"""
# main.py

# main.py

import os
import streamlit as st
import ast  # Import ast for safe evaluation

# Import UI modules
from ui.header import display_header
from ui.how_it_works import display_how_it_works
from ui.model_selection import model_selection
from ui.api_keys import prompt_for_api_keys
from ui.conversation import initialize_conversation, display_conversation, get_user_input
from ui.session_state import initialize_session_state

# Import other necessary modules
from configs.config import Config
from agents.agent_zero import AgentZero
from agents.agent_one import AgentOne
from agents.agent_two import AgentTwo
from utils.conversation_utils import ConversationManager
from utils.research_utils import ResearchManager
from utils.risk_profile_utils import RiskProfileManager
from utils.single_stock_fundamentals import FundamentalsManager
from utils.price_chart_manager import PriceChartManager  # Import PriceChartManager

# Initialize session state
initialize_session_state()

# Display header and logo
display_header()

# Display "How It Works" section
display_how_it_works()

# Model options for GPT and Claude
gpt_models = [
    'gpt-3.5-turbo',
    'gpt-4',
    'gpt-4o'
]

claude_models = [
    'claude-3-opus-20240229',
    'claude-3-sonnet-20240229'
]

# Model selection
selected_models = model_selection(gpt_models, claude_models)

# Determine required API keys
required_api_keys = set()
for model in selected_models.values():
    if model in gpt_models:
        required_api_keys.add('openai')
    if model in claude_models:
        required_api_keys.add('anthropic')

# Prompt for API keys
prompt_for_api_keys(required_api_keys)

# Configuration setup
config = Config()
config.setup()

# Initialize agents with the appropriate API keys
def get_api_key_for_model(model_name):
    if model_name in gpt_models:
        return st.session_state['api_keys']['openai']
    elif model_name in claude_models:
        return st.session_state['api_keys']['anthropic']
    else:
        return None

agent_zero_api_key = get_api_key_for_model(selected_models['agent_zero'])
agent_zero = AgentZero(selected_models['agent_zero'], agent_zero_api_key)

agent_one_api_key = get_api_key_for_model(selected_models['agent_one'])
agent_one = AgentOne(selected_models['agent_one'], agent_one_api_key)

agent_two_api_key = get_api_key_for_model(selected_models['agent_two'])
agent_two = AgentTwo(selected_models['agent_two'], agent_two_api_key)

# Initialize managers
conversation_manager = ConversationManager()
research_manager = ResearchManager()
risk_profile_manager = RiskProfileManager()
fundamentals_manager = FundamentalsManager()
price_chart_manager = PriceChartManager()  # Initialize PriceChartManager

# Initialize conversation
initialize_conversation()

# Display conversation history
display_conversation()

# Get user input
user_input = get_user_input()

if user_input:
    # Add user message to conversation history
    st.session_state['messages'].append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state['conversation_history'].append({"role": "user", "content": user_input})

    # Process the user input
    def process_user_input(user_input):
        # Agent One evaluates the user input
        evaluation_response = agent_one.evaluate_input(user_input)
        st.write(f"**Evaluation Report from Agent One:**\n{evaluation_response}")

        # Append Agent One's evaluation to conversation history
        st.session_state['conversation_history'].append({"role": "agent_one", "content": evaluation_response})

        # Parse the evaluation response
        try:
            evaluation_dict = ast.literal_eval(evaluation_response)
        except (SyntaxError, ValueError):
            st.error("Failed to parse evaluation response.")
            return

        # Check evaluation response
        if 'investment_advice' in evaluation_dict and 'Y' in evaluation_dict['investment_advice']:
            # The user is requesting investment advice
            with st.spinner('Generating detailed report...'):
                research_summary = research_manager.generate_research_summary()
                st.write(research_summary)
                report_summary_text = research_manager.summarize_report(
                    research_summary,
                    selected_models['agent_zero'],
                    agent_zero_api_key
                )
            assistant_response = conversation_manager.conversation(user_input, agent_zero, report_summary=report_summary_text)
            return assistant_response
        elif 'investment_advice' in evaluation_dict and 'R' in evaluation_dict['investment_advice']:
            # The user is answering a risk profile question
            risk_profile_report = risk_profile_manager.generate_risk_profile(st.session_state['conversation_history'], agent_two)
            st.session_state['risk_profile_report'] = risk_profile_report
            st.write(f"**Risk Profile Report from Agent Two:**\n{risk_profile_report}")
            st.session_state['conversation_history'].append({"role": "agent_two", "content": risk_profile_report})
            assistant_response = conversation_manager.conversation(user_input, agent_zero)
            return assistant_response
        elif 'fundamentals' in evaluation_dict:
            # The user is requesting stock fundamentals
            stock_tickers = evaluation_dict['fundamentals']
            # Assuming it's a list with one ticker
            stock_ticker = stock_tickers[0]
            # Call the function to generate the fundamentals report
            fundamentals_report = fundamentals_manager.generate_fundamentals_report(stock_ticker)
            st.session_state['fundamentals_report'] = fundamentals_report
            st.write(f"**Fundamentals Report for {stock_ticker}:**\n{fundamentals_report}")
            st.session_state['conversation_history'].append({"role": "fundamentals_report", "content": fundamentals_report})
            # Generate assistant response
            assistant_response = conversation_manager.conversation(
                user_input,
                agent_zero,
                fundamentals_report=fundamentals_report
            )
            return assistant_response
        elif 'price_chart' in evaluation_dict:
            # The user is requesting a price chart
            stock_tickers = evaluation_dict['price_chart']
            # Assuming the list is [stock_ticker, period]
            stock_ticker = stock_tickers[0]
            if len(stock_tickers) > 1:
                period = stock_tickers[1]
            else:
                period = '1mo'  # Default period

            # Fetch price data
            with st.spinner(f'Fetching price data for {stock_ticker} over {period}...'):
                price_data, latest_price, error_message = price_chart_manager.get_price_data(stock_ticker, period)
                if error_message:
                    st.error(error_message)
                    assistant_response = conversation_manager.conversation(user_input, agent_zero)
                    return assistant_response

            st.session_state['price_chart_data'] = price_data
            st.write(f"**Price Chart for {stock_ticker} over {period}: Latest Price - ${latest_price:.2f}**")
            # Display the chart
            st.line_chart(price_data['Close'])

            # Add a note for AgentZero
            price_chart_note = f"{stock_ticker} over {period}, Latest Price: ${latest_price:.2f}"

            # Generate assistant response
            assistant_response = conversation_manager.conversation(
                user_input,
                agent_zero,
                price_chart_note=price_chart_note
            )
            return assistant_response
        else:
            # Continue interaction with Agent Zero via conversation
            assistant_response = conversation_manager.conversation(user_input, agent_zero)
            return assistant_response

    # Process the user input
    process_user_input(user_input)

