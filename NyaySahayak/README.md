# NyaaSahayak - Multilingual Legal Document Assistant

## 🎯 Project Overview

A Retrieval-Augmented Generation (RAG) based multilingual legal information system designed to help nonprofit legal aid organizations serve low-income clients more effectively.

**⚠️ IMPORTANT: This system provides legal information, not legal advice.**

## 🌟 Key Features

- **Multilingual Support**: English and Hindi language processing
- **Document Processing**: PDF, DOCX, TXT, and scanned documents (OCR)
- **RAG Pipeline**: Context-bounded responses using FAISS vector store
- **Ethical AI**: Built-in safeguards, disclaimers, and uncertainty escalation
- **Structured Responses**: Summary, relevant law, plain language explanation, next steps

## 🏗️ Architecture

```
User Input (EN/HI) → Translation → RAG Retrieval → LLM Generation → Translation → Output
                                    ↓
                            FAISS + PostgreSQL
```

## 🛠️ Technology Stack

- **LLM**: LLaMA-3-8B-Instruct / Mistral-7B-Instruct
- **Embeddings**: intfloat/e5-large-v2
- **Vector Store**: FAISS
- **Database**: PostgreSQL
- **Backend**: FastAPI
- **UI**: Streamlit
- **OCR**: Tesseract
- **Translation**: IndicTrans2 / NLLB

## 🚀 Getting Started

### Prerequisites

```bash
Python 3.10+
PostgreSQL 14+
Tesseract OCR
```

### Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your configuration

# Run the application (coming soon)
# streamlit run ui/streamlit_app.py
```

## 📁 Project Structure

See detailed architecture documentation in `docs/architecture.md`

## 🎓 Academic Context

**Project Title**: A Multilingual Retrieval-Augmented Legal Information System for Nonprofit Legal Aid

**Keywords**: RAG, Legal NLP, Multilingual AI, OCR, Ethical AI, Access to Justice

## 📄 License

[To be specified]

## 👥 Contributors

[Your name and affiliations]

## 🙏 Acknowledgments

Built to support nonprofit legal aid organizations in providing accessible legal information to underserved communities.
