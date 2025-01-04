import requests
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import logging
from typing import Dict, List, Tuple, Optional
import re
import time
import random
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import nltk
from rake_nltk import Rake
from collections import Counter
import pytumblr

# Download required NLTK data
nltk.download('punkt')
nltk.download('stopwords')

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Social media configuration
FB_ACCESS_TOKEN = 'EAAZAUZCGL4QRoBO8ScQVfVn8e6DJ70rtfhtZAtTzZAeZBX6H0WGFzQ8NMJdhOZAZCJFKbKJccZCn2aepDWk556NeC8pZAiZC6oCcUznyQZAcZBvyYNKN55qG5aWiCWSZCt2WtF4kKJPJ8CfE2L0AC10ZCdccRUfHmZBGs8vR7eSi1PvdiSv2t9dTI4vZBGZBcoltrxw5VE2UnO39GpiemfFL3kOW2'
FB_PAGE_ID = '514966971702760'
FB_POST_URL = f'https://graph.facebook.com/{FB_PAGE_ID}/feed'

# Tumblr configuration
TUMBLR_CONSUMER_KEY = 'ziN085M7AMJw90HhZ3VtAx0w4teaxZG5lyIrbxAi8C2nBEqfZt'
TUMBLR_CONSUMER_SECRET = 'Ci243vMK7uu6q7Sql2kLOHOMKI6FSSdCdRLc31ddGb0caUbvTj'
TUMBLR_OAUTH_TOKEN = '7fWoM62TFQasGuf9d35FUsUBgpKWgEEpWCejeTFVzvPQcVX6Dd'
TUMBLR_OAUTH_SECRET = 'xZt7qpf2YERA9YfyeJNg1XMc6huDHBacbQiqsGZH9YLzeDIySV'
TUMBLR_BLOG_NAME = 'sincewebgames.tumblr.com'

# [Previous LLMProcessor class remains unchanged]
class LLMProcessor:
    def __init__(self):
        """Initialize the LLM models and processors."""
        logger.info("Initializing language models...")
        
        # Initialize text generation pipeline with GPT2
        self.generator = pipeline('text-generation', 
                                model='distilgpt2',
                                max_length=200)
        
        # Initialize BERT for keyword extraction
        self.tokenizer = AutoTokenizer.from_pretrained('distilbert-base-uncased')
        self.model = AutoModelForSequenceClassification.from_pretrained('distilbert-base-uncased')
        
        # Initialize RAKE for additional keyword extraction
        self.rake = Rake()
        logger.info("Models initialized successfully")

    def extract_keywords(self, text: str) -> List[str]:
        """Extract keywords using RAKE and BERT."""
        # Use RAKE for initial keyword extraction
        self.rake.extract_keywords_from_text(text)
        rake_keywords = self.rake.get_ranked_phrases()[:10]
        
        # Use BERT tokenizer to identify important terms
        tokens = self.tokenizer(text, truncation=True, padding=True, return_tensors="pt")
        important_tokens = tokens['input_ids'][0]
        words = self.tokenizer.convert_ids_to_tokens(important_tokens)
        
        # Combine and clean keywords
        all_keywords = rake_keywords + [word.replace('##', '') for word in words if not word.startswith('##')]
        cleaned_keywords = [k.lower() for k in all_keywords if len(k) > 3 and not k.startswith('#')]
        
        # Count frequencies and get top keywords
        keyword_freq = Counter(cleaned_keywords)
        top_keywords = [k for k, _ in keyword_freq.most_common(5)]
        
        return top_keywords

    def generate_seo_description(self, content: Dict[str, str]) -> Tuple[str, List[str]]:
        """Generate SEO description using GPT2 and extract keywords."""
        try:
            # Prepare input text
            input_text = f"""
            Generate a compelling SEO description (200 words max) that includes relevant keywords:
            Title: {content['title']}
            Topic: {content['meta_description']}
            Make sure the description summarizes the key themes and highlights of the content while enticing readers to engage further. The tone should be clear and engaging, encouraging clicks.
            """

            # Generate description
            generated = self.generator(input_text, 
                                    max_length=200,
                                    num_return_sequences=1,
                                    temperature=0.7)
            
            # Clean and format the generated text
            description = generated[0]['generated_text'].split('\n')[0]
            description = re.sub(r'\s+', ' ', description).strip()
            
            # Truncate to SEO-friendly length
            if len(description) > 155:
                description = description[:152] + '...'

            # Extract keywords from all available content
            full_content = f"{content['title']} {content['meta_description']} {content['main_content']}"
            keywords = self.extract_keywords(full_content)

            return description, keywords

        except Exception as e:
            logger.error(f"Error in description generation: {e}")
            return content['meta_description'][:155] if content['meta_description'] else content['title'][:155], []
