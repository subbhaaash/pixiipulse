# 🚀 PixiiPulse

Amazon Conversion Fix Engine built for the AI shopping era — optimized for humans + Amazon Rufus.

## Live Demo
https://pixiipulse.streamlit.app

## What it does
- Audits Amazon product listings
- Gives Conversion Score
- Checks Rufus / AEO readiness
- Finds critical fixes and quick wins
- Generates Pixii visual roadmap

## Tech Stack
- Python
- Streamlit
- Groq LLaMA 3.1
- Jina AI Reader

## How to run
```bash
pip install -r requirements.txt
streamlit run app.py
## 🎯 Interview Talking Points 

### 🔹 Problem
Amazon sellers struggle with low conversion because listings are not optimized for:
- Human buyers
- AI assistants like Amazon Rufus

---

### 🔹 Solution
Built **PixiiPulse**, an AI-powered system that:
- Takes Amazon product URL
- Extracts & cleans listing data
- Runs AI audit for:
  - Conversion optimization
  - SEO & AEO (AI search readiness)
- Returns actionable insights (score + fixes)

---

### 🔹 Tech Flow
1. User inputs Amazon URL  
2. Data extracted  
3. Cleaned & structured  
4. Sent to LLM (Groq - LLaMA 3)  
5. AI generates structured JSON  
6. UI shows score + fixes  

---

### 🔹 Key Challenges
- Invalid JSON from AI → fixed using parser  
- Consistency in scoring → fallback logic  
- Prompt optimization for structured output  

---

### 🔹 Why this is strong
- Live deployed AI product  
- Real-world use case  
- End-to-end system  

---

### 🔹 Future Improvements
- Auto rewrite titles & bullets  
- Bulk product analysis  
- Chrome extension
