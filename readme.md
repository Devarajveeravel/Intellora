# 🚀 Intellora AI

Intellora AI is a full-stack AI assistant built using React, FastAPI, Groq LLM, and RAG (Retrieval-Augmented Generation). It provides intelligent conversations, PDF document understanding, code generation, structured responses, and multi-chat support through a modern ChatGPT-style interface.

---

## ✨ Features

### 🤖 AI Chat Assistant

* Real-time AI conversations
* Powered by Groq LLM
* Context-aware responses
* Detailed explanations and coding assistance

### 📄 PDF Q&A (RAG)

* Upload PDF documents
* Automatic text extraction
* Ask questions about uploaded PDFs
* Generate summaries and insights
* Context-based document answers

### 💻 Code Generation

* Generate code in multiple programming languages
* Properly formatted code blocks
* Debugging support
* Algorithm explanations

### 📚 Structured Responses

* Clean and readable formatting
* Bullet-point explanations
* Step-by-step answers
* Improved readability

### 💬 Multi-Chat System

* Create multiple conversations
* Switch between chats
* Delete chats
* Session-based context management

### 📱 Responsive UI

* Mobile-friendly design
* Tablet support
* Desktop optimized
* Sidebar navigation

### ⚡ ChatGPT-Style Experience

* Typing animation
* Smooth auto-scrolling
* Markdown rendering
* Interactive chat interface

---

## 🛠 Tech Stack

### Frontend

* React.js
* React Markdown
* Remark GFM
* CSS3

### Backend

* FastAPI
* Python
* Groq API
* PyPDF2
* Python Multipart

### AI & RAG

* Groq LLM
* Retrieval-Augmented Generation (RAG)
* Document Processing
* Prompt Engineering

---

## 📂 Project Structure

```bash
Intellora/
│
├── frontend/
│   ├── src/
│   │   ├── App.js
│   │   ├── index.js
│   │   ├── index.css
│   │   └── reportWebVitals.js
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── services/
│   │   │   ├── llm.py
│   │   │   ├── rag.py
│   │   │   └── file_parser.py
│   │
│   └── requirements.txt
│
└── README.md
```

---

## ⚙️ Installation

### Clone Repository

```bash
git clone https://github.com/your-username/intellora-ai.git
cd intellora-ai
```

---

## Backend Setup

### Create Virtual Environment

```bash
python -m venv venv
```

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Create Environment Variables

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key
```

### Run Backend

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Backend URL:

```text
http://localhost:8000
```

---

## Frontend Setup

Navigate to frontend:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Run frontend:

```bash
npm start
```

Frontend URL:

```text
http://localhost:3000
```

---

## API Endpoints

### Chat Endpoint

```http
POST /query
```

Request Body:

```json
{
  "query": "What is AI?",
  "session_id": "123",
  "file_text": ""
}
```

---

### Upload PDF

```http
POST /upload/pdf
```

Upload a PDF file using multipart/form-data.

Response:

```json
{
  "text": "Extracted PDF content..."
}
```

---

## Example Use Cases

### AI Learning

```text
What is Machine Learning?
```

### Coding Assistance

```text
Write a Snake Game in Python
```

### PDF Summary

```text
Summarize the uploaded document
```

### Interview Preparation

```text
Give Data Engineer interview questions
```

---

## Deployment

### Backend (Render)

Start Command:

```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

### Frontend

Deploy using:

* Vercel
* Netlify
* Firebase Hosting

---

## Future Enhancements

* Voice Assistant
* Image Analysis
* Long-Term Memory
* Multi-Document RAG
* Streaming API
* AI Agents
* Dark Mode
* Export Chat as PDF
* User Authentication

---

## 👨‍💻 Author

**Devaraj Veeravel**

AI Engineer | Data Engineer | Full Stack AI Developer

Built with ❤️ using React, FastAPI, Groq, and RAG.
