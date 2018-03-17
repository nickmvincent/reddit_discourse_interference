"""
Analysis of Reddit posts related to 2016 and 2017 american discourse influence.
"""
import os
import pandas as pd
import glob

path = 'tweets_in_csv/'
all_files = glob.glob(os.path.join(path, "*.csv"))
infop_posts = pd.concat((pd.read_csv(f, encoding='latin1') for f in all_files))
infop_posts.subreddit = infop_posts.subreddit.astype('category')

counts = infop_posts.subreddit.value_counts()
counts.to_csv('infop_posts_value_counts.csv')

for subreddit, count in counts.to_dict().items():
    infop_posts[infop_posts.subreddit == subreddit].to_csv(
        'posts_by_sub/{}.csv'.format(subreddit)
    )
