# EXPECT: 1
def build_prompt():
    prompt = "This is a deliberately long prompt used by a function that also contains control logic and should be externalized for maintainability."
    if True:
        return prompt
