# AVA 1.7: **Agentic RAG for Equity Investment Advisory**

**AVA 1.7** is an **open-source** advisory system that employs **multi-agent Retrieval-Augmented Generation (RAG)** to offer structured, context-enriched, and ethically informed **single-stock investment insights**. Developed around a **directed acyclic graph (DAG)** design, it integrates **live financial data** (via the Yahoo Finance API) with **specialized AI agents**, each with discrete mandates. This architecture is rooted in emerging Design Science principles (Peffers et al. 2007) and addresses critical challenges of LLM-driven finance, including **contextual limitations**, **risk misalignment**, and **hallucinations** (Lewis et al. 2020; Liu et al. 2024).

> **Disclaimer:** AVA 1.7 demonstrates a _hardcoded financial amalgamation score_ (via Piotroski’s F-score **as an example only**). This score can be substituted with any other valuation or scoring framework—such as GuruFocus metrics or a custom fundamental analysis method. AVA 1.7 does **not** endorse Piotroski F-score as inherently superior and remains **agnostic** to the choice of scoring methodology.

---

## 1. Research Motivation & Objectives

The financial sector’s embrace of **generative AI** has exposed limitations in traditional, mono-agent LLMs, particularly in high-stakes contexts where external knowledge and real-time data are critical (Lo and Ross 2024). Drawing on the concerns about “lost in the middle” context gaps (Liu et al. 2024) and the documented shortcomings of static AI advisory tools (Fisch et al. 2019), AVA 1.7 adopts a **multi-agent RAG** pipeline to:

1. Distribute financial advisory tasks—such as risk profiling and data retrieval—across specialized AI agents.
2. Substantiate recommendations through **structured retrieval** of external data (e.g., yFinance).
3. Embed disclaimers and ethical safeguards into a chain-of-responsibility workflow, promoting transparency and mitigating hallucinations.
4. Provide **modular scoring** capabilities (illustrated by Piotroski’s score) that can be seamlessly replaced with alternative metrics.

This approach reflects a **Design Science Research** ethos (Peffers et al. 2007), aiming to deliver an artefact that is both theoretically rigorous and practically adaptable.

### **Key Innovations**

- **Multi-Agent RAG:** Segments LLM tasks across agents to diminish cognitive overload (Göldi & Rietsche 2024) and reduce factual inconsistencies.
- **DAG-Based Architecture** (🧩): Structures agents in a linear flow with no cyclical paths, enhancing scalability and **explainability**.
- **Live Financial Data Integration:** Uses **yFinance** to ground real-time insights in verifiable market conditions.
- **Flexible Valuation Models:** Illustrates how a _hardcoded F-score_ can be replaced with **any** alternative scoring technique (traditional or proprietary).

---

## 2. Architecture Overview

### **Multi-Agent System & DAG Structure**

**AVA 1.7** comprises four principal agents, each governed by text-based “mandates,” ensuring modularity, transparency, and risk-aware recommendations:

1. **Agent Zero** (User Interaction & Context Manager)

   - Captures user prompts and domain-specific needs.
   - Crafts preliminary instructions for subsequent agents in the DAG.

2. **Agent One** (Classification & Categorization)

   - Organizes inputs into structured categories (e.g., _portfolio insights_, _single-stock screening_, _risk assessment_).
   - Delegates tasks to the appropriate downstream agent.

3. **Agent Two** (Risk Profiling)

   - Generates a JSON-formatted risk profile, e.g. `{ "risk_ability": "medium", ... }`.
   - Aligns final recommendations with the user’s capacity and willingness to bear risk.

4. **Agent Summarizer**
   - Compacts conversation and analysis logs to conserve LLM context window.
   - Preserves essential details for subsequent queries and disclaimers.

**Chain of Responsibility** and **DAG** principles ensure each agent focuses on specialized tasks, thereby mitigating single-agent overload and “lost context” issues (Liu et al. 2024).

---

## 3. Key Features

1. **Multi-Agent RAG Workflow**

   - **Task Decomposition:** Agents manage discrete parts of the advisory pipeline.
   - **Explainability:** Traces each recommendation to agent-level data retrieval and risk classification.

2. **Real-Time Market Integration** (🔎)

   - **yFinance** integration for updated quotes, historical prices, and fundamentals.
   - Automates the retrieval and parsing of key financial metrics to ground AI in current data.

