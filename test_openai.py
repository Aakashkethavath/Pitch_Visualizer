import os
from dotenv import load_dotenv
import openai

load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")

if not API_KEY:
    print("API_KEY not loaded!")
else:
    print(f"Loaded key starting with {API_KEY[:10]}")
    try:
        client = openai.OpenAI(api_key=API_KEY)
        client.models.list()
        print("API Key is valid and working!")
        
        # Option to test DALL-E:
        # response = client.images.generate(model="dall-e-3", prompt="a tiny test cube", n=1, size="1024x1024")
        # print("DALL-E generation success!")
    except Exception as e:
        print(f"API Error: {e}")
