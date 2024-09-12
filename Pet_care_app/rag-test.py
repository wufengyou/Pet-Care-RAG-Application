import pandas as pd
import minsearch

def load_data():
    df=pd.read_csv('../data/update_category.csv')
    documents = df.to_dict(orient='records')
    index = minsearch.Index(
        text_fields=["Question", "Answer","Category"],
        keyword_fields=['id'])
    index.fit(documents)
    return index





# In[ ]:





# In[9]:


index.fit(documents)


# ## RAG flow

# In[10]:


from openai import OpenAI
client = OpenAI()


# In[11]:


def search(query):
    boost = {}

    results = index.search(
        query=query,
        filter_dict={},
        boost_dict=boost,
        num_results=10
    )

    return results


# In[ ]:





# In[12]:


response = client.chat.completions.create(
    model='gpt-4o-mini',
    messages=[{"role": "user", "content": q}]
)

print(response.choices[0].message.content)


# In[34]:





# In[12]:


query = 'which dog breed is the most friendly?'


# In[17]:


search_results=search(query)
print(search_results, len(search_results))


# In[14]:


from openai import OpenAI
client = OpenAI()


# In[16]:


prompt_template = """
You are a knowledgeable pet care expert specializing in dogs and cats. 
Answer the USER QUESTION based on the INFORMATION from our pet care database. 
Use only the facts from the INFORMATION when answering the USER QUESTION. 
If the information doesn't provide a complete answer, 
say so and suggest seeking professional veterinary advice.

USER QUESTION: {question}

INFORMATION:
{context}
""".strip()

entry_template = """
Question: {Question}
Answer: {Answer}
Category: {Category}
""".strip()


def build_pet_care_prompt(query, search_results): 
    context = ""
    
    for doc in search_results:
        context = context + entry_template.format(**doc)+"\n\n"
    
    prompt = prompt_template.format(question=query, context=context).strip()
    return prompt


# In[19]:


print(build_pet_care_prompt(query, search_results))


# In[20]:


def llm(prompt,model='gpt-4o-mini'):
    response = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response.choices[0].message.content


# In[18]:


# len(documents)


# In[21]:


def rag(query,model='gpt-4o-mini'):
    search_results = search(query)
    prompt = build_pet_care_prompt(query, search_results)
    answer = llm(prompt,model=model)
    return answer


# In[22]:


query = 'What traits define the personality of sporting dog breeds'
answer=rag(query)
print(answer)


# In[ ]:





# In[56]:


#rename first column to 'id'


# In[23]:


df.head()


# In[58]:


# update df back to file


# In[28]:


# df=pd.read_csv('Dog-Cat-QA.csv')


# In[24]:


df.head(),len(df)


# In[25]:


query="What are the signs of stress in cats and dogs?"
answer=rag(query)
print(answer)


# ## Retrieval evaluation 

# In[26]:


df_questions=pd.read_csv('../data/ground-truth-retrieval.csv')  
df_questions.head()


# In[27]:


len(df_questions)


# In[28]:


ground_truth = df_questions.to_dict(orient='records')


# In[29]:


ground_truth[0]


# In[31]:


def hit_rate(relevance_total):
    cnt = 0

    for line in relevance_total:
        if True in line:
            cnt = cnt + 1

    return cnt / len(relevance_total)

def mrr(relevance_total):
    total_score = 0.0

    for line in relevance_total:
        for rank in range(len(line)):
            if line[rank] == True:
                total_score = total_score + 1 / (rank + 1)

    return total_score / len(relevance_total)


# In[41]:


def minsearch_search(query):
    boost = {}

    results = index.search(
        query=query,
        filter_dict={},
        boost_dict=boost,
        num_results=10
    )

    return results


# In[43]:


def evaluate(ground_truth, search_function):
    relevance_total = []

    for q in tqdm(ground_truth):
        doc_id = q['id']
        results = search_function(q)
        relevance = [d['id'] == doc_id for d in results]
        relevance_total.append(relevance)

    return {
        'hit_rate': hit_rate(relevance_total),
        'mrr': mrr(relevance_total),
    }


# In[44]:


from tqdm.auto import tqdm


# In[54]:


# previous uncategorized results
evaluate(ground_truth, lambda q: minsearch_search(q['question'] ))


# In[35]:


evaluate(ground_truth, lambda q: minsearch_search(q['question'] ))


