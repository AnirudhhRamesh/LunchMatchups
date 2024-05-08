import random
import csv
from .components.agent.interface import Agent
from .components.llm.interface import LLM

class Simulation:
    def __init__(self, llm:LLM):
        self.current_iteration = 0
        self.llm = llm

    #Load all the agents
    def load_users(self, file_path:str, size:int):
        agents = []
        
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)

            for row in reader:
                if size == 0:
                    break
                agent = Agent(row, self.llm)
                agents.append(agent)
                size -= 1

        self.agents = agents

    def run_simulation(self):
        """Logic to make agents communicate goes here"""
        
        prompts = [
        "Here is the current discussion topic: Give a quick intro of yourself", 
        "Here is the current discussion topic: Given your experience, try start a conversation with each other. If you can't start a conversation, then say you are not interested in a conversation", 
        "Here is the current discussion topic: If there's anything else interesting to talk about discuss it. Otherwise, if you're not interested at all in each other then, tell them this was awkward and you're not interested in speaking with each other"]

        for i in range(len(self.agents)):
            for j in range(i+1, len(self.agents)):
                if i == j:
                    continue
            #Randomly set the order of the agents
            rand = random.randint(0, 1)
            if rand:
                first = self.agents[i]
                second = self.agents[j]
            else:
                first = self.agents[j]
                second = self.agents[i]

            for prompt in prompts:
                first_response = first.chat(prompt, second.id)
                second_response = second.chat(prompt + f". Here is {first.name}'s response: {first_response}", second.id)
                first.listen(second_response, second.id)

                print(f"{first.name} said: {first_response}")
                print(f"{second.name} said: {second_response}")
                print()

    def get_ratings(self):
        all_agent_ratings = []
        for agent in self.agents:
            current_agent_ratings = []
            for other_agent in self.agents:
                if agent == other_agent:
                    continue
                current_agent_ratings.append((other_agent.id, other_agent.name, agent.return_rating(other_agent.id)))
            all_agent_ratings.append((agent.id, agent.name, current_agent_ratings))
        
        for agent_ratings in all_agent_ratings:
            print(f"{agent_ratings[1]}'s ratings: {agent_ratings[2]}")
