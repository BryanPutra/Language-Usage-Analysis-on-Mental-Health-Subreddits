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
    print(currentEpoch)
    age = int(currentEpoch - createdEpoch)
    return age

def printSubmissionAttributes(submission):
    pprint.pprint(vars(submission))



# Change subreddit to get datasets from other subreddit topic for now its r/suicidewatch

for submission in reddit.subreddit('SuicideWatch').new(limit= 1):

    # print('Title: {},\nUsername: {},\nContent Post: {},\nUpvotes: {},\nAwards: {}'.format(submission.title, submission.author.name, submission.selftext, submission.ups, submission.all_awardings))
    if not submission.stickied and submission.is_self:
        accountAge = getAccountAge(submission)

        # printSubmissionAttributes(submission)

        # append somewhat cleaned data to dataframe
        df = df.append({
            'Title': submission.title,
            'Username': submission.author.name,
            'Content': submission.selftext,
            'Upvotes': submission.ups,
            'NumberOfComments': submission.num_comments,
            'CreatedOn': submission.created_utc,
            'AccountAgeMili' : accountAge,
        }, ignore_index=True)

        # append raw data to dataframe
        # df = df.append(vars(submission), ignore_index=True)
df.to_csv('test.csv', index=False)

# print(df)