# [Previous ContentFetcher class remains unchanged]
class ContentFetcher:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })

    def fetch_sitemap(self, sitemap_url: str) -> List[str]:
        """Fetch URLs from sitemap."""
        try:
            response = self.session.get(sitemap_url)
            response.raise_for_status()
            
            content = response.text.replace(' xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"', '')
            root = ET.fromstring(content)
            
            urls = root.findall('.//loc') or root.findall('./url/loc')
            return [url.text for url in urls]
            
        except Exception as e:
            logger.error(f"Failed to fetch sitemap: {e}")
            return []

    def fetch_page_content(self, url: str) -> Optional[Dict[str, str]]:
        """Fetch and parse page content."""
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            content = {
                'title': '',
                'meta_description': '',
                'h1': '',
                'main_content': '',
            }

            # Extract title
            if soup.title:
                content['title'] = soup.title.text.strip()

            # Extract meta description
            meta_desc = soup.find('meta', attrs={'name': 'description'})
            if meta_desc:
                content['meta_description'] = meta_desc.get('content', '').strip()

            # Extract H1
            h1 = soup.find('h1')
            if h1:
                content['h1'] = h1.text.strip()

            # Extract main content
            main_content = soup.find('main') or soup.find('article') or soup.find('div', class_='content')
            if main_content:
                for element in main_content(['script', 'style']):
                    element.decompose()
                content['main_content'] = ' '.join(main_content.stripped_strings)

            return content

        except Exception as e:
            logger.error(f"Failed to fetch page {url}: {e}")
            return None

class SocialMediaPoster:
    def __init__(self, fb_token: str, fb_page_id: str, 
                 tumblr_credentials: Dict[str, str], tumblr_blog: str):
        self.posted_urls = set()
        
        # Facebook setup
        self.fb_token = fb_token
        self.fb_page_id = fb_page_id
        self.fb_post_url = f'https://graph.facebook.com/{fb_page_id}/feed'
        
        # Tumblr setup
        self.tumblr_client = pytumblr.TumblrRestClient(
            tumblr_credentials['consumer_key'],
            tumblr_credentials['consumer_secret'],
            tumblr_credentials['oauth_token'],
            tumblr_credentials['oauth_secret']
        )
        self.tumblr_blog = tumblr_blog

    def create_post_content(self, url: str, description: str, keywords: List[str]) -> str:
        """Create formatted post content with description and hashtags."""
        hashtags = ' '.join([f"#{keyword.replace(' ', '').replace('-', '')}" 
                           for keyword in keywords[:3] 
                           if keyword and len(keyword) < 20])
        
        return (f"{description}\n\n"
                f"{hashtags}\n\n"
                f"Play online Games on Sinceweb: {url}")

    def post_to_facebook(self, url: str, message: str) -> bool:
        """Post content to Facebook page."""
        try:
            payload = {
                'access_token': self.fb_token,
                'message': message,
                'link': url
            }

            response = requests.post(self.fb_post_url, data=payload)
            response.raise_for_status()
            logger.info(f"Successfully posted to Facebook: {url}")
            return True

        except Exception as e:
            logger.error(f"Failed to post to Facebook: {e}")
            return False

    def post_to_tumblr(self, url: str, message: str, content: Dict[str, str]) -> bool:
        """Post content to Tumblr blog."""
        try:
            self.tumblr_client.create_link(
                self.tumblr_blog,
                title=content['title'],
                url=url,
                description=message,
                tags=['html5games', 'games', 'gaming', 'onlinegame'],
                state="published"
            )
            logger.info(f"Successfully posted to Tumblr: {url}")
            return True

        except Exception as e:
            logger.error(f"Failed to post to Tumblr: {e}")
            return False

    def post_content(self, url: str, description: str, keywords: List[str], content: Dict[str, str]) -> bool:
        """Post content to all configured social media platforms."""
        message = self.create_post_content(url, description, keywords)
        
        # Post to both platforms
        fb_success = self.post_to_facebook(url, message)
        tumblr_success = self.post_to_tumblr(url, message, content)
        
        if fb_success or tumblr_success:
            self.posted_urls.add(url)
            return True
            
        return False

def main():
    # Initialize components
    content_fetcher = ContentFetcher()
    llm_processor = LLMProcessor()
    
    tumblr_credentials = {
        'consumer_key': TUMBLR_CONSUMER_KEY,
        'consumer_secret': TUMBLR_CONSUMER_SECRET,
        'oauth_token': TUMBLR_OAUTH_TOKEN,
        'oauth_secret': TUMBLR_OAUTH_SECRET
    }
    
    social_media = SocialMediaPoster(
        FB_ACCESS_TOKEN, 
        FB_PAGE_ID,
        tumblr_credentials,
        TUMBLR_BLOG_NAME
    )
    
    sitemap_url = 'https://sinceweb.games/sitemap.xml'

    try:
    # Fetch URLs from sitemap
        logger.info(f"Fetching URLs from sitemap: {sitemap_url}")
        urls = content_fetcher.fetch_sitemap(sitemap_url)

        if not urls:
            logger.error("No URLs found in sitemap")
        else:
        # Filter out already posted URLs
            available_urls = [url for url in urls if url not in social_media.posted_urls]

            if not available_urls:
                logger.info("All URLs have been posted.")
            else:
            # Select random URL to post
                url_to_post = random.choice(available_urls)
            
            # Fetch content
                content = content_fetcher.fetch_page_content(url_to_post)
                if content:
                # Generate SEO description and keywords using LLM
                    description, keywords = llm_processor.generate_seo_description(content)

                # Post to social media platforms
                    success = social_media.post_content(url_to_post, description, keywords, content)
                
                    if success:
                        logger.info(f"Posted URL: {url_to_post}")
                        logger.info(f"Description: {description}")
                        logger.info(f"Keywords: {keywords}")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()