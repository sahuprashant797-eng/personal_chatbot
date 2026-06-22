# 🤖 Personal Chatbot Web App

A **Streamlit-based AI chatbot** powered by Hugging Face LLMs, designed to provide a conversational interface with **multi-session memory and persistent chat history**.

---

## 🚀 Features

* 💬 Real-time AI conversation interface
* 🧠 Multi-session chat support (like ChatGPT)
* 💾 Persistent chat history using JSON storage
* 🏷️ Automatic session title generation
* 🔄 Switch between previous conversations
* ⚡ Clean and interactive Streamlit UI

---

## 🛠️ Tech Stack

* **Frontend:** Streamlit
* **Backend:** Python
* **LLM Integration:** Hugging Face (`Qwen2.5-7B-Instruct`)
* **Framework:** LangChain
* **Storage:** JSON (local session persistence)

---

## 📂 Project Structure

```
.
├── chatbot.py          # Main application file
├── chat_sessions.json  # Stored chat history (auto-generated)
├── .env                # API keys (not uploaded)
```

---

## ⚙️ Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/personal-chatbot.git
cd personal-chatbot
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Setup Environment Variables

Create a `.env` file and add your Hugging Face API token:

```
HUGGINGFACEHUB_ACCESS_TOKEN=your_api_key_here
```

---

## ▶️ Run the Application

```bash
streamlit run chatbot.py
```

---

## 🧠 How It Works

* Uses **LangChain message objects** to manage conversation flow
* Integrates **Hugging Face LLM endpoint** for generating responses
* Stores chat sessions in a **JSON file** for persistence
* Uses Streamlit session state for managing UI and chat switching

---

## 📸 Demo

*(Add screenshots or screen recording here for better understanding)*

---

## 💡 Learning Outcomes

* Built a full-stack AI application using LLMs
* Learned session management and state handling
* Integrated external APIs (Hugging Face)
* Implemented persistent storage for conversations

---

## 🚧 Future Improvements

* Add **RAG (Retrieval-Augmented Generation)** with vector database
* Deploy on **Streamlit Cloud / Hugging Face Spaces**
* Add user authentication
* Improve UI/UX and response streaming

---

## 🤝 Contributing

Feel free to fork this repository and improve it.

---

## 📬 Contact

If you have suggestions or feedback, feel free to connect with me on LinkedIn.

---

⭐ If you like this project, consider giving it a star!
