from curl_cffi import requests

APP_ID = "FGVI612DFZ"
API_KEY = "NzYwYzI2MGU3NTM4NGMwODU4NzdkZTI3OGEwMzQ4ZDRmZmRiZWI3MjMwYmY1ZTQzZTk1MTU3OTNmNzQyMzYwMHZhbGlkVW50aWw9MTc2NTk0MDgyMg=="
INDEX_NAME = "fragrantica_perfumes"

def search_algolia(brand: str, name: str, results = 20) -> dict:  

    url = f"https://{APP_ID}-dsn.algolia.net/1/indexes/{INDEX_NAME}/query"

    headers = {
        "X-Algolia-Application-Id": APP_ID,
        "X-Algolia-API-Key": API_KEY,
        "Content-Type": "application/json"
    }

    query = f'{brand} {name}'
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

    # the search is pretty trash, you'll have to sift through the results in order to find the correct one
    hit_names = []
    for hit in hits:
        f_brand = hit["dizajner"]
        f_name = hit["naslov"]
        hit_names.append({"brand": f_brand, "name": f_name})

        # check for the exact brand and name, might be too strict (use in or iterate every char? additionally and return the best result)
        if brand == f_brand and name == f_name:
            result = {}
            f_id = hit["id"]
            f_link = hit["url"]["EN"][0]
            f_year = hit["godina"]
            result["brand"] = f_brand
            result["name"] = f_name
            result["id"] = f_id
            result["link"] = f_link
            result["year"] = f_year
            return result
    
    # executes if match is not found
    raise Exception(f'Match not found with query: {query}, in results: {hit_names}')

# TODO add real tests
# res = search_algolia("Jean Paul Gaultier", "Le Male Le Parfum")
# print(res)