3. **Amalgamation Scores & Flexibility**

   - **Piotroski F-score** is showcased as a _hardcoded example._
   - Users can easily substitute alternative metrics (e.g., GuruFocus score, ratio-based valuation, or custom fundamentals).

4. **Ethically Informed Advisory**
   - **Disclaimers** integrated at each step, cautioning users that final decisions rest with human investors.
   - Risk-profiling logic ensures alignment with user’s declared preferences and tolerance.

---

## 4. Dependencies

- **Python 3.7+**
- **Streamlit** (UI)
- **Pandas** (data manipulation)
- **YFinance** (real-time market data)
- **LLMWare** (prompt management & integration with OpenAI/Anthropic APIs)
- **OpenAI/Anthropic** (LLM endpoints; optional cloud-based or self-hosted models)

---

## 5. Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone https://github.com/<your-username>/ava-1.7.git
   cd ava-1.7
   ```
2. **Create & Activate Virtual Environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # (Windows: venv\Scripts\activate)
   ```
3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```
4. **Run the Streamlit Application**
   ```bash
   streamlit run main.py
   ```

---

## 6. Usage Instructions

1. **Start the App**
   - Launch via `streamlit run main.py`.
2. **Provide API Keys**
   - Input relevant OpenAI/Anthropic keys or local model configurations.
3. **Select Models for Each Agent**
   - Customize the LLM choice for Agents Zero, One, Two, and Summarizer.
4. **Interact with AVA 1.7**
   - Pose investment-related queries and observe the multi-agent synergy in real-time.
5. **Retrieve Risk Profile**
   - Download the JSON-based risk report for subsequent analysis or compliance needs.

---

## 7. Customization & Scalability

- **Extend Agents:** Add new specialized agents by deriving from `AgentBase` (in `agents/`), then define mandates in the `prompts/` folder.
- **Adapt Valuation Logic:** Update or replace the Piotroski-based demonstration in `config.py` to incorporate your preferred financial scoring frameworks.
- **Scale to Production:** Container-friendly and amenable to CI/CD; designed to scale horizontally should the number of agents or data retrieval endpoints expand.

---

## 8. Limitations

- **Equity Focus**: Presently optimized for single-stock analysis; expansions for ETFs or bonds are in progress.
- **Context Boundaries**: Some LLMs have limited context windows, which may constrain deep historical analysis.
- **Data Latency & Reliability**: Real-time feeds depend on external APIs; data inaccuracies or downtime can affect results.

---

## 9. Ethical Considerations (⚖️)

- **Not Official Financial Advice**: All outputs serve as informational prompts, underscored by disclaimers in the user flow.
- **User Privacy**: Minimal data storage; no sensitive personal details are retained.
- **Transparency & Accountability**: Each chain-of-responsibility output is explained, emphasizing that **human oversight** is indispensable in final decision-making.

---

## 10. Future Roadmap

- **Portfolio-Level Insights**: Transition from single-equity analysis to multi-asset recommendations.
- **Enhanced Summarization Agents**: Improve efficiency for extended dialogues, addressing context-truncation hazards (Liu et al. 2024).
- **Multi-Metric Valuation Support**: Broaden _Piotroski only_ demonstration to seamlessly integrate any fundamental or technical scoring method.
- **Regulatory & Compliance Features**: Integrate advanced KYC modules and ethical safeguards consistent with emerging guidelines (Caton & Haas 2024).

---

## 11. References

- **Peffers, K. et al. (2007)**. _A Design Science Research Methodology for Information Systems Research._
- **Lewis, P. et al. (2020)**. _Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks._
- **Liu, N. F. et al. (2024)**. _Lost in the Middle: How Language Models Use Long Contexts._
- **Lo, A. W. & Ross, J. (2024)**. _Generative AI & Investment Advisory: Bridging Theory and Practice._
- **Göldi, A. & Rietsche, R. (2024)**. _Making Sense of Large Language Model-Based AI Agents._

_(Full bibliographic details available in the research manuscript.)_

---

### **License**

Released under the **MIT License**, allowing free use, modification, and distribution.

### **Contact & Contributions**

Contributions are warmly encouraged! Please submit a pull request or open an issue on GitHub to propose improvements, share ideas, or report bugs.

---

**© 2025 AVA 1.7** – _Empowering research-based, ethically aligned, and modular AI-driven investment advisory._
