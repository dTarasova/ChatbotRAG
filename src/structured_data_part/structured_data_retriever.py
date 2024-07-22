from langchain.agents.agent_types import AgentType
from langchain_experimental.agents.agent_toolkits import create_csv_agent, create_pandas_dataframe_agent
from langchain_openai import ChatOpenAI, OpenAI
from langchain.prompts import ChatPromptTemplate
import chardet
import openai
import os
import pandas as pd


FILE_PATH = "data/napire_data/napire_best2.csv"

class StructuredDataRetriever:
    def __init__(self, data_source=FILE_PATH):
        self.data_source = data_source
        self.df = self.preprocess_data()
        self.agent = self.create_agent()

    def preprocess_data(self):
        # folder_path = "data/napire_data"
        # docs = [file for file in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, file))]
        # print(docs)
        df = pd.read_csv(self.data_source, header=0)
        # with open(self.data_source, 'rb') as rawdata:
        #     result = chardet.detect(rawdata.read(100000))
        #     encoding = result['encoding']
        # df = pd.read_csv(self.data_source, header=0, sep=";", encoding=encoding)

        # cols_df = pd.read_csv("data/napire_data/columns_encoded.csv")
        # rename_dict = dict(zip(cols_df['original_name'], cols_df['webapp_name']))
        # df.rename(columns=rename_dict, inplace=True)
        # df.drop(df.columns[df.columns.str.contains('unnamed|drop', case=False)], axis=1, inplace=True)
        # df.to_csv('napire_best.csv', index=False)
        return df

    def create_agent(self):
        agent = create_pandas_dataframe_agent(
            ChatOpenAI(temperature=0, model="gpt-3.5-turbo-16k"),
            self.df,
            verbose=True,
            agent_type=AgentType.OPENAI_FUNCTIONS ,
            allow_dangerous_code=True
        )
        return agent
    
    def retrieve_context(self, question: str):
        extended_question = f"""
Use the provided DataFrame (df) to answer the question. Ensure that you incorporate up to 10 relevant columns that could add value to your response. Exclude any values such as 'not shown', 'not answered', and similar entries. Here is the question: {question}
"""
        context = self.agent.invoke(extended_question)
        answer = context["output"]
        return answer
    
    
    # def generate_answer():
       

    #     llm = ChatOpenAI(temperature=0)
    #     messages = [("human", question), ("system", template)]
    #     result = llm.invoke(messages)
    #     result.content
   