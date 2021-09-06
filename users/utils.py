import re
import string

import tweepy

from bs4 import BeautifulSoup
from django.conf import settings
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer


MBTI_TYPES = [
    "INFJ", "ENTP", "INTP", "INTJ", "ENTJ", "ENFJ", "INFP", "ENFP",
    "ISFP", "ISTP", "ISFJ", "ISTJ", "ESTP", "ESFP", "ESTJ", "ESFJ",
]

stop_words = stopwords.words("english") + ['rt']
lemmatizer = WordNetLemmatizer()


def lemmatize(text):
    for mbti_type in map(str.lower, MBTI_TYPES):
        text = text.replace(f' {mbti_type}', "")

    text = " ".join([
        lemmatizer.lemmatize(word)
        for word in text.split(" ")
        if word not in stop_words
    ])
    return text


def cleanText(text):
    text = BeautifulSoup(text, "lxml").text.lower()
    text = re.sub(r'\|\|\|', r' ', text)
    text = text.translate(str.maketrans('', '', string.punctuation))

    useless_patterns = [r'…', r'http\S+', r'@[\S]+\s', r'\s@[\S]+', r'\srt\s']
    for pattern in useless_patterns:
        text = re.sub(pattern, '', text)

    text = lemmatize(text)

    return text


auth = tweepy.AppAuthHandler(settings.TWITTER_API_KEY, settings.TWITTER_API_SECRET)
API = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)


def get_user_tweets(username, page, count=200):
    rows = []
    try:
        tweets = API.user_timeline(username, count=count, page=page, tweet_mode='extended')
        for tweet in tweets:
            rows.append(tweet.full_text)
    except Exception as e:
        print(e)
    return '\n'.join(list(filter(lambda x: not x.lower().startswith('i rated'), rows)))


def get_mbti_from_twitter_id(twitter_id):
    users_tweets = get_user_tweets(twitter_id, 0)
    if not users_tweets:
        return 'INVALID'
    if len(users_tweets) < 1000:
        return 'NEED_MORE'
    cleaned_text = cleanText(users_tweets)
    model = settings.USER_PREDICT_MODEL
    return model.predict([cleaned_text])[0]


def generate_mbti(mbti):
    personalities = ['e', 'n', 'f', 'p']
    result = []
    for personality in personalities:
        result.append(1 if personality in mbti.lower() else 0)
    return result
