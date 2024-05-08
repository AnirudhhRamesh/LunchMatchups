from .persona import Persona

class Memory:
    
    def __init__(self):
        # An object which stores information about the agent's past interactions & chat history
        self.memory = {}

        #memory:
        # {
        #   "persona_id_1": {
        #       "chat_history": [...],
        #       "data": {...}
        #   },
        #   "persona_id_2": 
        # }

    #GENERAL Methods
    def get(self, persona_id: int):
        return self.memory.get(persona_id, {})

    def save(self, persona_id: int, data:dict):
        self.memory[persona_id] = data

    #FINE-GRAINED Methods
    #CHAT HISTORY Methods
    def get_chat_history(self, persona_id: int):
        return self.memory.get(persona_id, {}).get("chat_history", [])

    def update_chat_history(self, persona_id: int, chat_history: list):
        if persona_id not in self.memory:
            self.memory[persona_id] = {"chat_history": [], "data": {}}
        self.memory[persona_id]["chat_history"] = chat_history

    #OTHER Persona Methods
    def get_data(self, persona_id: int):
        return self.memory.get(persona_id, {}).get("data", {})

    def update_data(self, persona_id: int, data: dict):
        if persona_id not in self.memory:
            self.memory[persona_id] = {"chat_history": [], "data": {}}
        self.memory[persona_id]["data"] = data

