# AI-Powered Lost & Found 🧠🔍

An AI-powered, privacy-first Lost & Found system designed for college campuses, built using Google AI.

---

## 🚩 Problem Statement
On campuses, lost items such as ID cards, bottles, wallets, and earbuds are usually reported through WhatsApp groups or notice boards.  
These methods are unstructured, inefficient, and have a very low recovery rate.

---

## 💡 Our Solution
A centralized AI-powered Lost & Found platform where:
- Users can report lost or found items
- AI automatically matches lost items with found ones
- Only relevant matches are shown (no public browsing)
- Secure claim and verification ensures trust and privacy

---

## 🧠 AI Features
- **Google Gemini Text Embeddings** for semantic text matching
- **Image similarity matching** for visual verification
- **Hybrid scoring** using text, image, and location context
- **Gemini Generative AI** to explain matches in natural language

---

## 🔐 Privacy & Safety
- No public listing of lost or found items
- Items visible only when a match is found
- Mandatory image upload for found items
- Admin-mediated handover via Lost & Found desk
- No direct contact sharing between users

---

## 🛠 Tech Stack
- Google Gemini (AI Studio)
- Python
- Streamlit
- SQLite

---

## 🚀 Future Scope
- Firebase Authentication (OTP / Gmail login)
- Admin dashboard for Lost & Found desk
- Vertex AI for scalable AI deployment
- Google Cloud Storage for secure image storage
- BigQuery for analytics and recovery insights

---

## ▶️ How to Run the Project

```bash
pip install -r requirements.txt
streamlit run app.py