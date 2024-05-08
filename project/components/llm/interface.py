
class LLM:
    def __init__(self, model=None) -> None:
        self.model = model
        self.system_prompt = ""

    def query(self, prompt:str) -> str:
        return NotImplementedError("The subclass must implement this interface!")

    def chat(self, chat_history:list[tuple[str,str]]) -> str:
        return NotImplementedError("The subclass must implement this interface!")

    @staticmethod
    def parse_history(chat_history:list[tuple[str,str]]):
        return NotImplementedError("The subclass must implement this interface!")

    def set_system_prompt(self, system_prompt:str):
        self.system_prompt = system_prompt
        return NotImplementedError("The subclass must implement this interface!")