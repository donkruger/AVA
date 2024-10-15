import re
import pandas as pd
import os
import streamlit as st
from importlib import util

from llmware.web_services import YFinance
from llmware.models import ModelCatalog
from llmware.library import Library
from llmware.retrieval import Query
from llmware.library import LLMWareConfig
from llmware.resources import CustomTable
from llmware.configs import LLMWareConfig, MilvusConfig
from llmware.parsers import WikiParser
from llmware.agents import LLMfx
from llmware.prompts import Prompt

# Set up the Streamlit app
st.title("AVA 1.0 - An Agentic RAG Artifact for LLM Investment Advice")

# Set up the OpenAI API key input
api_key = st.text_input("Enter your OpenAI API key", type='password')

if 'api_key' not in st.session_state:
    st.session_state['api_key'] = None

if api_key:
    st.session_state['api_key'] = api_key
    os.environ["USER_MANAGED_OPENAI_API_KEY"] = api_key  # Set the environment variable

# Check if the API key is set
if st.session_state['api_key'] is None:
    st.warning("Please enter your OpenAI API key to continue.")
    st.stop()

# Configuration
LLMWareConfig().set_active_db("sqlite")
MilvusConfig().set_config("lite", True)  # Enable Milvus Lite

# Check for yfinance installation
if not util.find_spec("yfinance"):
    st.error("The 'yfinance' package is required. Please install it using 'pip install yfinance'.")
    st.stop()

# Initialize conversation history
if 'messages' not in st.session_state:
    st.session_state['messages'] = []
    st.session_state['messages'].append({"role": "assistant", "content": "Hi, how can I help you today?"})

# Display conversation history
for message in st.session_state['messages']:
    if message['role'] == 'user':
        with st.chat_message("user"):
            st.markdown(message['content'])
    else:
        with st.chat_message("assistant"):
            st.markdown(message['content'])

# Input text box for the user
user_input = st.chat_input("Type your message...")

