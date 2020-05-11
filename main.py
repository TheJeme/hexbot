import tweepy
import time
import urllib.request
import os

auth = tweepy.OAuthHandler(os.environ["CONSUMER_TOKEN"], os.environ["CONSUMER_SECRET"]) # Place consumer_token and consumer_secret
auth.set_access_token(os.environ["ACCESS_TOKEN"], os.environ["ACCESS_TOKEN_SECRET"]) # Place access_token and access_token_secret
api = tweepy.API(auth)

def main():
    global color_number
    while color_number < 16777216: # Till last possible hex number
        hex_number = str(hex(color_number))[2:]
        format_length = 6 - len(hex_number)

        for i in range(format_length): #Adds 0 if needed
            hex_number = "0" + hex_number

        media_url = f"http://www.singlecolorimage.com/get/{hex_number}/500x500.png" # Path to image
        urllib.request.urlretrieve(media_url, "temp_image.jpg")            

        api.update_with_media("temp_image.jpg", status="#" + hex_number)
        print(media_url)
        color_number = color_number + 1

        f = open(os.getcwd() + "/count.txt","w+")
        f.write(str(color_number))
        f.close()

        time.sleep(15 * 60) # Posts every 15 minutes



if __name__ == "__main__":
    if not os.path.exists(os.getcwd() + "/count.txt"):
        f = open(os.getcwd() + "/count.txt","w+")
        f.write("0")
        f.close()
    f = open(os.getcwd() + "/count.txt", "r") 
    color_number = int(f.read())
    f.close()
    main()

