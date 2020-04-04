import pandas
from preprocessing import *
from sentiment import *
tweet_df = pandas.read_csv('sarcasm.csv')
# evaluation count
actualPositive = (tweet_df[tweet_df['Sarcasm'] == 1].size) / 2
actualNegative = (tweet_df[tweet_df['Sarcasm'] == 0].size) / 2
predictedPositive = 0
predictedNegative = 0
truePositive = 0
trueNegative = 0
falsePositive = 0
falseNegative = 0

for row in tweet_df.iterrows():
    tweet = row[1]['text']
    preprocess = preProcessing()
    prediction = predictSentiment()
    sarcasmPrediction = pridictSarcasm()
    removeURL = preprocess.remove_pattern(tweet, "http\S+")
    removeMentions = preprocess.remove_pattern(removeURL, "@[\w]*")
    removePuncs = preprocess.remove_punct(removeMentions)
    uniquewords = ' '.join(preprocess.unique_list(removePuncs.split()))
    convertEmoji = preprocess.convert_emojis(uniquewords)
    lemmatizedwords = preprocess.lemmatizationWithTagging(convertEmoji)
    removeStopwords = preprocess.removeStopWords(lemmatizedwords)
    resultString = ' '.join(removeStopwords)
    # print(removeStopwords)
    result = prediction.sentiment(resultString)
    # print('normal result: ',result)
    sarcasmResult = sarcasmPrediction.sarcasm(uniquewords, result)
    # print("sarcasm result:", sarcasmResult)
    if (sarcasmResult == "positive"):
        row[1]['result'] = 0
        predictedNegative = predictedNegative + 1
    else:
        row[1]['result'] = 1
        predictedPositive = predictedPositive + 1

    # evaluation
    if (sarcasmResult == "positive" and row[1]['Sarcasm'] == 1):
        truePositive = truePositive + 1
    elif (sarcasmResult == "positive" and row[1]['Sarcasm'] == 0):
        falsePositive = falsePositive + 1
    elif (sarcasmResult == "negative" and row[1]['Sarcasm'] == 1):
        trueNegative = trueNegative + 1
    else:
        falseNegative = falseNegative + 1

print(predictedNegative, predictedPositive)
print(truePositive, falsePositive)
print(trueNegative, falseNegative)
accuracy = (truePositive + trueNegative) / (truePositive + trueNegative + falsePositive + falseNegative)
recall = (truePositive) / (truePositive + falseNegative)






