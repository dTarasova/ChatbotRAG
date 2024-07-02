from langchain_core.documents.base import Document
from json import loads, dumps

class ResultsRanker:
    def __init__(self, cutoff_number=3):
        self.cutoff_number = cutoff_number

    def get_results(self, results):
        ranked_results = self.rank(results)
        top_results = self.cutoff(ranked_results)
        return top_results
    
    def cutoff(self, results):
        return results[:self.cutoff_number]
    
    def rank(self, results):
        return results
    

class RRFResultsRanker(ResultsRanker):
    def __init__(self, k=60, cutoff_number=3):
        super().__init__(cutoff_number)
        self.k = k

    def rank(self, results: list[Document]):
    
        # fused_scores = {}

        # for rank, doc in enumerate(results):
        #     #todo: add metadata to the document
        #     doc_str = doc.page_content
        #     if doc_str not in fused_scores.keys():
        #         fused_scores[doc_str] = 0
        #     fused_scores[doc_str] += 1 / (rank + self.k)

        # reranked_results = [
        #     (doc_str, score)
        #     for doc_str, score in sorted(fused_scores.items(), key=lambda x: x[1], reverse=True)
        # ]

        # reranked_documents = [Document(page_content=doc, score=score, metadata=doc.metadata) for doc, score in reranked_results]

        # return reranked_documents

        fused_scores = {}

        for rank, doc in enumerate(results):
            #todo: add metadata to the document
            if doc not in fused_scores.keys():
                fused_scores[doc] = 0
            fused_scores[doc] += 1 / (rank + self.k)

        reranked_results = [
            (doc, score)
            for doc, score in sorted(fused_scores.items(), key=lambda x: x[1], reverse=True)
        ]

        reranked_documents = [Document(page_content=doc.page_content, score=score, metadata=doc.metadata) for doc, score in reranked_results]

        return reranked_documents