# -*- coding: utf-8 -*-
import scrapy

import html2text
import psycopg2

h = html2text.HTML2Text()
# h.ignore_links = True

conn = psycopg2.connect(database="kc_database", user="kc_user", password="qwerty", host='localhost')
cur = conn.cursor()
def prepare_database():
    cur.execute("""
CREATE OR REPLACE FUNCTION upsert_post(id_ INT,date_ TIMESTAMP, text_ TEXT, url_ TEXT, thread_ INT) RETURNS VOID AS $$
DECLARE 
BEGIN 
    UPDATE post SET  date=date_, text=text_, url=url_, thread=thread_
    WHERE id=id_;
    IF NOT FOUND THEN 
    INSERT INTO post values (id_, date_, text_, url_, thread_);
    END IF; 
END; 
$$ LANGUAGE 'plpgsql';
""")
    cur.execute("""
CREATE TABLE IF NOT EXISTS post
(
    id INTEGER PRIMARY KEY NOT NULL,
    date TIMESTAMP WITH TIME ZONE,
    text TEXT,
    url TEXT,
    thread INTEGER
);
""")
    print('Table created')
class KrautchanSpider(scrapy.Spider):
    name = "krautchan"
    allowed_domains = ["krautchan.net"]
    start_urls = (
        'http://krautchan.net/catalog/int',
    )
    errors_count = 0
    succesful_count = 0
    def clean_html(self, text):
        try:
            text = h.handle(text)
            text = text.strip()
            return text
        except Exception as e:
            print(e)
            self.errors_count += 1
            return ''

    def parse(self, response):
        prepare_database()
        for uri in \
            response.xpath('//main[@class="catalog"]/article/article/div/header/a/@href').extract():
            url = 'http://krautchan.net' + uri
            yield scrapy.Request(url, callback=self.parse_page)

    def parse_page(self, response):
        url = response.url

        thread_id = response.xpath('//*/div[1]/div/div[1]/span[4]/a[2]/text()').extract_first() 
        id = thread_id 
        date = response.xpath('//*/div[1]/div/div[1]/span[3]/text()').extract_first()
        text = h.handle(response.xpath('//*/div[1]/div/div[@class="postbody"]/blockquote').extract_first())
        text = self.clean_html(text)
        # print(id, date,  text, url, thread_id)
        cur.execute("SELECT upsert_post(%s, %s::TIMESTAMP, %s, %s,%s);", (id, date,  text, url, thread_id))
        conn.commit()
        self.succesful_count += 1
        for reply in response.xpath('//*[@class="postreply"]'):
            date = reply.xpath('.//*[@class="postdate"]/text()').extract_first()
            id = reply.xpath('.//*[@class="postnumber"]/a[2]/text()').extract_first()
            text = reply.xpath('div/blockquote').extract_first()
            text = self.clean_html(text)
            cur.execute("SELECT upsert_post(%s, %s::TIMESTAMP, %s, %s,%s);", (id, date,  text, url,
                thread_id) )
            conn.commit()
            self.succesful_count += 1


        print(self.errors_count, self.succesful_count)
