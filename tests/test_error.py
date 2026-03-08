from parser.error_parser import ErrorParser

parser = ErrorParser()

error = "TypeError: parse_file() missing 1 required argument"

result = parser.parse(error)

print(result)