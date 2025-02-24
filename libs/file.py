

def load_document(file):
    from langchain.document_loaders import UnstructuredFileLoader
    loader = UnstructuredFileLoader(file)
    data = loader.load()
    return data
