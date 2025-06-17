
# 🧠 Gemini + MongoDB Conversational Agent

An advanced natural language interface for querying MongoDB using Google Gemini 1.5 Flash via LangChain. This project allows users to ask questions about their database using plain English and receive structured results via aggregation pipelines.

---

## 🚀 Features

✅ Natural Language to MongoDB Aggregation  
✅ Google Gemini 1.5 Flash (via LangChain)  
✅ Real-time MongoDB execution  
✅ Memory buffer to handle conversation context  
✅ Voice output (Text-to-Speech using `gTTS`)  
✅ Streamlit-based UI  
✅ World Model dashboard insights

---

## 🏗️ Project Structure

```
project/
│
├── app.py                      # Streamlit frontend with voice and text interface
├── nlu.py                      # LangChain + Gemini-based query translator with memory
├── config.py                   # Schema, few-shot examples, and Gemini API key
├── dashboard.py                # World model insights (analytics panel)
├── db_connection.py            # MongoDB connection logic
├── requirements.txt            # All dependencies
├── Dockerfile                  # For containerized deployment
└── README.md                   # Project documentation
```
## Data set used sample_analytics with Mongodb compass
---

## 🛠️ Tech Stack

- 🧠 **LangChain** (with memory buffer)
- 🤖 **Google Gemini 1.5 Flash**
- 🔍 **MongoDB** (for real-time query)
- 🎙️ **gTTS** (text-to-speech)
- 🌐 **Streamlit** (UI framework)
- 🐳 **Docker** (containerization)

---

## 🔧 Setup Instructions

### 1. 🔑 API Keys

 update `config.py` with your Gemini API key:

```python
GEMINI_API_KEY = "your-google-api-key"
```

---

### 2. 🐍 Install Requirements

```bash
pip install -r requirements.txt

```
## ⚙️ Prerequisites

1. MongoDB
   - Install and start MongoDB locally or use [MongoDB Atlas](https://www.mongodb.com/atlas/database).
   - Import your data into `customers`, `accounts`, and `transactions` collections.
   - Use Mongodb compass to make connection with the app
---

or Edit

# .env

from pymongo import MongoClient
db = MongoClient("<your_mongodb_connection_string>")["<your_database_name>"]


### 3. 🚦 Run the App

```bash
streamlit run app.py
```

Visit [http://localhost:8501](http://localhost:8501) in browser.

---

### 4. 🐳 Docker Setup 

**Build Image:**

```bash
docker build -t mongo-agent .
```

**Run Container:**

```bash
docker run -p 8501:8501 --env MONGO_URI="your_mongo_uri" mongo-agent
```

> ✅ Make sure MongoDB is running locally or remotely and accessible.

---



## Use test_query.txt to test te Agent 

-- All the examples are provided in the text file 
-- With different operations from Simple --> Advance



## 🗃️ Sample Queries to Try

| Query Type                       | Example 

| Single Entity                    | `How many accounts does Elizabeth Ray have?` 
| Multi-turn follow-up             | `What is her email?'
| Aggregation                      | `What is the total AMD stock bought?` 
| Nested joins                     | `What are the limits of accounts linked to Elizabeth Ray?` 
| Benefits & tier logic            | `What benefits does she have?` 
| Date range                       | `When was the last transaction for account 716662?`
| Counts                           | `Total number of customers?` 

---

## 📈 Dashboard

A visual overview of customer, account, and transaction insights is available under the **📊 Database Insights** expandable panel in the app.

---

## 🧠 LangChain Memory

We use `ConversationBufferMemory` to support contextual, multi-turn queries. The assistant can handle pronouns and follow-ups like:

```
Q: Show me Elizabeth Ray's accounts.
Q: Now show me her transactions.
Q: What’s the most recent one?
```

---


## 📦 Dependencies

See [`requirements.txt`](./requirements.txt)

---

## 👨‍💻 Author

**Abhinav Kangle**  
[LinkedIn](https://www.linkedin.com/in/abhinav-kangle-523773249/) • [GitHub](https://github.com/akaabhinav002)
