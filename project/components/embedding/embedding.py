import csv
import streamlit as st
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import PCA

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


#DUMMY DATASET
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

emma_data = {
        "id": 2,
        "name": "Emma",
        "uni": "MIT",
        "studies": "BSc Data Science",
        "sph": False,
        "experiences": "AI/ML Software Engineer @ Apple, Autonomous Navigation Software Engineer @ Tesla, Research Intern @ Deepmind",
        "biggest_achievement": "During my undergrad I grinded AI/ML courses and started doing projects early on. This allowed me to intern in 3 top companies in my dream positions where I learn so much about software engineering and applied ML.",
        "biggest_failure": "During a coursework, due to my heavy workload I was unable to contribute to help out my teammmates that much - felt really bad like a burden to them.",
        "success_definition": "Having the time and space to focus entirely on myself and studying what fascinates me - not everyone has this luxury.",
        "hobbies": "Climbing definitely. I recently tried doing some muscle pump too."
}

# persons = [arnie_data, alice_data, emma_data]


#REAL DATASET
persons=[]

with open("data/lunch_submissions.csv", 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        persons.append(row)

# Preprocess data
concatenated_strings = [f"{p['name']} : {p['uni']} : {p['studies']} : {p['sph']} : {p['experiences']} : {p['biggest_achievement']} : {p['biggest_failure']} : {p['success_definition']} : {p['hobbies']}" for p in persons]

# Embed data
model = SentenceTransformer('all-MiniLM-L6-v2')
embeddings = model.encode(concatenated_strings)

# Perform dimensionality reduction using PCA
pca = PCA(n_components=3)
reduced_embeddings = pca.fit_transform(embeddings)

# Create a 3D plot
fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection='3d')

# Plot data points
for i, person in enumerate(persons):
    ax.scatter(reduced_embeddings[i, 0], reduced_embeddings[i, 1], reduced_embeddings[i, 2], label=person['name'])

# Set plot labels and title
ax.set_xlabel('PC1')
ax.set_ylabel('PC2')
ax.set_zlabel('PC3')
ax.set_title('Person Embeddings in 3D Space')

# Add a legend
ax.legend()

# Streamlit app
def main():
    st.title("Person Embeddings Visualization")
    
    # Display the plot using Streamlit
    st.pyplot(fig)
    
    # Calculate similarity
    query_sentence = st.text_input("Enter a query sentence:")
    if query_sentence:
        query_embedding = model.encode([query_sentence])
        similarities = cosine_similarity(query_embedding, embeddings)
        
        # Retrieve most similar person
        most_similar_index = similarities.argmax()
        most_similar_person = persons[most_similar_index]
        
        st.subheader("Most Similar Person")
        st.write(most_similar_person)

if __name__ == '__main__':
    main()