import praw
from stem import Signal
from stem.control import Controller

import pickle
passList = []
#load the list of list of [username,password,client_id,client_secret]
with open('reddit_pass.p','rb') as pfile:
    passList = pickle.load(pfile)

comment_url = input("Enter comment url: ")
print(comment_url)


slash_pos = comment_url[:-1].rfind("/")
submission_url = comment_url[:slash_pos]
comment_id = comment_url[slash_pos+1: len(comment_url)-1]
print(submission_url)
print(comment_id)

for credentials in passList:

    bot = praw.Reddit(user_agent='Me',
                      client_id=credentials[2],
                      client_secret=credentials[3],
                      username=credentials[0],
                      password=credentials[1])

    subreddit = bot.subreddit('Tronix')
    comments = subreddit.stream.comments()

    submission = bot.submission(url=submission_url)

    i=0
    for comment in submission.comments:
        if comment.id == comment_id:
            print(comment.body)
