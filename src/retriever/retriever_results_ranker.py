from json import loads, dumps
from  langchain_core.documents.base import Document

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
    def __init__(self, k=60):
        self.k = k
        ResultsRanker.__init__(self)

    def rank(self, results: list[Document]):
        fused_scores = {}

        for rank, doc in enumerate(results):
            doc_str = dumps(doc.page_content)
            if doc_str not in fused_scores:
                fused_scores[doc_str] = 0
            fused_scores[doc_str] += 1 / (rank + self.k)

        reranked_results_contents = [
            (loads(doc), score)
            for doc, score in sorted(fused_scores.items(), key=lambda x: x[1], reverse=True)
        ]
        reranked_results = [Document(page_content=doc, score=score) for doc, score in reranked_results_contents]

        return reranked_results