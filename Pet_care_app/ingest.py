import pandas as pd
import minsearch
import os

DATA_PATH = os.getenv("DATA_PATH", "data/update_category.csv")

def load_index(data_path=DATA_PATH):
    df = pd.read_csv(data_path)
    documents = df.to_dict(orient='records')
    index = minsearch.Index(
        text_fields=["Question", "Answer","Category"],
        keyword_fields=['id'])
    index.fit(documents)
    return index

if __name__ == "__main__":
    load_index()
