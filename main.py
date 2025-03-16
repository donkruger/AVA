"""
This is the main entry point of the AVA application. It sets up the Streamlit app and orchestrates 
the interaction between the user and the various agents in the RAG pipeline. Specifically, it:

- Initializes the Streamlit interface, including API key input and model selection for each agent.
- Sets up configuration using the Singleton pattern from `configs.config`.
- Instantiates the agents (`AgentZero`, `AgentOne`, `AgentTwo`) and utility managers 
  (`ConversationManager`, `ResearchManager`, `RiskProfileManager`).
- Manages conversation history and session state using `st.session_state`.
- Processes user inputs and directs them through the appropriate agents using the 
  Chain of Responsibility pattern.
- Ensures seamless interaction between the user interface and the backend logic.

**Updates:**

- Enhanced model selection to include both GPT and Claude models.
- Improved UI to request the appropriate API keys based on the selected models.
- Includes logic for state management, such that agent_0 has a historical summarised version 
  of the conversation.

**Additional updates to handle parsing issues**:
- A robust parsing function `parse_agent_response` is added to handle unexpected JSON-like 
  formatting or extra text around the dictionary. It uses regex to extract the substring 
  from the first '{' to the final '}', then attempts parsing via `ast.literal_eval` and 
  finally `json.loads`.
- All occurrences of direct `ast.literal_eval` usage are replaced by 
  `parse_agent_response` to avoid crashes on invalid/extra text.
"""

import os
import re
import json
import ast
import pandas as pd
import streamlit as st

# Import UI modules
from ui.header import display_header
from ui.how_it_works import display_how_it_works
from ui.model_selection import model_selection
from ui.api_keys import prompt_for_api_keys
from ui.conversation import initialize_conversation, display_conversation, get_user_input
from ui.session_state import initialize_session_state
from ui.settings_pane import display_settings  # Import the settings pane

# Import configuration and agents
from configs.config import Config
from configs.conversation_memory import ConversationMemoryConfig
from agents.agent_zero import AgentZero
from agents.agent_one import AgentOne
from agents.agent_two import AgentTwo
from agents.agent_summarizer import AgentSummarizer  # Import AgentSummarizer

# Import utility managers
from utils.conversation_utils import ConversationManager
from utils.research_utils import ResearchManager
from utils.risk_profile_utils import RiskProfileManager
from utils.single_stock_fundamentals import FundamentalsManager
from utils.price_chart_manager import PriceChartManager

# -----------------------------------------------------------------------------
# Utility function to robustly parse a dictionary from the agent's response
# -----------------------------------------------------------------------------

def parse_agent_response(response_text: str):
    """
    Attempts to extract the first dictionary-like substring from response_text 
    and parse it into a Python dictionary.
    
    1. Uses regex to find a curly-braced substring (from the first '{' to the matching '}')
    2. Tries ast.literal_eval (handles Python dict syntax, single quotes).
    3. Tries json.loads (handles JSON syntax, double quotes) if the above fails.
    4. Returns an empty dictionary if no parse is successful.
    """
    # Regex to capture everything from the first '{' to the final '}'
    match = re.search(r"(\{[\s\S]*\})", response_text)
    if not match:
        # No curly-braced content found
        return {}
    
    extracted = match.group(1).strip()

    # Try ast.literal_eval
    try:
        return ast.literal_eval(extracted)
    except (SyntaxError, ValueError):
        pass
    
    # Try JSON
    try:
        return json.loads(extracted)
    except (json.JSONDecodeError, ValueError):
        pass

    # If both attempts fail, return empty
    return {}

# -----------------------------------------------------------------------------
# Main Streamlit App
# -----------------------------------------------------------------------------

# Initialize session state
initialize_session_state()

# Initialize conversation memory configuration
conversation_memory_config = ConversationMemoryConfig()

# Display settings pane to adjust conversation memory settings
display_settings(conversation_memory_config)

# Display header and logo
display_header()

# Display "How It Works" section
display_how_it_works()

