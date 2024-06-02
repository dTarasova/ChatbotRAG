# from chains import review_chain
import keyboard
from chatbot import hospital_agent_executor

# question = """Has anyone complained about cleanliness of the place"""
# answer = review_chain.invoke(question)
# print(answer)



# answer = hospital_agent_executor.invoke(
#     {"input": "What is the current wait time at hospital C?"}
# )
# answer =  hospital_agent_executor.invoke(
#     {"input": "What have patients said about their comfort at the hospital?"}
# )
# print(answer)

# while True:
#     print("How can I help you? For the end of the conversation please press q")
#     if keyboard.is_pressed("q"):
#         # Key was pressed
#         break
#     else:
#         question = input()
#         answer =  hospital_agent_executor.invoke( {"input": question} )
#         print(answer) 


try:
    while True:
        print("/nHow can I help you? For the end of the conversation please press Ctrl+c")
        question = input()
        answer =  hospital_agent_executor.invoke( {"input": question} )
        print(answer) 
except KeyboardInterrupt:
    pass
