if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test
import io
import requests
import pandas as pd




@data_loader
def load_data(*args, **kwargs):
    """
    Template code for loading data from any source.

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    # Specify your data loading logic here
     # GitHub raw content URL
    url = "https://raw.githubusercontent.com/wufengyou/Pet-Care-RAG-Application/main/0_dataset/Dog-Cat-QA.csv"
    
    # 如果需要访问私有仓库，可以使用 GitHub token
    # github_token = get_secret_value('GITHUB_TOKEN')
    # headers = {'Authorization': f'token {github_token}'}
    # response = requests.get(url, headers=headers)
    
    response = requests.get(url)
    response.raise_for_status()  # 如果请求失败则抛出异常
    
    # 读取 CSV 内容
    df = pd.read_csv(io.StringIO(response.text))
    
    # 创建 categories 列表
    categories = ['D']*20 + ['C']*382 + ['B']*17 + ['D']*152 + ['B']*12
    
    # 添加 Category 列
    df['Category'] = categories
    
    # 创建 category_mapping
    category_mapping = {
        'D': 'Dog',
        'C': 'Cat',
        'B': 'Dog,Cat'
    }
    
    # 应用 mapping
    df['Category'] = df['Category'].map(category_mapping)
    
    # 打印唯一的 categories
    print("Unique categories:", df['Category'].unique())
    result = df.to_dict('records')
    return result


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'