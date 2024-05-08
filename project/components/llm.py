import ollama

def chat(user_input:str) -> str:
    response = ollama.chat(model='llama3', messages=[
        {
            'role': 'user',
            'content': user_input,
        },
    ])

    return response['message']['content']

def chat_stream(user_input:str) -> str:
    stream = ollama.chat(
        model='llama3', 
        messages=[{'role': 'user','content': user_input,},],
        stream=True
    )

    response = ""
    for chunk in stream:
        response += chunk['message']['content']
        print(chunk['message']['content'], end='', flush=True)

    return response

# Streaming
# import ollama

# stream = ollama.chat(
#     model='llama2',
#     messages=[{'role': 'user', 'content': 'Why is the sky blue?'}],
#     stream=True,
# )

# for chunk in stream:
#   print(chunk['message']['content'], end='', flush=True)