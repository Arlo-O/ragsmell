# EXPECT: 1
def answer(llm, query):
    try:
        return llm.invoke(query)
    except Exception:
        return None
