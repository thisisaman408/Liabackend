# LIA Plus - Backend

This is the brain behind **LIA Plus**. It's a Python-based API built with **FastAPI** that handles the natural language processing, sentiment analysis, and conversation management.

## 🚀 Live Application
**You can use the chatbot directly via the deployed frontend here:** 👉 **https://liafrontend-five.vercel.app/**

* **Frontend Repository:** https://github.com/thisisaman408/liafrontend

---

The core idea here isn't just to return text, but to *understand* it. I implemented a hybrid engine that uses both rule-based heuristics (VADER) and dynamic context adjustments. There is also a reinforcement learning loop where the system accepts user feedback to correct its sentiment labels.

## Tech Stack

* **FastAPI**: For a high-performance, easy-to-document API.
* **PostgreSQL + SQLAlchemy**: For persistent storage of conversations and message history.
* **VADER + Custom Heuristics**: A custom-tuned NLP engine for sentiment detection.
* **Groq API**: Integrated for generating human-like responses when needed.

## Key Components

* **engine.py**: The "Custom Linguistic Engine" that extends VADER with domain-specific rules.
* **orchestrator.py**: Controls input analysis, sentiment scoring, response generation, and logging.
* **database.py**: Handles PostgreSQL connectivity and schema migrations.
* **storage.py**: Provides persistence layer for chat records.

## Setup & Running

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
2. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure environment variables (`DATABASE_URL`, `GROQ_API_KEY`).
4. Run the server:
   ```bash
   uvicorn main:app --reload
   ```

The API will be available at: **http://localhost:8000**

## API Endpoints

* **POST /chat**: Send a message and receive an intelligent reply.
* **GET /conversations**: Fetch past chat sessions.
* **GET /history/{id}**: Retrieve full chat history for a specific session.
* **POST /feedback**: Submit corrected sentiment labels for system learning.

> This system is built with clean modular design and strict separation of concerns.

## 📝 Note
Due to my participation in the Smart India Hackathon (SIH), I couldn't prepare video documentation. I hope the live deployment and repository provide sufficient project insight.

