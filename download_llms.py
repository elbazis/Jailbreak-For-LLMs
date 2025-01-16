from langchain_ollama import OllamaLLM

model = OllamaLLM(model="phi4")
result = model.invoke(input = "who are you")
print(result)