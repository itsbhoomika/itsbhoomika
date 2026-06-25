<h1 align="center">BHOOMIKA RAVISHANKAR</h1>

<p align="center">
	<b>Data / Product Analyst · Data Scientist</b><br>
	Experimentation & causal inference · NPS / customer analytics · LLMs & applied ML · BI (Tableau, Power BI, SQL)
</p>

Hi! I'm a data scientist and analyst who turns messy data into decisions leadership actually acts on. I build NPS driver models, causally validated insights, A/B-test-ready experimentation, and BI dashboards that move product and operational outcomes — backed by a strong statistical foundation and production data experience at Synchrony Financial.

I'm completing my **MS in Information Management at the University of Illinois Urbana-Champaign** (4.0 GPA, Phi Kappa Phi). My interests sit at the intersection of **causal inference, customer/product analytics, and large language models**, from modeling survey drivers to building LLM pipelines that turn unstructured text into predictive features. I care as much about whether a model is *useful and understandable* as whether it's accurate.

---
[📄 RESUME](data/resume/Bhoomika_Ravishankar_Resume.pdf)
---

## 📚 Table of Contents
- [Research Experience](#-research-experience)
- [Projects](#-projects)
- [Professional Experience](#-professional-experience)
- [Research Reports & Writing](#-research-reports--writing)
- [Contact](#-contact)

---
## 🔬 Research Experience

### [Facet Generation for Question Disambiguation — Clarification-Seeking LLMs](data/Research/Clarification-Seeking-LLMs/README.md)

Research on systems where LLMs identify ambiguity in questions and generate high-quality **facets** that explain disambiguation QA pairs. Built a three-stage pipeline — data preparation with backwards filtering, supervised fine-tuning, and **Direct Preference Optimization (DPO)** — using **Qwen 2.5 7B** for facet generation and **Gemini** as an evaluation judge, scored across six quality metrics. *(CS546, UIUC)*

### [Predictive Modeling for Clinical Trials with an LLM Feedback Loop](data/Research/LLM-Healthcare-ClinicalTrials/README.md)

Research at the **UIUC Statistics Department** on whether LLMs can automatically extract structured attributes from clinical-trial narratives and convert them into predictive features. Built an end-to-end pipeline over **115K+ ClinicalTrials.gov cancer studies**, predicting trial completion vs. termination; LLM-derived features accounted for **97.2% of feature importance** in a Lasso logistic benchmark, with iterative prompt refinement guided by model feedback.

---
## 🛠️ Projects

### [Real-Time Data Quality & Monitoring Pipeline](data/Projects/Real-Time-Data-Quality-Monitoring/README.md)

Real-time data engineering pipeline using **Apache Kafka, Snowflake, dbt, and Streamlit** to ingest application events, validate schemas, and monitor ingestion-to-warehouse latency. Implemented **dbt tests**, anomaly detection rules, and monitoring dashboards to flag **schema drift, data quality failures, and pipeline delays** in real time.

### [AI-Driven M&A Prediction](data/Projects/AI-MA-Prediction/README.md)

Predictive analytics system combining **14 structured financial ratios** with **298K+ unstructured market-news headlines** (TF-IDF, Word2Vec, FinBERT sentiment) and an **XGBoost** classifier — reaching **~89–93% accuracy** and **2.4× F1**, demonstrating an investment-banking-style decision use case.

### [LSTM Credit Spend Forecasting — UIUC × Synchrony Datathon](data/Projects/LSTM-Credit-Forecasting/README.md)

Sequence model (**LSTM**) forecasting **Q4 2025 spend across 14,099 accounts** at **~$2,444 MAE**, translating forecasts into credit-line recommendations for **288 high-value accounts** (~2% of the segment).

### [Contract Pricing Intelligence](data/Projects/Contract-Pricing-Intelligence/README.md)

A **Django + DRF** application that parses raw contract text into structured pricing fields, exposes full CRUD workflows and a REST API, runs contract-level analytics (total value, recurring revenue, discounts), and integrates **AWS S3** for document storage.

### [ClearLedger — SQL Personal Finance Management System](data/Projects/ClearLedger-Finance-DB/README.md)

A normalized **MySQL** database for personal finance: accounts, transactions, budgets, and savings goals — delivering **7 analytical reports** (budget-vs-actual variance, net-worth, spending trends) and **11 CRUD operations**, cutting manual monthly reporting from **~4 hrs to under 30 seconds**.

---
## 💼 Professional Experience

### Synchrony Financial — *Data Scientist, Customer Analytics & Credit Risk* (May 2025 – May 2026)

Replaced an external consultancy's **NPS model** with an internally built solution whose findings were **adopted by customer-analytics leadership to redesign survey structure**. Modeled NPS drivers with **XGBoost** and **Lasso** in parallel (imputing 100K+ missing values), validated causal robustness via **Placebo Refutation Testing**, and migrated legacy SAS/SQL to Python (**100M+ records, 87% faster**). In Credit Risk, built **PD/EAD models** across 6 portfolios informing a **$7.49B CECL loss reserve**, with **PySpark ETL on 900M+ records** (92% faster).

### Business Intelligence Group (BIG) — *Data Consultant* (Jan 2025 – May 2025)

Designed an NLP decision-support system (**RAG chatbot + topic modeling**) with **Power BI dashboards** automating resource allocation and overtime planning — a **90% reduction in pilot lookup time**.

### University of Illinois Urbana-Champaign — *Research Assistant, AI Engineer* (Jan 2025 – May 2026)

Built an LLM pipeline structuring **100,000 clinical-trial studies** into analytical features and benchmarked predictors with Lasso logistic regression and feature-importance analysis.

### Repute India Pvt. Ltd. — *Data Analyst* (Feb 2023 – Apr 2023)

Automated financial & operational **KPI dashboards** (SQL Server, Excel), cutting reporting cycle time **30%**, and surfaced **~30% cost inefficiencies** through reconciliations across cost, production, and financial data.

---
## 📄 Research Reports & Writing

### [Facet Generation for Question Disambiguation — Final Report](data/Research/Clarification-Seeking-LLMs/CS546_Final_Report-Bhoomika-2%20(1).pdf)
CS546 research report on improving facet generation in question-disambiguation systems with LLMs.

### [Predictive Modeling for Text-Rich Data Using an LLM Feedback Loop](data/Research/LLM-Healthcare-ClinicalTrials/Predictive%20Modeling-Bhoomika-Ravishankar.pdf)
Write-up of the clinical-trials LLM feature-extraction and predictive-modeling pipeline (UIUC Statistics Dept).

---
## 📞 Contact
I'd love to hear from you — feel free to reach out for questions or collaboration opportunities.

- **Email**: [itsbhoomika.r@gmail.com](mailto:itsbhoomika.r@gmail.com)
- **LinkedIn**: [Bhoomika Ravishankar](https://www.linkedin.com/in/bhoomikaravishankar)
- **GitHub**: [itsbhoomika](https://github.com/itsbhoomika)
- **Portfolio**: [itsbhoomika.github.io](https://itsbhoomika.github.io)

---
