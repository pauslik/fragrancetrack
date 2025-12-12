from curl_cffi import requests
from enum import Enum
import unicodedata

APP_ID = "FGVI612DFZ"
API_KEY = "NzYwYzI2MGU3NTM4NGMwODU4NzdkZTI3OGEwMzQ4ZDRmZmRiZWI3MjMwYmY1ZTQzZTk1MTU3OTNmNzQyMzYwMHZhbGlkVW50aWw9MTc2NTk0MDgyMg=="
INDEX_PERFUMES = "fragrantica_perfumes"
INDEX_DESIGNERS = "fragrantica_designers"


def build_result(hit: dict) -> dict:
    result = {}
    result["brand"] = hit["dizajner"]
    result["name"] = hit["naslov"]
    result["id"] = hit["id"]
    result["link"] = hit["url"]["EN"][0]
    result["year"] = hit["godina"]
    return result

def str_eq(s1: str, s2: str) -> bool:
    s1n = unicodedata.normalize('NFC', s1)
    s2n = unicodedata.normalize('NFC', s2)
    return s1n.casefold() == s2n.casefold()

def find_best(brand: str, name: str, hits: list) -> dict:
    if len(hits) == 1:
        return build_result(hits[0])
    elif len(hits) == 0:
        raise Exception(f'No search hits for {brand} {name}')
    
    brand_matches = []
    for hit in hits:
        if str_eq(brand, hit["dizajner"]) or brand in hit["dizajner"]:
            brand_matches.append(hit)
    
    name_matches = []
    for m in brand_matches:
        if name in m["naslov"]:
            name_matches.append(m)
    
    name_matches.sort(key=len)
    # worst case, check char by char, but this doesn't work if start of 'name' is incorrect
    # TODO rewrite this to check every char in name with every char in match
    # for i in range(len(name)):
    #     if len(matches) > 1:
    #         for match in matches:
    #             if i <= len(match["naslov"]):
    #                 if not str_eq(name[i], match["naslov"][i]):
    #                     matches.remove(match)
    if len(name_matches) == 0:
        if len(brand_matches) == 0:
            print(f'No exact matches found for brand {brand}, best result: {hits[0]["url"]["EN"][0]}')
            return build_result(hits[0])
        return build_result(brand_matches[0])
    print(f'No exact matches found for name {name}, best result: {brand_matches[0]["url"]["EN"][0]}')
    return build_result(name_matches[0])

def algolia_search(query: str, index: str, results = 20):
    url = f"https://{APP_ID}-dsn.algolia.net/1/indexes/{index}/query"

    headers = {
        "X-Algolia-Application-Id": APP_ID,
        "X-Algolia-API-Key": API_KEY,
        "Content-Type": "application/json"
    }

    query = query
    payload = {
        "query": query,
        "hitsPerPage": results
    }

    response = requests.post(
        url, 
        json=payload, 
        headers=headers,
        impersonate="chrome"
    )

    # 5. Extract links from the JSON response
    data = response.json()
    hits = data.get("hits", [])

    if len(hits) == 0:
        raise Exception(f'No results found with query: {query}')
    return hits

# this function is not really reliable, the first result is not always the best match
# I use it only in the DB import function, it searches for both brand and name
def auto_search_fragrance(brand: str, name: str) -> dict:  
    query = f'{brand} {name}'
    hits = algolia_search(query, INDEX_PERFUMES)

    # sifting through the results in order to find the best one
    hit_names = []
    for hit in hits:
        f_brand = hit["dizajner"]
        f_name = hit["naslov"]
        hit_names.append({"brand": f_brand, "name": f_name})

        # check for the exact brand and name
        if str_eq(brand, f_brand) and str_eq(name, f_name):
            return build_result(hit)

    # find the best result if exact name not found
    best = find_best(brand, name, hits)
    return best

# TODO use this for the web search, display only ['dizajner']
def search_designers(brand, n=9):
    query = brand
    hits = algolia_search(query, INDEX_DESIGNERS, n)

    results = []
    for hit in hits:
        hit_dict = {}
        hit_dict["id"] = hit['id']
        hit_dict["brand"] = hit['dizajner']
        hit_dict["slug"] = hit['slug']
        hit_dict["niche"] = hit['niche']
        results.append(hit_dict)
    # get these values:
    # "Louis Vuitton"
    # id = hits[0]['id'] = 2747
    # brand = hits[0]['dizajner'] = 'Louis Vuitton'
    # slug = hits[0]['slug'] = 'Louis-Vuitton'
    # niche = hits[0]['niche'] = 'niche'->True / ''->False
    # generate_website = f'https://www.fragrantica.com/designers/{slug}.html'
    return results


# TODO use this for the web search, display only ['naslov']
def search_fragrance(brand, name, n=10):
    query = f'{brand} {name}'
    hits = algolia_search(query, INDEX_PERFUMES, 50)

    results = []
    for hit in hits:
        if str_eq(brand, hit['dizajner']):
            hit_dict = {}
            hit_dict["id"] = hit['id']
            hit_dict["name"] = hit['naslov']
            hit_dict["brand"] = hit['dizajner']
            hit_dict["sex"] = hit['spol']
            hit_dict["year"] = hit['godina']
            hit_dict["slug"] = hit['slug']
            hit_dict["rating"] = hit['rating']
            hit_dict["link"] = hit['url']['EN']
            hit_dict["thumb"] = hit['thumbnail']
            hit_dict["picture"] = hit['picture']
            results.append(hit_dict)
    return results[:n]

# TODO add real tests
# dess = search_designers("Jean Paul Gaultier")
# frags = search_fragrance(dess[0]['brand'], "Le Male Le Parfum")
# print(frags)