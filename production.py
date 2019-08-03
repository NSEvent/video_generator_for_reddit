#! usr/bin/env python3
# Kevin Tang
# Started 7/8/2019

import praw
from post import Post


# Returns a subreddit obj given a reddit obj and a subreddit name
# Modularized for future changes on how subreddit is chosen (maybe videos from multiple subreddits)
def get_subreddit(reddit_obj, subreddit_name):
	return reddit.subreddit(subreddit_name)


# Searches for submissions given a subreddit obj and a query
# Returns submission limit number of submissions up to 1000
def get_submissions(subreddit_obj, query, submission_limit = 5):
	return subreddit.search(query, limit = submission_limit)


# Downloads and processes a video given a url to a reddit hosted video post
# Finished videos are stored in ./<subreddit_name>/gif/
def scrape_video(post_url):
	reddit = praw.Reddit(client_id='', \
			     client_secret='', \
			     user_agent='', \
			     username='', \
			     password='')
	sub = praw.models.Submission(reddit, url = post_url)


	# Intitialize post object, scrape comments, and generate top tags
	p = Post(sub)

	# Save top videos and normalize to 1920x1080
	if (p.save_video()):
		# Process video

		# Save comments to txt file
		p.save_comments()

		# Overlay scrolling comments on left margin
		p.overlay_comments()

		# Overlay gif on bottom right corner
		p.overlay_gif()
