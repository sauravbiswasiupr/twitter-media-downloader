from concurrent.futures.thread import ThreadPoolExecutor
from base_tweet_parser import BaseTweetParser


class ThreadedTweetParser(BaseTweetParser):
    def __init__(self, num_threads):
        super(ThreadedTweetParser, self).__init__()
        self.num_threads = num_threads

    def download(self, urls, file_type, destination):
        batch_size = int(len(urls)/self.num_threads) + 1
        print("Batch size: {}".format(batch_size))
        with ThreadPoolExecutor(max_workers=self.num_threads) as executor:
            offset = 0
            for i in range(self.num_threads):
                batch = urls[offset:offset + batch_size]
                executor.submit(self._download_from_urls, i, batch, file_type, destination)
                offset += batch_size
