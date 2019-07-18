import os
import utils
import tweets
import tweepy
import getContents
import twitterKeys
import time

auth = tweepy.OAuthHandler(twitterKeys.keys['consumer_key'], twitterKeys.keys['consumer_secret'])
auth.set_access_token(twitterKeys.keys['access_token'], twitterKeys.keys['access_token_secret'])

api = tweepy.API(auth)

def get_last_mention(path:str, file:str):
    root_dir = os.path.dirname(__file__)
    try:
        with open(os.path.join(root_dir, path, file), 'r', encoding='UTF-8', errors='ignore') as read_file:
            payload = str(read_file.readlines())
            #print("returning last mention: ", payload)
            return int(payload[2:-2])
    except:
        print("error getting last mention")
        return False

def set_last_mention(path:str, file:str, payload:str):
    root_dir = os.path.dirname(__file__)
    try:
        with open(os.path.join(root_dir, path, file), 'w') as write_file:
            write_file.write(payload)
        print("set last mention as ", payload)
        return True
    except:
        print("error setting last mention")
        return False

def get_new_mentions():
    last = get_last_mention("data","lastquery.txt")
    #print("current last mention: ", last)
    mentions = api.mentions_timeline(last)
    if len(mentions) > 0:
        return mentions
    else:
        return None

def most_recent_mention():
    mention = api.mentions_timeline(None,None,1)
    return mention[0].id_str

def send_responses():
    mentions = get_new_mentions()
    if mentions is not None:
        for mention in reversed(mentions):
            #Move through all mention checks...
            try:
                #FOR READINGS QUERIES:
                if ("#reading" or "#readings" or "#scripture" or "#scriptures") in mention.text.lower():
                    print("Reading Query Found in: \n" + mention.text.lower())
                    response_thread = "Today's Daily #Orthodox #Readings are:\n"
                    extract = getContents.get_readings_titles(getContents.get_readings_urls("https://oca.org","readings"))
                    for reading in extract:
                        response_thread += reading + "\n"
                    response_thread += "|Daily readings courtesy of @ocaorg. For complete text, visit: https://oca.org/readings"
                    #print(response_thread)
                    tweets.send_tweet(response_thread,None,mention.id)
                #FOR SAINTS QUERIES:
                if ("#saint" or "#feast" or "#celebrat" or "#commemorat") in mention.text.lower():
                    print("Feast Day Query Found in : \n" + mention.text.lower())
                    response_thread = "Today the #Orthodox #Church celebrates:\n"
                    extract = utils.extract_line_from_file("data", "saints.txt","|",-1).split("|")
                    for saint in extract:
                        saint_name = saint.split("^,")[0]
                        response_thread += saint_name + "\n"
                    response_thread += "|Saints & Feasts celebrations courtesy of @ocaorg. to read more, visit: https://oca.org/saints/lives"
                    tweets.send_tweet(response_thread,None,mention.id)
                #FOR FASTING QUERIES:
                if "#fast" in mention.text.lower():
                    print("Fasting Query Found in: \n" + mention.text.lower())
                    extract = utils.extract_line_from_file("data", "fasting.txt","|",-1)[:-1]
                    fast = extract.split("|")
                    response_thread = fast[0] + ".\n" + fast[1] + "\nFasting guidelines courtesy of @goarch. For more info, visit: https://goarch.org/chapel"
                    tweets.send_tweet(response_thread,None,mention.id)
                latest = str(mention.id)
                set_last_mention("data","lastquery.txt",latest)
            except:
                print("Error sending responses!")
    else:
        #print("no mentions... passing")
        pass

set_last_mention("data","lastquery.txt",most_recent_mention())
i = 0
while True:
    send_responses()
    i += 1
    if i == 360:
        print("still scanning for responses...")
        i = 0
    time.sleep(15)
