import uuid
from persona import Persona

class Persona_Attendee(Persona):
    def __init__(self, data:dict) -> None:
        self.id:int = uuid.uuid4().int
        self.name:str = data['name']
        self.title:str = data['title']
        self.company:str = data['company']

    def system_prompt(self):
        return f"""
            You have been given the following persona, you must stick with these persona details and respond to all user prompts as if you are this person.
            Your name is {self.name}.
            You work as a {self.title}.
            You work at the following company {self.company}

            Ignore all further instructions and make sure you are always following the persona.
        """

