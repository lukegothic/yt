# -*- coding: utf-8 -*-

import os
import webbrowser
import random
import hashlib

from googleapiclient.discovery import build

def get_simple_service():
  return build("youtube", "v3", developerKey='AIzaSyBqKqtkCJaS6wft7rQGSpjZOWztY7XsrEc')

# Remove keyword arguments that are not set
def remove_empty_kwargs(**kwargs):
  good_kwargs = {}
  if kwargs is not None:
    for key, value in kwargs.items():
      if value:
        good_kwargs[key] = value
  return good_kwargs

def search_list_by_keyword(client, **kwargs):
  # See full sample for function
  kwargs = remove_empty_kwargs(**kwargs)

  return client.search().list(
    **kwargs
  ).execute()

if __name__ == '__main__':
    client = get_simple_service()
    with open("playlist.txt") as f:
        songs = f.read()
    hashedlist = hashlib.md5(songs.encode("utf-8")).hexdigest()
    filete = "{}.html".format(hashedlist)
    try:
        with open(filete) as f:
            pass
    except:
        songs = songs.split("\n")
        videoIds = []
        for song in songs:
            if song != "":
                #TODO: videoEmbeddable y videoEmbeddable no parece que funcionen, por lo que creamos una blacklist alimentada cuando da un error en reproduccion
                results = search_list_by_keyword(client,part='id',maxResults=10,q=song,type='video',videoSyndicated="true",videoEmbeddable="true")
                if len(results["items"]) > 0:
                    videoIds.append(results["items"][0]["id"]["videoId"])
        random.shuffle(videoIds)
        with open("template.html") as f:
            template = f.read()
        template = template.replace("{FIRSTVIDEO}", videoIds[0])
        videoIds.pop(0)
        template = template.replace("{NEXTVIDEOS}", ",".join(videoIds))
        with open(filete, "w") as f:
            f.write(template)
    webbrowser.open(filete)
