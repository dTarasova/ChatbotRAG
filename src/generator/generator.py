from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import ChatPromptTemplate


class Generator:
    def __init__(self):
        self.llm = ChatOpenAI(temperature=0)
    
    def generate_answer(self, question, context):
        # prompt = self.get_prompt(question, context)
        # print("\n\nAnswer with RAG:")
        # result = self.llm.invoke(prompt)
        # print(result)
        prompt = self.get_prompt(question, context)
        chain = prompt | self.llm | StrOutputParser()
        result = chain.invoke({"question": question})
        return result
    # def generate_answer(self):
        # final_rag_chain = (
        # prompt
        # | self.llm
        # | StrOutputParser()
        # )
        # print("\n\nAnswer with RAG:")
        # result = final_rag_chain.invoke({"question": prompt})
        # print(result)
        # return result
    
    def get_prompt(self, question, context):
        template = f""" ### Instruction ### You are an expert in Requirements Engineering. 
                    Answer the following question with detailed and accurate information. Explain reasoning behind the. 
                    Use the provided context to enhance your response, but if the context does not add value, 
                    you may disregard it. Ensure that your answer directly addresses the user's question.

                    ### Context ###: {context}

                    ### Question ### : {question}""" 

        prompt = ChatPromptTemplate.from_template(template)
        print('\n\nPrompt:\n\n', prompt)
        return prompt

            
