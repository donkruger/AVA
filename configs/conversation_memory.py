# configs/conversation_memory.py

"""
📁 ConversationMemoryConfig Class - Configuration for Conversation Memory
-------------------------------------------------------------------------
Technical Overview:
This configuration file allows you to set the number of messages and reports to retain in the conversation for summarization purposes. Adjusting these values helps manage the context provided to agents while keeping within token limits.

In Simple Terms:
You can use this file to set how many past messages and reports you want to include when summarizing the conversation. This helps control how much context is given to the agents.

Attributes:
- num_messages: Number of past messages to include in the conversation summary.
- num_reports: Number of past reports to include in the reports summary.

Methods:
- None; this is a simple configuration class.

Usage:
- Adjust the `num_messages` and `num_reports` attributes as needed.
"""

class ConversationMemoryConfig:
    def __init__(self):
        # Set default values; you can adjust these as needed
        self.num_messages = 3
        self.num_reports = 3

    def set_num_messages(self, num_messages):
        self.num_messages = num_messages

    def set_num_reports(self, num_reports):
        self.num_reports = num_reports
