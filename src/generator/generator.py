from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import ChatPromptTemplate


class Generator:
    def __init__(self, type='basic'):
        self.llm = ChatOpenAI(temperature=0)
        self.type = type
    
    def generate_answer(self, question, context):
        prompt = self.get_prompt(question, context)
        chain = prompt | self.llm | StrOutputParser()
        result = chain.invoke({"question": question})
        return result

    
    def get_prompt(self, question, context):
        if self.type == 'basic':
            return self.get_basic_prompt(question, context)
        elif self.type == 'step-back':
            return self.get_step_back_prompt(question, context)
        
    def get_basic_prompt(self, question, context):
        template = f""" ### Instruction ### You are an expert in Requirements Engineering. 
                            Answer the following question with detailed and accurate information. Explain reasoning behind the. 
                            Use the provided context to enhance your response, but if the context does not add value, 
                            you may disregard it. Ensure that your answer directly addresses the user's question.

                            ### Context ###: {context}

                            ### Question ### : {question}""" 

        prompt = ChatPromptTemplate.from_template(template)
        return prompt
    
    def get_step_back_prompt(self, question, context):
        step_back_question = "What is the purpose of the requirement?" ### TODO: find a way to transfer it
        template = f""" ### Instruction ### You are an expert in Requirements Engineering. 
                            Answer the following question with detailed and accurate information. Explain reasoning behind the. 
                            Use the provided context to enhance your response, but if the context does not add value, 
                            you may disregard it. Ensure that your answer directly addresses the user's question.

                            ### Context ###: {context}
                            ### Steb-back question ###: {step_back_question}

                            ### Question ### : {question}""" 

        prompt = ChatPromptTemplate.from_template(template)
        return prompt


            
