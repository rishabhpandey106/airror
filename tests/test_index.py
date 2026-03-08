from whoosh.index import open_dir

ix = open_dir("data/index")

with ix.searcher() as searcher:
    print("Total documents:", searcher.doc_count())

    for doc in searcher.all_stored_fields():
        print("\nDOC:")
        print(doc)