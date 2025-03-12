import re
from crossref import search_crossref_by_author, search_crossref_by_orcid
from pubmed import search_pubmed_by_author_name, search_pubmed_by_orcid
from scopus import search_scopus

def main():
    query = input("Enter your search query: ")

    orcid_pattern = r'\d{4}-\d{4}-\d{4}-\d{4}'
    if re.match(orcid_pattern, query):
        pubmed_results = search_pubmed_by_orcid(query)
        crossref_results = search_crossref_by_orcid(query)
    else:
        pubmed_results = search_pubmed_by_author_name(query)
        crossref_results = search_crossref_by_author(query)
    
    scopus_results = search_scopus(query)

    # merge results by doi, if available. Treat doi as unique identifier, if no doi, treat the entry as unique.
    merged_results = {}
    for paper in pubmed_results:
        if paper["doi"]:
            merged_results[paper["doi"]] = paper
        else:
            merged_results[paper["title"]] = paper
    for paper in scopus_results:
        if paper["doi"]:
            merged_results[paper["doi"]] = paper
        else:
            merged_results[paper["title"]] = paper
    for paper in crossref_results:
        if paper["doi"]:
            merged_results[paper["doi"]] = paper
        else:
            merged_results[paper["title"]] = paper
    
    print(f"Found {len(merged_results)} unique papers:")
    for paper in merged_results.values():
        print(f"Title: {paper['title']}")
        print(f"Authors: {', '.join(paper['authors'])}")
        print(f"Publication Date: {paper['publication_date']}")
        print(f"Journal: {paper['journal']}")
        print(f"DOI: {paper['doi']}")
        print(f"Abstract: {paper.get('abstract', 'No abstract')}")
        print()

if __name__ == "__main__":
    main()