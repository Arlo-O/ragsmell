# EXPECT: 0
def answer(retriever, llm, query):
    context = retriever.similarity_search(query)
    return llm.invoke(context)
