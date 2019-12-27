import json
import os
import shutil
import logging

import tweepy
import wget
from tweepy import OAuthHandler

from os.path import expanduser
home = expanduser("~")
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")


class BaseTweetParser(object):
    def __init__(self):
        self.video_urls = []
        self.image_urls = []
        self.api = None
        consumer_key, consumer_secret = self._fetch_credentials()
        auth = OAuthHandler(consumer_key, consumer_secret)
        self.api = tweepy.API(auth)

    def _fetch_credentials(self):
        consumer_key = os.getenv("CONSUMER_KEY")
        consumer_secret = os.getenv("CONSUMER_SECRET")
        data = None
        if not all([consumer_secret, consumer_key]):
            with open(os.path.join(home, ".twitter.json"), "r") as f:
                data = json.loads(f.read())
        consumer_key = data["consumer_key"]
        consumer_secret = data["consumer_secret"]
        return consumer_key, consumer_secret

    def download(self, urls, file_type, destination):
        self._download_from_urls("MAIN", list(urls), file_type, destination)

    def _download_from_urls(self, name, batch, file_type, dest_dir):
        for url in batch:
            logging.info("Thread: {} downloading {}".format(name, url))
            media_file = url.split("/")[-1]
            path = os.path.join(dest_dir, media_file)
            wget.download(url, path)

    def process_tweet(self, tweet):
        try:
            extended = tweet.extended_entities
            if not extended:
                return []
            rv = []
            if "media" in extended:
                for x in extended["media"]:
                    if x["type"] == "photo":
                        url = x["media_url"]
                        rv.append(url)
                    elif x["type"] in ["video", "animated_gif"]:
                        variants = x["video_info"]["variants"]
                        variants.sort(key=lambda x: x.get("bitrate", 0))
                        url = variants[-1]["url"].rsplit("?tag")[0]
                        rv.append(url)
            return rv
        except AttributeError:
            logging.error("Extended entities not present in tweet")
            return []

    def fetch(self, account, tweet_mode='extended', limit=None):
        dir_name = account
        api = self.api

        epoch = 1
        video_urls = set()
        image_urls = set()
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
        os.mkdir(dir_name)

        for tweet in tweepy.Cursor(api.user_timeline, id=account, tweet_mode=tweet_mode).items(limit):
            print("Epoch: {}".format(epoch))
            epoch += 1
            rv = self.process_tweet(tweet)
            for r in rv:
                if r.endswith("mp4"):
                    video_urls.add(r)
                else:
                    image_urls.add(r)

        self.video_urls = list(video_urls)
        self.image_urls = list(image_urls)
