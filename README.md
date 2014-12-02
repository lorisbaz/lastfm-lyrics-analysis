lastfm-lyrics-analysis
======================

Inspired by the work done by karpathy for organizing the papers by topics I created a script that takes someone's most-listened songs in lastfm and clusters the lyrics using LDA.
It works with Python 2.7.


##Instruction

1. Install pylast from https://code.google.com/p/pylast/
2. Get the dev keys from lastfm: http://www.lastfm.it/api/account/create
3. Copy the API key and the API secret in the `API_INFO.txt` file (two separate rows)
4. Open `main_track_lyrics_analysis.py` and replace the username with yours (line 16)
5. Run `python2 main_track_lyrics_analysis.py` and look at the results in `songsnice.html`


##Dependencies

- lyrics https://github.com/tremby/py-lyrics
- pylast https://code.google.com/p/pylast/
- lda https://github.com/shuyo/iir/tree/master/lda
- numpy

## Licence

BSD license.
