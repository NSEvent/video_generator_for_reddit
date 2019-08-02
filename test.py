#! usr/bin/env python3
# Kevin Tang
# Started 7/8/2019

import praw
from post import Post

def test(post_url):
	# Sign up for Reddit API access and fill in these fields
	reddit = praw.Reddit(client_id='', \
			     client_secret='', \
			     user_agent='', \
			     username='', \
			     password='')
	sub = praw.models.Submission(reddit, url = post_url)

	p = Post(sub)
	p.save_video()
	p.save_comments()
	p.overlay_comments()
	p.overlay_gif()
