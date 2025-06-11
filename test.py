from langchain_google_genai import GoogleGenerativeAIEmbeddings
import os
from dotenv import load_dotenv

load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

print("API Key:", os.environ.get("GOOGLE_API_KEY"))  # Should NOT be None

embedding = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
result = embedding.embed_query("What is AI?")
print(result)
