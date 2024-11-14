

from src.interface.streamlit_incorporation import setup_streamlit 
setup_streamlit()
###################################
# Example usage
# from src.logging_extractor import process_log_file


# input_file = 'log_entries.txt'  # Replace with your input .txt file path
# output_file = 'output.tex'      # Replace with your desired output .tex file path
# process_log_file(input_file, output_file)


#################################
# from src.rag.retriever.unstructured_data_loading.document_database import DocumentDatabaseFaiss
# path_db = 'knowledge_bases/amdire_napire_software4kmu_faiss'
# path_data = 'data/amdire_napire_software4kmu'
# documentDatabase = DocumentDatabaseFaiss(path_to_db_directory=path_db)
# # vector_store = documentDatabase.create_db(path_data)
# # # documentDatabase.add_docs_from_folder(path_data)
# vector_store = documentDatabase.get_vectorstore()
# documentDatabase.print_vectorstore_collections()
# documents = documentDatabase.check_findings("Abbotts textual analysis technique")
# documents2 = documentDatabase.check_findings("However, a first step towards the definition of an artefact-based methodology for a company-wide use consists in the precise definition of the artefacts and their relationsbeing of interest for a particular development process, in our case for RE")


############################################
# from src.interface.helper_functions import load_questions
# from src.rag.rag_model import RAGModel, RAGTypes
# from termcolor import colored

# questions = load_questions()
# rag_model = RAGModel(text_retriever_type='step-back', evaluate_answers=True)

# for i, question in enumerate(questions):
#     print(colored(f"Question: {question}", "blue"))
#     results = rag_model.query(question, query_types=[RAGTypes.GPT, RAGTypes.COMBINED, RAGTypes.SUMMARISER])
#     print("Question # ", i, " processed. ")

############################################

# from termcolor import colored
# from src.rag.rag_model import RAGModel, RAGTypes

# TODO: adjust prompts so that it relies more on the context not the general knowledge
# try:
#     while True:
#         print(colored("\nHow can I help you? For the end of the conversation please press Ctrl+c", "blue"))
#         question = input()
#         rag_model = RAGModel(text_retriever_type='step-back')
#         print_context = True
#         query_types=[RAGTypes.TEXT_DATA, RAGTypes.STRUCTURED_DATA, RAGTypes.COMBINED, RAGTypes.SUMMARISER]
#         #query_types=[RAGTypes.STRUCTURED_DATA]
#         results = rag_model.query(question, query_types)
#         print(results)
#         answer = results["models"][RAGTypes.STRUCTURED_DATA.name]["answer"]
#         context = results["models"][RAGTypes.STRUCTURED_DATA.name]["context"]
#         evaluation = results["models"][RAGTypes.STRUCTURED_DATA.name]["evaluation"]
#         print(evaluation)
#         # print(colored(("\n\nAnswer:\n\n"), "blue"))
#         # print((results["answers"][0]["answer"]))    
#         # if print_context:
#         #     print(colored("\n\nContext:\n\n", "blue"))
#         #     print(context)

# except KeyboardInterrupt:
#     pass

