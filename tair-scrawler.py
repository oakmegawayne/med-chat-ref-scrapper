import requests
from bs4 import BeautifulSoup

def check_links_in_table(url):
    # Fetch the HTML content from the URL
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        return

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the specific table
    table = soup.find('table', {'class': 'object_table title_table'})

    # Find all <a> tags with href attributes within the table
    if table:
        success_count = 0
        failure_count = 0
        article_links = table.find_all('a', href=True)

        # Check the HTTP status code for each link
        for link in article_links:
            url = link['href']
            if url.startswith('http'):
                try:
                    response = requests.head(url, allow_redirects=True)
                    if response.status_code >= 200 and response.status_code < 400:
                        success_count += 1
                    else:
                        failure_count += 1
                    print(f"URL: {url} - Status Code: {response.status_code}")
                except requests.RequestException as e:
                    print(f"URL: {url} - Error: {e}")
                    failure_count += 1
    else:
        print("Table not found.")
        return
        
    print(f"Total Links: {len(article_links)}")
    print(f"Success: {success_count}")
    print(f"Failure: {failure_count}")

if __name__ == "__main__":
    start = 0

    for i in range(3):
        url = f'https://tair.org.tw/browse-author-title?author=%E7%8E%8B%E4%B8%80%E4%B8%AD&order=date&num=50&start={start}'
        print(f"Checking links in table for page {i+1}")
        check_links_in_table(url)
        start += 50
