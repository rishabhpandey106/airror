class ContextRetriever:

    def get_context(self, file_path, line_number, window=20):
        try:
            # if isinstance(file_path, list):
            #     if not file_path:
            #         return None
            #     file_path = file_path[0]

            with open(file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()

            start = max(0, line_number - window)
            end = min(len(lines), line_number + window)

            snippet = "".join(lines[start:end])

            return {
                "function_name": "context_window",
                "file_path": file_path,
                "line_number": line_number,
                "code_snippet": snippet
            }

        except Exception as e:
            print("Context retrieval error:", e)
            return None