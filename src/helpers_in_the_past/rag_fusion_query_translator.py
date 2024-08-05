"""
We can now put it all together and define the full chain. This chain:

1. Generates a bunch of queries
2. Looks up each query in the retriever
3. Joins all the results together using reciprocal rank fusion

https://towardsdatascience.com/forget-rag-the-future-is-rag-fusion-1147298d8ad1
"""


import helpers_in_the_past.prompts as prompts
import helpers_in_the_past.retriever_generator as retriever_generator
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain.load import dumps, loads
from operator import itemgetter
from wo_rag import get_openai_answer
from json import dumps, loads
from operator import itemgetter

def create_query_pipeline():
    prompt_rag_fusion = prompts.get_rag_fusion_prompt()
    return (
        prompt_rag_fusion 
        | ChatOpenAI(temperature=0)
        | StrOutputParser() 
        | (lambda x: x.split("\n"))
    )

def apply_reciprocal_rank_fusion(results: list[list], k=60):
    """Applies Reciprocal Rank Fusion (RRF) to a list of ranked documents."""
    
    fused_scores = {}

    for docs in results:
        for rank, doc in enumerate(docs):
            doc_str = dumps(doc.page_content)
            if doc_str not in fused_scores:
                fused_scores[doc_str] = 0
            fused_scores[doc_str] += 1 / (rank + k)

    reranked_results = [
        (loads(doc), score)
        for doc, score in sorted(fused_scores.items(), key=lambda x: x[1], reverse=True)
    ]

    return reranked_results

def setup_retrieval_chain():
    retriever = retriever_generator.get_retriever()
    query_pipeline = create_query_pipeline()
    return query_pipeline | retriever.map() | apply_reciprocal_rank_fusion

def setup_rag_chain(retrieval_chain):
    prompt = prompts.get_basic_rag_prompt()
    llm = ChatOpenAI(temperature=0)
    
    return (
        {"context": retrieval_chain, 
         "question": itemgetter("question")} 
        | prompt
        | llm
        | StrOutputParser()
    )

def main():
    question = "Is the requirement 'System should be secure' good?"

    retrieval_chain_rag_fusion = setup_retrieval_chain()
    final_rag_chain = setup_rag_chain(retrieval_chain_rag_fusion)

    print("\n\nAnswer with RAG:")
    result = final_rag_chain.invoke({"question": question})
    print(result)

    get_openai_answer(question)

if __name__ == "__main__":
    main()


    


""""
TODO: Experiment1 - simple repeat 
[(Document(page_content='3! Information System Requirements..................................................................................... 11!\n3.1! Actors .......................................................................................................................... 11!', metadata={'author': '', 'creationDate': 'D:20161201030720Z', 'creator': 'LaTeX with hyperref package', 'file_path': 'data/first_batch\\Artefact-based Requirements Engineering The AMDiRE Approach.pdf', 'format': 'PDF 1.5', 'keywords': '', 'modDate': 'D:20161201030720Z', 'page': 13, 'producer': 'pdfTeX-1.40.12', 'source': 'data/first_batch\\Artefact-based Requirements Engineering The AMDiRE Approach.pdf', 'subject': '', 'title': '', 'total_pages': 48, 'trapped': ''}), 0.04839549075403121), (Document(page_content='by a system and specify how the system is intended to be used in interaction', metadata={'author': '', 'creationDate': 'D:20161201030720Z', 'creator': 'LaTeX with hyperref package', 'file_path': 'data/first_batch\\Artefact-based Requirements Engineering The AMDiRE Approach.pdf', 'format': 'PDF 1.5', 'keywords': '', 'modDate': 'D:20161201030720Z', 'page': 15, 'producer': 'pdfTeX-1.40.12', 'source': 'data/first_batch\\Artefact-based Requirements Engineering The AMDiRE Approach.pdf', 'subject': '', 'title': '', 'total_pages': 48, 'trapped': ''}), 0.03333333333333333), 

TODO: Experiment2 - use only page_content
still horrible, but fusiomn scores a bit higher 

TODO: Expertiment3 - Enhanced prompt. Not what I was hoping for. 
Certainly! Here’s an improved version of the prompt:

---

"Answer the following question using the provided context to enhance the detail and accuracy of your response. If the context does not contribute to a better answer, you may ignore it:

Context: {context}

Question: {question}"

Yes, the requirement 'System should be secure' is a good requirement. In the context provided, there are mentions of system quality requirements and architectural constraints, indicating the importance of ensuring 
the security of the system. Security is a crucial aspect of any information system to protect data, prevent unauthorized access, and maintain the integrity of the system. Therefore, including a requirement for the 
system to be secure is essential for its overall functionality and reliability.


TODO: Experiment 4 - add role to instruction
Instruction: You are an expert in Requirements Engineering. Answer the following question with detailed and accurate information. Use the provided context to enhance your response, but if the context does not add value, you may disregard it. Ensure that your answer directly addresses the user's question.

Context: {context}

Question: {question}


Result - very good. BUT - only because of the . Still the quality of received documents sucks. However,
general ansewr become much better . 

However - it did mention unamiguity, other criteria that contributes a lot. BUT examples are quite the same 

The requirement "System should be secure" is a good starting point, but it is not specific 
or detailed enough to be considered a complete requirement in the context of Requirements Engineering.
In Requirements Engineering, requirements need to be clear, unambiguous, and measurable to ensure 
that they can be effectively implemented and tested. Therefore, a more detailed and specific 
requirement related to security would be beneficial.
For example, a more comprehensive security requirement could include aspects such as 
encryption protocols to be used, access control mechanisms, authentication requirements, 
data protection measures, compliance with specific security standards or regulations, 
and regular security audits or penetration testing.
By providing more specific details and criteria, stakeholders and development 
teams can have a clearer understanding of what is expected in terms of security for the system, 
leading to a more robust and secure final product.

\n Answer without RAG :
'The requirement "System should be secure" is a good starting point, but it is not specific enough. 
It is important to define what aspects of security are required for the system, such as 
data encryption, access control, authentication mechanisms, and vulnerability management. 
Additionally, it is important to specify any compliance standards or regulations that 
the system needs to adhere to in terms of security. By providing more detailed and specific security
 requirements, the development team can better understand and implement the necessary measures 
 to ensure the system is secure.
"""