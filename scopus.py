import requests
import dotenv
import os
dotenv.load_dotenv()

API_KEY = os.environ.get("SCOPUS_API_KEY")

def search_scopus(query):
    url = f"https://api.elsevier.com/content/search/scopus?query={query}"
    headers = {"Accept": "application/json", "X-ELS-APIKey": API_KEY}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        papers = []
        data = response.json()
        for entry in data.get("search-results", {}).get("entry", []):
            papers.append({
                "title": entry.get("dc:title", "無標題"),
                "publication_date": entry.get("prism:coverDate", "未知日期"),
                "journal": entry.get("prism:publicationName", "未知期刊"),
                "authors": [author.get("ce:indexed-name", "無作者") for author in entry.get("author", [])],
                "doi": entry.get("prism:doi", ""),
            })
        return papers
    return None