import datetime
import random
import string
import warnings
from json import dumps
from .models import logs
import nltk
import pandas as pd
from django.shortcuts import render
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

warnings.filterwarnings('ignore')
df = pd.read_csv("D:/Projects/chatbot/qna.txt")
f = open('D:/Projects/chatbot/q.txt', 'r', errors='ignore')  # open the file
raw = f.read()  # read the file
raw = raw.lower()  # convert to lower case

sent_tokens = nltk.sent_tokenize(raw)  # converts to list of sentences (sentence tokenizer punkt)
word_tokens = nltk.word_tokenize(raw)  # converts to list of words     (wordnet is the dictionary for english language)

lemmer = nltk.stem.WordNetLemmatizer()

def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]

remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)


def LemNormalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))


greeting_inputs = ("hello", "hi", "greetings", "sup", "what's up", "hey", "hii")
greeting_responses = ["hii", "hey", "hi there", "hello"]


# check whether greeting words are present in user response and answer accordingly
def greeting(sentence):
    for word in sentence.split():
        if word.lower() in greeting_inputs:
            return random.choice(greeting_responses)


def response(user_response):
    chatbot_response = ""
    sent_tokens.append(user_response)
    l = user_response.split(" ")
    # append the user response to the list of sentences
    if len(l) <= 4:
        TfidfVec = TfidfVectorizer(tokenizer=LemNormalize)
    else:
        TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words="english")

    tfidf = TfidfVec.fit_transform(sent_tokens)
    vals = cosine_similarity(tfidf[-1], tfidf)

    idx = vals.argsort()[0][-2]
    flat = vals.flatten()  # this converts multidimentional array [[]] to one dimentional array []
    flat.sort()  # this is done to check whether the matching value is not zero
    req_tfidf = flat[-2]
    if (req_tfidf == 0):
        chatbot_response = chatbot_response + "I am sorry! I didn't understand you"
        return chatbot_response
    else:
        chatbot_response = chatbot_response + sent_tokens[idx]
        return chatbot_response


print()
l = []

flag = 1


def chatbot(request):
    global flag
    user_response = request.POST.get("your_name")

    print(user_response)
    if user_response == None:
        user_response = ""
    else:
        user_response = user_response.lower()

    for i in user_response.split(" "):
        if i in ["amazon", "flipkart"]:
            user_response = "I am a delivery guy"
    if user_response != "bye":
        if (user_response == "thanks" or user_response == "thank you" or user_response == "okay thank you"):
            data = "You are Welcome"

        elif (user_response == "yes"):
            data = "okay,thank you"

        elif (user_response == "no" or user_response == "okay"):
            data = "okay"

        elif ("time" in user_response):
            time = datetime.datetime.now()
            data = str(time.hour) + ":" + str(time.minute) + ":" + str(time.second)

        elif ("date" in user_response or "month" in user_response or "year" in user_response or "day" in user_response):
            time = datetime.datetime.now()
            data = str(time.day) + "/" + str(time.month) + "/" + str(time.year)

        else:
            if greeting(user_response) is not None:
                data = greeting(user_response)
            else:
                if flag == 0:
                    stop_words = set(stopwords.words("english"))
                    l = user_response.split(" ")
                    l1 = []
                    for i in range(len(l)):
                        if l[i] not in stop_words and l[i] != "name":
                            l1.append(l[i])  
                    name1 = logs(NAME=l1[0])
                    name1.save()

                    data = "Hello " + str(l1[0]) + " how can i help you"
                    flag = 2
                elif flag == 1:
                    data = "MY name is Flash. What is your name"
                    flag = 0

                else:
                    q = response(user_response)
                    if q == "I a m sorry! I didn't understand you":
                        data = q

                    elif q == "when will the owners return." or q == "when will they come back.":
                        data = "value taken from database"

                    elif (
                            q == "money not received." or q == "payment is yet to be done." or q == "payment is remaining."):
                        data = "Owner will return by (database value) can you come again by that time."
                    else:
                        try:
                            data = df[df["question"] == str(q)]["answer"].values[0]
                        except:
                            data = "I am sorry! I didn't understand you"

                    sent_tokens.remove(user_response)


    else:
        data = "Bye take care"
        flag = 1

    context = {"response": data}
    Json = dumps(context)

    return render(request, "index.html", {"data": Json})
