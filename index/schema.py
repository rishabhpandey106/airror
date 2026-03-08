from whoosh.fields import Schema, TEXT, ID, NUMERIC


def get_schema():

    return Schema(

        type=TEXT(stored=True),

        function_name=TEXT(stored=True),

        file_path=ID(stored=True),

        code_snippet=TEXT(stored=True),

        line_number=NUMERIC(stored=True)
    )