# AVA 1.7: **Agentic RAG for Equity Investment Advisory**

**AVA 1.7** is an **open-source** application that brings agentic intelligence to **equity investment advisory**. By leveraging **multiple LLMs** and real-time data retrieval (e.g., Yahoo Finance), it delivers **dynamic**, up-to-date stock insights. The system employs **design patterns** like **Chain of Responsibility**, **Factory Method**, **Strategy**, and **Singleton** to ensure **modularity**, **scalability**, and **maintainability**.

## Table of Contents

1. [Introduction](#introduction)
2. [Architecture Overview](#architecture-overview)
3. [Key Features](#key-features)
4. [Dependencies](#dependencies)
5. [Setup Instructions](#setup-instructions)
6. [Usage Instructions](#usage-instructions)
7. [Agent Flows](#agent-flows)
8. [Adding a New Static Pipeline Event](#adding-a-new-static-pipeline-event)
9. [Customization](#customization)
10. [Limitations](#limitations)
11. [Ethical Considerations](#ethical-considerations)
12. [Future Work](#future-work)
13. [References](#references)

---

## 1. Introduction

**AVA 1.7** focuses on **equity investment advisory** by using a **Retrieval-Augmented Generation (RAG)** pipeline and an **agent-based** architecture. Through real-time data retrieval and structured conversation management, it provides **Piotroski F-score-based** recommendations, personalized risk profiles, price charts, fundamentals, comparative radar charts, and more.

---

## 2. Architecture Overview

The system is designed around **four** primary agents, each with a **single responsibility**:

1. **Agent Zero (Conversation Agent)**

   - The main user-facing agent. Gathers user input, provides rapport, and integrates downstream data into final responses.

2. **Agent One (Evaluation Agent)**

   - Evaluates and classifies user requests into structured categories (e.g., investment advice, risk profile, fundamentals).

3. **Agent Two (Risk Profiling Agent)**

   - Generates a **JSON**-formatted risk profile report (e.g., `{"risk_ability": "high", ...}`) by analyzing conversation history.

4. **Agent Summarizer**
   - Condenses the conversation and report history to keep context relevant without exceeding LLM token limits.

All agents communicate through a **Chain of Responsibility** pattern, ensuring each agent focuses on its own mandate.

---

## 3. Key Features

1. **Multi-Agent Flow**

   - Each agent (Zero, One, Two, Summarizer) handles a unique part of the conversation or data processing.

2. **Retrieval-Augmented Generation (RAG)**

   - Integrates real-time data (Yahoo Finance) into LLM responses for **accurate** equity insights.

3. **Structured Risk Profiling**

   - Agent Two returns a strict JSON object for risk tolerance/willingness, with logic to parse it safely.

4. **Agent Summarizer**

   - Dynamically shortens conversation context and prior reports to keep tokens within bounds.

5. **Chain of Responsibility**

   - Orchestrates calls among agents in a **linear** yet **modular** pipeline, letting you easily add new steps.

6. **User-Friendly**
   - Built on Streamlit for an intuitive UI. Prompts for API keys at runtime, offers model dropdowns, and supports easy **risk profile** downloads.

---

## 4. Dependencies

- **Python 3.7+**
- **Streamlit** for UI
- **Pandas** for CSV handling
- **YFinance** for real-time stock data
- **LLMWare Library** (handles LLM prompt management)
- **OpenAI** or **Anthropic** API Key

---

## 5. Setup Instructions

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/ava-1.7.git
   cd ava-1.7
   ```

2. **Create a Virtual Environment**

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   # Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure API Key**

   - Obtain an OpenAI or Anthropic key and keep it ready. The app prompts you at runtime.

5. **Run the Application**
   ```bash
   streamlit run main.py
   ```

---

## 6. Usage Instructions

1. **Launch the App**
   - Running `streamlit run main.py` opens the UI in your browser.
2. **Enter Your API Key**
   - When prompted, provide the key for your selected model (e.g., GPT-4).
3. **Select Agent Models**
   - Configure which model is used for Agent Zero, One, and Two, plus the summarizer, via dropdowns.
4. **Interact**
   - Type in the chat. **Agent Zero** responds with equity investment advice or data from other agents.
5. **Risk Profile**
   - If you answer risk-related questions, **Agent Two** returns a structured JSON risk profile.
   - Download your risk profile using the **“Download”** button once generated.
6. **Charting & Fundamentals**
   - Ask about a stock’s price or fundamentals to see real-time data from yfinance.

---

## 7. Customization

- **Add New Agents**: Subclass `AgentBase` in `agents/`, create a new mandate in `prompts/`, then integrate in `main.py`.
- **Edit Mandates**: The `.txt` prompt files define each agent’s instructions (very easy to tweak).
- **Adjust Pipeline**: The `main.py` user input processing flow can be modified to skip or reorder agent calls.

---

## 8. Limitations

- **LLM-Dependent**: Responses are bound by the chosen LLM’s reliability and knowledge cutoffs.
- **Equity-Focused**: Currently specialized in **publicly listed stocks**—other asset classes (e.g., bonds, crypto) are not covered.
- **Data Delays**: Real-time market data from Yahoo Finance may have slight latency or partial data.

---

## 9. Ethical Considerations

- **Informational Purposes Only**: AVA 1.7’s recommendations are **not** financial advice—always consult a qualified professional.
- **User Privacy**: Be mindful when sharing sensitive investment info via the chat.

---

## 10. Future Work

- **Enhanced Summaries**: Expand the Summarizer to handle multiple conversation segments and advanced compression.
- **Automated KYC**: Integrate optional compliance checks.
- **Multi-Asset Support**: Extend beyond equities to cover ETFs, bonds, or mutual funds.
- **Fine-Tuned LLM**: Incorporate domain-specific LLM models for more accurate analysis.

---

## 11. References

- **Gamma, E. et al. (1994)**. _Design Patterns: Elements of Reusable Object-Oriented Software._
- **Lewis, P. et al. (2020)**. _Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks._
- **Piotroski, J.D. (2000)**. _Value Investing: The Use of Historical Financial Statement Information to Separate Winners from Losers._
