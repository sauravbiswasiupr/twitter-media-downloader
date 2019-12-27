import logging
import os
from argparse import ArgumentParser
from time import time

from base_tweet_parser import BaseTweetParser
from threaded_tweet_parser import ThreadedTweetParser

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")


if __name__ == "__main__":
    arg_parser = ArgumentParser()
    arg_parser.add_argument("--account", type=str, help="Twitter account handle", default="funnycat96")
    arg_parser.add_argument("--limit", type=int, default=3200, help="Number of media urls to download")
    arg_parser.add_argument("--scrape-link", dest="scrape", help="Store scraped links to file",
                            action='store_true')
    arg_parser.add_argument("--threaded", help="Use a threaded approach to download media. By default spawns 10 threads",
                            action="store_true")
    args = arg_parser.parse_args()
    if args.threaded:
        logging.info("Using threads to download images and videos")
        parser = ThreadedTweetParser(64)
    else:
        parser = BaseTweetParser()

    parser.fetch(args.account, limit=args.limit)

    if args.scrape:
        logging.info("Saving image and video links to file")
        with open(os.path.join(args.account, "images.txt"), "w") as f:
            for url in parser.image_urls:
                f.write(url + "\n")

        with open(os.path.join(args.account, "videos.txt"), "w") as f:
            for url in parser.video_urls:
                f.write(url + "\n")

    else:
        os.mkdir(os.path.join(args.account, "images"))
        os.mkdir(os.path.join(args.account, "videos"))

        start = time()
        parser.download(parser.video_urls, "videos", os.path.join(args.account, "videos"))
        parser.download(parser.image_urls, "images", os.path.join(args.account, "images"))
        end = time()
        logging.info("Spent {} seconds downloading".format(end - start))

        logging.info("Fetched {} image files".format(len(parser.image_urls)))
        logging.info("Fetched {} video files".format(len(parser.video_urls)))
