#!/bin/bash

# This is the first step in the pipeline
rm cats.*
scrapy crawl categories -o cats.json -s DOWNLOAD_DELAY=2 -s DEPTH_LIMIT=0 -s LOG_FILE=cats.log
mv cats.* /vagrant