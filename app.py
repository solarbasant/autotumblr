import requests
import xml.etree.ElementTree as ET
import time

# Tumblr API credentials
API_KEY = "your_api_key"
API_SECRET = "your_api_secret"
OAUTH_TOKEN = "your_oauth_token"
OAUTH_TOKEN_SECRET = "your_oauth_token_secret"
BLOG_IDENTIFIER = "your_blog_identifier"  # e.g., "example.tumblr.com"

# Sitemap URL
SITEMAP_URL = "https://sinceweb.games/sitemap.xml"

def parse_sitemap(sitemap_url):
    """
    Parses a sitemap and extracts URLs.
    """
    response = requests.get(sitemap_url)
    response.raise_for_status()
    
    root = ET.fromstring(response.content)
    namespace = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
    urls = [url.find('ns:loc', namespace).text for url in root.findall('ns:url', namespace)]
    return urls

def create_tumblr_post(title, description, link):
    """
    Creates a post on Tumblr.
    """
    url = f"https://api.tumblr.com/v2/blog/{BLOG_IDENTIFIER}/post"
    headers = {
        "Authorization": f"Bearer {OAUTH_TOKEN}"
    }
    data = {
        "type": "link",
        "title": title,
        "description": description,
        "url": link
    }
    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 201:
        print(f"Successfully posted: {link}")
    else:
        print(f"Failed to post: {link}, Error: {response.json()}")

def main():
    """
    Main script to parse sitemap and post each link to Tumblr.
    """
    print("Fetching sitemap...")
    urls = parse_sitemap(SITEMAP_URL)
    
    for url in urls:
        title = f"Check out this link: {url}"  # Customize your title
        description = f"Visit the following link for more information: {url}"  # Customize your description
        
        print(f"Posting: {url}")
        create_tumblr_post(title, description, url)
        time.sleep(2)  # Rate limiting

if __name__ == "__main__":
    main()
