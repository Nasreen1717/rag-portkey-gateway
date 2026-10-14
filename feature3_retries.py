import os
from dotenv import load_dotenv
from portkey_ai import Portkey

load_dotenv()

client = Portkey(
    api_key=os.getenv("PORTKEY_API_KEY"),
    config=os.getenv("PORTKEY_RETRY_CONFIG"),
    metadata={"_user": "user_001", "feature": "retries", "env": "dev"},
)

response = client.chat.completions.create(
    model="@my-groq/openai/gpt-oss-20b",
    messages=[{"role": "user", "content": "What is a retry in APIs? Answer in 2 lines."}],
    max_tokens=300,
)

print(response.choices[0].message.content)