# Model options for GPT and Claude
gpt_models = [
    'gpt-3.5-turbo',
    'gpt-4',
    'gpt-4o',
    'gpt-4o-2024-08-06'
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

# -----------------------------------------------------------------------------
# Helper function to map user-provided themes
# -----------------------------------------------------------------------------

def map_theme(theme_input: str) -> str:
    """
    Maps a user-provided theme input to a recognized theme in the dataset.
    
    Args:
        theme_input (str): The theme input provided by the user.

    Returns:
        str: The mapped theme, or the original input if no mapping is found.
    """
    theme_mapping = {
        'ai': 'artificial intelligence',
        'arificial intelligence': 'artificial intelligence',
        'artificial intelligence': 'artificial intelligence',
        'ev': 'electric vehicle',
        'electric vehicle': 'electric vehicles',
        'electric vehicles': 'electric vehicles',
        'electric cars': 'electric vehicles',
        'cars': 'automobiles & parts',
        'vehicles': 'automobiles & parts',
        'tech': 'information technology',
        'technology': 'information technology',
        'fintech': 'financial services',
        'financial services': 'financial services',
        'blockchain': 'blockchain companies',
        'gaming': 'gaming',
        'games': 'gaming',
        'sports': 'active lifestyle',
        'active lifestyle': 'active lifestyle',
        'psychedelics': 'psychedelics',
        'entheogens': 'psychedelics',
        'green energy': 'sustainable energy',
        'renewables': 'sustainable energy',
        'crisper': 'biotechnology',
        'biotech': 'biotechnology',
        'biotechnology': 'biotechnology',
        'fashion': 'personal goods',
        'gold': 'mining',
        'pharma': 'pharmaceuticals & biotechnology',
        'pharmaceuticals': 'pharmaceuticals & biotechnology',
        'robotics': 'robotics',
        'coffee': 'beverages',
        'fast food': 'food producers',
        'travel': 'travel & leisure',
        'leisure': 'travel & leisure',
        'social media': 'social networking',
        'social networking': 'social networking',
        'microchips': 'technology hardware & equipment',
        'chips': 'technology hardware & equipment',
        'tobacco': 'tobacco',
        'real estate': 'real estate investment & services',
        'reit': 'real estate investment trusts',
        'insurance': 'life insurance',
        'mining': 'mining',
        'oil': 'oil & gas producers',
        'gas': 'oil & gas producers',
        'media': 'media',
        'dividends': 'dividends',
        'support': 'support services',
        'construction': 'household goods & home construction',
        'industrial': 'industrial engineering',
        'metals': 'industrial metals & mining',
        'forestry': 'forestry & paper',
        'healthcare': 'health care equipment & services',
        'health care': 'health care equipment & services',
        'food': 'food & drug retailers',
        'retail': 'general retailers',
        'luxury': 'personal goods',
    }

    theme_lower = theme_input.lower()
    if theme_lower in theme_mapping:
        return theme_mapping[theme_lower]
    return theme_lower

# -----------------------------------------------------------------------------
# Agent Initialization
# -----------------------------------------------------------------------------

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

# Initialize AgentSummarizer
agent_summarizer_api_key = get_api_key_for_model(selected_models['agent_zero'])
agent_summarizer = AgentSummarizer(selected_models['agent_zero'], agent_summarizer_api_key)

# Initialize managers
conversation_manager = ConversationManager(
    agent_zero,
    agent_summarizer,
    num_messages=conversation_memory_config.num_messages,
    num_reports=conversation_memory_config.num_reports
)
research_manager = ResearchManager()
risk_profile_manager = RiskProfileManager()
fundamentals_manager = FundamentalsManager()
price_chart_manager = PriceChartManager()

# -----------------------------------------------------------------------------
# UI and Conversation Flow
# -----------------------------------------------------------------------------

# Initialize conversation in session state
initialize_conversation()

# Display conversation history
display_conversation()

# Get user input from the UI
user_input = get_user_input()

if user_input:
    # Add user message to conversation history
    st.session_state['messages'].append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state['conversation_history'].append({"role": "user", "content": user_input})

    def process_user_input(user_input_text):
        # Initialize report_summaries
        report_summaries = st.session_state.get('report_summaries', [])

        # Generate conversation summary for context
        conversation_summary = agent_summarizer.summarize_conversation(
            st.session_state['conversation_history'],
            num_messages=conversation_memory_config.num_messages
        )

        # AgentOne evaluates the user input with context
        evaluation_response = agent_one.evaluate_input(
            user_input_text,
            conversation_summary=conversation_summary
        )
        st.write(f"**Evaluation Report from Agent One:**\n{evaluation_response}")

        # Append AgentOne's evaluation to conversation history
        st.session_state['conversation_history'].append({"role": "agent_one", "content": evaluation_response})

        # ---------------------------
        # Parse the evaluation response
        # ---------------------------
        evaluation_dict = parse_agent_response(evaluation_response)
        if not evaluation_dict:
            st.error("Failed to parse Agent One's evaluation into a dictionary. Please try again.")
            return

        # Summarize existing reports if any
        if report_summaries:
            reports_summary = agent_summarizer.summarize_reports(
                report_summaries,
                num_reports=conversation_memory_config.num_reports
            )
        else:
            reports_summary = None

        # ---------------------------
        # Handle Different Keys in the Dictionary
        # ---------------------------

        # 1) investment_advice: ['Y', 'R', or 'N']
        if 'investment_advice' in evaluation_dict and 'Y' in evaluation_dict['investment_advice']:
            # User is requesting investment advice
            with st.spinner('Generating detailed report...'):
                research_summary = research_manager.generate_research_summary()
                st.write(research_summary)
                report_summary_text = research_manager.summarize_report(
                    research_summary,
                    selected_models['agent_zero'],
                    agent_zero_api_key
                )
            report_summaries.append(report_summary_text)
            st.session_state['report_summaries'] = report_summaries

            # Update the summarized reports
            reports_summary = agent_summarizer.summarize_reports(
                report_summaries,
                num_reports=conversation_memory_config.num_reports
            )

            assistant_response = conversation_manager.conversation(
                user_input_text,
                conversation_summary=conversation_summary,
                reports_summary=reports_summary
            )
            return assistant_response

        # ===========================================
        # RISK PROFILE LOGIC
        # ===========================================
        if 'investment_advice' in evaluation_dict and 'R' in evaluation_dict['investment_advice']:
            # User answered a risk profile question -> call AgentTwo
            raw_risk_profile_report = risk_profile_manager.generate_risk_profile(
                st.session_state['conversation_history'],
                agent_two
            )

            # Store the raw JSON string for display/downloading
            st.session_state['risk_profile_report'] = raw_risk_profile_report

            # Parse the JSON into a dict for internal usage
            parsed_profile = risk_profile_manager.parse_risk_profile_report(raw_risk_profile_report)
            st.session_state['risk_profile_data'] = parsed_profile  # e.g. {'risk_ability': 'medium', 'age': '45'}

            st.write("**Risk Profile Report from Agent Two (Raw JSON):**")
            st.json(raw_risk_profile_report)

            st.write("**Parsed Risk Profile Data (Dictionary):**")
            st.write(parsed_profile)

            # Append the raw report to conversation history
            st.session_state['conversation_history'].append({"role": "agent_two", "content": raw_risk_profile_report})

            report_summaries.append(raw_risk_profile_report)
            st.session_state['report_summaries'] = report_summaries

            # Summarize updated reports
            reports_summary = agent_summarizer.summarize_reports(
                report_summaries,
                num_reports=conversation_memory_config.num_reports
            )

            # Pass the raw text to AgentZero if you want
            assistant_response = conversation_manager.conversation(
                user_input_text,
                conversation_summary=conversation_summary,
                reports_summary=reports_summary,
                risk_profile_report=raw_risk_profile_report
            )
            return assistant_response


        elif 'investment_advice' in evaluation_dict and 'N' in evaluation_dict['investment_advice']:
            # General conversation
            assistant_response = conversation_manager.conversation(
                user_input_text,
                conversation_summary=conversation_summary,
                reports_summary=reports_summary
            )
            return assistant_response

        # 2) fundamentals
        elif 'fundamentals' in evaluation_dict:
            stock_tickers = evaluation_dict['fundamentals']
            if not stock_tickers:
                st.warning("No stock ticker provided in 'fundamentals'.")
                return

            stock_ticker = stock_tickers[0]
            fundamentals_type = evaluation_dict.get('fundamentals_type', None)

            # Generate fundamentals report
            fundamentals_report = fundamentals_manager.generate_fundamentals_report(stock_ticker, fundamentals_type)
            st.session_state['fundamentals_report'] = fundamentals_report

            st.write(f"**Fundamentals Report for {stock_ticker}:**\n{fundamentals_report}")
            st.session_state['conversation_history'].append(
                {"role": "fundamentals_report", "content": fundamentals_report}
            )

            report_summaries.append(fundamentals_report)
            st.session_state['report_summaries'] = report_summaries

            # Update summarized reports
            reports_summary = agent_summarizer.summarize_reports(
                report_summaries,
                num_reports=conversation_memory_config.num_reports
            )

            assistant_response = conversation_manager.conversation(
                user_input_text,
                conversation_summary=conversation_summary,
                reports_summary=reports_summary,
                fundamentals_report=fundamentals_report
            )
            return assistant_response

        # 3) price_chart
        elif 'price_chart' in evaluation_dict:
            stock_tickers = evaluation_dict['price_chart']
            if not stock_tickers:
                st.warning("No stock ticker provided in 'price_chart'.")
                return

            stock_ticker = stock_tickers[0]
            period = stock_tickers[1] if len(stock_tickers) > 1 else '1mo'

            with st.spinner(f'Fetching price data for {stock_ticker} over {period}...'):
                price_data, latest_price, error_message = price_chart_manager.get_price_data(stock_ticker, period)
                if error_message:
                    st.error(error_message)
                    return conversation_manager.conversation(
                        user_input_text,
                        conversation_summary=conversation_summary,
                        reports_summary=reports_summary
                    )

            st.session_state['price_chart_data'] = price_data
            st.write(f"**Price Chart for {stock_ticker} over {period}: Latest Price - ${latest_price:.2f}**")
            st.line_chart(price_data['Close'])

            price_chart_note = f"{stock_ticker} over {period}, Latest Price: ${latest_price:.2f}"
            assistant_response = conversation_manager.conversation(
                user_input_text,
                conversation_summary=conversation_summary,
                reports_summary=reports_summary,
                price_chart_note=price_chart_note
            )
            return assistant_response

        # 4) compare_price_chart
        elif 'compare_price_chart' in evaluation_dict:
            chart_params = evaluation_dict['compare_price_chart']
            if not chart_params:
                st.warning("No tickers provided in 'compare_price_chart'.")
                return

            possible_period = chart_params[-1]
            known_periods = ['1d', '5d', '1mo', '3mo', '6mo', '1y', '5y', 'max']

            if possible_period in known_periods:
                period = possible_period
                stock_tickers = chart_params[:-1]
            else:
                period = '1mo'
                stock_tickers = chart_params

            if not stock_tickers:
                st.warning("No stock tickers provided for comparison.")
                return

            with st.spinner(f'Fetching comparative price data for {", ".join(stock_tickers)} over {period}...'):
                compare_data, error_message = price_chart_manager.get_comparative_price_data(stock_tickers, period)
                if error_message:
                    st.error(error_message)
                    return conversation_manager.conversation(
                        user_input_text,
                        conversation_summary=conversation_summary,
                        reports_summary=reports_summary
                    )

            st.write(f"**Comparative Price Chart for {', '.join(stock_tickers)} over {period}:**")
            st.line_chart(compare_data)

            price_chart_note = f"Comparison of {', '.join(stock_tickers)} over {period}"
            assistant_response = conversation_manager.conversation(
                user_input_text,
                conversation_summary=conversation_summary,
                reports_summary=reports_summary,
                price_chart_note=price_chart_note
            )
            return assistant_response

        # 5) radar_chart
        elif 'radar_chart' in evaluation_dict:
            chart_params = evaluation_dict['radar_chart']
            if len(chart_params) < 2:
                st.warning("You must provide at least one list of metrics and at least one ticker.")
                return conversation_manager.conversation(
                    user_input_text,
                    conversation_summary=conversation_summary,
                    reports_summary=reports_summary
                )

            metrics = chart_params[0]
            if not isinstance(metrics, list) or len(metrics) == 0:
                st.warning("The first element must be a non-empty list of metrics.")
                return conversation_manager.conversation(
                    user_input_text,
                    conversation_summary=conversation_summary,
                    reports_summary=reports_summary
                )

            stock_tickers = chart_params[1:]
            if len(stock_tickers) == 0:
                st.warning("Please provide at least one stock ticker.")
                return conversation_manager.conversation(
                    user_input_text,
                    conversation_summary=conversation_summary,
                    reports_summary=reports_summary
                )

            from utils.radar_chart_manager import RadarChartManager
            radar_manager = RadarChartManager()

            # Fetch data for radar metrics
            with st.spinner(
                f"Fetching data for {', '.join(stock_tickers)} on metrics: {', '.join(metrics)}..."
            ):
                radar_data, warning_message = radar_manager.get_metric_data(stock_tickers, metrics)
                if not radar_data:
                    st.error(f"Unable to retrieve data for {', '.join(stock_tickers)}.")
                    return conversation_manager.conversation(
                        user_input_text,
                        conversation_summary=conversation_summary,
                        reports_summary=reports_summary
                    )
                if warning_message:
                    st.warning(warning_message)

            # Create the radar chart
            radar_fig = radar_manager.create_radar_chart(radar_data, metrics)
            st.write(
                f"**Radar Chart for metrics {', '.join(metrics)} across {', '.join(radar_data.keys())}:**"
            )
            st.plotly_chart(radar_fig, use_container_width=True)

            radar_chart_note = (
                f"Radar chart for metrics {', '.join(metrics)} "
                f"on {', '.join(radar_data.keys())}"
            )
            assistant_response = conversation_manager.conversation(
                user_input_text,
                conversation_summary=conversation_summary,
                reports_summary=reports_summary,
                radar_chart_note=radar_chart_note
            )
            return assistant_response

        # -----------------------------------------------------
        # Possibly handle 'pe_div_yield_table' in a second pass
        # -----------------------------------------------------
        dividends_response = agent_one.evaluate_input(user_input_text, conversation_summary=conversation_summary)
        dividends_dict = parse_agent_response(dividends_response)

        if 'pe_div_yield_table' in dividends_dict:
            table_params = dividends_dict['pe_div_yield_table']
            fields = table_params.get('fields', ['pe_ratio', 'dividen_yield'])
            theme = table_params.get('theme', '')
            sort_by = table_params.get('sort_by', 'market_cap_usd')
            order = table_params.get('order', 'desc')
            limit = table_params.get('limit', None)  # optional limit

            table_path = os.path.join(os.getcwd(), 'data/pe_div_yield_table.csv')
            if os.path.exists(table_path):
                df = pd.read_csv(table_path)

                if theme:
                    # Map theme if it's an abbreviation
                    mapped_theme = map_theme(theme)
                    df = df[df['theme'].str.lower().str.contains(mapped_theme.lower())]
                    if df.empty:
                        st.warning(f"No results found for theme '{theme}'. Please try a different theme.")
                        return conversation_manager.conversation(
                            user_input_text,
                            conversation_summary=conversation_summary,
                            reports_summary=reports_summary
                        )

                # Desired column order
                desired_order = ['name', 'ticker', 'market_cap_usd', 'pe_ratio', 'dividen_yield', 
                                 'description', 'theme']

                # Ensure all requested fields are included (without duplication)
                for f in fields:
                    if f not in desired_order:
                        desired_order.append(f)

                # Filter df to only include columns that exist
                available_columns = [c for c in desired_order if c in df.columns]
                df = df[available_columns]

                # Sort if possible
                if sort_by in df.columns:
                    ascending = (order == 'asc')
                    df = df.sort_values(by=sort_by, ascending=ascending)

                # Apply limit if specified
                if isinstance(limit, int) and limit > 0:
                    df = df.head(limit)

                # Formatting for better readability
                format_dict = {
                    'market_cap_usd': '${:,.2f}',
                    'dividen_yield': '{:.2%}'
                }
                styled_df = df.style.format(format_dict)

                st.write("**Results from pe_div_yield_table:**")
                st.dataframe(styled_df)
            else:
                st.error("pe_div_yield_table.csv not found.")

            assistant_response = conversation_manager.conversation(
                user_input_text,
                conversation_summary=conversation_summary,
                reports_summary=reports_summary
            )
            return assistant_response

        # ------------------------------------------------------
        # If none of the conditions matched, continue normally
        # ------------------------------------------------------
        assistant_response = conversation_manager.conversation(
            user_input_text,
            conversation_summary=conversation_summary,
            reports_summary=reports_summary
        )
        return assistant_response

    # Process the user input
    process_user_input(user_input)

# Risk Profile - Download Button
if st.session_state.get('risk_profile_report'):
    st.download_button(
        label="Download Risk Profile (JSON)",
        data=st.session_state['risk_profile_report'].encode('utf-8'),
        file_name="risk_profile_report.json",
        mime="application/json"
    )
