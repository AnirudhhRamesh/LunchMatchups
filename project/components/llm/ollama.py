from .interface import LLM
import ollama

class OllamaLLM(LLM):

    def __init__(self, model=None) -> None:
        super().__init__(model)

        if model is None:
            self.model = "llama3"
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

        response = ollama.chat(
                                model=self.model, 
                                messages=messages)
        
        return response['message']['content']

    def chat(self, chat_history:list[tuple[str,str]]) -> str:
        if self.system_prompt:
            chat_history.insert(0, ('system', self.system_prompt))

        chat_messages = self.parse_history(chat_history)
        response = ollama.chat(
                                model=self.model, 
                                messages=chat_messages)
        
        return response['message']['content']

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