from langchain.agents.agent_types import AgentType
from langchain_experimental.agents.agent_toolkits import create_csv_agent, create_pandas_dataframe_agent
from langchain_openai import ChatOpenAI, OpenAI
from langchain.prompts import ChatPromptTemplate
import pandas as pd

from src.llm_settings import MODEL, TEMPERATURE



FILE_PATH = "data/napire_data/napire_for_agent.csv"

class StructuredDataRetriever:
    def __init__(self, data_source=FILE_PATH):
        self.data_source = data_source
        self.df = self.preprocess_data()
        self.agent = self.create_agent()

    def preprocess_data(self):
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
            ChatOpenAI(model=MODEL, temperature=TEMPERATURE),
            self.df,
            verbose=True,
            agent_type=AgentType.OPENAI_FUNCTIONS ,
            allow_dangerous_code=True
        )
        return agent
    
    def retrieve_context(self, question: str):
        extended_question = f"""
Use the provided DataFrame (df) to answer the question, 
incorporating up to 10 relevant columns to add value. Summarize the data without giving specific rows or exact values.

If the answer cannot be deduced, reply: 'Sorry, the DataFrame doesn't provide enough information.' 
Exclude placeholder values like 'not shown' or 'not answered.'

Here is the question: {question}. 

"""
        context = self.agent.invoke(extended_question)
        answer = context["output"]
        return answer
    