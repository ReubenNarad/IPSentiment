import requests
import uuid
from bs4 import BeautifulSoup
from langchain.vectorstores.chroma import Chroma
from langchain.embeddings import OpenAIEmbeddings
from tqdm.auto import tqdm
from langchain_core.documents import Document

def scrape_cnn(date):

    # URL of the webpage
    url = f'https://www.cnn.com/middleeast/live-news/israel-hamas-war-gaza-news-{date}/index.html'

    # Send a GET request to the URL
    response = requests.get(url)

    # Parse the HTML content using Beautiful Soup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all article sections, which have class "sc-bwzfXH"
    articles = soup.find_all(class_='sc-bwzfXH')

    docs = []

    # Extract and print the contents of the elements
    for element in articles:
        content = element.find('div', class_="post-content-rendered")
        header = element.find('h2', class_="kvaBeP")
        if header:
            text = content.get_text(separator='', strip=True)
            metadata = {
                "title": header.text,
                "date": date,
                "source": "CNN",
                "link": url
            }
            docs.append(Document(page_content=text, metadata=metadata))

    # Create an instance of ChromaDB using the persistent directory
    embeddings = OpenAIEmbeddings()
    db = Chroma(persist_directory="chroma_db", embedding_function=embeddings)

    # Add the documents to the ChromaDB and assign unique IDs
    for doc in tqdm(docs):
        doc_id = str(uuid.uuid1())  # Generate a unique ID for the document
        db.add_documents(documents=[doc], ids=[doc_id])

    print(f"Added {len(docs)} CNN articles")