import praw
import pprint
import pandas as pd
import re

from datetime import datetime
from config import REDDIT_API as redditCredentials

reddit = praw.Reddit(
    client_id = redditCredentials['clientID'],
    client_secret = redditCredentials['secretKey'],
    user_agent = redditCredentials['userAgent'],
    username = redditCredentials['username'],
    password = redditCredentials['password']
)

# top_level_comments = list(submission.comments)
# all_comments = submission.comments.list()

# to sort comments or sort posts by 
# controversial
# gilded
# hot
# new
# rising
# top

# submission.comment_sort = "new"
# top_level_comments = list(submission.comments)

df = pd.DataFrame()

# get account age
def getAccountAge(authorName):
    createdEpoch = 0
    redditor = reddit.redditor(authorName)
    try:
        createdEpoch = redditor.created_utc
    except AttributeError:
        print(authorName)
        print("Could not get attribute")
    return createdEpoch

def printSubmissionAttributes(submission):
    pprint.pprint(vars(submission))

# Change subreddit to get datasets from other subreddit topic
subredditName = 'SuicideWatch'


# Change subreddit to get datasets from other subreddit topic for now its r/suicidewatch
for submission in reddit.subreddit(subredditName).hot(limit = 1000):
    # print('Title: {},\nUsername: {},\nContent Post: {},\nUpvotes: {},\nAwards: {}'.format(submission.title, submission.author.name, submission.selftext, submission.ups, submission.all_awardings))
    if not submission.stickied and submission.is_self:
        authorName = ""
        accountAge = 0
        if(submission.selftext == '[deleted]' or submission.selftext == '[removed]'):
            # Ignore deleted submissions
            continue
        elif(not (submission.author is None)):
            authorName = submission.author.name
            accountAge = getAccountAge(authorName)

        if(not submission.selftext is None):
            submissionContent = submission.selftext.replace("\n", "")
        
        # Lowercase content
        submissionTitle = submission.title.lower()
        submissionContent = submissionContent.lower()
        
        df = df.append({
            'Title': submissionTitle,
            'Username': authorName,
            'Content': submissionContent,
            'Upvotes': submission.ups,
            'NumberOfComments': submission.num_comments,
            'AccountCreatedEpoch' : accountAge,
            'Subreddit' : subredditName
        }, ignore_index=True)
df.to_csv(subredditName + 'Cleaned.csv', index=False)

# print(df)

        # print(getAccountAge(submission))  

        # printSubmissionAttributes(submission)

        # append somewhat cleaned data to dataframe
        # df = df.append({
        #     'Title': submission.title,
        #     'Username': submission.author,
        #     'Content': submission.selftext.replace("\n", ""),
        #     'Upvotes': submission.ups,
        #     'NumberOfComments': submission.num_comments,
        #     'CreatedOn': submission.created_utc
        # }, ignore_index=True)

        # append raw data to dataframe
        # df = df.append(vars(submission), ignore_index=True)

# print(df)

# df.to_csv('SuicideWatchRapi1.csv')
