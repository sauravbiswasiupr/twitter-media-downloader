Twitter Media Downloader
========================

Download images and videos belonging to a particular twitter account. One needs to have a file 
called `.credentials.json` with entries for the attributes `consumer_key` and `consumer_secret`
of the json file. Alternatively if these attributes are present in the environment, the script 
will attempt to load them from the env. If both possibilites don't exist, then the script will fail.

Installation
------------

`pip install twitter-media-downloader`

Usage
-----


```
usage: twitter_media_dl [-h] [--key KEY] [--secret SECRET]
                                   [--account ACCOUNT] [--limit LIMIT]
                                   [--scrape-link] [--threaded]

optional arguments:
  -h, --help         show this help message and exit
  --account ACCOUNT  Twitter account handle
  --limit LIMIT      Number of media urls to download
  --scrape-link      Store scraped links to file
  --threaded         Use a threaded approach to download media. By default
                     spawns 10 threads
```

Examples
--------

`twitter_media_dl --account catsofinstagram --limit 100  --threaded`