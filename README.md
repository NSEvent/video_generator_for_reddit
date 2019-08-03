# reddit_video_generator_demo
A tool that creates videos out of reddit-hosted video posts, given a url to the post.

## Examples of generated videos
1. [ORIGINAL POST](https://www.reddit.com/r/aww/comments/c5xurx/my_dad_sent_me_this_and_i_have_a_new_favorite/) |  [VIDEO](https://giphy.com/gifs/Q7joL1dJHT6kARdV5T)
2. [ORIGINAL POST](https://www.reddit.com/r/aww/comments/clheav/how_im_greeted_each_time_i_come_home_from_work/) |  [VIDEO](https://giphy.com/gifs/YS5zvunBQIMtrtMEek)
3. [ORIGINAL POST](https://www.reddit.com/r/aww/comments/clk47p/ups_man_took_a_moment_yesterday_for_himself_it/) |  [VIDEO](https://giphy.com/gifs/W22iA9jWyFDXi6p7y2)

## About
This program scrapes post information using [PRAW](https://praw.readthedocs.io/en/latest/#).

The program performs its video manipulation using [ffmpy](https://ffmpeg.org/)
- downloads a video from a reddit-hosted video post
- normalizes the video dimensions to 1920x1080
- overlays top reddit comments scrolling up the left sidebar
- overlays a gif on the bottom right corner

The video dimensions are normalized to 1920x1080 to be easily combined to create a compilation later.

Top tags for each video are drawn from top comments. [nltk](http://www.nltk.org/) is used to select 1-word, 2-word-phrase, and 3-word-phrase tags to represent a post. This feature works best if the post has a large number of comments.

Tested with Python 3.7.0 in Linux environment

# To try yourself
1. Create a [new reddit app](https://www.reddit.com/prefs/apps). Choose "script" as the type of app. Use `http://localhost:8080` for the "redirect uri".
2. Enter your reddit app information in test.py.
3. Add a call to `scrape_video(your_url_goes_here)` in main.py.
4. Install the required dependencies listed below.

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
```bash
python3 main.py
```
Finished videos are stored in `<subreddit_name>/gif/`


