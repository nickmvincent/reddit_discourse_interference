"""
This script samples some posts for a user test.
"""
import os
import pandas as pd
from random import shuffle


def main():
    """run"""
    subreddits_of_interest = [
        'The_Donald',
        'news',
        'conspiracy',
        'politics',
    ]

    for subreddit in subreddits_of_interest:
        inf_op_posts = pd.read_csv('posts_by_sub/{}.csv'.format(subreddit), encoding='latin-1')
        non_inf_op_posts = pd.read_csv('non_infop_posts_by_sub/{}.csv'.format(subreddit), encoding='latin-1')

        n = len(inf_op_posts.index)
        if n > 5:
            n = 5
        infop_samp = list(inf_op_posts.sample(n).title)
        inf_op_lines = [
            '{},1'.format(x) for x in infop_samp
        ]
        noninfop_samp = list(non_inf_op_posts.sample(n).title)
        non_inf_op_lines = [
            '{},0'.format(x) for x in noninfop_samp
        ]
        titles_with_answers = inf_op_lines + non_inf_op_lines
        shuffle(titles_with_answers)
        with open('posts_by_sub_for_manual_exam/{}_answers.csv'.format(subreddit), 'w', encoding='latin-1') as file:
            file.write('\n'.join(titles_with_answers))
        title_without_answers = [
            x[:-2] for x in titles_with_answers
        ]
        with open('posts_by_sub_for_manual_exam/{}.csv'.format(subreddit), 'w', encoding='latin-1') as file:
            file.write('\n'.join(title_without_answers))




if __name__ == '__main__':
    main()