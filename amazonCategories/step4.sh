#!/bin/bash

# This is the fourth and final step in the pipeline
rm prices.*
scrapy crawl bookDetails -o prices.json -s DOWNLOAD_DELAY=0.1 -s DEPTH_LIMIT=0 -s LOG_FILE=prices.log -s USER_AGENT="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36"
mv prices.* /vagrant