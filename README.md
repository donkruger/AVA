
📊 **AVA 1.0: An Agentic RAG Artifact for LLM Investment Advice** 🤖💰

---

## 📝 Introduction

**AVA 1.0** is an interactive financial advisory app designed to provide equity investment advice using Large Language Models (LLMs). It leverages an **agent-based architecture** within a **Retrieval-Augmented Generation (RAG)** pipeline to deliver personalized investment recommendations and risk assessments. 🤝💼

The app orchestrates multiple agents to simulate conversations with clients, assess their inputs, generate risk profiles, and retrieve financial data for well-informed decisions.

---

## 🏛️ **Architecture Overview**

The app uses a **multi-agent framework** consisting of three key agents:

- **Agent-0 (Conversation Agent)**: 🤵 Interacts directly with the user, gathers necessary info, and provides investment advice.
- **Agent-1 (Evaluation Agent)**: 📊 Analyzes inputs to categorize them as inquiries, risk profiles, or investment advice requests.
- **Agent-2 (Risk Profiling Agent)**: 📝 Generates a structured risk profile report based on the conversation history with Agent-0.

Together, they ensure tailored, accurate, and aligned advice to meet your risk tolerance and goals. 🎯

---

## 🔑 **Key Features**

- **Agent-Based Interaction**: 🧑‍💻 Simulates a multi-agent environment where each agent has a specific task, making the advice more robust.
- **Retrieval-Augmented Generation (RAG)**: 📈 Integrates real-time data sources like Yahoo Finance for accurate, up-to-date advice.
- **Risk Profiling**: 📉 Generates personalized risk profiles to offer advice based on the user’s tolerance and financial situation.
- **User-Friendly Interface**: 🖥️ Built with Streamlit, offering an intuitive user experience.

---

## 🛠️ **Dependencies**

- Python 3.7+
- Streamlit
- Pandas
- YFinance
- LLMWare Library
- OpenAI API

---

## 🏗️ **Setup Instructions**

### Clone the Repository

```bash
git clone https://github.com/yourusername/ava-1.0.git
cd ava-1.0
```

### Create a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scriptsctivate`
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Set Up OpenAI API Key 🔑

Obtain an API key from OpenAI. You’ll be prompted to enter it when running the app.

---

## 🚀 **Run the Application**

```bash
streamlit run app.py
```

---

## 💡 **Usage Instructions**

1. **Launch the App**: Running the command will open the app in a new browser window.
2. **Enter API Key**: Input your OpenAI API key in the provided field.
3. **Select Models for Agents**: Choose models (e.g., GPT-4, GPT-3.5) for each agent from dropdowns.
4. **Start the Conversation**: Type your messages in the chat input box. Agent-0 will guide you through your investment needs.
5. **Receive Advice**: Request investment advice, and the app will provide recommendations based on Piotroski F-score analysis. 📊
6. **View Risk Profile**: Agent-2 generates a risk profile report, viewable in-app.

---

## ⚙️ **Underlying Methods**

### **Agentic Architecture** 🤖
Each agent has a distinct role:
- **Agent-0**: User interaction & rapport-building.
- **Agent-1**: Input evaluation & routing.
- **Agent-2**: Risk profile generation.

### **Retrieval-Augmented Generation (RAG)** 🔄
- **Data Retrieval**: Yahoo Finance provides real-time financial data using the `yfinance` library.
- **Data Integration**: The data is merged with the LLM’s responses to give current investment advice.

### **Financial Data Processing**
- **CSV Processing**: Handles a CSV file with company info and Piotroski F-scores.
- **Database Integration**: Uses SQLite for efficient data access.

---

## 📂 **Code Structure**
- `app.py`: Main app script (Streamlit interface & agent logic).
- `requirements.txt`: Python dependencies.
- `companies.csv`: CSV file with company data and Piotroski F-scores.

---

## ⚒️ **Customization**
- **Model Selection**: Tailor the models used for each agent to improve performance.
- **Data Sources**: Swap out Yahoo Finance for another data provider if needed.

---

## 🚧 **Limitations**
- **LLM Dependency**: Quality depends on the language model selected.
- **Data Currency**: There may be delays or inaccuracies in the data retrieved.
- **Scope**: Currently limited to publicly listed equity investments.

---

## ⚖️ **Ethical Considerations**
- **Financial Responsibility**: Advice is for informational purposes only—please consult a professional for financial decisions.
- **User Data**: Be cautious about sharing sensitive financial info.

---

## 🛠️ **Future Work**
- **Enhanced Risk Profiling**: Incorporate advanced risk models.
- **Expanded Investment Options**: Add support for bonds, ETFs, mutual funds.
- **Regulatory Compliance**: Ensure features comply with financial regulations.

---

## 🎓 **Conclusion**
**AVA 1.0** highlights how agent-based systems and RAG pipelines can personalize investment advice using LLMs. It sets the stage for further exploration into AI-driven financial advisory services in both academic and professional realms.

---

## 🔍 **References**
- **Retrieval-Augmented Generation**: Lewis, P. et al. (2020). *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks.*
- **Piotroski F-Score**: Piotroski, J.D. (2000). *Value Investing: The Use of Historical Financial Statement Information to Separate Winners from Losers.*

