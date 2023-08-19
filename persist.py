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
        # self.db = Chroma(persist_directory="./chroma_db", embedding_function=self.embedding_function)
        pass

    def save_content_to_location(self, topic_name, file_contents):
        if not os.path.exists(self.data_directory + '/' + topic_name):
            os.makedirs(self.data_directory + '/' + topic_name)
        for contents in file_contents:
            filepath = os.path.join(self.data_directory + '/' + topic_name, str(uuid.uuid4()) + '.txt')
            with open(filepath, 'w') as f:
                f.write(contents)

    def load_content_to_db(self, topic_name):
        try:
            topic_directory = self.data_directory + '/' + topic_name
            files = [_ for _ in os.listdir(topic_directory) if os.path.isfile(os.path.join(topic_directory, _))]
            for f in files:
                # load the document and split it into chunks
                loader = TextLoader(f)
                documents = loader.load()

                # split it into chunks
                text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
                docs = text_splitter.split_documents(documents)

                # load it into Chroma
                # self.db = Chroma.from_documents(docs, self.embedding_function, persist_directory="./chroma_db")
                # load it into Weaviate
                self.db = Weaviate.from_documents(docs, self.embedding_function, client=self.client, by_text=False)
        except Exception as e:
            print('Exception occurred to load content in the DB', e)

    def query_from_the_db(self, query):
        return self.db.similarity_search(query)
