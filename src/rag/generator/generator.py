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
#             SystemMessage(
#                 content=(
#                     """	
#                     ### Instruction ###
# You are an expert text analyst and researcher. Select 5-10 most relevant sentences to the qusetion. Your task is to produce 
# an extractive summary of the provided context that is relevant to the accompanying question.
#                     """
#                 )
#             ),
            SystemMessage(
                content=(
                    """	
                    ### Instruction ###
You are a specialized assistant in extracting highly relevant information from large contexts.
Your task is to retrieve the most important details that directly respond to the user's query.

Focus only on information that is directly relevant.
Omit any unrelated, redundant, or excessive details.
Condense longer sections without losing key meaning or important facts.
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

    def generate_summary_structured(self, context, question):
        prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessage(
                content=(
                    """	
                    ### Instruction ###
You will be provided with a user query about requirements engineering and relevant context gathered from dataframe insights on how companies conduct requirements engineering in the real world.

Your task is to select points from the context that are relevant to the user question. Please use approximate percentages instead of exact values when presenting the insights. If no relevant context is provided, say 'No relevant context found'.
                    """
                )
            ),
            AIMessage(content=f"### Context ###\n{context}\n"),
            HumanMessage(content=f"### Question ###\n{question}\n")
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

        # prompt = ChatPromptTemplate.from_messages(
        #     [
        #         SystemMessage(
        #             content=(
        #               """### Instruction ### You are an expert in Requirements Engineering.
        #                     Answer the following question with detailed and accurate information. Explain reasoning behind the.
        #                     Use the provided context to enhance your response, but if the context does not add value,
        #                     you may disregard it. Ensure that your answer directly addresses the user's question. """
        #             )
        #         ),
        #         HumanMessage(f" ### Question ### : {question}"),
        #         AIMessage( content=f" ### Context ###: {context}")
        #     ]
        # )

        prompt = ChatPromptTemplate.from_messages(
            [
                # SystemMessage(
                #     content=(
                    #   """### Instruction ### 
                    #   You are an expert in Requirements Engineering.
                    #         Using the information contained in the context, 
                    #         give a comprehensive elaborate structured answer to the question. 
                    #         Respond only to the question asked, response should be concise and relevant to the question.
                    #         If the answer cannot be deduced from the context, do not give an answer."""
                #     )
                # ),
                SystemMessage(
                    content=(
                      """### Instruction ### 
                      You are an expert in Requirements Engineering.
                    Using the following context, provide a structured and well-organized response that directly addresses the query. 
                    Ensure that the response incorporates the key information from the context without introducing irrelevant or unsupported details. 
                    The answer should be clear, concise, and formatted as follows:

                    Introduction: Briefly summarize the main point of the response.
                    Details: Provide supporting information or evidence from the context to back up the response.
                    Conclusion: Conclude by summarizing the key takeaway based on the context."""
                    )
                ),
                HumanMessage(content=f"""
                                    ### Context ###: {context}, 
                                    ---
                                    Now here is the question you need to answer: 

                                    Question : {question}
                                    """)
            ]
        )
        return prompt

    def get_structured_data_prompt(self, question, context):

        # prompt = ChatPromptTemplate.from_messages(
        #     [
        #         SystemMessage(
        #             content=( """	
        #               ### Instruction ### You are an expert in Requirements Engineering.
        # Given the statistical information from the provided data frame (df), answer the following question with detailed and accurate information.
        #  Ensure that your explanation is clear and understandable. Use ratios instead of concrete values in your response.

        # Start your answer with the line "According to the data, ..."""
        #             )
        #         ),
        #         HumanMessage(f" ### Question ### : {question}"),
        #         AIMessage( content=f" ### Context ###: {context}")
        #     ]
        # )

        prompt = ChatPromptTemplate.from_messages(
            [
                SystemMessage(
                    content=(
                      """### Instruction ### 
                      You are an expert in Requirements Engineering.
                            Using the information contained in the context about df data, 
                            give a comprehensive answer to the question. 
                            Respond only to the question asked, response should be concise and relevant to the question.
                            Use ratios instead of concrete values in your response
                            If the answer cannot be deduced from the context, do not give an answer.
                            Start your answer with the line "According to the practical data, ..."""
                    )
                ),
                HumanMessage(content=f"""
                                    ### Context ###: {context}, 
                                    ---
                                    Now here is the question you need to answer: 

                                    Question : {question}
                                    """)
            ]
        )
        return prompt
    
    def get_combined_prompt(self, question, context):
        # prompt = ChatPromptTemplate.from_messages(
        #     [
        #         SystemMessage(
        #             content=(
        #               """### Instruction ### You are an expert in Requirements Engineering.
        #                     Answer the following question with detailed and accurate information. Explain reasoning behind the answer.
        #                     Select the most relevant parts of the provided context and use it to enhance your response. Ensure that your answer directly addresses the user's question. """
        #             )
        #         ),
        #         HumanMessage(f" ### Question ### : {question}"),
        #         AIMessage( content=f" ### Context ###: {context}")
        #     ]
        # )

        prompt = ChatPromptTemplate.from_messages(
            [
                SystemMessage(
                    content=(
                    #   """### Instruction ### 
                    #         You are an expert in Requirements Engineering.
                    #         Using the information contained in the context, 
                    #         give a comprehensive elaborate structured answer to the question. 
                    #         Respond only to the question asked, response should be concise and relevant to the question.
                    #         If the answer cannot be deduced from the context, do not give an answer."""
#                                           """### Instruction ### 
#                     You are an expert in Requirements Engineering. 
#                     Using the provided information, deliver a structured and well-organized response 
#                     to the query. Incorporate key details without introducing irrelevant information 
#                     or unnecessary references to the source. 
#                     The answer should be clear, concise, and structured as follows:

#                    Answer: Give short presise answer to the question.
# Details: Present supporting information from the given details in a structured way, include explanations, examples."""

"""### Instruction ###
As an expert in Requirements Engineering, your task is to generate a well-structured and organized response to the given query using the provided context. Your response should seamlessly integrate key information from the context. Refrain from using explicit phrases that reference the context itself. Follow the specific format outlined below:

**Answer**: Deliver a clear and direct answer to the question.
**Details**: Present supporting information drawn from the context, including relevant explanations and examples. Improve readability of this part by breaking it down into smaller sections.
"""
                    )
                ),
                HumanMessage(content=f"""
                                    ### Context ###: {context}, 
                                    ---
                                    Now here is the question you need to answer: 

                                    Question : {question}
                                    """)
            ]
        )

        return prompt
