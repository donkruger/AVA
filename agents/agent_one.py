'''
🌐 AgentOne Class - Evaluation Agent for Interactive Financial Advisory App
--------------------------------------------------------------------------
Technical Overview:
AgentOne operates as an evaluation agent within the advisory app's agentic pipeline. This agent’s role 
is to assess user input and classify it based on predefined rules (mandates) stored in an external text file. 
This agent triggers pipeline events. AgentOne retrieves its mandate, which defines specific evaluation criteria, and uses it to contextualize 
the user’s input. By constructing a prompt with the mandate and user input, AgentOne generates a 
structured response via the LLM. This response is designed to streamline decision-making in the 
pipeline by categorizing inputs, enabling other agents to perform targeted tasks based on these 
classifications.

In Simple Terms:
AgentOne is a background agent that evaluates what the user says, helping the system understand and 
categorize the user's input. It combines a set of evaluation rules with the user’s words and uses these 
rules to get a structured response from the model. This makes it easier for the app to handle different 
types of requests and respond accurately.

Attributes:
- Inherits all attributes from AgentBase, including model_name, api_key, and prompter.

Methods:
- get_mandate: Retrieves the agent’s evaluation criteria from a text file, outlining how user input should 
  be interpreted.
- evaluate_input: Combines the mandate and user input, then prompts the model to generate an evaluation, 
  which classifies and refines the input for further processing by other agents.
'''

# agents/agent_one.py

from .agent_base import AgentBase
import os

class AgentOne(AgentBase):
    def get_mandate(self):
        with open(os.path.join('prompts', 'agent_one_mandate.txt'), 'r') as f:
            return f.read()

    def evaluate_input(self, user_input, conversation_summary=None):
        evaluation_mandate = self.get_mandate()

        # Include conversation summary if provided
        if conversation_summary is not None:
            evaluation_mandate += f"\n\nHere is a summary of the conversation history:\n{conversation_summary}"

        evaluation_input = f"{evaluation_mandate}\n\nUser input: {user_input}"
        response = self.prompter.prompt_main(evaluation_input)
        llm_response = response['llm_response'].strip()
        return llm_response

