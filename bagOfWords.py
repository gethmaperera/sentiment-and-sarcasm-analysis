ACCESS_TOKEN = 
ACCESS_TOKEN_SECRET = 
CONSUMER_KEY = 
CONSUMER_SECRET = 

import tweepy
import json
import nltk
from nltk.corpus import stopwords

stoplist = set(stopwords.words('english')) - set(['not'])
nltk.download('wordnet')
import pymongo
from collections import Counter
from owlready2 import *
from rdflib.plugins.sparql import prepareQuery
from rdflib import URIRef
from sentiment import *

# import twitter_credentials
connection = pymongo.MongoClient('localhost', 27017)
database = connection['catogery_base']
collection = database ['uber_category']
coll = database ['personalized_message']
col = database ['customer_profile']



class TwitterAuthenticator():
    def authenticate_twitter_app(self):
        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        return auth


class TwitterStreamer():
    """
        Class for streaming and processing live tweets.
    """

    def __init__(self):
        self.twitter_authenticator = TwitterAuthenticator()

    def stream_tweets(self, fetched_tweets_filename, user):
        # This handles Twitter authetification and the connection to Twitter Streaming API
        listener = TwitterListener(fetched_tweets_filename)
        auth = self.twitter_authenticator.authenticate_twitter_app()
        # api = tweepy.API(auth)
        stream = tweepy.Stream(auth, listener)
        stream.filter(track=user)


class TwitterListener(tweepy.StreamListener):
    """
    This is a basic listener class that just prints received tweets to stdout.
    """

    def __init__(self, fetched_tweets_filename):
        self.fetched_tweets_filename = fetched_tweets_filename

    def on_data(self, data):
        tweettext = bagOfWords()
        try:
            with open(self.fetched_tweets_filename, 'a') as tf:
                json_load = json.loads(data)
                text = json_load['text']
                print("Question Raised : ",text)
                tweettext.preprocess_text(text)
                # tf.write(text) can write in a text file for further store
                # tf.write('\n')
            return text
        except BaseException as e:
            print("Error on_data %s" % str(e))
        return True

    def on_status(self, status):
        print(status.text)

    def on_error(self, status):
        if status == 420:
            # Returning False on_data method in case rate limit occurs.
            return False
        print(status.text)


# public_tweets = api.home_timeline()
# for tweet in public_tweets:
#     print tweet.text


