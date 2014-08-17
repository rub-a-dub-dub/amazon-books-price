#!/usr/bin/env python

import io
import json
import argparse

def cmdLine():
    parser = argparse.ArgumentParser(description="Outputs a list of all leaf categories found from the Amazon crawler.")
    parser.add_argument("filename", help="JSON encoded output file from the crawler")
    parser.add_argument("output", help="JSON encoded output from this tool")
    return parser.parse_args()

def getLeafNodes(jsonData):
    answers = dict()
    retVal = []

    for entry in jsonData:
        name = entry["name"]
        parent = entry["ref"]
        url = entry["url"]
        count = entry["count"]

        if url.startswith("http"):
            # Get rid of some malformed entrants from crawling
            if parent in answers.keys():
                # this entry's parent is in the answers hash
                # that can't be since we only want leaf nodes
                try:
                    del answers[parent]
                except KeyError:
                    pass

            if url in answers:
                # that's strange - same category twice? ignore
                pass
            else:
                # we're not in the answer bin, put us in there
                answers[url] = [name, count]

    for url, value in answers.items():
        [name, count] = value
        count = int("".join(count.strip()[1:-1].split(",")))
        retVal.append({"url": url, "name": name, "count": count})

    return retVal

def main():
    args = cmdLine()
    dataFile = open(args.filename)
    data = json.load(dataFile)
    writeData = getLeafNodes(data)
    writeFile = io.open(args.output, "w", encoding="utf-8")
    writeFile.write(unicode(json.dumps(writeData, ensure_ascii=False)))

if __name__ == "__main__":
    main()