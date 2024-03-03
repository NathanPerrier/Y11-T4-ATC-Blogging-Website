import openai
from decouple import config

openai.api_key = config('OPENAI_API_KEY')
