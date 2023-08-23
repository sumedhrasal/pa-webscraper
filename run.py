import streamlit as st

from app import sidebar
from app import persist
from app import file_utils
from app import search


def run_app():
    st.set_page_config(page_title="PA WebScraper", layout="wide") #, page_icon=""
    st.header("PA WebScraper")

    sidebar()
    p = persist.Persist()
    s = search.Search()

    topic = st.text_input("Enter topic")
    if topic:
        st.write("Topic: " + topic)
        data_found = file_utils.load_data(topic, s, p)
        if data_found:
            st.write('Data found on DuckDuckGo')
            work_with_the_data(p)
        else:
            st.markdown('No data found on DuckDuckGo')


def work_with_the_data(p):
    question = st.text_area("Enter your question")
    if st.button('Long answer') and question:
        result = p.ask_a_question(question)
        st.write("Answer")
        for _ in result['data']['Get']['Knowledge']:
            st.write(_['text'])
    # if st.button('Short answer') and question:
    #     result = persist.q_and_a_result(question)
    #     st.write("Answer")
    #     for _ in result['data']['Get']['Knowledge']:
    #         st.write(_['_additional']['answer']['result'])
    # if st.button('Summarize'):
    #     result = persist.summarize()
    #     print(result)
    #     if result['data']['Get']['Knowledge']:
    #         for _ in result['data']['Get']['Knowledge']:
    #             st.write(_)
    #     else:
    #         st.write('No data found')


if __name__ == "__main__":
    run_app()
