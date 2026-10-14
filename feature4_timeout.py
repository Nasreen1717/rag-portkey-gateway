import os
from dotenv import load_dotenv
from portkey_ai import Portkey

load_dotenv()

client = Portkey(
    api_key=os.getenv("PORTKEY_API_KEY"),
    config=os.getenv("PORTKEY_TIMEOUT_CONFIG"),
    metadata={"_user": "user_001", "feature": "timeout", "env": "dev"},
)

response = client.chat.completions.create(
    model="@my-groq/openai/gpt-oss-20b",
    messages=[{"role": "user", "content": "Explain request timeouts in one short paragraph."}],
    max_tokens=400,
)

print(response.choices[0].message.content)
client.close()