# TEAM PROJECT

This is implementation of our academic project for 'Team Project' class.

In this project, we fetch informations about publications and their authors from https://dblp.org API, and we create graphs based on data we collected.

## Setting up environment and running the programm
We recommend to use Python's virtual environment, although our project contain only two dependencies (listed in requirements.txt).

Clone the project, create and activate virtual environment:
```shell
python -m venv .venv
source .venv/bin/activate
```

Install requirements (after enviroment is activated):
```shell
pip install -r requirements.txt
```

Now, you can run your main.py file:
```shell
python main.py
```

## Customizing inputs
You can customize variables in our code, to fetch only the data you need.

### Keywords
To customize keywords that programm is fetching, just update the `KEYWORDS` list, initialized at the top of the main.py file.
```python
KEYWORDS = [
    '5G',
    'LLM',
    'Distributed systems',
    'Graphs'
]
```

### Pagination
Our programm behaves in such way: if you pass `pages=0` as an argument to `fetch_data_from_api` function, the program will calculate how many pages there are in total, and will try to fetch all of the data that is available.

If you wish to fetch less pages, just change this `pages` argument into `fetch_data_from_api` function, which is excecuted in `main()` function:
```python
data = fetch_data_from_api(keyword, 0)  # this will fetch all of data
data = fetch_data_from_api(keyword, 10) # this will fetch 10 pages
data = fetch_data_from_api(keyword, 5)  # this will fetch 5 pages 
```
