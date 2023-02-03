import dotenv
import time
import praw
dotenv.load_dotenv()
import os
import requests
# import redis
import random

# client = redis.Redis()
thanks = [
            "danke gosaimasu!",
            "dhanyavaad ji",
            "thank you, you so kind 🥺",
            "shukriya maalik 🙏🏻"
        ]

def process_comment(comment, reddit):
    body = comment.body
    author = comment.author.name
    id = comment.id
    # if client.exists(id):
    #     # we had replied to it so
    #     print("already replied to comment", id)
    #     return
    if comment.submission.author.name == "USI-BOT" or True:
        # we will listen to it
        lines = body.lower().split("\n")
        for line in lines:
            if line.startswith("alexa play"):
                sterm = line[10:]
                print(sterm, "song requested {sterm}")
                result = requests.get(
                                        "https://youtuber.onrender.com/alexa", 
                                        params={"sterm": sterm}
                                      ).json()
                if result:
                    title = result["data"]["title"]
                    url = result["data"]["url"]
                    views = result["data"]["views"]
                    imglink = result["data"]["snippet"]["thumbnails"]["url"]
                    if author == "peekybastards" or author == "kaptainkhichdi":
                        pass
                    else:
                        comment.upvote()
                    comment.reply(f"##### NOW PLAYING: \n\n [{title}]({url})")
                    client.set(id, 1)
                else:
                    print("invalid block", line)
            if line.startswith("good bot"):
                comment.reply(random.choice(thanks))
                if author == "peekybastards" or author == "kaptainkhichdi":
                    pass
                else:
                    comment.upvote()




def main():
   reddit = praw.Reddit(client_id=os.getenv("clientId"), 
                        client_secret=os.getenv("clientSecret"), 
                        username=os.getenv("username"), 
                        password=os.getenv("password"), 
                        user_agent=os.getenv("userAgent"))
   
   
   for comment in reddit.subreddit("unitedstatesofindia").stream.comments(skip_existing=True):
       process_comment(comment, reddit)

def start():
    while True:
        try:
            main()
        except Exception as e:
            print(e)
            time.sleep(10)

start()
