"""
Analysis of Reddit posts related to 2016 and 2017 american discourse influence.
"""
import os
import pandas as pd
import glob

with open('handles.txt', 'r') as handles_file:
    handles = handles_file.read().split('\n')
path = 'raw_data/'
all_files = glob.glob(os.path.join(path, "*.csv"))
posts_df = pd.concat((pd.read_csv(f) for f in all_files))

posts_df.author.value_counts().to_csv('author_values_counts.csv')
posts_df.domain.value_counts().to_csv('domain_values_counts.csv')
print(posts_df.describe(include='all'))
urls_lowercase = posts_df.url.str.lower().str

marked_posts = None
reddit_user_matches_twitter_handle = None


# probably should not do this

with open('checked_handles.txt', 'r') as checked_handles_file:
    checked_handles = checked_handles_file.read().split('\n')

for handle in handles:
    if handle in checked_handles:
        continue
    print(handle)
    twitter_posts_fn = '{}_twitter_posts.csv'.format(handle)
    matched_user_posts_fn = '{}_matched_user_posts.csv'.format(handle)
    search = 'twitter.com/{}'.format(handle.lower())
    print(search)
    posts = posts_df[urls_lowercase.contains(search)]
    if not posts.empty:
        posts.to_csv(twitter_posts_fn)
        if marked_posts is None:
            marked_posts = posts
        else:
            marked_posts = pd.concat([marked_posts, posts])
    matched_user_posts = posts_df[posts_df.author.str.lower() == handle.lower()]
    if not matched_user_posts.empty:
        matched_user_posts.to_csv(matched_user_posts_fn)
        if reddit_user_matches_twitter_handle is None:
            reddit_user_matches_twitter_handle = matched_user_posts
        else:
            reddit_user_matches_twitter_handle = pd.concat([reddit_user_matches_twitter_handle, matched_user_posts])
    with open('checked_handles.txt', 'w') as checked_handles_file:
        checked_handles_file.write('\n'.join(lines))
    

marked_posts.to_csv('marked_posts.csv')