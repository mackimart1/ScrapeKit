import requests
import time
import os
import random
import json
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

def get_search_results(query, num_results=10):
    url = f"https://www.google.com/search?q={query}&num={num_results}"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        search_results = soup.find_all('div', class_='yuRUbf')
        return [result.find('a')['href'] for result in search_results[:num_results]]
    except requests.RequestException as e:
        print(f"Error fetching search results: {e}")
        return []

def scrape_content(url):
    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
        response.raise_for_status()
        return BeautifulSoup(response.content, 'html.parser')
    except requests.RequestException as e:
        print(f"Error fetching the URL {url}: {e}")
        return None

def extract_text(soup):
    if soup is None:
        return []
    text_elements = soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li'])
    return [element.text.strip() for element in text_elements if element.text.strip()]

def search_content(content, query):
    query = query.lower()
    return [text for text in content if query in text.lower()]

def save_to_file(content, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        for item in content:
            f.write(item + '\n\n')

def generate_related_queries(main_topic):
    related_queries = [
        f"What is {main_topic}",
        f"{main_topic} definition",
        f"{main_topic} examples",
        f"{main_topic} importance",
        f"{main_topic} history",
        f"{main_topic} advantages and disadvantages",
        f"How does {main_topic} work",
        f"{main_topic} applications",
        f"Latest developments in {main_topic}",
        f"{main_topic} future trends"
    ]
    return related_queries

def automated_research(main_topic, num_websites_per_query=3):
    related_queries = generate_related_queries(main_topic)
    all_content = []
    sources = []

    for query in related_queries:
        print(f"\nResearching: {query}")
        urls = get_search_results(query, num_websites_per_query)
        
        print(f"Debug: URLs found for query '{query}': {urls}")
        
        for url in urls:
            print(f"Scraping: {url}")
            soup = scrape_content(url)
            if soup:
                content = extract_text(soup)
                all_content.extend(content)
                sources.append(url)
            time.sleep(random.uniform(1, 3))
        time.sleep(random.uniform(2, 5))

    return all_content, sources

def save_research_data(main_topic, content, sources):
    directory = f"{main_topic.replace(' ', '_')}_research"
    os.makedirs(directory, exist_ok=True)

    content_filename = os.path.join(directory, "research_content.txt")
    save_to_file(content, content_filename)

    sources_filename = os.path.join(directory, "sources.json")
    with open(sources_filename, 'w') as f:
        json.dump(sources, f, indent=2)

    print(f"Research data saved in the '{directory}' folder.")

def main():
    print("Welcome to the Automated Research Assistant!")
    main_topic = input("Enter the main topic you want to research: ")
    num_websites = int(input("Enter the number of websites to scrape per query (default is 3): ") or "3")

    print(f"\nStarting automated research on '{main_topic}'...")
    content, sources = automated_research(main_topic, num_websites)

    if content:
        print(f"\nScraped {len(content)} text elements from {len(sources)} websites.")
        save_research_data(main_topic, content, sources)

        while True:
            search_query = input("\nEnter a search query to find specific information (or 'quit' to exit): ")
            if search_query.lower() == 'quit':
                break

            results = search_content(content, search_query)
            if results:
                print(f"Found {len(results)} matches:")
                for i, result in enumerate(results[:5], 1):  # Limit to first 5 results
                    print(f"{i}. {result}\n")
                
                if len(results) > 5:
                    print(f"... and {len(results) - 5} more results. Refine your search for more specific information.")
            else:
                print("No matches found.")

        print("\nThank you for using the Automated Research Assistant!")
    else:
        print("No content found. This could be due to network issues or content blocking.")

if __name__ == "__main__":
    main() 