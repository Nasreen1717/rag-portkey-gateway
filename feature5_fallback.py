import os
from dotenv import load_dotenv
from portkey_ai import Portkey

load_dotenv()

client = Portkey(
    api_key=os.getenv("PORTKEY_API_KEY"),
    config=os.getenv("PORTKEY_FALLBACK_CONFIG"),
    metadata={"_user": "user_001", "feature": "fallback", "env": "dev"},
)

response = client.chat.completions.create(
    messages=[{"role": "user", "content": "Explain fallbacks in an LLM gateway in one short paragraph."}],
    max_tokens=400,
)

print(response.choices[0].message.content)
client.close()