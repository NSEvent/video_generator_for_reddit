# reddit_video_generator_demo
A personal project that creates videos out of reddit-hosted (https://v.redd.it) video posts, given a url to the post.

See a demo of the video generated from [LINK](reddit.com)

This program scrapes information using [PRAW](https://praw.readthedocs.io/en/latest/#)

The program downloads a video from a reddit-hosted video post, normalizes the dimensions of the video, and overlays scrolling reddit comments on the left sidebar and a gif on the right sidebar. The video dimensions are normalized to 1920x1080 to be combined easily later. The goal is to create random compilations of reddit videos given a subreddit. This project is still under development in a private repository.

Top tags for each video are drawn from top comments. [nltk](http://www.nltk.org/) is used to select 1-word, 2-word-phrase, and 3-word-phrase tags to represent a post. This feature works best if the post has a large number of comments.

Tested with Python 3.7.0

# To try yourself
1. Signup for [reddit api access](https://www.reddit.com/prefs/apps) and create a new app. Choose "script" as the type of app. Use `http://localhost:8080` for the "redirect uri". More information about OAuth2 can be found [here](https://github.com/reddit-archive/reddit/wiki/OAuth2)

2. Enter your reddit api information in test.py

3. Enter a reddit-hosted video post link in main.py

4. Install the required dependencies listed below

## Install required dependencies
```python
sudo apt install ffmpeg

pip install praw
pip install nltk

python3
import nltk

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')
```

## Run
`python3 main.py`


