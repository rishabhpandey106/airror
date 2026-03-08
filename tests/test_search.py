from search.bm25_search import HybridSearch

search = HybridSearch()

results = search.search("validate_token TypeError missing argument function parameter")

for r in results:
    print("\n--- RESULT ---")
    print(r["function_name"])
    print(r["file_path"])
    print(r["code_snippet"])