from pymilvus import MilvusClient, DataType
import ast
import pandas as pd

client = MilvusClient(
    uri="http://localhost:19530"
)

try:
    client.drop_collection("open_api_embeddings")
except Exception as e:
    print(e)

client.create_collection(
    collection_name="open_api_embeddings",
    dimension=1536, # length for embeddings vector
    auto_id=True
)

try:
    df = pd.read_csv("/Users/nardoarevalo/Desktop/pandas_learning/notebooks/openai_embeddings/data.csv")
except Exception as e:
    print("loading from web!")
    df = pd.read_csv("https://raw.githubusercontent.com/nardoguy14/jupyter_notebooks/main/notebooks/openai_embeddings/data.csv")
df['embeddings'] = df['embeddings'].apply(ast.literal_eval)

df['vector'] = df['embeddings']
df.drop(['embeddings'], axis=1, inplace=True)


new_order = ['vector', 'text', 'embeddings_type']
df['embeddings_type'] = "covered_california_insurance"
df_reordered = df[new_order]
data = df_reordered.to_dict(orient='records')

res = client.insert(
    collection_name="open_api_embeddings",
    data=data
)