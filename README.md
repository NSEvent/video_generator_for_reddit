# reddit_video_generator_demo
A personal project that creates a video out of reddit video posts, given a url to the post.

See a demo of the video generated from [LINK](reddit.com)

The program downloads the video, normalizes the size, overlays the reddit comments on the left sidebar and a gif on the right sidebar.

Tags for each video are drawn from top comments.

The original goal was to create random compilations of reddit videos given a subreddit. This project is still under development in a private repository.


# To try yourself
Follow this to signup for [reddit api access](https://github.com/reddit-archive/reddit/wiki/OAuth2)

Enter your api information into test.py

Enter your desired link to a reddit video post in main.py

## Install
sudo apt install ffmpeg


pip install praw

pip install nltk


python3

import nltk

nltk.download('punkt')

nltk.download('stopwords')

nltk.download('averaged_perceptron_tagger')


