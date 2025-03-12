from xml.etree import ElementTree

import requests

def search_pubmed_by_author_name(author_name, max_results=10):
    # search for publications by author name in PubMed, return title, publication date, journal, and DOI of the publications
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
    search_url = f"{base_url}esearch.fcgi"
    search_params = {
        "db": "pubmed",
        "term": f"{author_name}[Author]",  # search by author name
        "retmode": "json",
        "retmax": max_results,  # limit the number of results
    }
    search_res = requests.get(search_url, params=search_params)
    search_data = search_res.json()
    pmids = search_data.get("esearchresult", {}).get("idlist", [])
    if not pmids:
        return []
    fetch_url = f"{base_url}efetch.fcgi"
    fetch_params = {
        "db": "pubmed",
        "id": ",".join(pmids),
        "retmode": "xml",
    }
    fetch_res = requests.get(fetch_url, params=fetch_params)
    root = ElementTree.fromstring(fetch_res.content)
    papers = []
    for article in root.findall(".//PubmedArticle"):
        title = article.findtext(".//ArticleTitle", default="No title")
        authors_list = [f"{author.findtext('LastName', '')}, {author.findtext('ForeName', '')}" for author in article.findall(".//Author")]
        pub_date = article.findtext(".//PubDate/Year", default="Unknown year")
        journal = article.findtext(".//Journal/Title", default="Unknown journal")
        doi = article.findtext(".//ArticleId[@IdType='doi']", default="")
        abstract = article.findtext(".//Abstract/AbstractText", default="No abstract")
        paper_info = {
            "title": title,
            "authors": authors_list,
            "publication_date": pub_date,
            "journal": journal,
            "doi": doi,
            "abstract": abstract,
        }
        papers.append(paper_info)
    return papers

def search_pubmed_by_orcid(orcid):
    # use orcid to search for publications in PubMed, return title, authors, and other details of the publications
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
    search_url = f"{base_url}esearch.fcgi"
    search_params = {
        "db": "pubmed",
        "term": f"{orcid}[ORCID]",  # search by ORCID
        "retmode": "json",
        "retmax": 10,  # limit the number of results
    }
    search_res = requests.get(search_url, params=search_params)
    search_data = search_res.json()
    pmids = search_data.get("esearchresult", {}).get("idlist", [])
    if not pmids:
        return []
    fetch_url = f"{base_url}efetch.fcgi"
    fetch_params = {
        "db": "pubmed",
        "id": ",".join(pmids),
        "retmode": "xml",
    }
    fetch_res = requests.get(fetch_url, params=fetch_params)
    root = ElementTree.fromstring(fetch_res.content)
    papers = []
    for article in root.findall(".//PubmedArticle"):
        title = article.findtext(".//ArticleTitle", default="No title")
        authors = article.findall(".//Author")
        authors_list = [f"{author.findtext('LastName', '')}, {author.findtext('ForeName', '')}" for author in authors]
        journal = article.findtext(".//Journal/Title", default="Unknown journal")
        pub_date = article.findtext(".//PubDate/Year", default="Unknown year")
        doi = article.findtext(".//ArticleId[@IdType='doi']", default="")
        abstract = article.findtext(".//Abstract/AbstractText", default="No abstract")
        paper_info = {
            "title": title,
            "authors": authors_list,
            "journal": journal,
            "publication_date": pub_date,
            "doi": doi,
            "abstract": abstract,
        }
        papers.append(paper_info)
    return papers
