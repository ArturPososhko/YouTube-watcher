#!/usr/bin/env python3

import json
import logging
from pprint import pformat
import sys
import requests
from config import config

def get_playlist_items_page(google_api_key, youtube_playlist_id, page_token=None):
    response = requests.get("https://www.googleapis.com/youtube/v3/playlistItems", params={
        "key": google_api_key,
        "playlistId": youtube_playlist_id,
        "part": "contentDetails",
        "pageToken": page_token,
    })
    payload = json.loads(response.text)
    logging.debug("GOT %s", payload)
    return payload

def get_playlist_items(google_api_key, youtube_playlist_id, page_token=None):
    payload = get_playlist_items_page(google_api_key, youtube_playlist_id, page_token)

    yield from payload["items"]

    next_page_token = payload.get("nextPageToken")

    if next_page_token is not None:
        yield from get_playlist_items(google_api_key, youtube_playlist_id, next_page_token)
        
def get_videos_page(google_api_key, video_id, page_token=None):
    response = requests.get("https://www.googleapis.com/youtube/v3/videos", params={
        "key": google_api_key,
        "id": video_id,
        "part": "snippet,statistics",
        "pageToken": page_token
    })
        
    payload = json.loads(response.text)
    logging.debug("GOT %s", payload)
    return payload



def get_videos(google_api_key, youtube_playlist_id, page_token=None):
    payload = get_videos_page(google_api_key, youtube_playlist_id, page_token)

    yield from payload["items"]

    next_page_token = payload.get("nextPageToken")

    if next_page_token is not None:
        yield from get_videos(google_api_key, youtube_playlist_id, next_page_token)


def summarize_video(video):
    return {
        "video_id": video["id"],
        "title": video["snippet"]["title"],
        "views": int(video["statistics"].get("viewCount", 0)),
        "likes": int(video["statistics"].get("likeCount", 0)),
        "comments": int(video["statistics"].get("commentCount", 0)),
    }

def main():
    logging.info('START')
    google_api_key = config["google_api_key"]
    youtube_playlist_id = config["youtube_playlist_id"]

    for video_item in get_playlist_items(google_api_key, youtube_playlist_id):
        video_id = video_item["contentDetails"]["videoId"]
        for video in get_videos(google_api_key, video_id):
            logging.info("GOT %s", pformat(summarize_video(video)))

            


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    sys.exit(main())