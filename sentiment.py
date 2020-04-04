# _________________________3______________________________
# Import libraries
import pandas as pd
import numpy as np
import emoji
import re
from preprocessing import *
from emojiSentiment import *
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')
from nltk.corpus import stopwords
import joblib
stoplist = set(stopwords.words('english')) - set(['not'])
filename = joblib.load('finalized_model.sav')
vectorizer=joblib.load(open("vectorizer.sav", 'rb'))


class predictSentiment():

    def sentiment(self, twt):

        review_vector = vectorizer.transform([twt])  # vectorizing

        sentiment=filename.predict(review_vector)

        if (sentiment == 0):
            return "negative"
        else:
            return "positive"

    def sentimentScore(self, twt):
        review_vector = vectorizer.transform([twt])
        sentiment= filename.predict_proba(review_vector)
        return sentiment


class pridictSarcasm():

    def sarcasm(self, uniquewords, result):
        preprocess = preProcessing()
        emojiSentimentCal= emojiSentiment()
        prediction = predictSentiment()
        if (result == "negative"):
            return "negative"
        else:
            tweetText = preprocess.deEmojify(uniquewords)
            tweetEmoji = preprocess.extract_emojis(uniquewords)
            print('Extracted Emoji: ', tweetEmoji)
            sarcasmList = ['sarcasm', 'humor', "sarcastic", "irony", "satire", "caustic", "mockery", "raillery",
                           "ridicule"]
            noSarcasmList = ['not sarcasm', 'notsarcasm', "eulogy", "compliment", "panegyric", "eulogium", "nosarcasm",
                             "noirony", "not funny"]
            if any(word in tweetText for word in noSarcasmList):
                return "positive"
            elif any(word in tweetText for word in sarcasmList):
                return "negative"
            elif (tweetEmoji != ''):
                resultText = prediction.sentiment(tweetText)
                tweetEmojiMeaning = preprocess.convert_emojis(tweetEmoji)
                print('Extracted Emoji Meaning: ', tweetEmojiMeaning)
                try:
                    resultEmoji = emojiSentimentCal.emojiSentimentValue(tweetEmojiMeaning)
                except:
                    resultEmoji='positive'

                print('emoji sentiment',resultEmoji)
                print('text sentiment', resultText)

                if (resultText == "positive" and resultEmoji == "positive"):
                    return "positive"
                elif (resultText == "negative" and resultEmoji == "negative"):
                    return "negative"
                else:
                    scoreEmoji = emojiSentimentCal.emojiSentimentScore(tweetEmojiMeaning)
                    scoreText = prediction.sentimentScore(tweetText)
                    maxScoreText = max(scoreText)
                    if (maxScoreText >= scoreEmoji[0]).any():
                        if (resultText == "positive"):
                            return "positive"
                        else:
                            return "negative"
                    else:
                        if (resultEmoji == "positive"):
                            return "positive"
                        else:
                            return "negative"
            else:
                return "positive"
