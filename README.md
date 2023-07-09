# CNN Crawler
## Introduction
CNN Web Crawler is a web crawler that ceawls the CNN new website based on the categories provided while running it.

## Requirements
- Python 3.9
- BeautifulSoup4
- requests


## How to run
1. Clone the repository
```bash
git clone https://github.com/sameeramin/cnn-crawler.git
cd cnn-crawler
```
2. Install the requirements
```bash
pip install -r requirements.txt
```
3. Run the crawler file
```bash
python cnn_crawler.py --category world --page-limit 5 --output cnn_news.json
```

## Arguments
- `--category`: The category of the news to crawl. The default value is `world`.
- `--page-limit`: The number of pages to crawl. The default value is `5`.
- `--output`: The output file name. The default value is `cnn_news.json`.

