# agents/web_research_agent.py

import requests
from bs4 import BeautifulSoup
from transformers import pipeline
import logging

# Initialize the summarization pipeline
summarizer = pipeline("summarization")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fetch_web_content(url):
    """
    Fetches the content of a web page.
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        logger.info(f"Fetched content from {url}")
        return response.text
    except requests.RequestException as e:
        logger.error(f"Error fetching {url}: {e}")
        return None

def extract_text(html_content):
    """
    Extracts and cleans text from HTML content.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    # Remove scripts and styles
    for script_or_style in soup(['script', 'style']):
        script_or_style.decompose()
    text = soup.get_text(separator=' ')
    # Collapse whitespace
    clean_text = ' '.join(text.split())
    logger.info("Extracted and cleaned text from HTML")
    return clean_text

def summarize_text(text, max_length=150, min_length=50):
    """
    Summarizes the extracted text.
    """
    try:
        summary = summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)
        logger.info("Generated summary of the text")
        return summary[0]['summary_text']
    except Exception as e:
        logger.error(f"Error summarizing text: {e}")
        return ""

def research_topic(topic, num_articles=3):
    """
    Conducts web research on a given topic by fetching, extracting, and summarizing content from multiple sources.
    """
    search_query = topic.replace(' ', '+')
    search_url = f"https://www.google.com/search?q={search_query}&num={num_articles}"
    
    # Fetch search results (Note: Scraping Google results directly may violate their TOS. Consider using an API.)
    try:
        response = requests.get(search_url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        logger.error(f"Error fetching search results: {e}")
        return []
    
    soup = BeautifulSoup(response.text, 'html.parser')
    links = []
    for item in soup.find_all('div', class_='tF2Cxc'):
        link_tag = item.find('a', href=True)
        if link_tag:
            links.append(link_tag['href'])
        if len(links) >= num_articles:
            break
    
    summaries = []
    for url in links:
        html_content = fetch_web_content(url)
        if html_content:
            text = extract_text(html_content)
            summary = summarize_text(text)
            summaries.append({'url': url, 'summary': summary})
    
    logger.info(f"Completed web research on topic: {topic}")
    return summaries
