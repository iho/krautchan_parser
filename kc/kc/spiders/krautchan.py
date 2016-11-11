# -*- coding: utf-8 -*-
import psycopg2
import scrapy


conn = psycopg2.connect(database="kc_database",
                        user="kc_user", password="qwerty", host='localhost')
cur = conn.cursor()


def prepare_database():
    cur.execute("""
CREATE OR REPLACE FUNCTION upsert_post(id_ INT,date_ TIMESTAMP, text_ TEXT, url_ TEXT, country_code_ TEXT, country_path_ TEXT, thread_ INT, main_post_ BOOLEAN) RETURNS VOID AS $$
DECLARE 
BEGIN 
    UPDATE post SET  date=date_
    WHERE id=id_;
    IF NOT FOUND THEN 
    INSERT INTO post (id, date, text, url, country_code, country_path, thread, main_post ) values 
    (id_, date_, text_, url_, country_code_, country_path_, thread_, main_post_);
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
    country_code TEXT,
    country_path TEXT,
    thread INTEGER, 
    main_post BOOLEAN 
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
    def parse(self, response):
        prepare_database()
        for uri in \
                response.xpath('//main[@class="catalog"]/article/article/div/header/a/@href').extract():
            url = 'http://krautchan.net' + uri
            yield scrapy.Request(url, callback=self.parse_page)

    def parse_page(self, response):
        base_url = response.url
        thread_id = response.xpath(
            '//*/div[1]/div/div[1]/span[4]/a[2]/text()').extract_first()
        id = thread_id
        date = response.xpath(
            '//*/div[1]/div/div[1]/span[3]/text()').extract_first()
        text = response.xpath(
            '//*/div[1]/div/div[@class="postbody"]/blockquote').extract_first()
        anchor = response.xpath(
            '//*/div[1]/div[1]/span[4]/a[1]/@href').extract_first()
        url = base_url + anchor
        country_image_path = response.xpath('//*/div[1]/div/img/@src').extract_first()
        country = country_image_path[14:-4]
        main_post = True
        cur.execute("""SELECT upsert_post(%s, %s::TIMESTAMP, %s, %s, %s, %s, %s, %s);""",
                    (id, date,  text, url, country, country_image_path, thread_id, main_post ))

        conn.commit()
        self.succesful_count += 1

        main_post = False
        for reply in response.xpath('//*[@class="postreply"]'):
            anchor = reply.xpath(
                './/*[@class="postnumber"]/a[1]/@href').extract_first()
            url = base_url + anchor
            date = reply.xpath( './/*[@class="postdate"]/text()').extract_first()
            country_image_path = reply.xpath( './/img/@src').extract_first()
            country = country_image_path[14:-4]
            id = reply.xpath('.//*[@class="postnumber"]/a[2]/text()').extract_first()
            text = reply.xpath('div/blockquote').extract_first()
            cur.execute("""SELECT upsert_post(%s, %s::TIMESTAMP, %s, %s, %s, %s, %s, %s);""",
                    (id, date,  text, url, country, country_image_path, thread_id, main_post ))
            conn.commit()
            self.succesful_count += 1
        print(self.errors_count, self.succesful_count)
