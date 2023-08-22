import streamlit as st


def faq():
    st.markdown(
        """
        # FAQ
        ## How does PA-WebScraper work?
        You enter a topic of your interest in the search field, the app will 
        query the web and fetch the most recent news/articles about your topic.

        Once the app finds enough data points about the topic, it will summarize 
        the news/articles for you. You can even ask basic questions to the app
        to learn more.

        ## Are the answers 100% accurate?
        No, the answers are not 100% accurate. PA-WebScraper uses duckduckgo to 
        search for the latest information and stores the data into Weaviate Vector DB.
        The summarization process can make mistakes.
        """
    )
