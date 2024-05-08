
import json
import csv
import re
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
        self.llm.set_system_prompt(self.persona.system_prompt())

        user_prompt = ("user", chat)
        
        chat_history = self.memory.get_chat_history(other_id)
        chat_history.append(user_prompt)
        
        response = ("assistant", self.llm.chat(chat_history))

        chat_history.append(response)

        self.memory.update_chat_history(other_id, chat_history)

        return response[1]

    def query(self, prompt:str):
        self.llm.set_system_prompt(self.persona.system_prompt())

        return self.llm.query(prompt)

    def listen(self, prompt:str, other_id:int):
        self.llm.set_system_prompt(self.persona.system_prompt())

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
            You are a very strict and judgy person. You are very selective with the people you would like to speak/talk with.
            You are only interested in talking with people who share very similar passions/experiences/interests as you.
            Given the following conversation between you and another person, give a short reason whether or not you would like to talk to them again. 
            Then provide a number rating from 1-10 where 1 means you never want to meet them again and 10 means you definitely want to meet them.

            Your output should be in the format of "Rating: /10, 'reason'"
            Here is the conversation: {chat_history_str}
        """

        query = self.llm.query(prompt)

        #Parse the query

        #Take the first number to appear in the string, otherwise return 5
        rating:int = int(query.split(" ")[0]) if query.split(" ")[0].isdigit() else -1

        pattern = r"Rating: (\d+)"
        match = re.search(pattern, query)
        
        rating:int = -1
        if match:
            rating = match.group(1)
            print("Rating:", rating)
        else:
            print("No rating found.")

        reason:str = query

        parsed_query = {"rating": rating, "reason": reason}
        
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