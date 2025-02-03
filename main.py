import requests
import json
import time

from loguru import logger


API_URL = "https://dblp.org/search/publ/api"
KEYWORDS = [
    '5G',
    'LLM',
    'Distributed systems',
    'Graphs'
]


# function that fetches data from dblp API
def fetch_data_from_api(search_phrase: str, pages: int) -> dict:
    offset = 1000
    num_of_pages = pages
    data = []
    sleep_interval_s = 60

    # when pages argument is equal to zero,
    # use this request to count how many pages needs to be fetched
    if pages == 0:
    
        while True:
            url = API_URL + f"?q={search_phrase}&format=json"
            response = None
            try:
                response = requests.get(url)
            
            except Exception as e:
                print(str(e), response.json())
            
            if response.status_code != 200:
                logger.info(f"Sleeping {sleep_interval_s} seconds...")
                time.sleep(sleep_interval_s)
                continue

            num_of_pages = int(response.json().get('result').get('hits').get('@total')) // 1000
            break
    
    # actual data fetching
    logger.info(f"I will fetch {num_of_pages} pages.")
    for i in range(num_of_pages):
        url = API_URL + f"?q={search_phrase}&f={offset * i}&h={offset}&format=json"
        
        response = None
        try:
            response = requests.get(url)
            print(response)

        except Exception as e:
            logger.error(str(e))
            continue
    
        if response.status_code != 200:
            i = i - 1
            logger.info(f"Sleeping for {sleep_interval_s} seconds...")
            time.sleep(sleep_interval_s)
            continue
        
        data.append(response.json())
    
    return data


def raw_json_to_preprocessed(keyword: str):
    data = []
    raw_json = None

    with open(f'{keyword}.json', 'r') as f:
        raw_json = json.load(f)
    
    for page in raw_json:

        hits = page.get('result').get('hits').get('hit')
        if not hits:
            continue

        for hit in hits:
            info_field = hit.get('info')
            authors_field = info_field.get('authors')

            authors = []
            if authors_field == None:
                continue

            elif isinstance(authors_field['author'], dict):
                authors = [authors_field['author']['text']]
            
            elif isinstance(authors_field['author'], list):
                authors = [a['text'] for a in authors_field['author']]
            
            row = {
                'id': hit.get('@id'),
                'authors': authors,
                'publication': info_field.get('title'),
                'year': info_field.get('year')
            }
            data.append(row)
    
    with open(f'{keyword}_preprocessed.txt', 'w+') as f:
        
        for d in data:
            f.write(f'{json.dumps(d)}\n')


def preprocessed_to_txt(fname: str):
    authors = set()
    data = []

    lines = []
    with open(fname, 'r') as f:
        lines = f.readlines()
    
    for line in lines:
        pub = json.loads(line)

        for author in pub['authors']:
            authors.add(author)
    
    for line in lines:
        temp = set()
        pub = json.loads(line)

        for author in authors:

            if author not in pub['authors']:
                continue
            
            for pub_author in pub['authors']:
                if pub_author in temp:
                    continue

                if pub_author == author:
                    continue
                
                temp_list = sorted([author, pub_author])
                data.append(
                    f"{pub['year']},{temp_list[0]},{temp_list[1]}"
                )

            temp.add(author)
    

    counter = {}
    for d in data:

        if d in counter.keys():
            counter[d] = counter[d] + 1
            continue

        counter[d] = 1 
    
    return counter


    


def main():
    for keyword in KEYWORDS:

        logger.info(f"Processing keyword: {keyword}")

        data = fetch_data_from_api(keyword, 0)
        
        with open(f"{keyword}.json", 'w+') as f:
            json.dump(data, f, indent=4, default=str)
        
        raw_json_to_preprocessed(keyword)

        with open(f"{keyword}.txt", "w+") as f:

            for k, v in preprocessed_to_txt(f'{keyword}_preprocessed.txt').items():
                f.write(f"{k},{v}\n")



if __name__ == '__main__':
    main()
