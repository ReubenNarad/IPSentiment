import requests
import uuid
from bs4 import BeautifulSoup
from langchain.document_loaders import UnstructuredURLLoader
from langchain.vectorstores.chroma import Chroma
from langchain.embeddings import OpenAIEmbeddings
from tqdm.auto import tqdm
from datetime import datetime

def scrape_aljazeera(date):
    # Parse date from MM-DD-YY to yyyymmdd
    parsed_date = datetime.strptime(date, '%m-%d-%y')
    formatted_date = parsed_date.strftime('%Y%m%d%H%M%S')

    # Format URL with date
    url = f'https://web.archive.org/web/{formatted_date}/https://www.aljazeera.com/tag/israel-palestine-conflict/'

    # Send a GET request to the URL
    response = requests.get(url)

    # Parse the HTML content using Beautiful Soup
    soup = BeautifulSoup(response.content, 'html.parser')
    article_elements = soup.find_all('article')

    links = []
    titles = []
    
    # Find clickable card elements within each <article> element
    for article in article_elements:
        a_tags = article.find_all(class_="u-clickable-card__link")
        for a_tag in a_tags:
            # Format link
            href = a_tag.get('href')
            href = href.split('//')[1]
            links.append('https://' + href)
            
            # Find and assign title
            title = a_tag.get_text(separator='', strip=True)
            title = title.replace("\u00AD", "")
            titles.append(title)
            
            # print(title)
            # print(f"{href}")

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
            'source': 'Al Jazeera',
            'link': url
        }
        doc.metadata = metadata


    # Create an instance of ChromaDB using the persistent directory
    embeddings = OpenAIEmbeddings()
    db = Chroma(persist_directory="chroma_db", embedding_function=embeddings)

    # Add the documents to the ChromaDB and assign unique IDs
    for doc in tqdm(docs[:10]):
        doc_id = str(uuid.uuid1())  # Generate a unique ID for the document
        db.add_documents(documents=[doc], ids=[doc_id])
    
    print(f"Added {len(docs)} Al Jazeera articles")
