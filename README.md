# Sinceweb Games Content Automation

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
git clone https://github.com/your-username/sinceweb-content-automation.git
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
