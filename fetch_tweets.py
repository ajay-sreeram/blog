import requests, json, urllib, os

top_k = 5
token = os.getenv('NOTION_SECRET', '').strip()
databaseID ="060af882b1024f73a172515e2089c615"
headers = {
    "Authorization": "Bearer " + token,
    "Content-Type": "application/json",
    "Notion-Version": "2022-02-22"
}

def readDatabase(databaseID, headers):
    if not token:
        return None
    readUrl = f"https://api.notion.com/v1/databases/{databaseID}/query"
    res = requests.request("POST", readUrl, headers=headers)
    data = res.json()
    if res.status_code == 200:
        print("notion access success")
        return data
    else:
        return None

def readTweets():
    data = readDatabase(databaseID, headers)
    tweets = []
    if data is None:
        return tweets
    for result in data['results']:
        props = result['properties']
        url_with_x = props['URL']['url']
        if type(url_with_x) == str and 'x.com' in url_with_x:
            twitter_url = url_with_x.replace('x.com', 'twitter.com')
            tweets.append(twitter_url)

    tweets = tweets[:top_k]
    return tweets

def get_embed_code(tweet_url):
    payload = {
        'url': tweet_url,
        'hide_thread': 'false'
    }
    params = urllib.parse.urlencode(payload)
    readUrl = f'https://publish.twitter.com/oembed?{params}'
    res = requests.request("GET", readUrl)
    data = res.json()
    if res.status_code == 200:
        return data['html'].strip()
    else:
        return None

def main():
    tweets = readTweets()
    top_tweets = []
    for tweet in tweets:
        block_code = get_embed_code(tweet)
        if type(block_code) == str:
            block_code = block_code.replace('<script async src=\"https://platform.twitter.com/widgets.js\" charset=\"utf-8\"></script>', '')
            block_code = block_code.strip()
            top_tweets.append({
                'url': tweet,
                'code': block_code
            })
    with open("tech-updates/top_tweets.json", "w") as f:
        json.dump(top_tweets, f)
    
if __name__ == '__main__':
    main()