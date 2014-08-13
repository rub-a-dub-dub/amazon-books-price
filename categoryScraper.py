#!/usr/bin/env python

'''
This file identifies all of the categories in an Amazon top level marketplace (e.g. books, movies and tv, kitchen and dining etc.). Run with no command line options to get detailed help.
'''

from bs4 import BeautifulSoup
import urllib
import argparse 
import time
import sys

def argCheck():
    '''Argument checking function'''
    parser = argparse.ArgumentParser(description="This script will crawl an Amazon URL looking for sub-categories. It prints to STDOUT the subcategory name, it's URL and the number of items in that sub-category")
    parser.add_argument("url", help="The URL to begin the crawl from.")
    parser.add_argument("--maxdepth", help="The maximum search depth for the crawler (default 10).", type=int, default=10)
    return parser.parse_args()

def startCrawl(url, curDepth, maxDepth):
    '''This procedure crawls a page for sub-categories, prints them out and recurses for each until curDepth == maxDepth'''

    def processCategory(tag):
        '''This procedure processes matching category tags'''
        try:
            linkTag = tag.a
            if linkTag is not None:
                href = linkTag["href"]
                kids = linkTag.contents
                nameTag = kids[1]
                countTag = kids[2]
                name = nameTag.string
                count = countTag.string
                print "\"" + unicode(name) + "\",\"" + unicode(count) + "\",\"" + unicode(href) + "\"," + str(curDepth+1)
                return unicode(href)
        except Exception as e:
            pass

    try:
        # We're going to be reading the source URL first
        fid = urllib.urlopen(url)
        data = fid.read()
        fid.close()

        # now use BS4 to get the classes of interest
        soup = BeautifulSoup(data)
        sectionOfInterest = soup.find_all("div", {"class" : "categoryRefinementsSection"})
        if len(sectionOfInterest) > 1:
            raise ValueError("More than 1 div.categoryRefinementsSection found! Expected just 1.")
        elif len(sectionOfInterest) == 1:
            # dig in further to get what we want
            nextCrawlList = []
            for tag in sectionOfInterest[0].descendants:
                try:
                    if (tag.name == "ul"):
                        if ("data-typeid" in tag.attrs):
                            # We've found the category list
                            ulTag = tag.descendants
                            for subTag in ulTag:
                                try:
                                    if subTag.name == "li":
                                        nextLink = processCategory(subTag)
                                        if nextLink is not None:
                                            nextCrawlList.append(nextLink)
                                except Exception as e:
                                    pass
                except Exception as e:
                    pass

        # Now we have finished printing all of the results from this crawl session. Move on to the next - if we haven't hit our depth limit
        if curDepth == (maxDepth - 1)
            return

        for nextLink in nextCrawlList:
            time.sleep(0.5)
            startCrawl(nextLink, curDepth+1, maxDepth)

    except IOError as e:
        sys.stderr.write("*** Unable to read from " + url)

def main():
    '''Main programme entry point'''
    args = argCheck()
    startCrawl(args.url, 0, args.maxdepth)

if __name__ == "__main__":
    main()