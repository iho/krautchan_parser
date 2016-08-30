setup_db: 
	sudo -u postgres psql  -c "CREATE DATABASE kc_database;"                            & 
	sudo -u postgres psql  -c "CREATE USER kc_user WITH password 'qwerty';"             &
	sudo -u postgres psql  -c "GRANT ALL privileges ON DATABASE kc_database TO kc_user;"&         

cli:
	pgcli postgresql+psycopg2://kc_user:qwerty@127.0.0.1:5432/kc_database

crawl:
	cd kc; time scrapy crawl krautchan
