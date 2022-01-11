import praw
import pprint
import pandas as pd
import re

from datetime import datetime
from psaw import PushshiftAPI
from config import REDDIT_API as redditCredentials

maleUsernamesString = ['mr', 'boy', 'man', 'gay', 'lgbt', 'mister', 'guy']
femaleUsernamesString = ['girl', 'woman', 'lgbt', 'miss', 'gurl']

reddit = praw.Reddit(
    client_id = redditCredentials['clientID'],
    client_secret = redditCredentials['secretKey'],
    user_agent = redditCredentials['userAgent'],
    username = redditCredentials['username'],
    password = redditCredentials['password']
)

# Change subreddit to get datasets from other subreddit topic
subredditName = 'SuicideWatch'
api = PushshiftAPI(reddit)
gen = api.search_submissions(subreddit=subredditName, limit=10000)

df = pd.DataFrame()
pd.set_option('display.max_columns', None)

# get account age
def getAccountAge(authorName):
    createdEpoch = 0
    redditor = reddit.redditor(authorName)
    try:
        createdEpoch = redditor.created_utc
    except AttributeError:
        print(authorName)
        print("Could not get attribute")
    except:
        print("HTTP Error")
    return createdEpoch

def findUserGender(username, listStrings):
    found = True
    for i in listStrings:
        if username.find(i) != -1:
            return True
        else:
            continue
    found = False
    return found




def printSubmissionAttributes(submission):
    pprint.pprint(vars(submission))

for submission in gen:
    # print('Title: {},\nUsername: {},\nContent Post: {},\nUpvotes: {},\nAwards: {}'.format(submission.title, submission.author.name, submission.selftext, submission.ups, submission.all_awardings))
    if not submission.stickied and submission.is_self:
        authorName = ""
        # accountAge = 0
        if(submission.selftext == '[deleted]' or submission.selftext == '[removed]'):
            # Ignore deleted submissions
            continue
        elif(not (submission.author is None)):
            authorName = submission.author.name
            # accountAge = getAccountAge(authorName)

        if not findUserGender(authorName, femaleUsernamesString):
            continue

        if(not submission.selftext is None):
            submissionContent = submission.selftext.replace("\n", "")
        
        # Lowercase content
        submissionTitle = submission.title.lower()
        submissionContent = submissionContent.lower()
        # df = df.append({
        #     'Title': submissionTitle,
        #     'Username': authorName,
        #     'Content': submissionContent,
        #     'Upvotes': submission.ups,
        #     'NumberOfComments': submission.num_comments,
        #     # 'AccountCreatedEpoch' : accountAge,
        #     'Subreddit' : subredditName
        # }, ignore_index=True)
        df = df.append({
            'Title': submissionTitle,
            'Username': authorName,
            # 'AccountCreatedEpoch' : accountAge,
            'Subreddit' : subredditName
        }, ignore_index=True)
        df = df.drop_duplicates(subset='Username')

# print(df.head(10))
df.to_csv(subredditName + 'HugeCleaned.csv', index=False)