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
            return step_back_translate(query)
        else:
            raise ValueError("Unsupported query translation type")
        
def step_back_translate(query):
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
