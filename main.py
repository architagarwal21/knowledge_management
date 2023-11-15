import pandas as pd
from db_operations.connection import create_client
from db_operations.insert_data import insert_into_edgedb

def main():
    df = pd.read_csv("/Users/yangyue/Downloads/Fragrantica.csv")
    client = create_client()
    insert_into_edgedb(df, client)

if __name__ == "__main__":
    main()
