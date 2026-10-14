import os
from dotenv import load_dotenv
from portkey_ai import Portkey

load_dotenv()

client = Portkey(api_key=os.getenv("PORTKEY_API_KEY"))

response = client.chat.completions.create(
    model="@my-groq/openai/gpt-oss-20b",
    messages=[
        {"role": "user", "content": "Explain an LLM gateway in 2 simple sentences."}
    ],
    max_tokens=300,
)

print(response.choices[0].message.content)