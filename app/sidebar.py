import streamlit as st
from app.faq import faq


def sidebar():
    with st.sidebar:
        st.markdown(
            "## How to use\n"
            "1. Enter the topic you want to learn more\n"
            "2. If results are found, ask questions about the topic\n"
        )

        st.markdown("---")
        st.markdown("# About")
        st.markdown(
            "PA-Webscraper allows you learn more about the topic "
            "of your choosing."
        )
        st.markdown(
            "You can contribute to the project on [GitHub](https://github.com/sumedhrasal/pa-webscraper) "
            "with your feedback and suggestions💡"
        )
        st.markdown("Made by Sumedh")
        st.markdown("---")

        faq()
