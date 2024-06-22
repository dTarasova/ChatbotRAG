from langchain.agents.agent_types import AgentType
from langchain_experimental.agents.agent_toolkits import create_csv_agent, create_pandas_dataframe_agent
from langchain_openai import ChatOpenAI, OpenAI
from langchain.prompts import ChatPromptTemplate
import chardet
import pandas as pd


FILE_PATH = "data/napire_data/data_with_columns.csv"

class StructuredDataRetriever:
    def __init__(self, data_source=FILE_PATH):
        self.data_source = data_source
        self.agent = self.create_agent()

    def create_agent(self):
        with open(self.data_source, 'rb') as rawdata:
            result = chardet.detect(rawdata.read(100000))
            encoding = result['encoding']
        df = pd.read_csv(self.data_source, header=0, sep=";", encoding=encoding)
        df.drop(df.columns[df.columns.str.contains('unnamed',case = False)],axis = 1, inplace = True)
        agent = create_pandas_dataframe_agent(
            ChatOpenAI(temperature=0, model="gpt-3.5-turbo-16k"),
            df,
            verbose=True,
            agent_type=AgentType.OPENAI_FUNCTIONS ,
            allow_dangerous_code=True
        )
        return agent
    
    def retrieve_context(self, question: str):
        context = self.agent.invoke(question)
        answer = context["output"]
        return answer
    
    # def generate_answer():
       

    #     llm = ChatOpenAI(temperature=0)
    #     messages = [("human", question), ("system", template)]
    #     result = llm.invoke(messages)
    #     result.content
   