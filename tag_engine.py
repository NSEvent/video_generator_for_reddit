#! usr/bin/env python3
# Kevin TangW
# Started 7/11/2019

import re
import string
import time
from collections import Counter
import nltk
from nltk.corpus import stopwords
from nltk.collocations import *


MAX_COMMENT_LENGTH = 10000


def print_num_list(ls):
	i = 1
	for word in ls:
		print(str(i) + ': ' + word)
		i += 1

# Tag_engine parses the comments of a submission for tags
class Tag_engine:

	# submission_fullname is a string, comm is a list of comment objects
	def __init__(self, submission_fullname, subreddit_name, comm):
		self.submission_fullname = submission_fullname
		self.subreddit_name = subreddit_name

		# All comments concatenated
		self.body = ''

		# Space-delim list of all sanitized comments
		self._words = list()

		# Contains a list of top level comments lists
		# These top level comments are a list of replies
		self._top_level = list()

		# Contains a set of tags
		self._tags = set()

		try:
			for i in range(0, 50):
				#time.sleep(4)
				body = self.add_comm(comm[i])
				author = comm[i].author.name
				self._top_level.append([body, author])

		except:
			pass

		assert not (self.body == '')
		assert not (len(self._top_level) == 0)

		self.__sanitize_body()
		self._words = self.body.split()

		# Parse stopwords
		#USER_STOPWORDS = ['I', 'like']
		stop_words = stopwords.words('english')# + USER_STOPWORDS
		self._words = [word for word in self._words if word not in stop_words]

		assert not (len(self._words) == 0)

	# This function sanitizes self.body
	def __sanitize_body(self):
		# TODO sanatize comment before adding to body
		# emojis and overflow?

		# Remove all links
		self.body = re.sub(r'http\S+', '', self.body)
		# Replace all non-alphanum with a space and convert to lowercase
		self.body = re.sub('[^a-zA-Z]', ' ', self.body).lower()

	def __print_num_list(self, ls):
		i = 1
		for word in ls:
			if type(word) is tuple:
				word = self.__cat_list(word)
			print(str(i) + ': ' + word)
			i += 1

	def __cat_list(self, ls):
		return " ".join(ls)

	# This function adds two word tags to self._tags and returns the same
	def __bigram_parser(self, num_tags):
		bigram_measures = nltk.collocations.BigramAssocMeasures()
		finder = BigramCollocationFinder.from_words(self._words)
		half1 = int(num_tags) // 2
		half2 = num_tags - half1

		print('_____________________________________________________________________________________________')
		print('TOP BIGRAMS: LIKELIHOOD RATIO: ')
		self.__print_num_list(finder.nbest(bigram_measures.likelihood_ratio, half1))
		print('_____________________________________________________________________________________________')
		print('TOP BIGRAMS: PMI: ')
		finder = BigramCollocationFinder.from_words(self._words)

		self.__print_num_list(finder.nbest(bigram_measures.pmi, half2))
		print('_____________________________________________________________________________________________')

		_bigrams = list()
		for bigram in finder.nbest(bigram_measures.likelihood_ratio, half1):
			_bigrams.append(self.__cat_list(bigram))
		for bigram in finder.nbest(bigram_measures.pmi, half2):
			_bigrams.append(self.__cat_list(bigram))

		self._tags.update(_bigrams)
		return _bigrams

	# This function adds three word tags to self._tags and returns the same
	def __trigram_parser(self, num_tags):
		trigram_measures = nltk.collocations.TrigramAssocMeasures()
		finder = TrigramCollocationFinder.from_words(self._words)
		half1 = num_tags // 2
		half2 = num_tags - half1

		print('_____________________________________________________________________________________________')
		print('TOP TRIGRAMS: LIKELIHOOD RATIO: ')
		self.__print_num_list(finder.nbest(trigram_measures.likelihood_ratio, half1))
		print('_____________________________________________________________________________________________')
		print('TOP TRIGRAMS: PMI: ')
		self.__print_num_list(finder.nbest(trigram_measures.pmi, half2))
		print('_____________________________________________________________________________________________')

		_trigrams = list()
		for trigram in finder.nbest(trigram_measures.likelihood_ratio, half1):
			_trigrams.append(self.__cat_list(trigram))
		for trigram in finder.nbest(trigram_measures.pmi, half2):
			_trigrams.append(self.__cat_list(trigram))

		self._tags.update(_trigrams)
		return _trigrams


	# This function adds one word tags to self._tags and returns the same
	def __tag_parser(self, num_tags):
		# Counter for word frequencies of all comments
		_counter = Counter()

		# Count word frequencies
		for word in self._words:
			_counter[word] += 1

		_tags = [_tag for _tag, _freq in _counter.most_common(num_tags)]
		self._tags.update(_tags)

		print('_____________________________________________________________________________________________')
		print('TOP SINGLE TAGS: FREQUENCY: ')
		self.__print_num_list(_tags)
		print('_____________________________________________________________________________________________')

		return _tags


	# This function is used to check whether a comment added to self._body
	def __is_valid(self, comm):
		# Handle comments from AutoModerator and bots
		username = comm.author.name.lower()
		if ('moderator' in username) or ('automod' in username) or ('mod' in username) or ('bot' in username):
			print('ABORTED: COMMENT HAS IRRELEVANT USERNAME\n')
			return False

		if (len(comm.body) > MAX_COMMENT_LENGTH):
			print('ABORTED: COMMENT TOO LONG\n')
			return False

		if (comm.stickied):
			print('ABORTED: COMMENT IS STICKIED (PROBABLY USELESS)')
			return False

		return True

	# comm is a comment obj, thread_size is how far down the comment tree this function will attempt to scan
	# This function is used to feed Tag_engine data from a single top level comment and its replies down its comment thread
	# Appends all comments to self.body
	# Returns a list of top level comment body and its replies bodies

	# This function cats a comment to self._body and returns the comment body
	def add_comm(self, comm):
		try:
			#print('ADDING COMMENT: ' + comm.body + ' by ' + comm.author.name + '\n')

			if not self.__is_valid(comm):
				return comm.body


			self.body += (' ' + comm.body + ' ')

		except:
			pass

		return comm.body

	# This function cats a comment thread (top level comment with its replies) to self._body and returns the a list of comments in the thread
	def add_comm_thread(self, comm, thread_size = 0):
		_thread = list()
		try:
			#print('ADDING COMMENT: ' + comm.body + ' by ' + comm.author.name + '\n')
			if not self.__is_valid(comm):
				return _thread

			_thread.append(comm.body)
			self.body += (' ' + comm.body + ' ')

			if (thread_size == 0):
				return comm.body

			comm.refresh()

			tabs = '\t'

			reply = comm.replies[0]

			for level in range(0, thread_size):
				#print(tabs + 'ADDING REPLY: ' + reply.body + ' by ' + reply.author.name + '\n')
				if not self.__is_valid(reply):
					return _thread

				_thread.append(reply.body)
				self.body += (' ' + reply.body + ' ')

				tabs += '\t'
				reply = reply.replies[0]

		except:
			pass

		return _thread


	def get_tags(self, num_tags = 60):
		if (len(self._tags) == 0):
			num_tags = num_tags // 3

			self.__tag_parser(num_tags)
			self.__bigram_parser(num_tags)
			self.__trigram_parser(num_tags)

		assert not (len(self._tags) == 0)

		return self._tags

	# Returns a list of (comment_body, author)
	def get_comments(self):
		return self._top_level # [:len]


	# comm is a comment obj
	def test_print_comments(self, comm):

		print('Author: ' + comm.author.name)
		print('Body: ' + comm.body + '\n')
		comm.refresh()
		#print(comm[0].body)
		#print(comm[1].body)
		tabs = '\t'

		try:
			reply = comm.replies[0]

			for level in range(0, 3):
				print(tabs + 'Author: ' + reply.author.name)
				print(tabs + 'Body: ' + reply.body + '\n')

				tabs = tabs + '\t'
				reply = reply.replies[0]

		except:
			print('END OF THREAD')

		print('_____________________________________________________________________________________________')
