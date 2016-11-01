# info7374_16fall
Liren Huang  

## Assignment 2
#### example: search "trump"  
`$ python3 analysis.py trump '`

#### The command line interface  
`
Since date, past 7 days allowed. Press ENTER to skip. e.g.2016-10-24  
--> 2016-10-30  
Until date, past 7 days allowed. Press ENTER to skip. e.g.2016-10-25  
--> 2016-11-1  
Option 1: Average number of friends  
Option 2: Percentage of non-english tweets  
Option 3: Top 10 retweeted  
Option 4: Top 10 influential (most followers)  
Option 5: Average twitter account age  
Input 1-5--> 1  
Average number of friends: 1550  
`

#### notes  
The program creates a "tweets" directory to save the search results as json files.  
Results for different analysis purposes on the same term are saved in the same folder.  


## Midterm
#### Analysis
1. Find the top questions on the topic, sorted by their weight.  
Weight: Askers' total badage value. Bronze counts as 1, silver counts as 4, gold counts as 10.  
> output: question_id, link  
  
2. Find the top answerers active in the topic, sorted by their answers' overal accept rate.  
> output: user_id, link  
  
3. Find the most awarded bronze badges recently.  
> output: badge_id, count, link
  
4. Find the most viewed questions that have received no answers.  
> output: question_id, view_count, link
  
5. Find the questions with a decent chance for the answerers to get the bounty.  
(questions with a high bounty, small view count or few answers)
> output: question_id, bounty_amount, view_count
