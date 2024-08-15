from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.prompts import HumanMessagePromptTemplate
from src.llm_settings import MODEL, TEMPERATURE

#todo: adjust prompts so that concrete values are not shown
#todo: rely more on the context in textual data prompts
class Generator:
    def __init__(self):
        self.llm = ChatOpenAI(model=MODEL, temperature=TEMPERATURE)

    def generate_answer(self, question, context, prompt_type='combined'):
        prompt = self.get_prompt(question, context, prompt_type)
        chain = prompt | self.llm | StrOutputParser()
        result = chain.invoke({"question": question})
        return result

    def get_prompt(self, question, context, prompt_type):
        if prompt_type == 'text_data':
            return self.get_text_data_prompt(question, context)
        elif prompt_type == 'structured_data':
            return self.get_structured_data_prompt(question, context)
        elif prompt_type == 'combined':
            return self.get_combined_prompt(question, context)
        
    def generate_summary(self, context, question):
        prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessage(
                content=(
                    """	
                    ### Instruction ###
                    You are the best summarizer. Given the context, summarize it to answer the question directly. 
                    Provide a concise and accurate summary without adding any additional information.
                    """
                )
            ),
            AIMessage(content=f"### Context ###\n{context}\n"),
            AIMessage(content=f"### Question ###\n{question}\n")
        ]
    )
    
    # Create the chain and invoke it
        try:
            chain = prompt | self.llm | StrOutputParser()
            result = chain.invoke({})
        except Exception as e:
            raise RuntimeError(f"Error generating summary: {e}")
        
        # Return the result
        return result


    def get_text_data_prompt(self, question, context):

        prompt = ChatPromptTemplate.from_messages(
            [
                SystemMessage(
                    content=(
                      """### Instruction ### You are an expert in Requirements Engineering.
                            Answer the following question with detailed and accurate information. Explain reasoning behind the.
                            Use the provided context to enhance your response, but if the context does not add value,
                            you may disregard it. Ensure that your answer directly addresses the user's question. """
                    )
                ),
                HumanMessage(f" ### Question ### : {question}"),
                AIMessage( content=f" ### Context ###: {context}")
            ]
        )
        return prompt

    def get_structured_data_prompt(self, question, context):

        prompt = ChatPromptTemplate.from_messages(
            [
                SystemMessage(
                    content=( """	
                      ### Instruction ### You are an expert in Requirements Engineering.
        Given the statistical information from the provided data frame (df), answer the following question with detailed and accurate information.
         Ensure that your explanation is clear and understandable. Use ratios instead of concrete values in your response.

        Start your answer with the line "According to the data, ..."""
                    )
                ),
                HumanMessage(f" ### Question ### : {question}"),
                AIMessage( content=f" ### Context ###: {context}")
            ]
        )
        return prompt
    
    def get_combined_prompt(self, question, context):
        prompt = ChatPromptTemplate.from_messages(
            [
                SystemMessage(
                    content=(
                      """### Instruction ### You are an expert in Requirements Engineering.
                            Answer the following question with detailed and accurate information. Explain reasoning behind the answer.
                            Select the most relevant parts of the provided context and use it to enhance your response. Ensure that your answer directly addresses the user's question. """
                    )
                ),
                HumanMessage(f" ### Question ### : {question}"),
                AIMessage( content=f" ### Context ###: {context}")
            ]
        )
        return prompt
