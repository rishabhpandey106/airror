from parser.code_parser import CodeParser

parser = CodeParser("repos/sample_repo")

records = parser.parse_repository()

for r in records:
    print(r)
    