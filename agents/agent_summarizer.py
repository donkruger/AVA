# agents/agent_summarizer.py

'''
📝 AgentSummarizer Class - Summarization Agent for Conversation History and Reports
----------------------------------------------------------------------------------
Problem: LLMs APIs are stateless. They have only memory of the last sent message. 
Solution: Create summarised conversation trail. 

Technical Overview:
AgentSummarizer is responsible for summarizing the conversation history and reports to maintain context within the token limits of the LLM. It inherits from AgentBase and uses the loaded model to generate concise summaries.

In Simple Terms:
AgentSummarizer is like a smart note-taker that condenses past conversations and reports into brief summaries. This helps AgentZero stay informed about the previous context without exceeding token limits.

Methods:
- summarize_conversation: Summarizes the conversation history up to a specified number of messages.
- summarize_reports: Summarizes past reports up to a specified number.
'''

from .agent_base import AgentBase

class AgentSummarizer(AgentBase):
    def get_mandate(self):
        # Define a simple mandate for summarization
        return "You are a helpful assistant that summarizes conversation history and reports concisely."

    def summarize_conversation(self, conversation_history, num_messages=3):
        # Get the last num_messages from the conversation history
        recent_messages = conversation_history[-num_messages*2:]  # Considering user and assistant messages

        # Prepare the text to summarize
        conversation_text = ""
        for message in recent_messages:
            role = message['role']
            content = message['content']
            conversation_text += f"{role.capitalize()}: {content}\n"

        # Prepare the prompt for summarization
        prompt = f"{self.get_mandate()}\n\nPlease provide a concise summary of the following conversation:\n\n{conversation_text}"

        # Get the summary from the model
        response = self.prompter.prompt_main(prompt)
        summary = response['llm_response'].strip()
        return summary

    def summarize_reports(self, reports, num_reports=3):
        # Get the last num_reports
        recent_reports = reports[-num_reports:]

        # Combine the reports into one text
        reports_text = "\n\n".join(recent_reports)

        # Prepare the prompt for summarization
        prompt = f"{self.get_mandate()}\n\nPlease provide a concise summary of the following reports:\n\n{reports_text}"

        # Get the summary from the model
        response = self.prompter.prompt_main(prompt)
        summary = response['llm_response'].strip()
        return summary
