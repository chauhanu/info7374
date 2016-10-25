#!/usr/bin/env python3

# Author: Liren Huang
# Due to Twitter's limited requests per application policy, the program only fecthes one page per analysis. I'll enable fetching multi-page data given enough time in the future.  #url = SEARCH_URL + r.json()['search_metadata']['next_results']
# Only Tweets published in the past 7 days are available using Twitter Search API

import json, heapq
from datetime import datetime, timezone, timedelta
from utils import search, save_file
e  = datetime.strptime('Sat Nov 15 10:36:22 +0000 2014', '%a %b %d %H:%M:%S %z %Y')  #UTC

PARENT_FOLDER = 'tweets'
# The number of tweets per page.
COUNT =100

def f0(term, time_window=""):
    """
    Test function.
    """
    params = {'q':'#'+term + time_window, 'result_type':'recent', 'count':COUNT}
    path = save_file(search(params), term, PARENT_FOLDER, 'analysis1')
    with open(path, 'r') as f:
        o = json.load(f)
    return o

def f1(term, time_window=""):
    """
    Analysis 1. For a given time window, return the average number of friends the users who tweet the topic have. Fetch the recent tweets if time_window is not provided.

    Arguments:
    term -- a single term e.g. 'haiku'
    time_window -- e.g. ' since:2016-10-23 until:2016-10-24'
    """
    params = {'q':'#'+term + time_window, 'result_type':'recent', 'count':COUNT}
    path = save_file(search(params), term, PARENT_FOLDER, 'analysis1')
    with open(path, 'r') as f:
        o = json.load(f)
    users = []
    total_friends = 0
    for status in o['statuses']:
        if status['user']['id'] not in users:
            users.append(status['user']['id'])
            total_friends += status['user']['friends_count']
    return total_friends // len(users)

def f2(term, time_window=""):
    """
    Analysis 2. For a given time window, return the percentage of non-english tweets about the topic. Fetch the recent tweets if time_window is not provided.

    Arguments:
    term -- a single term e.g. 'haiku'
    time_window -- e.g. ' since:2016-10-23 until:2016-10-24'
    """
    params = {'q':'#'+term + time_window, 'result_type':'recent', 'count':COUNT}
    path = save_file(search(params), term, PARENT_FOLDER, 'analysis2')
    with open(path, 'r') as f:
        o = json.load(f)
    en_count = 0
    cnt = 0
    for status in o['statuses']:
        if status['lang'] == 'en':
            en_count += 1
        cnt += 1
    return (cnt - en_count) / cnt

def f3(term, time_window=""):
    """
    Analysis 3. For a given topic, return the top 10 retweeted tweets during the time window. Fetch the recent tweets if time_window is not provided.

    Arguments:
    term -- a single term e.g. 'haiku'
    time_window -- e.g. ' since:2016-10-23 until:2016-10-24'
    """
    params = {'q':'#'+term + time_window, 'result_type':'recent', 'count':COUNT}
    path = save_file(search(params), term, PARENT_FOLDER, 'analysis3')
    with open(path, 'r') as f:
        o = json.load(f)
    return [x['text'] for x in heapq.nlargest(10, o['statuses'], key=lambda c: c['retweet_count'])]


def f4(term, time_window=""):
    """
    Analysis 4. For a given topic, return the top 10 influential (have most followers) tweets during the time window. Fetch the recent tweets if time_window is not provided.

    Arguments:
    term -- a single term e.g. 'haiku'
    time_window -- e.g. ' since:2016-10-23 until:2016-10-24'
    """
    params = {'q':'#'+term + time_window, 'result_type':'recent', 'count':COUNT}
    path = save_file(search(params), term, PARENT_FOLDER, 'analysis4')
    with open(path, 'r') as f:
        o = json.load(f)
    return [x['text'] for x in heapq.nlargest(10, o['statuses'], key=lambda c: c['user']['followers_count'])]

def f5(term, time_window=""):
    """
    Analysis 5. For a given time window, return the average twitter age (days since account creation) of the users who tweet the topic. Fetch the recent tweets if time_window is not provided.

    Arguments:
    term -- a single term e.g. 'haiku'
    time_window -- e.g. ' since:2016-10-23 until:2016-10-24'
    """
    params = {'q':'#'+term + time_window, 'result_type':'recent', 'count':COUNT}
    path = save_file(search(params), term, PARENT_FOLDER, 'analysis5')
    with open(path, 'r') as f:
        o = json.load(f)
    users = []
    age = timedelta()
    now = datetime.now(timezone.utc)
    for status in o['statuses']:
        if status['user']['id'] not in users:
            users.append(status['user']['id'])
            age += now - datetime.strptime(status['user']['created_at'], '%a %b %d %H:%M:%S %z %Y')
    return age.days // len(users)

def output(option, term, since, until):
    """
    Feed the arguments to the corresponding functions. Print the formatted output.
    """
    time_window = ""
    if since != "":
        time_window += " since:" + since
    if until != "":
        time_window += " until:" + until
    if option == 1:
        print("Average number of friends:", f1(term, time_window))
    elif option == 2:
        print("Percentage of non-english tweets:", f2(term, time_window))
    elif option == 3:
        print("Top 10 retweeted:\n----------------------------------------")
        l = f3(term, time_window)
        for i in range(10):
            print(str(i+1) + ".", l[i])
    elif option == 4:
        print("Top 10 influential:\n----------------------------------------")
        l = f4(term, time_window)
        for i in range(10):
            print(str(i+1) + ".", l[i])
    elif option == 5:
        print("Average twitter account age:", f5(term, time_window))
    else:
        print("Invalid option.")

def main():
    import argparse
    parser = argparse.ArgumentParser(description='Tweets analysis')
    parser.add_argument('term', nargs=1, type=str, help='the search term.')
    #parser.add_argument('option', nargs=1, type=int, help='the analysis option (1-5)')
    args = parser.parse_args()
    since = input('Since date, past 7 days allowed. Press ENTER to skip. e.g.2016-10-24\n--> ')
    until = input('Until date, past 7 days allowed. Press ENTER to skip. e.g.2016-10-25\n--> ')
    option = input('Option 1: Average number of friends\nOption 2: Percentage of non-english tweets\nOption 3: Top 10 retweeted\nOption 4: Top 10 influential (most followers)\nOption 5: Average twitter account age\nInput 1-5--> ')

    #print("Analysing", '"' + args.term[0] + '"', "with option", option, "with date:", since, until)
    return output(int(option), args.term[0], since, until)

if __name__ == "__main__":
    main()
