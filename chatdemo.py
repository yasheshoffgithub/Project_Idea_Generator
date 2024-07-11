import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()

#Extract api_key set in .env
GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)

#Give a simple prompt to test if you are connected to gemini
prompt="Hi Gemini! Say hi back"
model = genai.GenerativeModel('gemini-1.0-pro-latest')
response = model.generate_content(prompt)
print(response.text)