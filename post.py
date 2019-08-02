#! usr/bin/env python3
# Kevin Tang
# Started 7/11/2019


import os
import sys
import time
import praw
import datetime as dt
import urllib
import urllib.request
import pprint
import textwrap
import subprocess
import shlex
from tag_engine import Tag_engine
from tag_engine import print_num_list

ENCODING_OPTION_LOW = '-c:v libx264 -y -crf 30 -preset ultrafast'
ENCODING_OPTION_MID = '-c:v libx264 -y -crf 26 -preset veryfast'
ENCODING_OPTION_HIGH = '-c:v libx264 -y -crf 20 -preset veryfast'

ENCODING = ENCODING_OPTION_LOW

# Returns a subreddit obj given a reddit obj and a subreddit name
# Modularized for future changes on how subreddit is chosen (maybe videos from multiple subreddits)
def get_subreddit(reddit_obj, subreddit_name):
	return reddit.subreddit(subreddit_name)


def get_submissions(subreddit_obj, query, submission_limit = 5):
	return subreddit.search(query, limit = submission_limit)


class Post:
	# submission: a submission obj from PRAW, max_comments = number of top level comments that will be attempted to be scanned
	def __init__(self, submission, max_comments = 10):
		# Init video information
		self.fullname = submission.name
		self.subreddit_name = submission.subreddit.display_name

		# Associated files for this post
		self.filename_ppmp4 = self.subreddit_name + '/pp/' + self.fullname + '.mp4'
		self.filename_normmp4 = self.subreddit_name + '/norm/' + self.fullname + '.mp4'
		self.filename_ccmp4 = self.subreddit_name + '/cc/' + self.fullname + '.mp4'
		self.filename_gifmp4 = self.subreddit_name + '/gif/' + self.fullname + '.mp4'

		self.filename_comm = self.subreddit_name + '/comm/' + self.fullname + '.txt'

		# Try to get video information
		try:
			video_info = submission.media['reddit_video']
			self.fallback_url = video_info['fallback_url']
			self.duration = video_info['duration']
			self.height = float(video_info['height'])
			self.width = float(video_info['width'])
			self.aspect_ratio = self.width / self.height

			# in pixels
			self.normalized_height = 1920#1280
			self.normalized_width = 1080 * self.width / self.height #720
			self.margin_width = (self.normalized_height - self.normalized_width) / 2

			# in char widths
			estimated_chars_to_fill_width = 135#150
			precomment_width = 3#1
			self.wrap_len = int((self.margin_width / self.normalized_height) * estimated_chars_to_fill_width) - precomment_width
			# Takes care of videos that have no margins
			if (self.aspect_ratio >= 1.5):
				self.wrap_len = 30

			self.is_video = True

		except:
			self.is_video = False
			pass


		# Init attribution information
		self.author = submission.author.name
		self.title = submission.title
		self.post_url = submission.permalink

		# Init post statistics information
		self.num_upvotes = submission.score
		self.num_awards = submission.total_awards_received
		self.num_comments = submission.num_comments
		self.is_safe = (not submission.over_18) and (submission.parent_whitelist_status == 'all_ads')

		# Init tag information
		te = Tag_engine(self.fullname, self.subreddit_name, submission.comments)
		self._tags = te.get_tags(10)
		self._comments = te.get_comments()

		# Printing info
		print('POST OBJECT INITIALIZED')
		print('_____________________________________________________________________________________________')
		print('TITLE: ' + self.title)
		print('AUTHOR: ' + self.author)
		if self.is_video:
			print('IS_VIDEO: True')
			print('ASPECT_RATIO: ' + str(self.aspect_ratio))
		else:
			print('IS_VIDEO: False')

		print('URL: https://www.reddit.com' + self.post_url)
		print('PPMP4: ' + self.filename_ppmp4)
		print('MP4: ' + self.filename_normmp4)
		print('CCMP4: ' + self.filename_ccmp4)
		#print('BODY USED: ' + str(te._words))
		print('TOP TAGS: ')
		print_num_list(te._tags)
		print('_____________________________________________________________________________________________')


		if not os.path.exists(self.subreddit_name):
			os.mkdir(self.subreddit_name)


	def save_video(self):
		dls_size = 0

		ppdir = self.subreddit_name + '/pp'
		normdir = self.subreddit_name + '/norm'
		if not os.path.exists(ppdir):
			os.mkdir(ppdir)
		if not os.path.exists(normdir):
			os.mkdir(normdir)

		print('Attempting to download pp video at ' + self.filename_ppmp4)


		if not os.path.isfile(self.filename_ppmp4):
			try:
				# pprint.pprint(vars(sub))

				print('\tDownloading ' + self.filename_ppmp4 + '...', end='')
				sys.stdout.flush()

				# Sleep to avoid being blocked from reddit
				time.sleep(4)
				meta = urllib.request.urlretrieve(self.fallback_url, self.filename_ppmp4)[1]
				dl_size = float(meta['Content-Length'])

				print('success[' + str(round(dl_size / float(pow(2, 20)), 1)) + 'mb]')

				dls_size += dl_size


				# For normalizing to 720p HD 1280x720 videos
				# command = ('ffmpeg -i ' + self.filename_ppmp4 +' -vf "scale=1280:720:force_original_aspect_ratio=decrease, pad=1280:720:(ow-iw)/2:(oh-ih)/2" ' + self.filename_normmp4)# .split()

				# For normalizing to 1080p HD 1920x1080 videos
				command = 'ffmpeg -i {} \
				 		-vf "scale=1920:1080:force_original_aspect_ratio=decrease, pad=1920:1080:(ow-iw)/2:(oh-ih)/2" \
						{} {}'.format(self.filename_ppmp4, \
									ENCODING, self.filename_normmp4)

				print(command)
				subprocess.call(shlex.split(command))


			except TypeError:
				print('failed')



		else:
			print("File already exists")

	def save_comments(self):
		commdir = self.subreddit_name + '/comm'
		if not os.path.exists(commdir):
			os.mkdir(commdir)

		print('SAVING COMMENTS AT ' + self.filename_comm)

		if not os.path.isfile(self.filename_comm):
			f = open(self.filename_comm, 'w+', encoding='utf-8')

			tw = textwrap.TextWrapper(width=self.wrap_len, fix_sentence_endings=True, replace_whitespace=True)

			f.write(self.author + ':\n')
			f.write(tw.fill(self.title) + '\n\n')
			for (body, author) in self._comments:
				f.write(author + ': \n' + tw.fill(body) + '\n\n')
			f.close()

		else:
			print('File already exists')



	def overlay_comments(self):
		ccdir = self.subreddit_name + '/cc'
		if not os.path.exists(ccdir):
			os.mkdir(ccdir)

		print('SAVING VIDEO WITH COMMENTS AT ' + self.filename_ccmp4)

		if not os.path.isfile(self.filename_ccmp4):
			# Command adapted to 1080p
			command = 'ffmpeg -i {} \
					-filter_complex "[0]split[txt][orig]; \
					[txt]drawtext=fontfile=fonts/verdana.ttf:fontsize=28:fontcolor=white:x=5:y=h-60*t: \
					textfile={}:bordercolor=black:borderw=3:fix_bounds=1[txt]; \
					[orig]crop=iw:2:0:0[orig]; \
					[txt][orig]overlay" \
					{} {}'.format(self.filename_normmp4, \
								self.filename_comm, \
								ENCODING, self.filename_ccmp4)


			print(command)
			subprocess.call(shlex.split(command))
		else:
			print('File already exists')

	def overlay_gif(self):
		gifdir = self.subreddit_name + '/gif'
		if not os.path.exists(gifdir):
			os.mkdir(gifdir)

		print('SAVING VIDEO WITH GIF AT ' + self.filename_gifmp4)

		if not os.path.isfile(self.filename_gifmp4):
			filename_gif = 'giphy.gif'
			# In pixels
			gif_width = 268#480
			gif_height = 268#324

			# Aligned to bottom right corner
			command = 'ffmpeg -i {} \
				  	-ignore_loop 0 -i {} \
				  	-filter_complex "[0][1]overlay=x=main_w-{}:y=main_h-{}:shortest=1" \
				  	{} {}'.format(self.filename_ccmp4, \
								filename_gif, \
								gif_width, gif_height, \
								ENCODING, self.filename_gifmp4)
			print(command)
			subprocess.call(shlex.split(command))

		else:
			print('File already exists')
