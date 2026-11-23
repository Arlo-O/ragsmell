# EXPECT: 0
def answer(llm, query, logger):
    try:
        return llm.invoke(query)
    except Exception as error:
        logger.error(error)
        raise
