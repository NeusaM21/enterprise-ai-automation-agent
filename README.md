# Enterprise AI Automation Agent – WhatsApp + Shopify + Gemini AI
Robust AI Automation backend built with **FastAPI**, **Google Gemini AI**, **Shopify API** and **WhatsApp Cloud API**. Designed for **real-world business automation** such as product recommendations, AI customer support, and ecommerce assistance.

> **PT/BR abaixo**

[![Python](https://img.shields.io/badge/Python-3.11+-blue)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-💚-brightgreen)](https://fastapi.tiangolo.com/)
[![Gemini](https://img.shields.io/badge/Google%20AI-Gemini-black)](https://ai.google.dev/)

Production-style AI automation agent integrating **WhatsApp** and **Shopify** for sales & support. Built with **FastAPI**.  
Ready for RAG, memory and Slack notifications.

---

## ✅ Features
- 🤖 AI Text Automation using **Google Gemini AI**
- 💬 **WhatsApp Cloud API** integration (webhook inbound/outbound messages)
- 🛒 Shopify **product search** & catalog automation
- 🔄 Fallback Strategy: **Shopify Search → AI answer**
- 🧠 Context-ready for future **Memory / Actions / RAG**
- 🧱 Clean FastAPI **service architecture**
- 🔥 **Production-ready foundation**

---

## 🏗️ Architecture Overview
´´´
FastAPI
├─ /ai/ask → Gemini AI smart replies
├─ /ai/models → List allowed Gemini models
├─ /webhook/whatsapp → WhatsApp integration
├─ /catalog/products → Shopify catalog
├─ services/ → ai, shopify, whatsapp modules
├─ utils/ → logger helper
└─ config/ → environment settings
´´´

---


---

## ⚙️ Requirements
- Python **3.11+**
- Google Gemini API Key → https://aistudio.google.com
- Shopify Store + Private Admin API Key
- WhatsApp Cloud API (Meta Developers)

---

## 🔐 Environment Setup (.env)
Create a `.env` file in the root folder:
```ini
ENV=dev
HOST=127.0.0.1
PORT=8000

GEMINI_API_KEY=YOUR_GEMINI_KEY
AI_MODEL=models/gemini-2.5-flash

SHOPIFY_API_KEY=your_key
SHOPIFY_PASSWORD=your_password
SHOPIFY_STORE_URL=shop-name.myshopify.com

WHATSAPP_TOKEN=your_meta_whatsapp_token
WHATSAPP_VERIFY_TOKEN=your_webhook_verify_token
WHATSAPP_PHONE_ID=your_whatsapp_phone_id

---

🚀 Run the Project Locally
Option A – Quick Start (recommended)

./run.ps1

---

Option B – Manual

python -m venv .venv
& .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload

Swagger UI: http://127.0.0.1:8000/docs

API JSON: http://127.0.0.1:8000/openapi.json

---

✅ Canonical API Tests (PowerShell)

⚠️ Before running tests, confirm the server is running.
If not:

Stop any old server → CTRL + C

Activate venv → & .\.venv\Scripts\Activate.ps1

Start → ./run.ps1


Health check

Invoke-RestMethod -Method Get -Uri "http://127.0.0.1:8000/health"

---

List available AI models

Invoke-RestMethod -Method Get -Uri "http://127.0.0.1:8000/ai/models"

---

Send AI message (Gemini)

$body = @{ text = "Say a fun fact about AI in one line." } | ConvertTo-Json
Invoke-RestMethod -Method Post -Uri "http://127.0.0.1:8000/ai/ask" -ContentType "application/json" -Body $body


---

✅ Expected /ai/ask response:


{
  "model": "models/gemini-2.5-flash",
  "fallback": false,
  "latency_ms": 185,
  "reply": "Artificial intelligence doesn't sleep—but it may dream in algorithms!"
}


---

📡 WhatsApp Webhook (Cloud API)
Verify webhook

GET /webhook/whatsapp?hub.mode=subscribe&hub.verify_token=YOUR_TOKEN&hub.challenge=123456


Receive incoming WhatsApp messages

Tries Shopify product match first

Falls back to AI if no match

Sends reply automatically

---

🛒 Shopify Integration

GET /catalog/products?limit=5

---

✅ Development Quality

.editorconfig → code formatting

.gitattributes → avoid CRLF/LF issues

utils/logger.py → structured logs

.env.example → clean setup

run.ps1 → easy local execution

---


📦 Project Roadmap
Feature	Status
WhatsApp + Gemini AI Base	✅ Done
Shopify Catalog Search	✅ Done
/ai/ask fallback + timeout	✅ Done
README Professional (EN/PT)	✅ Done
Slack Notifications	🔜 Next
AI Chat Memory (/ai/messages)	🔜 Next
Product Recommendation AI	🔜 Planned
RAG for FAQ Knowledge Base	🔜 Planned
Web Dashboard	🔜 Planned

---

🛠️ Troubleshooting
Issue	Solution
Connection refused	Run API with ./run.ps1
Model not found	Check /ai/models and update AI_MODEL
Timeout error	Increase timeout_ms in /ai/ask
AI provider error (502)	Check GEMINI_API_KEY
CRLF warnings	Already fixed by .gitattributes

---

👩‍💻 Author

Built by Neusa Magalhães – AI Automation Engineer
🔗 GitHub: https://github.com/NeusaM21

🔗 LinkedIn: https://linkedin.com/in/neusam21dev

📩 contact.neusam21@gmail.com

---

🇧🇷 Visão Geral em Português

Backend profissional de automação com IA integrado com WhatsApp + Shopify + Gemini AI. Ideal para criar chatbots inteligentes, assistentes de vendas automáticos e IA aplicada a e-commerce. Possui arquitetura limpa, pronta para crescer com banco de dados, memória conversacional, painéis web e integrações com APIs.

---

📄 License

MIT License – Free for personal and commercial use.

---

🔥 Contributions and suggestions are welcome!




