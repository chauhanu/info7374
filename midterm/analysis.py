#Author Liren Huang

import requests, json, operator

SEARCH_URL = 'https://api.stackexchange.com/2.2'
HEADERS = {'key': 'wLZ7x470fJ2zruWosVW*rw(('}

def f1(*tags):
    """
    Analysis 1
    Returns the top questions with their links, sorted by their weight.
    Weight: askers' total badage weight. Bronze counts as 1, silver counts as 4, gold counts as 10.

    Argument:
    tags: one or more tags

    """
    if len(tags) > 1:
        tags = ';'.join(tags)
    else:
        tags = str(tags[0])
    # get questions
    r1 = requests.get(SEARCH_URL + '/tags/' + tags + '/faq?page=1&pagesize=10&site=stackoverflow', headers=HEADERS)
    items, users = r1.json()['items'], []
    for item in items:
        if 'user_id' in item['owner']:
            users.append(item['owner']['user_id'])
    query_users = ';'.join([str(x) for x in users])
    # get a list of users who asked the questions
    r2 = requests.get(SEARCH_URL + '/users/' + query_users + '?page=1&pagesize=10&order=desc&sort=reputation&site=stackoverflow', headers=HEADERS)
    user_weight = {}
    for item in r2.json()['items']:
        badge_weight = item['badge_counts']['bronze'] + 4 * item['badge_counts']['silver'] + 10 * item['badge_counts']['gold']
        user_weight[item['user_id']] = badge_weight
    items.sort(key=lambda x: user_weight[x['owner']['user_id']], reverse=True)
    return [(x['question_id'], x['link']) for x in items]

def f2(tag):
    """
    Analysis 2
    Returns the top answerers active in a single tag, sorted by their accept_rate.

    Argument:
    tag: a single tag
    """
    r1 = requests.get(SEARCH_URL + '/tags/' + tag + '/top-answerers/all_time?page=1&pagesize=10&site=stackoverflow', headers=HEADERS)
    items = r1.json()['items']
    for i in items[:]:
        if 'accept_rate' not in i['user']:
            items.remove(i)
    items.sort(key=lambda x: x['user']['accept_rate'], reverse=True)
    return [(x['user']['user_id'], x['user']['link']) for x in items]

def f3():
    """
    Analysis 3
    Returns the most awarded bronze badges recently.
    """
    r1 = requests.get(SEARCH_URL + '/badges/recipients?page=1&pagesize=30&site=stackoverflow', headers=HEADERS)
    items = r1.json()['items']
    badges = {}
    for i in items:
        if i['rank'] == 'bronze':
            if i['badge_id'] in badges:
                badges[i['badge_id']][0] += 1
            else:
                badges[i['badge_id']] = [1, i['link']]
    sorted_b = sorted(badges.items(), key=operator.itemgetter(1), reverse=True)
    return [(x[0], x[1][0], x[1][1]) for x in sorted_b]

def f4(*tags):
    """
    Analysis 4
    Returns the most viewed questions that have received no answers. 

    Argument:
    tags: one or more tags
    """
    if len(tags) > 1:
        tags = ';'.join(tags)
    else:
        tags = str(tags[0])
    # get questions tagged by 'python' and 'pandas'
    r1 = requests.get(SEARCH_URL + '/questions/no-answers?page=1&pagesize=10&order=desc&sort=activity&site=stackoverflow&tagged=' + tags, headers=HEADERS)
    items = r1.json()['items']
    items.sort(key=lambda x: x['view_count'], reverse=True)
    return [(x['question_id'], x['view_count'], x['link']) for x in items]

def f5(*tags):
    """
    Analysis 5
    Return the questions with a high bounty but have a small view count or have less than two answers.

    Argument:
    tags: one or more tags
    """
    if len(tags) > 1:
        tags = ';'.join(tags)
    else:
        tags = str(tags[0])
    r1 = requests.get(SEARCH_URL + '/questions/featured?page=1&pagesize=10&order=desc&sort=activity&site=stackoverflow&tagged=' + tags , headers=HEADERS)
    items = r1.json()['items']
    for i in items[:]:
        if i['bounty_amount'] < 50 or i['is_answered'] == 'true' or i['answer_count'] > 1:
            items.remove(i)
    items.sort(key=lambda x: x['view_count'])
    return [(x['question_id'], x['bounty_amount'], x['link'], x['view_count']) for x in items]

def output(lst, option):
    """
    Save the output as CSV format.
    """
    # Not sure why you need to do this.
    new_lst =[]
    for l in lst:
        new_lst.append([str(x) for x in l])

    with open("result_" + str(option) + ".csv", 'w') as f:
        for line in new_lst:
            f.write(','.join(line) + '\n')
# Do not hard code it for just two topics. Use argparse so the user can input what topics he want.
def main():
    output(f1('python', 'pandas'), 1)
    output(f2('python'), 2)
    output(f3(), 3)
    output(f4('python', 'pandas'), 4)
    output(f5('python'), 5)

if __name__ == "__main__":
    main()
