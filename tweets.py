import random
import tweepy
import twitterKeys

auth = tweepy.OAuthHandler(twitterKeys.keys['consumer_key'], twitterKeys.keys['consumer_secret'])
auth.set_access_token(twitterKeys.keys['access_token'], twitterKeys.keys['access_token_secret'])

api = tweepy.API(auth)



def split_tweet(payload, delimiter:str="|"):
    thread = []
    thread_length = len(payload)
    split_by_delimiter = payload.split("|")
    for status in split_by_delimiter:
        start = 0
        last_tweet = False
        while last_tweet == False:
            remaining = len(status[start:])
            if remaining <= 280:
                finish = start + remaining
                section = status[start:finish]
                last_tweet = True
            else:
                finish = start + 280
                section = status[start:finish]
            if last_tweet == False:
                to_space = section.rfind(' ')
                excess = 280 - to_space
                section = section[:to_space]
                start = start + to_space + 1
            thread.append(section.strip())
            #print("split_tweet | tweet added to thread!")
    #print("split_tweet | final thread: ", thread)
    return thread

def create_thread(payload:list, delimiter:str="|"):
    processed_thread = []
    status_thread = []
    split_thread = False
    if type(payload[0]) is list:
        print("create_thread | nested list found!")
        for tweet in payload:
            status = tweet[0]
            if len(status) > 280 or "|" in status:
                #print("create_thread | status exceeds character limit, splitting...")
                status_thread = split_tweet(status, delimiter)
                #print("create_thread | status split successfully!")
                split_thread = True
            try:
                img = tweet[1]
                #print("create_thread | adding image(s)")
            except:
                img = None
            try:
                reply = tweet[2]
                print("create_thread | adding reply ID: ", tweet[2])
            except:
                reply = None
            if split_thread == True:
                for item in status_thread:
                    if item == status_thread[0]:
                        processed_thread.append([item.strip(),img,reply])
                    else:
                        processed_thread.append([item.strip()])
                    print("create_thread | generating processed_thread")
            else:
                processed_thread.append([status.strip(),img,reply])
    else:
        print("create_thread | NO nested list available!")
        status = payload[0]
        if len(status) > 280 or "|" in status:
            #print("create_thread | status exceeds character limit, splitting...")
            status_thread = split_tweet(status, delimiter)
            #print("create_thread | status split successfully!")
            split_thread = True
        try:
            #print("create_thread | adding image(s)")
            img = payload[1]
        except:
            img = None
        try:
            print("create_thread | adding reply ID: ", payload[2])
            reply = payload[2]
        except:
            reply = None
        if split_thread == True:
            for item in status_thread:
                if item == status_thread[0]:
                    processed_thread.append([item.strip(),img,reply])
                else:
                    processed_thread.append([item.strip()])
            print("create_thread | generating processed_thread")
        else:
            processed_thread.append([status.strip(),img,reply])
    print("create_thread | returning processed thread: ", processed_thread)
    return processed_thread

def send_tweet(status:str, img:str=None, reply=None):
    #status processing
    if len(status) > 280 or "|" in status:
        print("send_tweet | threading required")
        tweet_thread(create_thread([status, img, reply], "|"))
    else:
        media_ids = []
        #split img by comma delim, add each image via media_upload to list
        if img is not None:
            print("send_tweet | adding image(s): ", img)
            for media in img.split(",",4):
                #try:
                media_ids.append(api.media_upload(media.strip()))
                # except:
                #     pass
            print("send_tweet | media ids added: " + str(media_ids))
        else:
            print("send_tweet | no image(s) to process")
        #process reply
        if reply is not None:
            reply = str(reply)
            print("send_tweet | adding reply: ", reply)
        else:
            print("send_tweet | no reply to add")
        #Send the tweet
        new_tweet = api.update_status(status=status, in_reply_to_status_id=reply, media_ids=media_ids, auto_populate_reply_metadata=True)
        print("Tweet sent: ",new_tweet.id)
        # print(
        #     "SENDING TWEET: "
        #     + "status:" + str(status)
        #     + " image(s):" + str(img)
        #     + " reply:" + str(reply)
        # )
        return new_tweet.id

def tweet_thread(payload:list):
    response = None
    for tweet in payload:
        #print("tweet_thread | adding status")
        status = tweet[0]
        try:
            #print("tweet_thread | adding image(s)")
            img = tweet[1]
        except:
            img = None
        try:
            response = tweet[2]
        except:
            pass
        response = send_tweet(status, img, response)
    return response
