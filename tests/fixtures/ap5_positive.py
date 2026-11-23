# EXPECT: 1
try:
    llm.invoke(question)
except Exception:
    pass
