import json
import bs4
import requests
import argparse


def get_args():
    category = [
        'world', 'us', 'politics', 'opinions', 'health',
        'entertainment', 'travel', 'style', 'sports'
    ]
    parser = argparse.ArgumentParser(
        description='CNN News Crawler',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        usage='python cnn_crawler.py --category world --page-limit 5 --output cnn_news.json'
    )
    parser.add_argument('--category', type=str, choices=category, help='Category of the news', required=True)
    parser.add_argument('--page-limit', type=int, default=5, help='Number of pages to crawl')
    parser.add_argument('--output', type=str, default='cnn_news.json', help='Output file name')
    args = parser.parse_args()
    return args


def parse_posts_links(soup):
    news_links = []
    for card in soup.select('a.container__link'):
        raw_link = card.get('href')
        if 'http' in raw_link:
            news_links.append(raw_link)
        else:
            news_links.append("https://edition.cnn.com" + raw_link)

    return list(set(news_links))


def parse_image_link(soup):
    srcs = []
    for img in soup.select('img'):
        if img.get('src') is not None:
            srcs.append(img.get('src').split('?')[0])

    return list(set(srcs))


def parse_other_links(soup):
    other_links = []
    for link in soup.select('a'):
        if link.get('href') is not None and "cnn.com" not in link.get('href') and "https" in link.get('href'):
            other_links.append(link.get('href'))

    return other_links


args = get_args()
max_pages = args.page_limit

print(f"Parsing {args.category} news.... ")
res = requests.get(f'https://edition.cnn.com/{args.category}')
soup = bs4.BeautifulSoup(res.text, 'html.parser')
print("Parsing posts links....")
news_links = parse_posts_links(soup)
total = len(news_links)

print(f"Found {total} posts links, crawling....")

crawled_pages = []

for link in news_links:
    print(f"Processing page {news_links.index(link) + 1} of {max_pages}")
    resp = requests.get(link)
    soup = bs4.BeautifulSoup(resp.text, 'html.parser')
    title = soup.title.text
    text = soup.select('div.article__content')
    text = text[0].text if len(text) > 0 else ""
    imgs = parse_image_link(soup)
    other_links = parse_other_links(soup)

    crawled_pages.append({
        'title': title,
        'text': text,
        'imgs': imgs,
        'other_links': other_links
    })
    if len(crawled_pages) >= max_pages:
        break

print(f"Writing to {args.output}....")

with open(args.output, 'w') as f:
    json.dump(crawled_pages, f)

print("Done!")
