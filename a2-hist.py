import os
import json
import nltk
import csv
import codecs
import cStringIO

# UnicodeWriter from https://docs.python.org/2/library/csv.html
class UnicodeWriter:
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        self.writer.writerow([unicode(s).encode("utf-8") for s in row])
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)

# Get directory and listing of tweet files
directory = "tweets"
listing = os.listdir(directory)

# Parse the docs in the listing
stopwords = nltk.corpus.stopwords.words('english')
tweets1 = [] # Tweet text for Finals
tweets2 = [] # Tweet text for Warriors
tweets3 = [] # Tweet text for Finals AND Warriors
for doc in listing:
   jsonF = open(directory+'/'+doc)
   data = json.load(jsonF)
   if "NBAFinals" in doc:
      for i in range(len(data)):
         for w in nltk.word_tokenize(data[i]["text"]):
            if w.isalnum() and w.lower() not in stopwords:
               tweets1.append(w.lower())
   if "Warriors" in doc and "Finals" not in doc:
      for i in range(len(data)):
         for w in nltk.word_tokenize(data[i]["text"]):
            if w.isalnum() and w.lower() not in stopwords:
               tweets2.append(w.lower())
   if "FinalsAndWarriors" in doc:
      for i in range(len(data)):
         for w in nltk.word_tokenize(data[i]["text"]):
            if w.isalnum() and w.lower() not in stopwords:
               tweets3.append(w.lower())

# Create frequency distributions and write them to a csv
fdist1 = nltk.FreqDist(tweets1)
with open("fdist1full.csv", "wb") as fp1:
   writer = UnicodeWriter(fp1, quoting=csv.QUOTE_ALL)
   writer.writerows(fdist1.most_common())

fdist2 = nltk.FreqDist(tweets2)
with open("fdist2full.csv", "wb") as fp2:
   writer = UnicodeWriter(fp2, quoting=csv.QUOTE_ALL)
   writer.writerows(fdist2.most_common())

fdist3 = nltk.FreqDist(tweets3)
with open("fdist3full.csv", "wb") as fp3:
   writer = UnicodeWriter(fp3, quoting=csv.QUOTE_ALL)
   writer.writerows(fdist3.most_common())
