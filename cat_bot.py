import tweepy
import time
import requests
#global vars
LAST_TWEET_FILENAME = 'last_tweet_id.txt'
KEYHASHTAG = '#catbot'

API_CALL = 'https://api.thecatapi.com/v1/images/search?mime_types=jpg'
PIC_FILENAME = 'cat_pic.jpg'

KEYS_FILENAME = 'keys.txt'
# functions
def write_last_tweet_id(last_tweet_id, FILE_NAME):
    f = open(FILE_NAME, 'w')
    f.write(str(last_tweet_id))
    f.close()
    return

def read_last_tweet_id(FILE_NAME):
    f = open(FILE_NAME, 'r')
    return f.read()

def file_exists(FILE_NAME):
    try:
        f = open(FILE_NAME)
    except IOError:
        return False
    f.close()
    return True

def get_cat_image_url():    # retrieve image url
     # make the request
    response = requests.get(API_CALL)
    # retrieve the first object
    json = response.json()[0]
    return json['url']

def download_image(image_url, FILE_NAME):   # download image
    image_content = requests.get(image_url).content
    f = open(FILE_NAME, 'wb')
    f.write(image_content)
    f.close()

def upload_image(FILE_NAME):
    image = api.media_upload(FILE_NAME)
    return image.media_id

# main reply function
def reply_to_tweets():
    print('retrieving and replying to tweets...')
    last_id = ''

    if(file_exists(LAST_TWEET_FILENAME)):
        last_id = read_last_tweet_id(LAST_TWEET_FILENAME)
        mentions = api.mentions_timeline(last_id)
    else:
        mentions = api.mentions_timeline()

    for mention in reversed(mentions):
        if KEYHASHTAG in mention.text.lower():
            print('replying to: ' + mention.text)
            download_image(get_cat_image_url(), PIC_FILENAME)
            media_ids = []
            media_ids.append(upload_image(PIC_FILENAME))
            api.update_status(
                status='@'+mention.user.screen_name+' Here\'s a picture for you, nyan!',
                in_reply_to_status_id = mention.id,
                media_ids = media_ids)
            
        last_id = mention.id
        write_last_tweet_id(last_id, LAST_TWEET_FILENAME)  

# read keys from txt file
# you first need to create a txt file that contains
# consumer key, consumer secret key, access key, and access secret key
# in this order, line by line
f = open(KEYS_FILENAME, 'r')
CONSUMER_KEY = f.readline()
CONSUMER_SECRET = f.readline()
ACCESS_KEY = f.readline()
ACCESS_SECRET = f.readline()

# authenticate twepy
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

# bot loop
while(True):
    reply_to_tweets()
    time.sleep(15)