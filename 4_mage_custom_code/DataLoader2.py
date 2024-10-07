if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

from mage_ai.data_preparation.shared.secrets import get_secret_value
from mage_ai.data_preparation.variable_manager import get_global_variable
from elasticsearch import Elasticsearch
import pandas as pd

@data_loader
def retrieve_from_elasticsearch(**kwargs):
    # 获取存储的查询
    # query = get_global_variable('query_memory', 'current_query')
    query="What health issues do dogs commonly experience?"
    if not query:
        raise ValueError("No query found in memory. Please set a query in the Memory block first.")

    print(f"Executing query: {query}")

    # 获取 Elasticsearch 连接信息
    es_host = 'my-elastic-search'
    es_port =  '9200'
    
    # 连接到 Elasticsearch
    es = Elasticsearch([f"http://{es_host}:{es_port}"])
    
    # 获取之前创建的索引名称
    index_name = get_global_variable('seraphic_mythos', 'index_name')
    if not index_name:
        raise ValueError("Index name not found. Ensure the data_exporter block has run.")
    
    # 准备查询
    es_query = {
        "query": {
            "multi_match": {
                "query": query,
                "fields": ["Question", "Answer", "Category"]
            }
        }
    }
    
    # 执行搜索
    response = es.search(index=index_name, body=es_query)
    
    # 提取结果
    results = [
        {
            "id": hit['_source']['id'],
            "score": hit['_score'],
            "Question": hit['_source'].get('Question', '')[:200],  # 增加到前200个字符
            "Answer": hit['_source'].get('Answer', ''),
            "Category": hit['_source'].get('Category', '')
        }
        for hit in response['hits']['hits']
    ]
    
    # 将结果转换为 DataFrame
    df = pd.DataFrame(results)
    
    # 打印查询结果摘要
    print(f"Found {len(df)} results for query: '{query}'")
    print("Top 3 document IDs:")
    for _, row in df.head(3).iterrows():
        print(f"- {row['id']} (score: {row['score']:.2f})")
    
    return df



@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'