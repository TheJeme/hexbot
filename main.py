import os
import time
import urllib.request

import redis
import tweepy


# This is stored as an `int`.
MAX_HEX = 0xffffff


auth = tweepy.OAuthHandler(os.environ["CONSUMER_TOKEN"], os.environ["CONSUMER_SECRET"])
auth.set_access_token(os.environ["ACCESS_TOKEN"], os.environ["ACCESS_TOKEN_SECRET"])
api = tweepy.API(auth)

r = redis.Redis(
    host=os.environ["HOST"],
    port=os.environ["PORTTI"],
    password=os.environ["PASSWORD"])


def main(color_number=0):
    while color_number < MAX_HEX:
        # 6-digit zero padded hex string. e.g. "012def"
        hex_number = f"{color_number:06x}"

        media_url = f"http://www.singlecolorimage.com/get/{hex_number}/500x500.png"
        try:
            urllib.request.urlretrieve(media_url, "temp_image.jpg")
        except urllib.error.HTTPError:
            print(f"Hex value: {hex_number}")
            raise

        api.update_with_media("temp_image.jpg", status=f"#{hex_number}")
        print(media_url)
        r.incr('num')
        color_number = int(r.get("num"))
        # Posts every 15 minutes.
        time.sleep(15 * 60)


if __name__ == "__main__":
    r.incr('asd')
    print(r.get('asd'))
    #color_number = int(r.get("num"))
    #main(color_number)
