import uvicorn
import random

from server.api import app

from project.components.data_loaders.csv_loader import CSVLoader

from project.components.llm.groq import GroqLLM
from project.components.agent.interface import Agent

from project.Simulation import Simulation
from project.Embedder import Embedder
from project.InPrompt import run_inprompt

def main():

    #FLAGS
    simulation_flag = True
    embeddings_flag = False
    inprompt_flag = False

    llama3_8b = "llama3-8b-8192"
    llama3_70b = "llama3-70b-8192"
    
    #DUMMY Dataset:
    arnie_data = {
            "id": 1,
            "name": "Arnie Ramesh",
            "uni": "ETH Zurich",
            "studies": "MSc Computer Science",
            "sph": True,
            "experiences": "iOS App Developer@Sleepiz, Host of AmbitiousxDriven Newsletter, SDE Intern at Amazon",
            "biggest_achievement": "Creating a 20 000 Revenue clothing enterprise at age 15",
            "biggest_failure": "Not finding my passion earlier during my bachelors",
            "success_definition": "Working I'm truly passionate about that will make impact in the world",
            "hobbies": "I used to go climbing in Lausanne, but now it's mostly just gym and studying Deeplearning.ai ML concepts"
        }

    alice_data = {
            "id": 2,
            "name": "Alice",
            "uni": "Trinity College Dublin",
            "studies": "PhD Politics and Law",
            "sph": False,
            "experiences": "European Union Intern, United Nations Intern, Political Candidate for Dublin Country",
            "biggest_achievement": "I wrote a legislation which got passed and implemented that banned studying computer science after 5pm",
            "biggest_failure": "Not implementing enough AI regulations in the European Union",
            "success_definition": "Being able to implement as many regulations as possible",
            "hobbies": "Reading books about law, watching law movies"
    }

    dataset = [arnie_data, alice_data]

    dataset = CSVLoader("data/lunch_submissions.csv")

    if simulation_flag:
        simulation = Simulation(llm=GroqLLM(model=llama3_8b))
        simulation.load_users(dataset.users(count=2))
        simulation.run_simulation()
        ratings = simulation.get_ratings()
        print(ratings)
    
    if embeddings_flag:
        embedder = Embedder(dataset.users())
        embeddings = embedder.embed()
        embedder.render(embeddings)

    if inprompt_flag:
        response = run_inprompt()

if __name__ == "__main__":
    main()
    # uvicorn.run(app, host="0.0.0.0", port=8000)
