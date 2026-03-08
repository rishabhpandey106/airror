from llm.explain import LLMExplainer

snippets = [
    {
        "function_name": "validate_token",
        "file_path": "auth.py",
        "line_number": 10,
        "code_snippet": """
def validate_token(token, secret):
    if token != secret:
        raise Exception("Invalid token")
"""
    }
]

error = "TypeError: validate_token() missing 1 required argument"

explainer = LLMExplainer(provider="gemini")

result = explainer.explain(error, snippets)

print(result)