from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma, Weaviate
from langchain.document_loaders import TextLoader

import uuid, os, weaviate

WEAVIATE_URL = 'http://localhost:8080'

class Persist:
    def __init__(self) -> None:
        self.data_directory = 'data'
        self.embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
        self.client = weaviate.Client(url=WEAVIATE_URL)

    def save_content_to_location(self, topic_name, file_contents):
        if not os.path.exists(self.data_directory + '/' + topic_name):
            os.makedirs(self.data_directory + '/' + topic_name)
        for contents in file_contents:
            filepath = os.path.join(self.data_directory + '/' + topic_name, str(uuid.uuid4()) + '.txt')
            with open(filepath, 'w') as f:
                f.write(contents)

    def query_from_the_db(self, topic_name, query):
        try:
            topic_directory = self.data_directory + '/' + topic_name
            files = [_ for _ in os.listdir(topic_directory) if os.path.isfile(os.path.join(topic_directory, _))]
            documents = []
            for f in files:
                # load the document and split it into chunks
                loader = TextLoader(os.path.join(topic_directory, f))
                documents.extend(loader.load())

            # split it into chunks
            text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
            docs = text_splitter.split_documents(documents)

            # load it into Chroma
            # db = Chroma.from_documents(docs, self.embedding_function, persist_directory="./chroma_db")
            # load it into Weaviate
            db = Weaviate.from_documents(docs, self.embedding_function, client=self.client, by_text=False)
            return db.similarity_search_with_score(query)
        except Exception as e:
            print('Exception occurred to load content in the DB', e)
