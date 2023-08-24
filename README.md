<h1 align="center">
PA - Webscraper
</h1>

This app aims to build a personal assistant that will scrape details of any particular topic of your choice and you can use this assistant to further ask questions related to the same topic.

## Features
- Use the app to search the web on a topic of your choosing.
- Using Weaviate Vector DB, summarize all the articles found from the web.

## Run locally

1. Clone the repository

```bash
git clone https://github.com/sumedhrasal/pa-webscraper.git
cd pa-webscraper
```

2. Install dependencies (install in a conda environment)

```bash
pip install -r requirements.txt
```

3. Start Weaviate Vector DB

```bash
docker compose up
```

or you can find the latest version at https://weaviate.io/developers/weaviate/installation/docker-compose

4. Run the application

```bash
cd pa-webscraper
streamlit run run.py
```
