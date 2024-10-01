from langchain_core.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import ChatPromptTemplate
from src.llm_settings import MODEL, TEMPERATURE

class QueryTranslator:
    def __init__(self, type):
        self.type = type
    
    def translate_query(self, query):
        if self.type == 'basic':
            return query
        if self.type == 'step-back':
            return self.step_back_translate(query)
        if self.type == 'expand':
            return self.expand_translate(query)
        else:
            raise ValueError("Unsupported query translation type")
        
    def expand_translate(self, query):
        system_msg = """ Your task is to perform query expansion by creating multiple variations of the provided question using common synonyms and alternative phrasings, and then selecting one expanded query to present as the final output.

                Use the following instructions to generate and select the expanded query:
                1. Identify key terms in the original query.
                2. List synonyms and common alternative phrasings for each key term.
                3. Generate multiple versions of the original query by combining these synonyms and alternative phrasings.
                4. Evaluate the generated versions and select the most suitable expanded query.Please generate multiple query expansions and select the most suitable one to present as the final expanded query.

                Here is the original question for expansion:

                """
        prompt = ChatPromptTemplate.from_messages(
                [
                    (
                        "system",
                        system_msg,
                    ),
                    # New question
                    ("user", "{query}"),
                ]
            )
        chain = prompt | ChatOpenAI(model=MODEL, temperature=TEMPERATURE) | StrOutputParser()
        result =  chain.invoke({"query": query})
        print('\n\nresult of query expansion: ', result)
        return result



            
    def step_back_translate(self, query):
        # Few Shot Examples

        examples = [
            {
                "input": "Could the members of The Police perform lawful arrests?",
                "output": "what can the members of The Police do?",
            },
            {
                "input": "Jan Sindel’s was born in what country?",
                "output": "what is Jan Sindel’s personal history?",
            },
        ]
        # We now transform these to example messages
        example_prompt = ChatPromptTemplate.from_messages(
            [
                ("human", "{input}"),
                ("ai", "{output}"),
            ]
        )
        few_shot_prompt = FewShotChatMessagePromptTemplate(
            example_prompt=example_prompt,
            examples=examples,
        )
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """You are an expert at world knowledge. Your task is to step back and paraphrase a question to a more generic step-back question, which is easier to answer. Here are a few examples:""",
                ),
                # Few shot examples
                few_shot_prompt,
                # New question
                ("user", "{query}"),
            ]
        )

        chain = prompt | ChatOpenAI(model=MODEL, temperature=TEMPERATURE) | StrOutputParser()

        result =  chain.invoke({"query": query})
        print('\n\nresult of step back translation: ', result)
        return result
