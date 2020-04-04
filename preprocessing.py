from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
from nltk.corpus import stopwords
stoplist = set(stopwords.words('english')) - set(['not','no'])
nltk.download('wordnet')
from nltk.stem import WordNetLemmatizer
import string
import re
import emoji
from autocorrect import Speller
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')
from nltk.corpus import stopwords
from nltk.corpus import wordnet
stoplist = set(stopwords.words('english')) - set(['not'])
from nltk.stem import WordNetLemmatizer

class preProcessing():

    def remove_pattern(self,input_txt, pattern):
        r = re.findall(pattern, input_txt)
        for i in r:
            input_txt = re.sub(i, '', input_txt)
        return input_txt

    def remove_punct(self,text):
        text=text.lower()
        text = "".join([char for char in text if char not in string.punctuation])
        text = re.sub('[0-9]+', '', text)
        text = re.sub(r"\s+[a-zA-Z]\s+", ' ', text)
        text = re.sub(r'\s+', ' ', text)
        return text

    def removeStopWords(self, text):
        spell = Speller(lang='en')
        clean_word_list = spell(text)
        clean_word_list = [word for word in clean_word_list.split() if word not in stoplist]
        return clean_word_list

    def deEmojify(self,inputString):
        emoji_pattern = re.compile("["
                                   u"\U0001F600-\U0001F64F"  # emoticons
                                   u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                   u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                   u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                   u"\U00002702-\U000027B0"
                                   u"\U000024C2-\U0001F251"
                                   "]+", flags=re.UNICODE)
        return emoji_pattern.sub(r'',inputString)

    def unique_list(self,l):
        ulist = []
        [ulist.append(x) for x in l if x not in ulist]
        return ulist

    def convert_emojis(self, text):
        return emoji.demojize(text).replace(":", "")

    def extract_emojis(self, text):
        return ''.join(c for c in text if c in emoji.UNICODE_EMOJI)

    def tokenizer(self,text):
        vectorizer = TfidfVectorizer()
        return vectorizer.fit_transform(text).todense()

    def lemmatization(self, text):
        lemmatizer = WordNetLemmatizer()
        lemmatizedwords = lemmatizer.lemmatize(text)
        return lemmatizedwords

    def get_wordnet_pos(word):
        tag = nltk.pos_tag([word])[0][1][0].upper()
        tag_dict = {"J": wordnet.ADJ, "N": wordnet.NOUN, "V": wordnet.VERB, "R": wordnet.ADV}
        return tag_dict.get(tag, wordnet.NOUN)

    def lemmatizationWithTagging(self, text):
        lemmatizer = WordNetLemmatizer()
        lemmatizedwords = (' '.join(lemmatizer.lemmatize(w, preProcessing.get_wordnet_pos(w)) for w in nltk.word_tokenize(text)))
        return lemmatizedwords