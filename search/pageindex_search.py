import os
from whoosh.index import open_dir
from whoosh.qparser import MultifieldParser, OrGroup


class PageIndexSearch:

    def __init__(self, project_path):

        index_dir = os.path.join(project_path, ".debug_index")

        self.ix = open_dir(index_dir)

    def compute_page_score(self, record, query_tokens):

        score = 0

        function_name = (record.get("function_name") or "").lower()
        file_path = (record.get("file_path") or "").lower()
        code = (record.get("code_snippet") or "").lower()

        for token in query_tokens:

            token = token.lower()

            if token in function_name:
                score += 5

            if token in file_path:
                score += 3

            if token in code:
                score += 1

        return score

    def search(self, query, k=10):

        results_list = []

        tokens = query.split()

        with self.ix.searcher() as searcher:

            parser = MultifieldParser(
                ["function_name", "code_snippet", "file_path"],
                schema=self.ix.schema,
                group=OrGroup
            )

            q = parser.parse(query)

            results = searcher.search(q, limit=50)

            for r in results:

                record = dict(r)

                page_score = self.compute_page_score(record, tokens)

                record["page_score"] = page_score

                results_list.append(record)

        # rank by page score
        ranked = sorted(
            results_list,
            key=lambda x: x["page_score"],
            reverse=True
        )

        return ranked[:k]