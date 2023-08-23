# from collections import defaultdict
# from itertools import chain

# from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
# from langchain.text_splitter import CharacterTextSplitter
# from langchain.vectorstores import Chroma, Weaviate
# from langchain.document_loaders import TextLoader

# from weaviate.embedded import EmbeddedOptions

import uuid, os, weaviate, json


class Persist:    
    def __init__(self) -> None:
        self.data_directory = 'data'
        # self.embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
        # self.client = weaviate.Client(embedded_options=EmbeddedOptions())
        self.WEAVIATE_URL = 'http://localhost:8080'
        self.client = weaviate.Client(url=self.WEAVIATE_URL)
        if not self.client.schema.exists("Knowledge"):
            class_obj = {
                "class": "Knowledge",
                "vectorizer": "text2vec-contextionary",
                "moduleConfig": {
                    "text2vec-contextionary": {
                        "vectorizeClassName": True,
                    }
                },
                "properties": [
                    {
                        "name": "title",
                        "description": "title of the article",
                        "dataType": ["text"],
                    }
                ]
                # "vectorizer": "text2vec-huggingface",
                # "moduleConfig": {
                #     "text2vec-huggingface": {
                #     "model": "sentence-transformers/all-MiniLM-L6-v2",
                #         "options": {
                #             "waitForModel": True,
                #         }
                #     }
                # }
            }
            self.client.schema.create_class(class_obj)
            print(self.client.schema.get(), 'created')
        # else:
        #     self.client.schema.delete_class("Knowledge")
        #     print('schema deleted')

    def save_content_to_location(self, topic_name, file_contents):
        if not os.path.exists(self.data_directory + '/' + topic_name):
            os.makedirs(self.data_directory + '/' + topic_name)
        for contents in file_contents:
            filepath = os.path.join(self.data_directory + '/' + topic_name, str(uuid.uuid4()) + '.txt')
            with open(filepath, 'w') as f:
                f.write(contents)

    def load_into_the_db(self, topic_name):
        try:
            topic_directory = self.data_directory + '/' + topic_name
            files = [_ for _ in os.listdir(topic_directory) if os.path.isfile(os.path.join(topic_directory, _))]

            for f in files:
                with open(os.path.join(topic_directory, f)) as file:
                    text = file.read()
                    record = self.client.data_object.create({
                        'name': f[0:36],
                        'description': f[0:36],
                        'text': text,
                    }, class_name='Knowledge', uuid=f[0:36])
                    # print(record)
        except Exception as e:
            print('Exception occurred to load content in the DB', e)

    def ask_a_question(self, input_query):
        response = (self.client.query
                    .get("Knowledge", ["text"])
                    # .with_near_text({
                    #     "concepts": [input_query]
                    # })
                    .with_hybrid(
                        query=input_query
                    )
                    .with_limit(1)
                    # .with_additional(["distance"])
                    .do()
        )
        return response

    def q_and_a_result(self, input_query):
        ask = {
            "question": input_query,
            "properties": ["text"]
        }
        result = (
            self.client.query
            .get("Knowledge", ["title", "_additional {answer {hasAnswer certainty property result startPosition endPosition} }"])
            .with_ask(ask)
            .with_limit(1)
            .do()
        )
        return result
    
    def summarize(self):
        result = (self.client.query
                  .get("Knowledge", ["title", "_additional { summary ( properties: [\"text\"]) { property result } }"])
                  .do())
        return result
