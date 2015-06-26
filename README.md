# hd-w205a2
HD W205 Assignment 2

## Link to S3 bucket
https://s3-us-west-2.amazonaws.com/hd-w205a2/

I manually uploaded the json tweet data through the AWS console. I have three seperate folders for each group of tweets. The directories are: NBAFinals2015, Warriors, NBAFinals2015_AND_Warriors

## Twitter acquisition code
The code is found in file a2-acquire.py

The authentication protocol makes use of AppAuthHandler and the keys have been removed from the code. The TweetSerializer class from the sync material was used and slightly modified. A retrieveTweets() function is implemented and takes as parameters a query for the cursor, a count for the cursor, a chunk size (in number of tweets) and a TweetSerializer object.

I used a count parameter of 100 (max) and chunked for every 2000 tweets. The resiliency is built using a while loop that will catch and pass for tweepy errors. I used the week period from 6/09 to 6/16 purposely in order to avoid the day of the last game, which was on 6/17.

Running the code requires a simple python call of: 

python a2-acquire.py

## Histogram
Three different histograms are provided:

1. fdist1full.csv represents the histogram for #NBAFinals2015 tag without #Warriors

2. fdist2full.csv represents the histogram for #Warriors tag without #NBAFinals2015

3. fdist3full.csv represents the histogram for both #NBAFinals2015 and #Warriors

The histograms were produced using the NLTK library by tokenizing the text of the tweets and removing stopwords in the English corpus for NLTK. There is further filtering by alphanumeric characters in order to remove characters such as hashtags are colons. The FreqDist function is subsequently used on the final text.

Running the code requires running a simple python call where all the json tweet data (and nothing else) is stored:

cd tweets

python a2-hist.py
