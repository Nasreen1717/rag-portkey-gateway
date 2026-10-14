import os
import time
from dotenv import load_dotenv
from portkey_ai import Portkey

load_dotenv()

client = Portkey(
    api_key=os.getenv("PORTKEY_API_KEY"),
    config=os.getenv("PORTKEY_PROD_CONFIG"),
    metadata={
        "_user": "user_001",
        "feature": "prod-config",
        "env": "dev",
    },
)

question = "Explain what an LLM gateway is in 2 sentences."

for run in (1, 2):
    start = time.time()
    response = client.chat.completions.create(
        messages=[{"role": "user", "content": question}],
        max_tokens=400,
    )
    elapsed = time.time() - start
    print(f"--- Run {run} ({elapsed:.2f}s) | model: {response.model} ---")
    print(response.choices[0].message.content)
    print()
    time.sleep(3)