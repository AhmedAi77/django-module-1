from http.client import responses

from openai import OpenAI
from django.conf import settings

class ContentClient():
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_APIKEY)
    def generate (self,prompt,system=None):
        messages=[]
        if system:
            messages.append({"role": "system", "content":system})
        messages.append({"role": "user","content":prompt})

        responses = self.client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=messages,
        )
        return responses.choices[0].message.content

