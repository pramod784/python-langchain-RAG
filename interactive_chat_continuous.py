from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

llm = ChatOllama(model="mistral")

set_role = input("Hey User, I'm Jarvis, personal assistant of Pramod. Set the role for me: ")

messages = [
    SystemMessage(content=f"Your name is Jarvis. Your role is: {set_role}")
]

print("\n🤖 Jarvis: Ready! (type 'exit' to quit)\n")

MAX_HISTORY = 10  # Keep last 10 messages + system message

while True:
    user_input = input("You: ").strip()
    
    if user_input.lower() in ['exit', 'quit', 'bye', 'q']:
        print("🤖 Jarvis: Goodbye!")
        break
    
    if not user_input:
        continue
    
    messages.append(HumanMessage(content=user_input))
    
    print("🤖 Jarvis: ", end="", flush=True)
    
    full_response = ""
    for chunk in llm.stream(messages):
        print(chunk.content, end="", flush=True)
        full_response += chunk.content
    
    print("\n")
    
    messages.append(AIMessage(content=full_response))
    
    # Keep only system message + last MAX_HISTORY messages
    if len(messages) > MAX_HISTORY + 1:
        messages = [messages[0]] + messages[-(MAX_HISTORY):]