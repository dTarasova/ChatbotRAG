import os
import openai
import pandas as pd

from src.wo_rag import get_openai_answer

def improve_column_name(column_name):
    print(column_name)
    prompt = f"Improve the following column name for better readability and clarity. Give only new column name. For every quality attribute / problem / etc. give name. Ignore questions {column_name} "
    # response = openai.Completion.create(
    #     engine="text-davinci-003",
    #     prompt=prompt,
    #     max_tokens=10,
    #     n=1,
    #     stop=None,
    #     temperature=0.5,
    # )
    improved_name = get_openai_answer(prompt)
    print(improved_name)
    #improved_name = response.choices[0].text.strip()
    return improved_name


def improve_column_names(df):
    # Improve column names using OpenAI
    new_column_names = {}
    for col in df.columns:
        new_column_names[col] = improve_column_name(col)

    # Rename the columns in the DataFrame
    df.rename(columns=new_column_names, inplace=True)

    return df

def improve_csv_quality(file_path, new_file_path):
    # Load the CSV file into a DataFrame
    df = pd.read_csv(file_path)

    # Improve the column names
    new_df = improve_column_names(df)

    # Save the new DataFrame to a CSV file
    new_df.to_csv(new_file_path, index=False)

    # Print the new DataFrame
    print(new_df.head())
