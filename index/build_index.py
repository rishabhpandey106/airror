import os
from whoosh.index import create_in
from parser.code_parser import CodeParser
from index.schema import get_schema


# INDEX_DIR = "data/index"


def build_index(repo):

    INDEX_DIR = os.path.join(repo, ".debug_index")

    if not os.path.exists(INDEX_DIR):
        os.makedirs(INDEX_DIR)

    schema = get_schema()

    ix = create_in(INDEX_DIR, schema)

    writer = ix.writer()

    parser = CodeParser(repo)

    records = parser.parse_repository()

    for r in records:

        writer.add_document(
            type=r["type"],
            function_name=r["function_name"],
            file_path=r["file_path"],
            code_snippet=r["code_snippet"],
            line_number=r["line_number"]
        )

    writer.commit()

    print("Indexed records:", len(records))

# build_index("repos/sample_repo")