import edgedb
import pandas as pd
from db_operations.insert_data import insert_into_edgedb

def create_client():
    return edgedb.create_client()

def close_client(client):
    client.close()

def load_data():
    df = pd.read_csv("/Users/yangyue/Downloads/Fragrantica.csv")
    client = create_client()
    insert_into_edgedb(df, client)
    close_client(client)