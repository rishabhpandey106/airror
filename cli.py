# import argparse
# from parser.error_parser import ErrorParser
# from search.bm25_search import HybridSearch
# from index.build_index import build_index
# import os

# INDEX_DIR = "data/index"


# def ensure_index():

#     if not os.path.exists(INDEX_DIR) or not os.listdir(INDEX_DIR):

#         print("Index not found. Building index...")

#         build_index(".")

#         print("Index created successfully.")


# def main():

#     parser = argparse.ArgumentParser(
#         description="AI Debug Code Search"
#     )

#     parser.add_argument(
#         "error",
#         nargs="?",
#         help="Error message"
#     )

#     args = parser.parse_args()

#     ensure_index()

#     if args.error:
#         error_message = args.error
#     else:
#         error_message = input("Paste error message:\n")

#     parser_engine = ErrorParser()

#     parsed = parser_engine.parse(error_message)

#     query = parsed["query"]

#     print("\nGenerated Query:", query)

#     search = HybridSearch()

#     results = search.search(query)

#     for r in results:

#         print("\n--- RESULT ---")

#         print("Function:", r.get("function_name"))
#         print("File:", r.get("file_path"))
#         print("Lines:", r.get("start_line"), "-", r.get("end_line"))

#         print("\nCode:\n")
#         print(r.get("code_snippet"))


# if __name__ == "__main__":
#     main()

import argparse
from parser.error_parser import ErrorParser
from search.bm25_search import HybridSearch
from index.build_index import build_index
import os


def ensure_index(project_path):

    index_dir = os.path.join(project_path, ".debug_index")

    if not os.path.exists(index_dir):

        print("Building index for project...")

        build_index(project_path)

        print("Index created.")


def main():

    parser = argparse.ArgumentParser(description="Debug Code Search")

    parser.add_argument(
        "--project",
        default=".",
        help="Path to project"
    )

    parser.add_argument(
        "error",
        nargs="?",
        help="Error message"
    )

    args = parser.parse_args()

    ensure_index(args.project)

    if args.error:
        error_message = args.error
    else:
        error_message = input("Paste error message:\n")

    ep = ErrorParser()

    parsed = ep.parse(error_message)

    query = parsed["query"]

    print("\nGenerated Query:", query)

    # IMPORTANT CHANGE
    search = HybridSearch(args.project)

    results = search.search(query)

    for r in results:

        print("\n--- RESULT ---")

        print("Function:", r.get("function_name"))
        print("File:", r.get("file_path"))
        print("Line:", r.get("line_number"))

        print("\nCode:\n")
        print(r.get("code_snippet"))


if __name__ == "__main__":
    main()