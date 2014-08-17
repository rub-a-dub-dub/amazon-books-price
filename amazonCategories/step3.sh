#!/bin/bash

# This is the third step in the pipeline
rm books.*
scrapy crawl bookListCategory -o books.json -s DOWNLOAD_DELAY=0.1 -s DEPTH_LIMIT=0 -s LOG_FILE=books.log -s USER_AGENT="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36"
mv books.* /vagrant