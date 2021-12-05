import praw
import pprint
import pandas as pd
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
def getAccountAge(submission):
    user = reddit.redditor(submission.author.name)
    createdEpoch = user.created_utc
    currentEpoch = datetime.now().timestamp()
    age = int(currentEpoch - createdEpoch)
    return age

def printSubmissionAttributes(submission):
    pprint.pprint(vars(submission))

# Change subreddit to get datasets from other subreddit topic for now its r/suicidewatch
for submission in reddit.subreddit('SuicideWatch').new(limit = 5):
    if not submission.stickied and submission.is_self:
        authorName = ""
        
        if(submission.selftext == '[deleted]' or submission.selftext == '[removed]'):
            # Ignore deleted submissions
            continue
        elif(not (submission.author is None)):
            authorName = submission.author.name
        
        submissionContent = submission.selftext.replace("\n", "")
        accountAge = getAccountAge(submission)
        
        # Preprocess goes here

        df = df.append({
            'Title': submission.title,
            'Username': authorName,
            'Content': submissionContent,
            'Upvotes': submission.ups,
            'NumberOfComments': submission.num_comments,
            'CreatedOn': submission.created_utc,
            'AccountAgeMili' : accountAge,
        }, ignore_index=True)
df.to_csv('SuicideWatchCleaned.csv', index=False)

# print(df)

