import os
from dotenv import load_dotenv
from portkey_ai import Portkey

load_dotenv()

client = Portkey(
    api_key=os.getenv("PORTKEY_API_KEY"),
    config=os.getenv("PORTKEY_LB_CONFIG"),
    metadata={"_user": "user_001", "feature": "loadbalance", "env": "dev"},
)

question = "What is an LLM gateway in one sentence?"

for i in range(1, 7):
    response = client.chat.completions.create(
        messages=[{"role": "user", "content": question}],
        max_tokens=300,
    )
    print(f"Run {i} model: {response.model}")
    print(response.choices[0].message.content)
    print("-" * 40)