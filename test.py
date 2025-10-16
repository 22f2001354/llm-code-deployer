from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

try:
    models = client.models.list()
    print("✅ OpenAI connected. Example model:", models.data[0].id)
except Exception as e:
    print("❌ Error:", e)