if user_input:
    # Add user message to conversation history
    st.session_state['messages'].append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Process the user input
    def process_user_input(user_input):
        # Load the GPT-4 model for evaluation purposes
        prompter_eval = Prompt().load_model("gpt-4", api_key=st.session_state['api_key'])

        # Mandate for GPT-4 (used to evaluate user input)
        evaluation_mandate = """
You are an analysis agent in a financial advisory pipeline. Your role is not to interact directly with clients. Instead, you evaluate user input and determine whether:
1. The input is casual conversation, rapport-building, or a general inquiry (e.g., greetings, small talk).
2. The input is a specific request for equity investment advice (focused on publicly listed companies).

Based on this evaluation, you must return a structured output in dictionary format:
- If the input is general conversation, return: {'investment_advice': ['N']}.
- If the input requests equity investment advice, return: {'investment_advice': ['Y']}.

Do not engage with the user. Simply evaluate the input and return the structured output as specified.

* Special condition: if you have already responded with {'investment_advice': ['Y']} once, respond with {'investment_advice': ['Delivered'].}
"""

        # Prepare input for GPT-4 using the evaluation mandate and user input
        evaluation_input = f"{evaluation_mandate}\n\nUser input: {user_input}"
        response = prompter_eval.prompt_main(evaluation_input)  # Get GPT-4's evaluation response

        # Extract and clean the structured report from GPT-4's response
        llm_response = re.sub("[\n\n]", "\n", response['llm_response'])
        st.write(f"**Evaluation Report:**\n{llm_response}")

        # If the evaluation result indicates a request for investment advice, generate a detailed report with state tracking
        if "'Y'" in llm_response:
            # Display a spinner while generating the report
            with st.spinner('Generating detailed report...'):
                research_summary = research_example_from_csv()
                st.write(research_summary)
                # Generate summarized context from research_summary
                prompter_conv = Prompt().load_model("gpt-3.5-turbo", api_key=st.session_state['api_key'])
                report_summary_text = summarize_report(research_summary, prompter_conv)
            # Now we can continue the conversation, passing report_summary_text
            assistant_response = conversation(user_input, report_summary=report_summary_text)
            return assistant_response
        else:
            # Continue interaction with Agent Zero via conversation
            assistant_response = conversation(user_input)
            return assistant_response

    # Define the conversation function
    def conversation(user_input, report_summary=None):
        # Load the GPT-3.5-Turbo model
        prompter = Prompt().load_model("gpt-3.5-turbo", api_key=st.session_state['api_key'])

        # Define the agent's mandate
        agent_0_mandate = """
You are Agent-0, a financial robo-advisor responsible for establishing rapport with the client. Your role in this RAG (Retrieval-Augmented Generation) pipeline is to interact with the client, understand their needs, and explain that you only provide equity investment advice for publicly listed companies.

Here are your specific responsibilities:
1. Establish rapport with the client by engaging in friendly, conversational interactions.
2. Inform the client that your expertise is limited to equity investment advice and publicly listed companies.
3. If the client inquires about other forms of investments such as cryptocurrency, real estate, bonds, or commodities, politely explain that you can only assist with equity investments.
4. Keep the conversation positive, encouraging, and continue to establish rapport while reminding the client of your area of expertise.
5. Remember that you are collaborating with other agents in the RAG pipeline, and they will read the client's responses to assist in providing the best insights.
6. If you have access to a research report, you should use it to provide insights to the client.
7. **If the client asks for elaboration or substantiation of the recommended assets, explain that the assets were selected based on a strong Piotroski F-score and provide relevant data from the research report.**

Please focus on rapport-building while maintaining professionalism and clarity about the types of investment advice you can offer.

Important Instructions:
- Do not include 'Client input:' or 'Agent-0:' in your response.
- Do not repeat the client's input back to them.
- Respond directly to the client in first person singular.
- Keep your response concise and relevant.
"""

        # If report_summary is available, include it in the mandate
        if report_summary is not None:
            agent_0_mandate += f"\nYou have access to the following research report summary:\n{report_summary}\nUse this information to assist the client."

        # Combine mandate as context and the user's input
        conversation_input = f"{agent_0_mandate}\nClient: {user_input}\n\nAgent-0:"

        # Display a spinner while the assistant is formulating a response
        with st.spinner('Formulating response...'):
            # Get the response from the model based on the combined input
            response = prompter.prompt_main(conversation_input)

        # Clean up the response
        llm_response = re.sub("[\n\n]", "\n", response['llm_response']).strip()
        st.session_state['messages'].append({"role": "assistant", "content": llm_response})
        with st.chat_message("assistant"):
            st.markdown(llm_response)
        return llm_response

    # Define the research function
    def research_example_from_csv(local_library_path="local_library"):
        """Processes a CSV of companies, retrieves financial data from Yahoo Finance."""

        # Point fp and fn at the file_path of the CSV file
        fp = "llmware/fast_start/rag_edited"  # Update with the actual CSV file path
        fn = "companies.csv"  # Update this to match your file name

        # First analyze the CSV and confirm that the rows and columns are consistently being extracted
        analysis = CustomTable().validate_csv(fp, fn, delimiter=',', encoding='utf-8-sig')

        st.write("\n**Analysis of the CSV file**")
        for key, value in analysis.items():
            st.write(f"**{key}**: {value}")

        table_name = "companies_table"

        # Use "postgres" | "mongo" | "sqlite"
        db_name = "sqlite"  # or another DB depending on your setup

        # Initialize the CustomTable object
        ct = CustomTable(db=db_name, table_name=table_name)

        # Load the CSV, which will identify the schema and data types, and package as 'rows' ready for DB insertion
        output = ct.load_csv(fp, fn)

        st.write("\n**Load CSV output**")
        for key, value in output.items():
            st.write(f"**{key}**: {value}")

        # Spot-check the rows that have been created before inserting into the database as a final check
        st.write("\n**Spot-Check Rows Before Inserting into DB Table**")
        sample_size = min(len(ct.rows), 10)
        for x in range(sample_size):
            st.write(f"Row {x}: {ct.rows[x]}")

        # Insert the rows into the database
        ct.insert_rows()

        # Retrieve companies data from the database
        companies = ct.rows  # Retrieve all rows from the database after insertion
        st.write("\n**Retrieved Companies Data from Database**")

        # Filter companies with f_score > 8
        filtered_companies = [row for row in companies if float(row.get('f_score', 0)) > 8]

        st.write("\n**Companies with F-Score above 8:**")
        st.write(filtered_companies)

        research_summary = {}

        for row in filtered_companies:
            company_name = row['name']
            ticker = row['ticker']
            f_score = row.get('f_score', 'N/A')
            research_summary[company_name] = {}
            research_summary[company_name]['f_score'] = f_score
            st.write(f"\n**Processing company: {company_name} (Ticker: {ticker})**\n")

            # Step 1: Use the stock ticker in web service lookup to YFinance
            ticker_core = ticker.split(":")[-1]

            # Display a spinner while fetching data from Yahoo Finance
            with st.spinner(f'Fetching data for {company_name}...'):
                yf = YFinance().get_stock_summary(ticker=ticker_core)
                st.write(f"**Yahoo Finance stock info for {company_name}:** {yf}")

                research_summary[company_name].update({
                    "current_stock_price": yf.get("currentPrice", "N/A"),
                    "high_ltm": yf.get("fiftyTwoWeekHigh", "N/A"),
                    "low_ltm": yf.get("fiftyTwoWeekLow", "N/A"),
                    "trailing_pe": yf.get("trailingPE", "N/A"),
                    "forward_pe": yf.get("forwardPE", "N/A"),
                    "volume": yf.get("volume", "N/A")
                })

                yf2 = YFinance().get_financial_summary(ticker=ticker_core)
                st.write(f"**Yahoo Finance financial info for {company_name}:** {yf2}")

                research_summary[company_name].update({
                    "market_cap": yf2.get("marketCap", "N/A"),
                    "price_to_sales": yf2.get("priceToSalesTrailing12Months", "N/A"),
                    "revenue_growth": yf2.get("revenueGrowth", "N/A"),
                    "ebitda": yf2.get("ebitda", "N/A"),
                    "gross_margin": yf2.get("grossMargins", "N/A"),
                    "currency": yf2.get("currency", "N/A")
                })

                yf3 = YFinance().get_company_summary(ticker=ticker_core)
                st.write(f"**Yahoo Finance company info for {company_name}:** {yf3}")

                research_summary[company_name].update({
                    "sector": yf3.get("sector", "N/A"),
                    "website": yf3.get("website", "N/A"),
                    "industry": yf3.get("industry", "N/A"),
                    "employees": yf3.get("fullTimeEmployees", "N/A")
                })

                execs = []
                if "companyOfficers" in yf3:
                    for entries in yf3["companyOfficers"]:
                        pay = entries.get("totalPay", "pay-NA")
                        age = entries.get("age", "age-NA")
                        execs.append((entries.get("name", "N/A"), entries.get("title", "N/A"), age, pay))
                research_summary[company_name].update({"officers": execs})

            # Commented out Wikipedia components
            # [Rest of your code remains the same]

        # Final output
        st.write("\n\n**Step 4 - Completed Research - Summary Output**\n")
        st.write("**Research summary:**")
        st.write(research_summary)

        item_counter = 1
        for company, details in research_summary.items():
            st.write(f"\n**Company: {company}**")
            for key, value in details.items():
                st.write(f"\t -- {item_counter} - {key.ljust(25)}: {str(value).ljust(40)}")
                item_counter += 1

        # Return research_summary
        return research_summary

    # Define the summarize_report function
    def summarize_report(research_summary, prompter):
        # Convert research_summary to text
        report_text = ""
        for company, details in research_summary.items():
            report_text += f"Company: {company}\n"
            for key, value in details.items():
                report_text += f"{key}: {value}\n"
            report_text += "\n"
        # Display a spinner while summarizing the report
        with st.spinner('Summarizing the report...'):
            summary_prompt = f"Please provide a concise summary of the following research report:\n\n{report_text}"
            response = prompter.prompt_main(summary_prompt)
            report_summary_text = response['llm_response']
        return report_summary_text.strip()

    # Process the user input
    process_user_input(user_input)
