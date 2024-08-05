from langchain_core.documents.base import Document

class ResultsRanker:
    def __init__(self, cutoff_number=5):
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
    def __init__(self, k=60, cutoff_number=5):
        super().__init__(cutoff_number)
        self.k = k
        self.length_weight = 0.01

    def rank(self, results: list[Document]):

        fused_scores = {}
        for rank, doc in enumerate(results):

            doc_key = (doc.page_content, frozenset(doc.metadata.items()))

            if doc_key not in fused_scores.keys():
                fused_scores[doc_key] = 0

            fused_scores[doc_key] += (1 / (rank + self.k)) * (1 + self.length_weight * len(doc.page_content))


        reranked_results = [
            (doc_key, score)
            for doc_key, score in sorted(fused_scores.items(), key=lambda x: x[1], reverse=True)
        ]

        reranked_documents = [
            Document(page_content=doc_key[0], score=score, metadata=dict(doc_key[1]))
            for doc_key, score in reranked_results
        ]

        return reranked_documents
