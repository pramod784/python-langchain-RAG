from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

llm = ChatOllama(model="mistral")
set_role = input("Hey User, Im Jarveis personal assistant of Pramod. Set the role for me, What I can help you with: ")
userinput = input("Ask me a question: ")
messages = [
    SystemMessage(content=f"Your name is Jarvis. Your role is: {set_role}"),
    HumanMessage(content=userinput),
]

response = llm.invoke(messages)
print(response.content)

# Continue conversation
messages.append(AIMessage(content=response.content))
messages.append(HumanMessage(content="Show me an example"))

# response2 = llm.invoke(messages)
# print(response2.content)

for chunk in llm.stream(messages):
    print(chunk.content, end="", flush=True)

print()

