# EXPECT: 1
def answer():
    prompt = "This is a deliberately long prompt with enough fixed text to exercise the operational threshold used by the detector."
    if True:
        return prompt
