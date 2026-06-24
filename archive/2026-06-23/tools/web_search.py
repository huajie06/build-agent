import requests
from bs4 import BeautifulSoup
from duckduckgo_search import DDGS


def web_search(query: str) -> str:
    """Searches the web using DuckDuckGo and returns top titles and URLs."""
    try:
        with DDGS() as ddgs:
            results = [r for r in ddgs.text(query, max_results=5)]
        if not results:
            return "No search results found."

        # Format cleanly for the LLM context window
        formatted_results = []
        for r in results:
            formatted_results.append(
                f"Title: {r['title']}\nURL: {r['href']}\nSnippet: {r['body']}\n---"
            )
        return "\n".join(formatted_results)
    except Exception as e:
        return f"Search failed: {str(e)}"


def scrape_webpage(url: str) -> str:
    """Fetches a webpage and extracts raw text content (stripping HTML tags)."""
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # Remove script and style elements so we only get readable text
        for script in soup(["script", "style"]):
            script.decompose()

        text = soup.get_text(separator="\n")
        # Clean up whitespace and limit length so it doesn't blow past context limits
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase for line in lines for phrase in line.split("  "))
        clean_text = "\n".join(chunk for chunk in chunks if chunk)

        return clean_text[:8000]  # Cap at ~8k characters for safety
    except Exception as e:
        return f"Failed to scrape webpage: {str(e)}"
