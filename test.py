import ollama

# Pass the model name and message in the correct order
response = ollama.chat(model="llama2", messages=[{"role": "user", "content": "What is the weather today?"}])

print(response)
