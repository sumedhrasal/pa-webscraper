

def load_data(topic_name, search, persist):
    result = search.search_for_topic(topic_name)
    urls = []
    for value in result:
        urls.append(value['url'])
        # print(value['date'])
        # print(value['title'])
        # print(len(value['body']))
        # print(value['url'])
        # print(value['source'])
    contents = [search.get_data_from_url(_) for _ in urls]
    persist.save_content_to_location(topic_name, contents)
    persist.load_into_the_db(topic_name)
    return True if len(contents) > 0 else False
