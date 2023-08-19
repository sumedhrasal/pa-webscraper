from bs4 import BeautifulSoup
from duckduckgo_search import DDGS
from langchain.document_loaders import UnstructuredURLLoader
# from langchain.tools import DuckDuckGoSearchRun, DuckDuckGoSearchResults
# from langchain.utilities import DuckDuckGoSearchAPIWrapper

import requests


class Search:
    def __init__(self) -> None:
        self.ddgs = DDGS()

    def search_for_topic(self, topic_name):
        # Query DuckDuckGo news search
        return self.ddgs.news(keywords=topic_name, region="us-en")

    def get_data_from_url(self, url):
        # loader = UnstructuredURLLoader(urls=[url])
        # return loader.load()

        # Send a GET request to the webpage
        response = requests.get(url)
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, "html.parser")
        # Get HTML content
        return soup.get_text(separator='\n', strip=True)

