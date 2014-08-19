#!/bin/bash

grep 'DEBUG: Crawled' books.log | awk '{print $8}' | sed 's/\&page.*$//' | uniq
