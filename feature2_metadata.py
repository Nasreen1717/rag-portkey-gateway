import os
import uuid
from dotenv import load_dotenv
from portkey_ai import Portkey

load_dotenv()

client = Portkey(
    api_key=os.getenv("PORTKEY_API_KEY"),
    metadata={
        "_user": "user_001",
        "feature": "rag-query",
        "env": "dev",
    },
    trace_id=f"trace-{uuid.uuid4().hex[:8]}",
)

response = client.chat.completions.create(
    model="@my-groq/openai/gpt-oss-20b",
    messages=[{"role": "user", "content": "What is a vector database? One sentence."}],
    max_tokens=300,
)

print(response.choices[0].message.content)
print("trace_id:", client.trace_id)