# In[45]:


evaluate(ground_truth, lambda q: minsearch_search(q['question'] ))


# ### Finding the best parameters
# 

# In[38]:


df_validation=df_questions[:100]
df_test=df_questions[100:]


# In[36]:


import random

def simple_optimize(param_ranges, objective_function, n_iterations=10):
    best_params = None
    best_score = float('-inf')  # Assuming we're minimizing. Use float('-inf') if maximizing.

    for _ in range(n_iterations):
        # Generate random parameters
        current_params = {}
        for param, (min_val, max_val) in param_ranges.items():
            if isinstance(min_val, int) and isinstance(max_val, int):
                current_params[param] = random.randint(min_val, max_val)
            else:
                current_params[param] = random.uniform(min_val, max_val)
        
        # Evaluate the objective function
        current_score = objective_function(current_params)
        
        # Update best if current is better
        if current_score > best_score:  # Change to > if maximizing
            best_score = current_score
            best_params = current_params
    
    return best_params, best_score


# In[39]:


gt_val = df_validation.to_dict(orient='records')


# In[46]:


def minsearch_search(query, boost=None):
    if boost is None:
        boost = {}

    results = index.search(
        query=query,
        filter_dict={},
        boost_dict=boost,
        num_results=10
    )

    return results


# In[47]:


param_ranges = {
    'Question': (0.0, 3.0),
    'Answer': (0.0, 3.0),
    'Category': (0.0, 3.0),
}

def objective(boost_params):
    def search_function(q):
        return minsearch_search(q['question'], boost_params)

    results = evaluate(gt_val, search_function)
    return results['mrr']


# In[48]:


simple_optimize(param_ranges, objective, n_iterations=20)


# In[49]:


def minsearch_improved(query):
    boost = {
        'Question': 1.133,
        'Answer': 2.518,
        'Category': 1.123,
    }

    results = index.search(
        query=query,
        filter_dict={},
        boost_dict=boost,
        num_results=10
    )

    return results

evaluate(ground_truth, lambda q: minsearch_improved(q['question']))


# ### RAG evaluation

# In[50]:


prompt2_template = """
You are an expert evaluator for a RAG system.
Your task is to analyze the relevance of the generated answer to the given question.
Based on the relevance of the generated answer, you will classify it
as "NON_RELEVANT", "PARTLY_RELEVANT", or "RELEVANT".

Here is the data for evaluation:

Question: {question}
Generated Answer: {answer_llm}

Please analyze the content and context of the generated answer in relation to the question
and provide your evaluation in parsable JSON without using code blocks:

{{
  "Relevance": "NON_RELEVANT" | "PARTLY_RELEVANT" | "RELEVANT",
  "Explanation": "[Provide a brief explanation for your evaluation]"
}}
""".strip()


# In[51]:


len(ground_truth)


# In[52]:


record = ground_truth[0]


# In[53]:


import json


# In[56]:


df_sample = df_questions.sample(n=200, random_state=1)
df_sample


# In[61]:


sample= df_sample.to_dict(orient='records')


# In[63]:


type(sample),len(sample)


# In[70]:


# evaluations = []

# for record in tqdm(sample):
#     print(record['question'])


# In[71]:


evaluations = []

for record in tqdm(sample):
    question = record['question']
    answer_llm = rag(question) 

    prompt = prompt2_template.format(
        question=question,
        answer_llm=answer_llm
    )

    evaluation = llm(prompt)
    evaluation = json.loads(evaluation)

    evaluations.append((record, answer_llm, evaluation))


# In[72]:


df_eval = pd.DataFrame(evaluations, columns=['record', 'answer', 'evaluation'])

df_eval['id'] = df_eval.record.apply(lambda d: d['id'])
df_eval['question'] = df_eval.record.apply(lambda d: d['question'])

df_eval['relevance'] = df_eval.evaluation.apply(lambda d: d['Relevance'])
df_eval['explanation'] = df_eval.evaluation.apply(lambda d: d['Explanation'])

del df_eval['record']
del df_eval['evaluation']


# In[73]:


df_eval.relevance.value_counts(normalize=True)


# In[74]:


df_eval.to_csv('../data/rag-eval-gpt-4o-mini.csv', index=False)


# In[75]:


df_eval[df_eval.relevance == 'NON_RELEVANT']


# In[77]:


df[df.id == 510]

