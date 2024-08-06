from termcolor import colored
from src.rag.rag_model import RAGModel
from src.interface.streamlit_incorporation import setup_streamlit, test_final_version 

# setup_streamlit()
# test_final_version()

try:
    while True:
        print(colored("\nHow can I help you? For the end of the conversation please press Ctrl+c", "blue"))
        question = input()
        rag_model = RAGModel(text_retriever_type='step-back')
        print_context = True
        query_types = ['text_data', 'structured_data', 'combined', 'summariser']
        results = rag_model.query(question, query_types)
        print(results)
        # print(colored(("\n\nAnswer:\n\n"), "blue"))
        # print((results["answers"][0]["answer"]))    
        # if print_context:
        #     print(colored("\n\nContext:\n\n", "blue"))
        #     print(context)

except KeyboardInterrupt:
    pass

