
---

````markdown
# 🧠 Professor AI

**Professor AI** is an intelligent AI-powered teaching assistant that helps users learn complex topics with deep explanations, visual aids, and trustworthy reference links. Built with React, FastAPI, and Groq's LLaMA models, it combines the power of conversational AI with educational tools to create a smarter learning experience.

---

## ✨ Features

- 🔍 Ask anything — get deep, intuitive topic explanations
- 🧠 Powered by LLaMA 3 
- 📚 Generates citations and reference links
- 🖼️ Auto fetches visual content (diagrams, illustrations)
- 🌓 Light/Dark mode toggle
- ⚡ Fast and lightweight UI (Vite + React)
- 💬 Session-aware explanations with memory

---

## 🧰 Tech Stack

| Layer     | Technologies                                      |
|-----------|---------------------------------------------------|
| Frontend  | React, Vite, TailwindCSS                          |
| Backend   | FastAPI, Python                                   |
| LLM API   | Groq API (LLaMA 3 70B)                            |
| Deployment| Vercel (Frontend + Backend)                       |

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/AnmolManiDubey/Professor.git
cd Professor
````

### 2. Install Frontend Dependencies

```bash
cd frontend/professor-frontend
npm install
```

### 3. Install Backend Dependencies

```bash
cd ../../backend
pip install -r requirements.txt
```

### 4. Run the App Locally

#### Backend

```bash
uvicorn app.main:app --reload
```

#### Frontend

```bash
cd frontend/professor-frontend
npm run dev
```

---

## 🌍 API Endpoint

**Backend (Deployed)**
`https://professor-backend.vercel.app/teach`

### Sample Request

```json
POST /teach
{
  "topic": "Convolutional Neural Networks",
  "messages": [{"role": "user", "content": "Explain CNN"}]
}
```

---

## 📸 Screenshots

> *(Add some screenshots/gifs showing the chat, light/dark mode, and image cards)*

---

## 📦 Folder Structure

```
Professor/
├── backend/
│   ├── app/
│   │   ├── routes/
│   │   ├── services/
│   │   └── main.py
├── frontend/
│   └── professor-frontend/
│       ├── src/
│       ├── public/
│       └── App.jsx
```

---

## 🧠 Powered By

* [Groq LLaMA 3 API](https://console.groq.com/)
* [React Markdown](https://github.com/remarkjs/react-markdown)
* [Vercel](https://vercel.com/)

---

## 📜 License

MIT License © 2025 [Anmol Mani Dubey](https://github.com/AnmolManiDubey)

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you'd like to change.

---
