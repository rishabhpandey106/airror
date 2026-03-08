import re
from typing import Dict, List


class ErrorParser:
    """
    Parses error messages and extracts structured information
    useful for code search.
    """

    ERROR_PATTERN = r"([A-Za-z]+Error)"
    FUNCTION_PATTERN = r"in ([a-zA-Z_][a-zA-Z0-9_]*)"
    FILE_PATTERN = r'File "([^"]+)"'
    LINE_PATTERN = r"line (\d+)"

    def parse(self, error_message: str) -> Dict:
        """
        Main parsing pipeline.
        """

        error_type = self.extract_error_type(error_message)
        functions = self.extract_function_names(error_message)
        files = self.extract_file_paths(error_message)
        lines = self.extract_line_numbers(error_message)
        keywords = self.extract_keywords(error_message)

        query = self.build_query(
            error_type,
            functions,
            files,
            keywords
        )

        return {
            "error_type": error_type,
            "functions": functions,
            "files": files,
            "lines": lines,
            "keywords": keywords,
            "query": query
        }

    def extract_error_type(self, text: str) -> str:
        """
        Extract error type (TypeError, ValueError etc.)
        """

        match = re.search(self.ERROR_PATTERN, text)

        if match:
            return match.group(1)

        return ""

    def extract_function_names(self, text: str) -> List[str]:
        """
        Extract function names from stacktrace.
        """

        matches = re.findall(self.FUNCTION_PATTERN, text)

        return list(set(matches))

    def extract_file_paths(self, text: str) -> List[str]:
        """
        Extract file paths from traceback.
        """

        matches = re.findall(self.FILE_PATTERN, text)

        return list(set(matches))

    def extract_line_numbers(self, text: str) -> List[int]:
        """
        Extract line numbers from traceback.
        """

        matches = re.findall(self.LINE_PATTERN, text)

        return list(set(int(x) for x in matches))

    def extract_keywords(self, text: str) -> List[str]:
        """
        Extract meaningful keywords from error message.
        """

        text = text.lower()

        text = re.sub(r"[^a-zA-Z0-9_ ]", " ", text)

        words = text.split()

        stopwords = {
            "the", "a", "an", "is", "in", "to",
            "of", "for", "and", "with", "required",
            "file", "line", "most", "recent",
            "call", "last", "traceback"
        }

        keywords = [w for w in words if w not in stopwords and len(w) > 2]

        return list(set(keywords))

    def build_query(
        self,
        error_type: str,
        functions: List[str],
        files: List[str],
        keywords: List[str]
    ) -> str:
        """
        Build optimized search query.
        """

        tokens = []

        if error_type:
            tokens.append(error_type)

        tokens.extend(functions)

        for f in files:
            tokens.append(f.split("/")[-1])  # only filename

        tokens.extend(keywords)

        # remove duplicates
        tokens = list(set(tokens))

        return " ".join(tokens)