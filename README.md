# Facebook and Tumblr Content Automation
From Sitemap URL to Tumblr Blog & Facebook Page.
## Project Description

This is an open-source project that automates the process of fetching content from a website, generating SEO-friendly descriptions, and posting the content to social media platforms like Facebook and Tumblr. The project is designed to help website owners and content creators streamline their content distribution and promotion efforts, ultimately driving more traffic and engagement to their online properties.

The key features of this project include:

1. **Sitemap Fetching**: The script fetches URLs from a sitemap, which is a file that lists all the pages on a website. This allows the script to identify and process new content as it is added to the website.

2. **Content Extraction**: The script uses web scraping techniques to extract relevant content from the web pages, including the title, meta description, H1 heading, and the main content body.

3. **SEO Description Generation**: The script utilizes a language model (GPT-2) to generate a compelling SEO-friendly description for each piece of content. This description is designed to entice readers and improve the content's visibility in search engine results.

4. **Keyword Extraction**: The script employs a combination of RAKE (Rapid Automatic Keyword Extraction) and BERT (Bidirectional Encoder Representations from Transformers) to identify the most relevant keywords from the content. These keywords are then used to generate relevant hashtags for the social media posts.

5. **Social Media Posting**: The script posts the content, along with the generated description and keywords, to a configured Facebook page and Tumblr blog. This helps to increase the visibility and reach of the content across multiple social media platforms.

6. **Duplicate Prevention**: The script keeps track of the URLs that have already been posted to avoid duplicating content on the social media platforms.

7. **Automated Scheduling**: The project includes a GitHub Actions workflow that automatically runs the content automation script on a scheduled basis (e.g., every hour) and allows for manual triggering as needed.

By automating these content distribution and promotion tasks, the Sinceweb Games Content Automation project aims to help website owners and content creators save time and resources while improving the visibility and engagement of their online content.

## Key Benefits

- **Increased Content Visibility**: The automated posting to social media platforms helps to increase the reach and visibility of the website's content, driving more traffic and engagement.
- **Improved SEO Performance**: The generation of SEO-friendly descriptions and the inclusion of relevant keywords can improve the content's performance in search engine results.
- **Time and Resource Savings**: By automating the content distribution and promotion tasks, website owners and content creators can focus on creating high-quality content rather than spending time on manual social media posting.
- **Consistent Content Promotion**: The scheduled and automated nature of the script ensures that new content is consistently promoted across the configured social media platforms.
- **Flexibility and Customization**: The project is open-source, allowing users to customize and extend the functionality to fit their specific needs and requirements.

## GitHub Workflow

This project includes a GitHub workflow that automatically runs the content automation script on a schedule and allows for manual triggering.

The workflow file is named `.github/workflows/auto-post-to-social-media.yml` and contains the following configuration:

```yaml
name: Auto Post to Social Media
on:
  schedule:
    - cron: '0 */1 * * *'  # Runs every 1 hour
  workflow_dispatch:        # Allows manual triggering

jobs:
  run-script:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v3
        
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          python -m nltk.downloader punkt stopwords
      
      - name: Run script
        run: python app.py
```

This workflow is triggered in two ways:

1. **Schedule**: The workflow runs every hour (at the top of the hour) due to the `cron: '0 */1 * * *'` schedule.
2. **Manual Triggering**: The workflow can be manually triggered using the "Run workflow" button in the GitHub Actions tab.

When the workflow runs, it performs the following steps:

1. **Checkout Repository**: The repository is checked out using the `actions/checkout@v3` action.
2. **Set up Python**: The Python environment is set up using the `actions/setup-python@v4` action, with Python version 3.9.
3. **Install Dependencies**: The required Python dependencies are installed using `pip install -r requirements.txt`, and the necessary NLTK data is downloaded.
4. **Run Script**: The `app.py` script is executed, which contains the content automation logic.

## Configuration

To use this project, you'll need to provide the necessary configuration values for the Facebook Graph API and Tumblr API. Update the following variables in the `app.py` file:

```python
FB_ACCESS_TOKEN = 'YOUR_FACEBOOK_ACCESS_TOKEN'
FB_PAGE_ID = 'YOUR_FACEBOOK_PAGE_ID'

TUMBLR_CONSUMER_KEY = 'YOUR_TUMBLR_CONSUMER_KEY'
TUMBLR_CONSUMER_SECRET = 'YOUR_TUMBLR_CONSUMER_SECRET'
TUMBLR_OAUTH_TOKEN = 'YOUR_TUMBLR_OAUTH_TOKEN'
TUMBLR_OAUTH_SECRET = 'YOUR_TUMBLR_OAUTH_SECRET'
TUMBLR_BLOG_NAME = 'YOUR_TUMBLR_BLOG_NAME'
```

## Installation and Usage

1. Clone the repository:

```
git clone https://github.com/sinceweb/autotumblr.git
```

2. Install the required dependencies:

```
pip install -r requirements.txt
```

3. Run the script:

```
python app.py
```

The script will fetch content from the specified sitemap, generate SEO descriptions and keywords, and post the content to the configured Facebook page and Tumblr blog.

## Contributing

If you find any issues or have suggestions for improvements, feel free to open an issue or submit a pull request. Contributions are welcome!

## License

This project is licensed under the [MIT License](LICENSE).
