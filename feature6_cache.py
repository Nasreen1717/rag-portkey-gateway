import os
import time
from dotenv import load_dotenv
from portkey_ai import Portkey

load_dotenv()

client = Portkey(
    api_key=os.getenv("PORTKEY_API_KEY"),
    config=os.getenv("PORTKEY_CACHE_CONFIG"),
    metadata={"_user": "user_001", "feature": "cache", "env": "dev"},
)

question = "What is an LLM gateway in one sentence?"

for i in (1, 2):
    start = time.time()
    response = client.chat.completions.create(
        messages=[{"role": "user", "content": question}],
        max_tokens=300,
    )
    elapsed = time.time() - start
    print(f"Run {i} took {elapsed:.2f}s")
    print(response.choices[0].message.content)
    print("-" * 40)