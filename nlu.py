import json
import re
from config import ConfigData
from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    google_api_key=ConfigData.GEMINI_API_KEY,
    temperature=0.3
)


memory = ConversationBufferMemory(
    memory_key="chat_history",
    input_key="question",
    return_messages=True
)

table_schema = json.dumps(ConfigData.TABLE_SCHEMA, indent=2).replace("{", "{{").replace("}", "}}")
schema_description = ConfigData.SCHEMA_DESCRIPTION
json_ex_1 = json.dumps(ConfigData.FEW_SHOT_EXAMPLES, indent=2).replace("{", "{{").replace("}", "}}")

# Prompt Template
PROMPT_TEMPLATE = PromptTemplate(
    input_variables=["question", "chat_history"],
    template=f"""
You are a senior MongoDB expert with 10 years of experience. 
You will be given a MongoDB database schema and a natural language user question. 
Your job is to convert the user question into a valid MongoDB aggregation pipeline in JSON format.
Handel different queries and chat with the user 

🧩 MongoDB Schema:
{table_schema}

📘 Schema Description:
{schema_description}

🧪 Example:
Input: How many accounts does Elizabeth Ray have?
Output:
{json_ex_1}

❗️Instructions:
- Always return a valid MongoDB aggregation pipeline in JSON format.
- Do not return any explanation, comments, or extra text.
- Only give the aggregation query. No preamble. No markdown. No SQL.

Now convert this:
Input: {{question}}
"""
)

# LLMChain
llm_chain = LLMChain(
    llm=llm,
    prompt=PROMPT_TEMPLATE,
    memory=memory,
    verbose=False
)

#funt
def extract_entities_and_intent(question: str):
    try:
        response = llm_chain.invoke({"question": question})
        raw_text = response["text"].strip()
        clean_text = re.sub(r"```json|```", "", raw_text).strip()
        return json.loads(clean_text)
    except Exception as e:
        return {
            "error": str(e),
            "raw": raw_text if 'raw_text' in locals() else "No response"
        }

def get_memory():
    return memory.buffer
