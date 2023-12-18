import requests
import uuid
from bs4 import BeautifulSoup
from langchain.document_loaders import UnstructuredURLLoader
from langchain.vectorstores.chroma import Chroma
from langchain.embeddings import OpenAIEmbeddings
from tqdm.auto import tqdm
from datetime import datetime

def scrape_jpost(date):
    # Parse date from MM-DD-YY to yyyymmdd
    parsed_date = datetime.strptime(date, '%m-%d-%y')
    formatted_date = parsed_date.strftime('%Y%m%d%H%M%S')

    # Format wayback machine URL with date
    url = f'https://web.archive.org/web/{formatted_date}/https://www.jpost.com/arab-israeli-conflict'

    # Send a GET request to the URL
    response = requests.get(url)

    # Parse the HTML content using Beautiful Soup
    soup = BeautifulSoup(response.content, 'html.parser')
    article_elements = soup.find_all(class_='itc')

    # Initiate lists to store post information
    links = []
    titles = []

    # Find clickable card elements within each <article> element
    for article in article_elements:
        a_tag = article.find('a')
        
        # Extract and format link
        href = a_tag.get('href')
        href = href.split('//')[2]
        links.append('https://' + href)
        
        # Format title
        title = article.find(class_='itc-info-title').get_text(separator='', strip=True)
        titles.append(title)
        
        print(f"\n{title}")
        print(f"https://{href}")

    # Load documents from links
    loaders = UnstructuredURLLoader(urls=links, show_progress_bar=True)
    docs = loaders.load()

    # Save title, source, and date to metadata
    for i, doc in enumerate(docs):
        # Extract title from url
        url = links[i]
        title = titles[i]

        # Set metadata
        metadata = {
            'title': title,
            'date': date,
            'source': "Jerusalem Post",
            'link': url
        }
        doc.metadata = metadata


    # Create an instance of ChromaDB using the persistent directory
    embeddings = OpenAIEmbeddings()
    db = Chroma(persist_directory="chroma_db", embedding_function=embeddings)

    # Add the documents to the ChromaDB and assign unique IDs
    for doc in tqdm(docs):
        doc_id = str(uuid.uuid1())  # Generate a unique ID for the document
        db.add_documents(documents=[doc], ids=[doc_id])

    print(f"Added {len(docs)} Jerusalem Post articles")