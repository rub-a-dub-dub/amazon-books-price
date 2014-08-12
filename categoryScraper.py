'''
This file identifies all of the categories in an Amazon top level marketplace (e.g. books, movies and tv, kitchen and dining etc.). Run with no command line options to get detailed help.
'''

from bs4 import BeautifulSoup
import urllib
import argparse 

def argCheck():
    '''Argument checking function'''
    parser = argparse.ArgumentParser(description="This script will crawl an Amazon URL looking for sub-categories. It prints to STDOUT the subcategory name, it's URL and the number of items in that sub-category")
    parser.add_argument("url", help="The URL to begin the crawl from.")
    parser.add_argument("--maxdepth", help="The maximum search depth for the crawler (default 10).", type=int, default=10)
    return parser.parse_args()

def startCrawl(url, curDepth, maxDepth):
    '''This procedure crawls a page for sub-categories, prints them out and recurses for each until curDepth == maxDepth'''
    if curDepth === maxDepth return
    try:
        # We're going to be reading the source URL first
        fid = urllib.urlopen(url)
        data = fid.readlines()
        fid.close()

        # now use BS4 to get the classes of interest
        soup = BeautifulSoup(data)
        print(soup.find_all("div", {"class" : "categoryRefinementsSection"}))
    except e as IOError:
        print "*** Unable to read from " + url

def main():
    '''Main programme entry point'''
    args = argCheck()
    startCrawl(args.url, 0, args.maxdepth)