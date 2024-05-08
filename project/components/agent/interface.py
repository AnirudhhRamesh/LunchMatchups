import json
import csv
from .persona import Persona
from .memory import Memory
from ..llm.interface import LLM
from ..llm.ollama import OllamaLLM

class Agent():
    def __init__(self, data:dict, llm:LLM=None) -> None:
        self.llm: LLM = OllamaLLM() if not llm else llm
        self.persona = Persona(data)
        self.memory = Memory()
        self.llm.set_system_prompt(self.persona.system_prompt())

    def chat(self, chat:str, other_id:int):
        """Query the LLM and store the chat history"""
        user_prompt = ("user", chat)
        
        chat_history = self.memory.get_chat_history(other_id)
        chat_history.append(user_prompt)
        
        response = ("assistant", self.llm.chat(chat_history))

        chat_history.append(response)

        self.memory.update_chat_history(other_id, chat_history)

        return response[1]

    def query(self, prompt:str):
        return self.llm.query(prompt)

    def listen(self, prompt:str, other_id:int):
        """Listen to what the other person says and store to chat history"""
        chat_history = self.memory.get_chat_history(other_id)
        user_prompt = ("user", prompt)
        chat_history.append(user_prompt)
        self.memory.update_chat_history(other_id, chat_history)
        

    def analyze_persona(self, chat_history:list[tuple[str,str]]):
        """Analyze the persona of the other person"""

        chat_history_str = ""

        #Parse the chat history
        for role, message in chat_history:
            if role == "user":
                chat_history_str += f"Them: {message}\n"
            elif role == "assistant":
                chat_history_str += f"You: {message}\n"
        
        prompt = f"""
            Given the following conversation between you and the other person, analyze them and how similar their interests/conversation style matches your personality. Be very critical - if they say harsh things, the conversation is not interesting/fun or you feel uncomfortable, then you will not want to meet them again, then give them a low rating. If otherwise, they held a conversation discussing many of your similar interests or have prior experience/research matching your interests, give them a higher rating. Then return whether or not you would like to meet them again and the reason why. Give a rating from 1-10 where 1 means you never want to meet them again and 10 means you definitely want to meet them. Return your response in JSON format with the keys "reason":"string", "rating":int.
            Here is the conversation: {chat_history_str}
        """

        query = self.llm.query(prompt)

        print(f"Query: {query}")

        # Attempt to extract JSON from the query response
        try:
            # Assuming the JSON object is at the end of the string and starts with '{'
            json_str = query[query.rindex('{'):]
            query_data = json.loads(json_str)
        except (ValueError, IndexError) as e:
            print(f"Failed to parse JSON from query: {e}")
            query_data = {"reason": "Failed to parse response", "rating": 0}

        #Parse the query
        parsed_query = {}
        parsed_query["reason"] = query_data.get("reason", "No reason provided")
        parsed_query["rating"] = query_data.get("rating", 0)
        
        return parsed_query

    def return_rating(self, other_id:int):
        """Return the rating of the other person"""

        persona_analysis = self.analyze_persona(self.memory.get_chat_history(other_id))
        self.memory.update_data(other_id, persona_analysis)

        return self.memory.get_data(other_id)

    @property
    def name(self):
        return self.persona.name

    @property
    def id(self):
        return self.persona.id