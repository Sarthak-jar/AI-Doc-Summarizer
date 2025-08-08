# 🧠 AI Document Summarizer

A web-based application that uses state-of-the-art transformer models to generate concise summaries from uploaded PDF or DOCX documents.

---

## 🚀 Features

- 📄 Upload PDF or DOCX files
- 🤖 Extracts text using `PyMuPDF` and `python-docx`
- 🧠 Summarizes content using Hugging Face's `facebook/bart-large-cnn` transformer model
- 🖥️ Simple web interface built with Flask

---

## 📸 Demo

Upload your document and get a clean, short summary in seconds!

*Add a screenshot here if available.*

---

## 🛠️ Tech Stack

| Component      | Technology                            |
|----------------|----------------------------------------|
| Backend        | Python, Flask                          |
| NLP Model      | Hugging Face Transformers (`BART`)     |
| Text Extraction| `PyMuPDF`, `python-docx`               |
| Frontend       | HTML (Jinja templating via Flask)      |

---

## 📂 Project Structure

```bash
├── app.py               # Flask app
├── summarizer.py        # HuggingFace summarization logic
├── extractors.py        # Text extraction from PDF & DOCX
├── templates/
│   └── index.html       # HTML upload & summary interface
├── uploads/             # Stores uploaded files temporarily
└── requirements.txt     # Python dependencies (create this)
