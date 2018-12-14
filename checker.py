#!/bin/env python

from sys import argv
import re
import json
import requests

params = {
    "DIR": argv[2] if len(argv) == 3 and argv[1].strip() == "-d" else None,
    "FILE": argv[2] if len(argv) == 3 and argv[1].strip() == "-f" else None,
    "URL": argv[2] if len(argv) == 3 and argv[1].strip() == "-u" else None
}

def check_url(url):
    r = requests.get(url)
    return extract_information(url, r.text)

def check_dir(dir):
    return

def check_file(file):
    with open(file) as f:
        data = json.loads(f.read())
        print("%s sites loaded" %len(data))
        for site in data:
            print(site['host'])
            extract_information(site["host"], site["data"])
    return

def extract_information(host, html):
    results = {}
    match = re.search("name=(\"|')generator(\"|')\scontent=(\"|')(WordPress .*)(\"|')\s/>", html)
    if match:
        results["wp-version"] = match.group(4).split('"')[0]
    pattern = re.compile("<script\s(.*)src=(.*)\?ver=(.*)('|\")", re.IGNORECASE)
    match = pattern.findall(html)
    results["scripts"] = []
    for m in match:
        results["scripts"].append({
            "script": m[1][1:].replace("http://%s" %host, "").replace("https://%s" %host, ""),
            "version": m[2]
        })
    print(results)
    return results


def main():
    results = None
    if params["DIR"]:
        results = check_dir(params["DIR"])
    elif params["FILE"]:
        results = check_file(params["FILE"])
    elif params["URL"]:
        results = check_url(params["URL"])
#    for result in results:
#        if result["wp-version"]:
            
    return 0

if __name__ == "__main__":
    exit(main())

