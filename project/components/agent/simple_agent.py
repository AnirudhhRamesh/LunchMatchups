from .interface import Agent

class SimpleAgent(Agent):

    def __init__(self, data:str) -> None:
        super().__init__(data)

    def chat(self):
        return super().chat()

    def query(self):
        return super().query()

    def load_data():
        pass