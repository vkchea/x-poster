import tweepy

def post_to_x(text, picture_path, emojis):
    """
    Posts a tweet with text, an image, and a list of emojis.

    Parameters:
        text (str): The text content of the tweet.
        picture_path (str): The file path of the picture to attach.
        emojis (list): A list of emojis to append to the tweet.
    """
    """
        Retrieve API and Access token information from a text file.
        1st line = API_KEY
        2nd line = API_SECRET
        3rd line = ACCESS_TOKEN
        4th line = ACCESS_TOKEN_SECRET
        5th line = API_BEARER_TOKEN 
    """
    access_list = []
    with open('Files/access.txt', 'r') as file:
        lines = file.readlines()

    for line in lines:
        access_list.append(line.strip())

    API_KEY = access_list[0]
    API_SECRET = access_list[1]
    ACCESS_TOKEN = access_list[2]
    ACCESS_TOKEN_SECRET = access_list[3]
    API_BEARER_TOKEN = access_list[4]

#     # Authenticate to Twitter
    auth = tweepy.OAuth1UserHandler(consumer_key=API_KEY,
                                    consumer_secret=API_SECRET,
                                    access_token=ACCESS_TOKEN,
                                    access_token_secret=ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)

    try:
#         # Combine text and emojis into a single string
        emojis_str = " ".join(emojis)
        tweet_content = f"{text} {emojis_str}"

        # Post the tweet with an image
        if picture_path:
            api.update_status_with_media(status=tweet_content, filename=picture_path)
        else:
            api.update_status(status=tweet_content)

        print("Tweet posted successfully!")

    except Exception as e:
        print(f"An error occurred: {e}")

# # Example usage
if __name__ == "__main__":
    text = "Check out my new post!"
    picture_path = ""  # Provide the correct path to your image
    emojis = ["🚀", "🌟", "📸"]  # List of emojis

    post_to_x(text, picture_path, emojis)