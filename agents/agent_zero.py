'''
🌐 AgentZero Class - Interface Agent for Interactive Financial Advisory App
--------------------------------------------------------------------------
Technical Overview:
AgentZero serves as the primary interface agent within the advisory app's agentic pipeline. It is the main 
agent with which clients interact, gathering user inputs and contextualizing data from downstream agents 
(such as summary reports and risk profiles). This agent’s role is pivotal in managing the conversation 
flow, integrating information from other agents, and delivering responses that feel coherent and tailored 
to the client’s needs. As AgentZero processes information from multiple agents, it’s essential to manage 
the amount of data passed through to avoid generating hallucinations. The architecture considers this 
potential limitation by defining a boundary on how many downstream agents can inform AgentZero’s 
responses, ensuring clarity and accuracy in interactions.

In Simple Terms:
AgentZero is the client-facing agent that interacts directly with users. It combines information from 
other agents, like risk profiles and research summaries, with user input to provide meaningful, informed 
responses. This setup ensures that AgentZero can be easily updated without overloading the conversation 
with unnecessary data, maintaining accurate and relevant advice.

Attributes:
- Inherits all attributes from AgentBase, including model_name, api_key, and prompter.

Methods:
- get_mandate: Retrieves the agent’s mandate from a text file, defining rules for user interactions.
- generate_response: Prepares and sends a conversation prompt to the model, incorporating the mandate, 
  user input, and optional data (e.g., report summaries) to produce a well-rounded, personalized response.
'''

# agents/agent_zero.py

from .agent_base import AgentBase
import os

class AgentZero(AgentBase):
    def get_mandate(self):
        with open(os.path.join('prompts', 'agent_zero_mandate.txt'), 'r') as f:
            return f.read()

    def generate_response(self, user_input, conversation_summary=None, reports_summary=None, risk_profile_report=None, fundamentals_report=None, price_chart_note=None, radar_chart_note=None):
        agent_zero_mandate = self.get_mandate()

        # Include conversation summary if available
        if conversation_summary is not None:
            agent_zero_mandate += f"\nHere is a summary of your recent conversation:\n{conversation_summary}"

        # Include reports summary if available
        if reports_summary is not None:
            agent_zero_mandate += f"\nHere is a summary of recent reports:\n{reports_summary}"

        # Include other reports as before
        if risk_profile_report is not None:
            agent_zero_mandate += f"\nYou have access to the following risk profile report:\n{risk_profile_report}\nUse this information to assist the client."

        if fundamentals_report is not None:
            agent_zero_mandate += f"\nYou have access to the following fundamentals report:\n{fundamentals_report}\nUse this information to assist the client."

        if price_chart_note is not None:
            agent_zero_mandate += f"\nYou have generated a price chart for the client. {price_chart_note}."

        if radar_chart_note is not None:
            agent_zero_mandate += f"\nYou have generated a radar chart for the client. {radar_chart_note}."


        # Prepare conversation input
        conversation_input = f"{agent_zero_mandate}\nClient: {user_input}\n\nAgent Zero:"

        # Get the response from the model
        response = self.prompter.prompt_main(conversation_input)
        llm_response = response['llm_response'].strip()
        return llm_response
