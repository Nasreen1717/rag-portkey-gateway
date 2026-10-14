import os, json, urllib.request
from dotenv import load_dotenv

load_dotenv()

req = urllib.request.Request(
    "https://api.groq.com/openai/v1/models",
    headers={
        "Authorization": f"Bearer {os.getenv('GROQ_API_KEY')}",
        "User-Agent": "Mozilla/5.0",
    },
)
data = json.load(urllib.request.urlopen(req))
for m in sorted(data["data"], key=lambda x: x["id"]):
    print(m["id"])