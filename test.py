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

	# Intitialize post object, scrape comments, and generate top tags
	p = Post(sub)

	# Save top videos and normalize to 1920x1080
	p.save_video()

	# Save comments to txt file
	p.save_comments()

	# Overlay scrolling comments on left margin
	p.overlay_comments()

	# Overlay gif on left corner
	p.overlay_gif()
