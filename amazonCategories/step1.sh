#!/bin/bash

# This is the first step in the pipeline
rm cats.*
scrapy crawl categories -o cats.json -s DOWNLOAD_DELAY=0.1 -s DEPTH_LIMIT=0 -s LOG_FILE=cats.log -s USER_AGENT="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36"
mv cats.* /vagrant