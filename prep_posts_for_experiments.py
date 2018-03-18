"""
This script creates one single dataframe with labeled data for machine learning applications.abs
It adds a new column: InfluenceOperation

It does so by first pulling all the known InfOp posts. They will have an InfluenceOperation value of 1.

Then it samples an equal number of non-InfoOp posts. They will have an InfluenceOperation value of 0.

Makes some assumptions about where data files live:
"""
import os
import pandas as pd
import glob

subreddits_of_interest = [
    'The_Donald',
    'worldnews',
    'news',
    'conspiracy',
]


# the csvs in raw_data/ should contain all reddit posts to twitter.com domains from 2016 and 2017
path = 'raw_data/'
all_files = glob.glob(os.path.join(path, "*.csv"))
# this one-liner loads all csv files into one pandas dataframe
posts_df = pd.concat((pd.read_csv(f) for f in all_files))


infop_path = 'tweets_in_csv/'
all_infop_files = glob.glob(os.path.join(infop_path, "*.csv"))
infop_posts = pd.concat((pd.read_csv(f, encoding='latin1') for f in all_infop_files))

print('Total num posts', len(posts_df.index))
print('Total infop posts', len(infop_posts.index))
infop_ids = list(infop_posts.id)
non_infop_posts = posts_df[~posts_df.id.isin(infop_ids)]
print('Total non-infop posts', len(non_infop_posts.index))

assert(len(posts_df.index) -  len(infop_posts.index) == len(non_infop_posts.index))


for subreddit in subreddits_of_interest:
    non_infop_posts[non_infop_posts.subreddit == subreddit].to_csv('non_infop_posts_by_sub/{}.csv'.format(subreddit))

infop_posts = infop_posts.assign(from_influence_operation=1)

non_infop_posts = non_infop_posts.assign(from_influence_operation=0)

# merged = pd.concat(
#     [
#         infop_posts,
#         non_infop_posts
#     ]

# )
# merged.to_csv('labeled_data/labeled_posts.csv')


posts_noninfop_sampled = pd.concat(
    [
        infop_posts,
        non_infop_posts.sample(10000),
    ]

)
posts_noninfop_sampled.to_csv('labeled_data/labeled_posts_10k_neg.csv')

# dev_posts = pd.concat(
#     [
#         infop_posts.sample(10),
#         non_infop_posts.sample(10),
#     ]

# )
# dev_posts.to_csv('labeled_data/dev_posts.csv')