"""
This script samples some posts for a user test.
"""
import os
import pandas as pd
from sklearn.metrics import classification_report, f1_score, fbeta_score, precision_score, recall_score
from collections import defaultdict
import numpy as np


def main():
    """run"""
    
    # order matters here

    
    subreddits_of_interest = [
        'politics',
        'The_Donald',
        'news',
        'conspiracy',
    ]
    responses = pd.read_csv('responses/data2.csv', encoding='latin-1')
    responses = responses.fillna('')
    # col 0 is timestamp
    # col 1 is comfort level
    # col 2 is where politics starts
    sub_to_precisions = defaultdict(list)
    sub_to_recalls = defaultdict(list)
    sub_to_f1s = defaultdict(list)

    for i_sub, subreddit in enumerate(subreddits_of_interest):
        y_true = []
        answer_strings = []
        with open('posts_by_sub_for_manual_exam/{}_answers.csv'.format(subreddit), 'r', encoding='latin-1') as file:
            for line in file.readlines():
                stripped_lines = line.strip('\n')
                y_true.append(int(stripped_lines[-1]))
                answer_strings.append(stripped_lines[:-2])
        for i_resp, row in responses.iterrows():
            # frequency = row[1]
            # if 'Less frequently' in frequency:
            #     continue
            pos_strings = row[i_sub+2]
            pos_strings = pos_strings.split(';')
            y_pred = [0] * 10
            for i_answer, answer_string in enumerate(answer_strings):
                if answer_string in pos_strings:
                    y_pred[i_answer] = 1
#            print(classification_report(y_true, y_pred))
            sub_to_f1s[subreddit].append(f1_score(y_true, y_pred))
            sub_to_precisions[subreddit].append(precision_score(y_true, y_pred))
            sub_to_recalls[subreddit].append(recall_score(y_true, y_pred))
    f1s = []
    precs = []
    recalls = []
    for subreddit in subreddits_of_interest:
        print(subreddit)
        f1s.append(np.mean(sub_to_f1s[subreddit]))
        precs.append(np.mean(sub_to_precisions[subreddit]))
        recalls.append(np.mean(sub_to_recalls[subreddit]))
        print(
            'f1', np.mean(sub_to_f1s[subreddit]),
            'precision', np.mean(sub_to_precisions[subreddit]),
            'recall', np.mean(sub_to_recalls[subreddit]),
        )
    print(np.mean(f1s), np.mean(precs), np.mean(recalls))







if __name__ == '__main__':
    main()