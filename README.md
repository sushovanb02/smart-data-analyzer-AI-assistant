# Smart Data Analyzer AI Assistant

An AI-powered platform that ingests CSV datasets, performs automated exploratory data analysis, applies machine learning models, and provides interactive, human-readable insights through a chat-based interface.

---

## Overview

Smart Data Analyzer is an end-to-end system that enables users to upload datasets, analyze them automatically, generate machine learning predictions, and interact with the data using natural language queries. The project combines machine learning, large language models, backend APIs, and a user-friendly interface.

---

## Features

- Automated exploratory data analysis (EDA)
- Machine learning model training and prediction
- Natural language query interface (chat-based interaction)
- LLM-based explanation of model outputs
- Missing value and statistical analysis
- Real-time API-driven processing
- Containerized deployment using Docker

---

## Installation and Setup

### Run with Docker

```bash
git clone https://github.com/your-username/smart-data-analyzer-AI-assistant.git
cd smart-data-analyzer
docker compose up --build
```
### Run Locally

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
streamlit run ui/frontend.py
```

---

## How It Works
- User uploads a CSV file
- Backend processes the dataset:
  - Data cleaning
  - Feature extraction
  - Statistical analysis
- Machine learning models generate predictions
- LLM generates explanations of results
- User interacts with the dataset through chat queries