class bagOfWords():

    def preprocess_text(self, tweet):
        preprocess = preProcessing()
        removeURL = preprocess.remove_pattern(tweet, "http\S+")
        removeMentions = preprocess.remove_pattern(removeURL, "@[\w]*")
        print("Pattern Removal : ",removeMentions)
        removePuncs = preprocess.remove_punct(removeMentions)
        print("Punctuation Removal : ", removePuncs)
        uniquewords = ' '.join(preprocess.unique_list(removePuncs.split()))
        print("Extracting Unique Words : ", uniquewords)
        removeEmoji = preprocess.deEmojify(uniquewords)
        print("Punctuation Removal : ", removeEmoji)
        lemmatizedwords = preprocess.lemmatizationWithTagging(removeEmoji)
        print("Lemmatization : ", lemmatizedwords)
        removeStopwords = preprocess.removeStopWords(lemmatizedwords)
        print("Stopwords Removal : ", removeStopwords)
        tweetEmoji = preprocess.extract_emojis(uniquewords)
        print('Extracted Emoji: ', tweetEmoji)
        tweetEmojiMeaning = preprocess.convert_emojis(tweetEmoji)
        print('Extracted Emoji Meaning: ', tweetEmojiMeaning)
        with open('words.txt', "r") as word_list:
            words = word_list.read().split(',')
            resultwords = [word for word in removeStopwords if word.lower() in words]
        ####appending gethma's Data to file
        file_object = open('sentimentModule.txt', 'a')
        file_object.write('______________New Log____________')
        file_object.write("\n")
        a = resultwords
        file_object.write("bag of words : ")

        for item in a:
            file_object.write("%s," % item)
        file_object.write("\n")
        print("bag of words",a)
        squares = []

        prop = collection.find({})
        for documents in prop:
            b = documents['keywords']
            a_vals = Counter(a)
            b_vals = Counter(b)

            # convert to word-vectors
            words = list(a_vals.keys() | b_vals.keys())
            a_vect = [a_vals.get(word, 0) for word in words]  # [0, 0, 1, 1, 2, 1]
            b_vect = [b_vals.get(word, 0) for word in words]  # [1, 1, 1, 0, 1, 0]

            # find cosine
            len_a = sum(av * av for av in a_vect) ** 0.5  # sqrt(7)
            len_b = sum(bv * bv for bv in b_vect) ** 0.5  # sqrt(4)
            dot = sum(av * bv for av, bv in zip(a_vect, b_vect))  # 3
            cosine = dot / (len_a * len_b)
            print(cosine)
            if (cosine > 0.6):
                squares.append(documents['property'])
        # print(squares)
        if (len(squares) > 0):
            onto = get_ontology("file://E:/Academic/Final.owl").load()
            graph = default_world.as_rdflib_graph()
            c = squares[0]
            UC = URIRef('http://www.semanticweb.org/hp/ontologies/2019/8/FinalProject#')
            q = prepareQuery('''SELECT ?o
                                                 WHERE {
                                                           ?subject UC:''' + c + ''' ?object;
                           UC:answer ?o.}''', initNs={'UC': UC})

            results = graph.query(q)
            response = []
            listToStr = " "
            for item in results:
                o = str(item['o'].toPython())
                o = re.sub(r'.*#', "", o)
                response.append(o)
                listToStr = ' '.join([str(elem) for elem in response])

                # print(listToStr)
                # print(response)
        else:
            onto = get_ontology("file://E:/Academic/Final.owl").load()
            graph = default_world.as_rdflib_graph()
            c = 'cantFind'
            UC = URIRef('http://www.semanticweb.org/hp/ontologies/2019/8/FinalProject#')
            q = prepareQuery('''SELECT ?o
                                                 WHERE {
                                                           ?subject UC:''' + c + ''' ?object;
                           UC:answer ?o.}''', initNs={'UC': UC})

            results = graph.query(q)
            response = []
            listToStr = " "
            for item in results:
                o = str(item['o'].toPython())
                o = re.sub(r'.*#', "", o)
                response.append(o)
                listToStr = ' '.join([str(elem) for elem in response])
                # print(response)

        #_____________________________
        prediction = predictSentiment()
        sarcasmPrediction = pridictSarcasm()
        convertEmoji = preprocess.convert_emojis(uniquewords)
        lemmatizedwords = preprocess.lemmatizationWithTagging(convertEmoji)
        removeStopwords = preprocess.removeStopWords(lemmatizedwords)
        resultString = ' '.join(removeStopwords)
        # print('beofore sentiment', resultString)
        result = prediction.sentiment(resultString)
        print("Question Raised: ",tweet)
        print("Preprocessed Tweet: " , resultString)
        file_object.write("Sentiment Result : ")
        file_object.write(result)
        file_object.write("\n")
        print('Sentiment Result: ', result)
        sarcasmResult = sarcasmPrediction.sarcasm(uniquewords, result)
        file_object.write("Sarcasm Result : ")
        file_object.write(result)
        file_object.write("\n")
        print('sarcasmResult: ', sarcasmResult)
        file_object.close()
        #_____________________________

        sentiment = "negative"
        user = "1"
        if (sentiment == "positive"):
            myquery = {"attitude": "anger"}

            mydoc = coll.find(myquery)

            for x in mydoc:
                msg = x['message']
                fans = listToStr + " " + msg + ". If you not satisfied with our answer, please contact our support team directly."
                print(fans)
        else:

            findAtt = {'user': user}
            doc = col.find(findAtt)
            for y in doc:
                att = y['attitude']
                myquery = {"attitude": att}

                mydoc = coll.find(myquery)

                for x in mydoc:
                    msg = x['message']
                    # print(listToStr)
                    # print(msg + ". If you not satisfied with our answer, please contact our support team directly.")
                    fans = listToStr + " " + msg + ". If you not satisfied with our answer, please contact our support team directly."
                    print(fans)




if __name__ == '__main__':
    user = ["@gethma_perera"]
    fetched_tweets_filename = "tweets.txt"


    twitter_streamer = TwitterStreamer()
    twitter_streamer.stream_tweets(fetched_tweets_filename, user)



