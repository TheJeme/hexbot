import os
import time
import urllib.request

import redis
import tweepy


auth = tweepy.OAuthHandler(os.environ["CONSUMER_TOKEN"], os.environ["CONSUMER_SECRET"]) # Place consumer_token and consumer_secret
auth.set_access_token(os.environ["ACCESS_TOKEN"], os.environ["ACCESS_TOKEN_SECRET"]) # Place access_token and access_token_secret
api = tweepy.API(auth)

r = redis.Redis(
    host=os.environ["HOST"],
    port=7839,
    password=os.environ["PASSWORD"])

def main():
    global color_number
    while color_number < 16777216: # Till last possible hex number
        hex_number = str(hex(color_number))[2:]
        format_length = 6 - len(hex_number)

        for i in range(format_length): #Adds 0 if needed
            hex_number = "0" + hex_number

        media_url = f"http://www.singlecolorimage.com/get/{hex_number}/500x500.png"
        try:
            urllib.request.urlretrieve(media_url, "temp_image.jpg")
        except urllib.error.HTTPError:
            print(f"Hex value: {hex_number}")
            raise

        api.update_with_media("temp_image.jpg", status="#" + hex_number)
        print(media_url)
        r.incr('num')
        color_number = int(r.get("num"))
        time.sleep(15 * 60) # Posts every 15 minutes



if __name__ == "__main__":
    color_number = int(r.get("num"))
    main()
