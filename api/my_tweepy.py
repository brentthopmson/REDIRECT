import tweepy
import os
import requests
from io import BytesIO

# Twitter API credentials (replace with your credentials)
consumer_key = "lFu7dSnaEW4vvtAYri2CupAFf"
consumer_secret = "uYDFv5toVf68AFzEkIV5FIMVAQCbGHjxmQTDMSwe2ZCunYxTrN"
access_token = "1749480702465228800-gf3v85auf4tuqPLSKhphLAF46eOvIL"
access_secret = "dFPjyeM4ByYAYes67F2XMAXWUFDqirPRO8UqacGfTPirm"


# Set up Tweepy client for Twitter API v1 (for media uploads)
client_v1 = tweepy.API(
    tweepy.OAuth1UserHandler(
        consumer_key=consumer_key,
        consumer_secret=consumer_secret,
        access_token=access_token,
        access_token_secret=access_secret,
    )
)

# Function to upload media from a list of URLs and return their media IDs
def upload_media_from_urls_and_get_ids(media_info_list):
    media_ids = []

    for media_info in media_info_list:
        url = media_info.get("url")
        file_name = media_info.get("file_name")

        if not url or not file_name:
            continue  # Skip if either URL or file name is missing

        try:
            # Fetch the media from the given URL
            response = requests.get(url, stream=True)

            if response.status_code == 200:
                # Use BytesIO to simulate a file in memory
                media_data = BytesIO()

                # Write content in chunks to handle large files
                for chunk in response.iter_content(chunk_size=1024):
                    media_data.write(chunk)

                # Reset the "file" pointer
                media_data.seek(0)

                # Upload the media to Twitter with the appropriate file name
                media = client_v1.media_upload(filename=file_name, file=media_data)

                media_ids.append(media.media_id)  # Add media ID to the list
            else:
                print(f"Failed to fetch media from URL: {url}")

        except Exception as e:
            print(f"Error uploading media from URL {url}: {e}")

    return media_ids  # Return list of media IDs