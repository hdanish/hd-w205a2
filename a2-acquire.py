import sys
import tweepy
import datetime
import urllib
import signal
import json

# Setup keys and tokens
consumer_key = "";
consumer_secret = "";
access_token = "";
access_token_secret = "";

# Setup authentication and API
#auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
#auth.set_access_token(access_token, access_token_secret)
auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)
api = tweepy.API(auth_handler=auth,wait_on_rate_limit=True,wait_on_rate_limit_notify=True)

# Setup search queries
q1 = "#NBAFinals2015-#Warriors since:2015-06-09 until:2015-06-16"
q2 = "#Warriors-#NBAFinals2015 since:2015-06-09 until:2015-06-16"
q3 = "#NBAFinals2015 AND #Warriors since:2015-06-09 until:2015-06-16"

# TweetSerializer class borrowed from Activities
class TweetSerializer:
   def __init__(self, tag):
      self.out = None
      self.first = True
      self.count = 0
      self.tag = tag

   def start(self):
      self.count += 1
      fname = "tweets-"+str(self.tag)+"-"+str(self.count)+".json"
      self.out = open(fname,"w")
      self.out.write("[\n")
      self.first = True

   def end(self):
      if self.out is not None:
         self.out.write("\n]\n")
         self.out.close()
      self.out = None

   def write(self,tweet):
      if not self.first:
         self.out.write(",\n\n\n")
      self.first = False
      self.out.write(json.dumps(tweet._json).encode('utf8'))

# Retrieval function
def retrieveTweets(q, count, chunkSize, ts):
   tscount = 0
   for tweet in tweepy.Cursor(api.search,q=q,count=count).items():
      if tscount%chunkSize==0:
         ts.start()
      ts.write(tweet)
      if tscount%chunkSize==chunkSize-1:
         ts.end()
      tscount+=1
   # Make sure to close the file if we didn't in the for loop
   if tscount%chunkSize!=chunkSize-1:
      ts.end()      

# Perform the retrieval
ts1 = TweetSerializer("NBAFinals2015")
ts2 = TweetSerializer("Warriors")
ts3 = TweetSerializer("FinalsAndWarriors")

while True:
   try:
      retrieveTweets(q1, 100, 2000, ts1)
      retrieveTweets(q2, 100, 2000, ts2)
      retrieveTweets(q3, 100, 2000, ts3)
   except tweepy.TweepError as tex:
      print tex.respsonse.status
      print tex.message[0]['code']
      print tex.args[0][0]['code']
      pass
   else:
      break

