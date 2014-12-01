import pylast
import numpy as np
import lyrics # from https://github.com/tramby/py-lyrics
import re
from string import punctuation
from operator import itemgetter
import cPickle as pickle
import os

from utils import *

# Params
N_words = 100
recompute_lda = False
top_songs = 200 # numbers of song to retrieve
username = "ADD_USERNAME_HERE"

API_KEY, API_SECRET = set_api_key("API_INFO.txt")

output_words = username + "_words_list.p"
output_lyrics = username + "_lyrics_list.p"
output_alllyrics = username + "_alllyrics.txt"

print("Setup configurations...")
network = pylast.LastFMNetwork(api_key = API_KEY, api_secret =
    API_SECRET)

user = pylast.User(username, network)

# Tracks analysis
#tracks = user.get_recent_tracks(limit=None)
library = user.get_library()
tracks = library.get_tracks(limit=top_songs)

# load stopwords file
stopwords = open("stopwords.txt", "r").read().split()
stiowords = [x.strip(punctuation) for x in stopwords if len(x)>2]

lyrics_list = {}
words_list = {}
if not os.path.exists(output_words) or not os.path.exists(output_alllyrics):
    print("Fetching tracks lyrics...")
    outfile = open(output_alllyrics, "w")
    for track_item in tracks:
        try:
            artist = str(track_item[0].get_artist().name)
            title = str(track_item[0].get_title())
            key = "{0} - {1}".format(artist, title)
        except:
            continue
        try:
            lyrics_now = lyrics.getlyrics(artist, title)
            if lyrics_now != '':
                lyrics_list[key] = lyrics_now
                # get words alphanumerics
                words = [x.lower() for x in lyrics_now.split() if \
                         re.match('^[\w-]+$', x) is not None]
                # remove stopwords
                words = [x for x in words if len(x)>2 and (not x in stopwords)]
                # count frequencies
                wcount = {}
                for w in words: wcount[w] = wcount.get(w, 0) + 1
                # write words to file
                outfile.write(" ".join(words))
                outfile.write("\n")
                # take top N
                top = sorted(wcount.iteritems(), key=itemgetter(1), \
                             reverse=True)[:N_words]
                words_list[key] = top
                print("Processed: {0}".format(key))
            else:
                print("Song not available: {0}".format(key))
        except:
            print("Song not recognized: {0}".format(key))
    outfile.close()
    pickle.dump(words_list, open(output_words, "wb"))
    pickle.dump(lyrics_list, open(output_lyrics, "wb"))
else:
    print("Loading tracks lyrics...")
    words_list = pickle.load(open(output_words, "r"))
    lyrics_list = pickle.load(open(output_lyrics, "r"))


# Run lda from shell
if not os.path.exists(username + "_ldaphi.p") or recompute_lda:
    cmd = "python2 lda.py -f " + output_alllyrics  + " -k 7 --alpha=0.5 --beta=0.5 -i 100"
    print("Running command {0}".format(cmd))
    os.system(cmd)
    os.system("mv ldaphi.p " + username + "_ldaphi.p")

print("Loading LDA results...")
(ldak, phi, voca) = pickle.load(open(username + "_ldaphi.p", "rb"))

# Generate the output html
print("Creating the html output...")
generatenicelda(lyrics_list, words_list, ldak, phi, voca)
