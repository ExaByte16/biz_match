import pinecone as pn
from langchain.embeddings import OpenAIEmbeddings
import pandas as pd
import tomli

# Get environment variables
with open("config.toml", mode="rb") as fp:
    config = tomli.load(fp)

# This will held the functions to be used in the backend of the app


# Returns df with the results of the query
def get_business(query):
    print("The query is: ", query)
    # Get OpenAI embeddings
    openai_embeddings = OpenAIEmbeddings(openai_api_key=config["OPENAI_API_KEY"])
    # Emmbed question
    query_embedding = openai_embeddings.embed_query(query)

    # Initializee Pinecone
    pn.init(api_key=config["PINECONE_API_KEY"], environment="us-west4-gcp")

    # Get pinecone index
    index_name = "intelliflex-1536-1"
    intelliflex_index = pn.Index(index_name)

    print("The index initialized is: ", intelliflex_index)

    # Define current namespace
    bizmatch_namespace = "biz_match"

    # Get Info from the index
    res = intelliflex_index.query(
        vector=query_embedding,
        top_k=10,
        namespace=bizmatch_namespace,
        include_values=True,
        include_metadata=True,
    )

    # Create list of dicts to convert to df
    list_of_dicts = []

    # print results
    for i, record in enumerate(res["matches"]):
        business_uid = record["id"]
        print("The results are " + business_uid + str(record["metadata"]))
        metadata = record["metadata"]
        list_of_dicts.append(metadata)

    df = pd.DataFrame(list_of_dicts)

    return df
