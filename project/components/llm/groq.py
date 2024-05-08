from .interface import LLM
import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

class GroqLLM(LLM):

    def __init__(self, model=None) -> None:
        super().__init__(model)

        if model is None:
            self.model = "llama3-8b-8192"
        else:
            self.model = model

    def query(self, prompt:str) -> str:
        messages = []
        if (self.system_prompt):
            messages.append({
                'role': 'system',
                'content': self.system_prompt
            })

        messages.append({
            'role': 'user',
            'content': prompt
        })

        response = client.chat.completions.create(
                                model=self.model, 
                                messages=messages)
        
        return response.choices[0].message.content

    def chat(self, chat_history:list[tuple[str,str]]) -> str:
        if self.system_prompt:
            chat_history.insert(0, ('system', self.system_prompt))

        chat_messages = self.parse_history(chat_history)
        response = client.chat.completions.create(
                                model=self.model, 
                                messages=chat_messages)
        
        return response.choices[0].message.content

    @staticmethod
    def parse_history(chat_history:list[tuple[str,str]]):
        #Given a list of strings, return in the format that Ollama can understand
        messages = []

        for role, message in chat_history:
            messages.append({
                'role': role,
                'content': message
            })
        
        return messages