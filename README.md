# krautchan_parser
Scrape all posts  from http://krautchan.net/int

## Require python3 and postgresql

## Setup 
For start scraping run in shell: 
```
pip install -r requirements.txt
make setup_db
cd kc 
time scrapy crawl krautchan
```
