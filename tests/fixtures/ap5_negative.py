# EXPECT: 0
try:
    llm.invoke(question)
except Exception as error:
    logger.error(error)
    raise
