# krautchan_parser
Scrape all posts  from http://krautchan.net/int

## Require python2.7.* and postgresql 9.*

## Setup 
For start scraping run in shell: 
```
pip install -r requirements.txt
make setup_db
make crawl
```

## Shell 
To run sql queries run: 
```
make cli
```
Example of output
```
kc_database> SELECT count(*) FROM post;
+---------+
|   count |
|---------|
|    7190 |
+---------+
SELECT 1
Time: 0.006s
kc_database> 
```
