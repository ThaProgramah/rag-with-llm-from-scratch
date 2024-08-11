#from duckduckgo_search import DDGS

def duckduckgo_search(keyword: str, max_results: int) -> str:
    '''this function search with duckduckgo search engine and 
    returns the search result
    keyword: is the search term for duckduckgo
    max_results: is the number of search term results'''
    return DDGS().text(keyword, max_results=1)