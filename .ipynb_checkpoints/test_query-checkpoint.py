import os
from langchain.vectorstores.chroma import Chroma
from langchain.embeddings import OpenAIEmbeddings

os.environ['OPENAI_API_KEY'] = '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'
embeddings = OpenAIEmbeddings()
db = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)

while True:

    query = input('QUERY: ')
    print('')

    best_match = db.similarity_search(query)[:5]

    for match in best_match:
        try:
            print(f"title: {match.metadata['title']}")
        except:
            pass
        try:
            print(f"source: {match.metadata['source']}")
        except:
            pass
        try:
            print(f"date: {match.metadata['date']}")
        except:
            pass
        print('')
