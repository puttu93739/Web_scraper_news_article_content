import sys
from http.client import HTTPException

import requests
from bs4 import BeautifulSoup

def fetch_html(url: str) -> str:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Referer": "https://www.google.com/",
        "DNT": "1",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-User": "?1",
        "Sec-Fetch-Dest": "document"
    }

    session = requests.Session()
    response = session.get(url, headers=headers)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch the URL")

    return response.text


def parse_article(html):
    """
    Parse the article HTML and extract title and content.
    Works on NYTimes, CNN, Reuters, Washington Post (general logic).
    """
    soup = BeautifulSoup(html, "lxml")

    # Extract title
    title = soup.find("h1")
    title_text = title.get_text(strip=True) if title else "No title found"

    # Extract paragraphs inside article body
    paragraphs = soup.find_all("p")
    content_text = "\n".join(p.get_text(strip=True) for p in paragraphs)

    return title_text, content_text


def main():
    if len(sys.argv) < 2:
        print("Usage: python scrape_article.py <article_url>")
        sys.exit(1)

    url = sys.argv[1]

    print("\nFetching article...\n")

    try:
        html = fetch_html(url)
        title, content = parse_article(html)

        print("===== ARTICLE TITLE =====")
        print(title)
        print("\n===== ARTICLE CONTENT =====")
        print(content[:5000])  # print first 5000 chars

    except Exception as e:
        print("Error:", e)


if __name__ == "__main__":
    main()
