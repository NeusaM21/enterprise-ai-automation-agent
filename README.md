<!-- Banner -->
<p align="center">
  <img src="assets/banner.png" alt="Enterprise AI Automation Agent Banner" style="max-width: 100%;">
</p>

# Enterprise AI Automation Agent – WhatsApp + Shopify + Google Gemini AI
**AI automation backend integrating WhatsApp + Shopify + Google Gemini AI for ecommerce automation, product assistance and intelligent conversations.**  

![Status](https://img.shields.io/badge/status-active-success)
![Python](https://img.shields.io/badge/python-3.11+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Ready-brightgreen)
![Gemini AI](https://img.shields.io/badge/Google%20Gemini-Integrated-black)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux-blue)
![License](https://img.shields.io/badge/license-MIT-purple)

<hr style="border: 0.5px solid #e5e5e5; margin: 20px 0">

## 📑 Table of Contents
- [✅ Feature Overview](#feature-overview)
- [⚙️ Tech Stack](#tech-stack)
- [🔧 How It Works](#how-it-works)
- [🚀 Local Setup](#local-setup)
- [🔐 Environment (.env)](#environment-env)
- [▶️ Run Server](#run-server)
- [⚡ Canonical API Tests (PowerShell)](#canonical-api-tests-powershell)
- [✅ Expected Response](#expected-response)
- [🔥 Demo (Terminal)](#demo-terminal)
- [🛒 Shopify Example](#shopify-example)
- [💬 WhatsApp Webhook](#whatsapp-webhook)
- [📂 Project Structure](#project-structure)
- [🛠️ Troubleshooting](#troubleshooting)
- [🌍 Links Oficiais](#links-oficiais)
- [🇧🇷 Visão Geral (Português)](#visão-geral-português)
- [🧭 Roadmap](#roadmap)
- [👩‍💻 Author](#author)
- [📄 License](#license)

<hr style="border: 0.5px solid #e5e5e5; margin: 20px 0">

<a id="feature-overview"></a>
## ✅ Feature Overview
| Feature | Status | Description |
|----------|--------|-------------|
| AI Reply Engine (Gemini) | ✅ Done | Smart responses powered by Google Gemini |
| WhatsApp Integration | ✅ Done | Webhook + AI replies |
| Shopify Integration | ✅ Done | Product search by title |
| Error-safe AI Engine | ✅ Done | Timeout + fallback + model validation |
| REST API Docs | ✅ Done | Swagger ready |
| Slack Notifications | 🔜 Next | Team alerts from automation |
| AI Memory (/ai/messages) | 🔜 Next | Conversation history |
| Ecommerce AI Assistant | 🔜 Next | Smart product advisor |
| RAG for Knowledge Base | 🔜 Planned | Load product FAQ / docs |
| Dashboard UI | 🔜 Planned | Manage flows visually |

<hr style="border: 0.5px solid #e5e5e5; margin: 20px 0">

<a id="tech-stack"></a>
## ⚙️ Tech Stack
| Area | Technology |
|------|-------------|
| Language | Python 3.11 |
| Framework | FastAPI |
| AI Provider | Google Gemini |
| Ecommerce | Shopify API |
| Messaging | WhatsApp Cloud API |
| HTTP Client | httpx |
| ASGI Server | uvicorn |
| Env | python-dotenv |

<hr style="border: 0.5px solid #e5e5e5; margin: 20px 0">

<a id="how-it-works"></a>
## 🔧 How It Works
User (WhatsApp) → Webhook → Check Shopify Products  
↳ Found → Product response to user  
↳ Not Found → Ask Gemini AI → Smart reply to WhatsApp  

<hr style="border: 0.5px solid #e5e5e5; margin: 20px 0">

<a id="local-setup"></a>
## 🚀 Local Setup
1. Clone o repositório:  
`git clone https://github.com/NeusaM21/enterprise-ai-automation-agent.git`  
2. Acesse a pasta do projeto:  
`cd enterprise-ai-automation-agent`  
3. Crie o ambiente virtual:  
`python -m venv .venv`  
4. Ative no PowerShell:  
`& .\.venv\Scripts\Activate.ps1`  
5. Instale dependências:  
`pip install -r requirements.txt`  

<hr style="border: 0.5px solid #e5e5e5; margin: 20px 0">

<a id="environment-env"></a>
## 🔐 Environment (.env)

Crie um arquivo `.env` na raiz do projeto com:  

Create a .env file:


ENV=dev
HOST=127.0.0.1
PORT=8000

GEMINI_API_KEY=YOUR_GEMINI_KEY
AI_MODEL=models/gemini-2.0-flash-001

SHOPIFY_API_KEY=your_key
SHOPIFY_PASSWORD=your_password
SHOPIFY_STORE_URL=shop-name.myshopify.com

WHATSAPP_TOKEN=your_meta_whatsapp_token
WHATSAPP_VERIFY_TOKEN=your_webhook_verify_token
WHATSAPP_PHONE_ID=your_whatsapp_phone_id


<hr style="border: 0.5px solid #e5e5e5; margin: 20px 0">

<a id="run-server"></a>
## ▶️ Run Server
Execute o servidor local:  
`uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload`  
Acesse a documentação Swagger:  
[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

<hr style="border: 0.5px solid #e5e5e5; margin: 20px 0">

<a id="canonical-api-tests-powershell"></a>
## ⚡ Canonical API Tests (PowerShell)
Antes de testar, confirme se o servidor FastAPI está rodando!  
Se não estiver:
- Pressione **CTRL + C** para parar o servidor antigo.  
- Ative a venv: `& .\.venv\Scripts\Activate.ps1`  
- Inicie com: `./run.ps1`  

Testes:

Invoke-RestMethod -Method Get -Uri "http://127.0.0.1:8000/health"
Invoke-RestMethod -Method Get -Uri "http://127.0.0.1:8000/ai/models"
$body = @{ text = "Hello Gemini, how are you?" } | ConvertTo-Json
Invoke-RestMethod -Method Post -Uri "http://127.0.0.1:8000/ai/ask" -ContentType "application/json" -Body $body


<hr style="border: 0.5px solid #e5e5e5; margin: 20px 0;">


<a id="expected-response"></a>
## ✅ Expected Response

{
  "model": "models/gemini-2.5-flash",
  "fallback": false,
  "latency_ms": 210,
  "reply": "Hi! I'm great and ready to help! 😊"
}


<hr style="border: 0.5px solid #e5e5e5; margin: 20px 0;">


<a id="demo-terminal"></a>
## 🔥 Demo (Terminal)

curl -X POST http://127.0.0.1:8000/ai/ask \
  -H "Content-Type: application/json" \
  -d "{\"text\":\"Say one fun fact about AI\"}"


<hr style="border: 0.5px solid #e5e5e5; margin: 20px 0;">


<a id="shopify-example"></a>
## 🛒 Shopify Example

GET http://127.0.0.1:8000/catalog/products?limit=5


<hr style="border: 0.5px solid #e5e5e5; margin: 20px 0;">


<a id="whatsapp-webhook"></a>
## 💬 WhatsApp Webhook

GET /webhook/whatsapp?hub.mode=subscribe&hub.verify_token=YOUR_TOKEN&hub.challenge=1234


Receive:

POST /webhook/whatsapp


<hr style="border: 0.5px solid #e5e5e5; margin: 20px 0;">


<a id="project-structure"></a>
## 📂 Project Structure (Clean Architecture Ready)

```plaintext
This project follows a modular and scalable architecture to support future extensions such as conversation memory, Slack actions, RAG knowledge base, and persistent storage. The structure is clean and organized to make maintenance easy.

Este projeto segue uma arquitetura modular e escalável, preparada para receber expansões futuras como memória conversacional, ações via Slack, RAG para base de conhecimento e persistência de dados. A organização facilita manutenção e evolução.

```plaintext
enterprise-ai-automation-agent
├─ app/
│  ├─ main.py                # FastAPI app and route definitions / App FastAPI e rotas
│  ├─ services/              # External integrations: AI, Shopify, WhatsApp / Integrações externas
│  ├─ utils/                 # Logger and shared helpers / Utilitários e logger
│  ├─ config/                # Environment and global settings / Configuração e variáveis de ambiente
│
├─ tests/                    # Automated tests / Testes automatizados
│
├─ assets/                   # Static project assets (images/banners) / Arquivos estáticos do projeto
│  └─ banner.png             # Project cover image used in README / Imagem de capa
│
├─ run.ps1                   # Local startup script for Windows PowerShell
├─ requirements.txt          # Python dependencies
└─ README.md                 # Project documentation

```


<hr style="border: 0.5px solid #e5e5e5; margin: 20px 0;">


<a id="troubleshooting"></a>
## 🛠️ Troubleshooting
Issue	Fix
Connection refused	Start server: ./run.ps1
Model not found	Check /ai/models and .env
Timeout	Add timeout_ms to /ai/ask body
AI error 502	Check GEMINI_API_KEY
CRLF/LF warning	Already fixed with .gitattributes

<hr style="border: 0.5px solid #e5e5e5; margin: 20px 0;">


<a id="links-oficiais"></a>
## 🌍 Links Oficiais

Gemini AI Docs → https://ai.google.dev

WhatsApp API → https://developers.facebook.com

Shopify API → https://shopify.dev


<hr style="border: 0.5px solid #e5e5e5; margin: 20px 0;">


<a id="visão-geral-português"></a>
## 🇧🇷 Visão Geral (Português)

Este projeto é um agente de automação com IA para e-commerce. Ele integra:
✅ WhatsApp (atendimento automático)
✅ Shopify (busca de produtos)
✅ IA (Gemini) para respostas inteligentes

Use para criar automações reais de suporte, vendas e chat com IA.


<hr style="border: 0.5px solid #e5e5e5; margin: 20px 0;">


<a id="roadmap"></a>
## 🧭 Roadmap

Slack alerts ✅ soon

AI conversation memory

RAG for store FAQ

Product recommendations

Web dashboard


<hr style="border: 0.5px solid #e5e5e5; margin: 20px 0;">


<a id="author"></a>
## 👩‍💻 Author

Developed by Neusa M. – AI Automation Engineer

📩 Email: contact.neusam21@gmail.com

🌐 GitHub: https://github.com/NeusaM21

🔗 LinkedIn: https://linkedin.com/in/neusam21dev


<hr style="border: 0.5px solid #e5e5e5; margin: 20px 0;">


<a id="license"></a>
## 📄 License

This project is licensed under the [MIT License](LICENSE) — free for commercial and academic use.


---


<p align="left">
  <a href="https://github.com/NeusaM21">
    <img src="https://img.shields.io/badge/⬅️-Voltar%20para%20o%20portfólio%20principal-blue?style=for-the-badge"/>
  </a>
</p>