
import pandas as pd
df = pd.read_csv('emojiSentiment.csv')

class emojiSentiment():

    def emojiSentimentScore(self,unicode):
        emojiSentimentScore= df[df['Unicode_name'] ==unicode.upper()][['Sentiment_score']]
        score = abs(emojiSentimentScore).values[0]
        return score

    def emojiSentimentValue(self,unicode):
        emojiSentimentScore= df[df.Unicode_name ==unicode.upper()][['Sentiment_score']]
        score = emojiSentimentScore.values[0]
        if (score[0]<0):
            emojiSentimentValue='negative'
            return emojiSentimentValue
        else:
            emojiSentimentValue='positive'
            return emojiSentimentValue



