# test of litellm support for Ollama testbed

from litellm import completion, embedding 
import numpy as np

response = completion(
    model="ollama_chat/hf.co/MaziyarPanahi/Mistral-7B-Instruct-v0.3-GGUF:Q8_0",

)

from litellm import completion

response = completion(
    model="ollama_chat/hf.co/MaziyarPanahi/Mistral-7B-Instruct-v0.3-GGUF:Q8_0", 
    messages=[{ "content": "what is the capital of hawaii","role": "user"}], 
    api_base="http://localhost:11434"
)
print(response)

embedding_response = embedding(
    model="ollama/nomic-embed-text", 
    input=["hello world", "goodbye world"], 
    api_base="http://localhost:11434"
)

print(np.array([x["embedding"] for x in embedding_response.data]).shape)