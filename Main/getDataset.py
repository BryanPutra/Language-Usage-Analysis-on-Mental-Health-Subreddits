import praw
import pprint
import pandas as pd
from config import REDDIT_API as redditCredentials

reddit = praw.Reddit(
    client_id=redditCredentials['clientID'],
    client_secret=redditCredentials['secretKey'],
    user_agent=redditCredentials['userAgent'],
    username=redditCredentials['username'],
    password=redditCredentials['password']
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

# Change subreddit to get datasets from other subreddit topic for now its r/suicidewatch

for submission in reddit.subreddit('SuicideWatch').hot(limit= 1000):

    # print('Title: {},\nUsername: {},\nContent Post: {},\nUpvotes: {},\nAwards: {}'.format(submission.title, submission.author.name, submission.selftext, submission.ups, submission.all_awardings))
    if not submission.stickied and submission.is_self:
        # pprint.pprint(vars(submission))
        # df = df.append({
        #     'Title': submission.title,
        #     'Username': submission.author,
        #     'Content': submission.selftext,
        #     'Upvotes': submission.ups,
        #     'NumberOfComments': submission.num_comments,
        #     'CreatedOn': submission.created_utc
        # }, ignore_index=True)

        # df = df.append(vars(submission), ignore_index=True)

# print(df)

df.to_csv('SuicideWatchRaw.csv', index=False)
