import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from portkey_ai import PORTKEY_GATEWAY_URL, createHeaders

load_dotenv()

llm = ChatOpenAI(
    model="@my-groq/openai/gpt-oss-20b",
    api_key="dummy",  # real key Portkey ke paas hai
    base_url=PORTKEY_GATEWAY_URL,
    default_headers=createHeaders(
        api_key=os.getenv("PORTKEY_API_KEY"),
        config=os.getenv("PORTKEY_FALLBACK_CONFIG"),
        metadata={"_user": "user_001", "feature": "langchain", "env": "dev"},
    ),
    max_tokens=400,
)

response = llm.invoke("In one sentence, what is an LLM gateway?")
print(response.content)