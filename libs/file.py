

def load_document(file):
    import nltk
    nltk.download("punkt")
    from langchain.document_loaders import UnstructuredFileLoader
    loader = UnstructuredFileLoader(file)
    data = loader.load()
    return data
