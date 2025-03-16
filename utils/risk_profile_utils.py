"""
RiskProfileManager – Generates and parses user-specific risk profiles using AgentTwo.

This class requests a risk profile from AgentTwo based on conversation history and 
parses the response into a usable dictionary. This helps tailor investment advice 
to each user's risk tolerance.
"""

import re
import streamlit as st
import json

class RiskProfileManager:
    def generate_risk_profile(self, conversation_history, agent_two):
        """
        Generates a risk profile JSON string from the conversation history using AgentTwo.
        """
        return agent_two.generate_risk_profile(conversation_history)

    def parse_risk_profile_report(self, raw_report: str) -> dict:
        """
        Parses the raw JSON string returned by AgentTwo into a Python dictionary by:
          1. Removing code fences (```...```).
          2. Extracting content from the first '{' to the last '}'.
          3. Using json.loads on that substring.

        Returns an empty dictionary if parsing fails.
        """
        # Remove triple-backtick fences and any extra whitespace
        cleaned = re.sub(r"```[^\n]*\n?", "", raw_report).replace("```", "").strip()

        # Extract JSON between the first '{' and the last '}'
        match = re.search(r"(\{[\s\S]*\})", cleaned)
        if not match:
            st.warning("No JSON object found in AgentTwo's response.")
            return {}

        json_str = match.group(1)

        # Deserialize the substring into a Python dictionary
        try:
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            st.warning(f"Failed to parse risk profile JSON: {e}")
            return {}
