#! usr/bin/env python3

# Kevin Tang
# Started 7/10/2019

from production import scrape_video


def main():

	scrape_video('https://www.reddit.com/r/aww/comments/c5xurx/my_dad_sent_me_this_and_i_have_a_new_favorite/')
	# scrape_video('https://www.reddit.com/r/aww/comments/clheav/how_im_greeted_each_time_i_come_home_from_work/')
	# scrape_video('https://www.reddit.com/r/aww/comments/clk47p/ups_man_took_a_moment_yesterday_for_himself_it/')


if __name__ == "__main__":
	main()
