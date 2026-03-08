from whoosh.index import open_dir
from whoosh.qparser import MultifieldParser, OrGroup
import os

# INDEX_DIR = "data/index"


class HybridSearch:

    def __init__(self, project_path):

        index_dir = os.path.join(project_path, ".debug_index")

        self.ix = open_dir(index_dir)

    def search(self, query, k=10):

        results_list = []

        with self.ix.searcher() as searcher:

            parser = MultifieldParser(
                ["function_name", "code_snippet", "file_path"],
                schema=self.ix.schema,
                group=OrGroup
            )

            q = parser.parse(query)

            results = searcher.search(q, limit=k)

            for r in results:

                results_list.append(dict(r))

        return results_list