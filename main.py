from termcolor import colored

from src.rag.evaluation.generate_test_set import get_contexts
from src.rag.rag_model import RAGModel, RAGTypes
from src.interface.streamlit_incorporation import setup_streamlit 

# setup_streamlit()
#test_final_version()
# TODO: adjust prompts so that it relies more on the context not the general knowledge
try:
    while True:
        print(colored("\nHow can I help you? For the end of the conversation please press Ctrl+c", "blue"))
        question = input()
        rag_model = RAGModel(text_retriever_type='step-back')
        print_context = True
        #query_types=[RAGTypes.TEXT_DATA, RAGTypes.STRUCTURED_DATA, RAGTypes.COMBINED, RAGTypes.SUMMARISER]
        query_types=[RAGTypes.STRUCTURED_DATA]
        results = rag_model.query(question, query_types)
        print(results)
        answer = results["models"][RAGTypes.STRUCTURED_DATA.name]["answer"]
        context = results["models"][RAGTypes.STRUCTURED_DATA.name]["context"]
        evaluation = results["models"][RAGTypes.STRUCTURED_DATA.name]["evaluation"]
        print(evaluation)
        # print(colored(("\n\nAnswer:\n\n"), "blue"))
        # print((results["answers"][0]["answer"]))    
        # if print_context:
        #     print(colored("\n\nContext:\n\n", "blue"))
        #     print(context)

except KeyboardInterrupt:
    pass

