from fastapi import FastAPI

from api.schemas import DebugRequest, DebugResponse
from parser.error_parser import ErrorParser
from search.bm25_search import HybridSearch
from llm.explain import LLMExplainer
from search.context_retrieval import ContextRetriever

app = FastAPI(title="StackTrace AI")

# initialize components
error_parser = ErrorParser()
search_engine = HybridSearch()
context = ContextRetriever()
llm = LLMExplainer(provider="gemini")


@app.get("/")
def root():
    return {"message": "StackTrace AI running"}


@app.post("/debug", response_model=DebugResponse)
def debug_error(request: DebugRequest):

    parsed = error_parser.parse(request.error)

    snippets = []

    # priority 1: stacktrace context
    if parsed["files"] and parsed["lines"]:

        context_snippet = context.get_context(
            parsed["files"][0],
            parsed["lines"][0]
        )

        if context_snippet:
            snippets.append(context_snippet)

    # fallback to search
    if not snippets:

        query = parsed["query"]

        snippets = search_engine.search(query)

    llm_result = llm.explain(request.error, snippets)

    return DebugResponse(
        function=llm_result.get("function"),
        file=llm_result.get("file"),
        explanation=llm_result.get("explanation"),
        suggested_fix=llm_result.get("suggested_fix")
    )