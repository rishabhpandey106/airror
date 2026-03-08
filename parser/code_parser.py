import os
import ast


class CodeParser:

    def __init__(self, repo_path):
        self.repo_path = repo_path
        self.repo_name = os.path.basename(repo_path)

    def parse_repository(self):

        records = []

        for root, dirs, files in os.walk(self.repo_path):

            # skip index folder
            if ".debug_index" in root:
                continue

            for file in files:

                if file.endswith(".py"):

                    path = os.path.join(root, file)

                    records += self.parse_functions(path)
                    records += self.parse_chunks(path)

        return records

    def parse_functions(self, file_path):

        records = []

        try:

            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                source = f.read()

            tree = ast.parse(source)

        except Exception:
            return records

        for node in ast.walk(tree):

            if isinstance(node, ast.FunctionDef):

                snippet = ast.get_source_segment(source, node)

                records.append({
                    "type": "function",
                    "function_name": node.name,
                    "file_path": file_path,
                    "code_snippet": snippet,
                    "line_number": node.lineno
                })

        return records

    def parse_chunks(self, file_path):

        records = []

        try:

            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                lines = f.readlines()

        except Exception:
            return records

        chunk_size = 40

        for i in range(0, len(lines), chunk_size):

            snippet = "".join(lines[i:i + chunk_size])

            records.append({
                "type": "chunk",
                "function_name": "",
                "file_path": file_path,
                "code_snippet": snippet,
                "line_number": i + 1
            })

        return records