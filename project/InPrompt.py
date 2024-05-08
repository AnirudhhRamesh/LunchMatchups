import csv

from project.components.llm.interface import LLM
from project.components.llm.groq import GroqLLM
from project.components.llm.ollama import OllamaLLM

def run_inprompt():
    llama3_8b = "llama3-8b-8192"
    llama3_70b = "llama3-70b-8192"

    llm:LLM = OllamaLLM(model="llama3")
    llm:LLM = GroqLLM(model=llama3_70b)

    persons=[]

    with open("data/lunch_submissions.csv", 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            row_str = ", ".join(row)
            persons.append(row_str)

    persons = persons[0:20] #TODO Vary the count
    persons_str = "\n".join(persons)

    person = "Arnie Ramesh"
    response = llm.query(
        f"""
        Here is a list of ambitious people who filled out a form for lunch/dinner at the mensa in groups of 4: {persons_str}
        Who are the 3 people that share the most common amibition, experience and research/tech fields to {person} that, that {person} would want to meet and discuss?
        """
    )

    print(response)

    return response