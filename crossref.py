import re
import requests

def search_crossref_by_orcid(orcid):
    url = f"https://api.crossref.org/works?filter=orcid:{orcid}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        results = []
        for item in data['message']['items']:
            result = {
                'title': item.get('title', [''])[0],
                'publication_date': item.get('published-print', {}).get('date-parts', [['']])[0],
                'authors': [author.get('given', '') + ' ' + author.get('family', '') for author in item.get('author', [])],
                'journal': item.get('container-title', [''])[0],
                'abstract': remove_tags(item.get('abstract', '')),
                'doi': item.get('DOI', '')
            }
            results.append(result)
        return results
    else:
        return None

def search_crossref_by_author(author_name):
    url = f"https://api.crossref.org/works?query.author={author_name}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        results = []
        for item in data['message']['items']:
            result = {
                'title': item.get('title', [''])[0],
                'publication_date': item.get('published-print', {}).get('date-parts', [['']])[0],
                'authors': [author.get('given', '') + ' ' + author.get('family', '') for author in item.get('author', [])],
                'journal': item.get('container-title', [''])[0],
                'abstract': remove_tags(item.get('abstract', '')),
                'doi': item.get('DOI', '')
            }
            results.append(result)
        return results
    else:
        return None
    
"""
abstracts contain tags like <jats:italic> and <jats:sup>, which are not rendered properly in the console.
To remove these tags, you can use the following function:
"""
def remove_tags(text):
    return re.sub(r'<[^>]*>', '', text)