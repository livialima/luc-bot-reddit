#!/usr/bin/env python

"""
   bot-script.py - Pulls the lessons for the Linux Upskill Challenge from Github into the subreddit

    Note 1: Don't run more that once a day - you'll risk multiple posting

    Note 2: This is basically a "Steve simulator":
         - Steve, in NZ, gets out of bed on a Monday morning
         - Feeds the cats, and makes himself a miso soup
         - Then posts Monday's lesson - (it's about 8 or 9am by this time)
         - However, because this script runs "in the cloud", the server will be
           running (almost always) on UTC - so the task must be scheduled for
           8PM. But, on Monday morning Steve's time, while it will be 8pm in Greenwich
           and it will be SUNDAY
         - So, the script will run and say "No lesson on a weekend" - not good
         - This is why the "time_bump" variable exists...

    Note 3: This also means that the script can't be run just Monday-Friday (which might
            seem sensible), but instead should be scheduled EVERY day

         """

import praw
import datetime
from functions import *
from settings import *

subreddit = None

def main():

    #   pull in the creds
    reddit = praw.Reddit(
        user_agent=REDDIT_USER_AGENT,
        client_id=REDDIT_CLIENT_ID,
        client_secret=REDDIT_CLIENT_SECRET,
        username=REDDIT_USERNAME,
        password=REDDIT_PASSWORD,
    )

    if len(sys.argv) < 2:
        sys.exit(
            "\n Usage: bot-script.py LIVE|TEST [<date>]"
            "\n "
            "\n e.g     bot-script LIVE             "  #   Production, today's date
            "\n         bot-script TEST             "  #   Test, today, to r/linuxupskillBotTest
            "\n         bot-script TEST 2020-11-01  "  #   Test, 1Nov2020 to r/linuxupskillBotTest"
            "\n "
        )

    if sys.argv[1] == "LIVE":
        today_date = datetime.datetime.today()
        subreddit = reddit.subreddit("linuxupskillchallenge")
        print("\nPosting to: r/upskillchallenge - with today's date: ", today_date)

    if sys.argv[1] == "TEST":
        TEST = True
        subreddit = reddit.subreddit("LinuxUpSkillBotTest")
        print("\nIn TESTing mode...")

        if len(sys.argv) > 2:
            today_date = datetime.datetime.strptime(sys.argv[2], "%Y-%m-%d")
            print("Using BOGUS date of: ", today_date)

        else:
            today_date = datetime.datetime.today()
            print("And working with today's date: ", today_date)

    #   Hardcode the correct 'time_bump'
    # time_bump = 0   #   If local timezone is NZ
    time_bump = +12 #     If local timezone is UTC (i.e. a cloud server)

    print("Before bump: ", today_date)
    today_date = today_date + datetime.timedelta(hours=time_bump)
    print("After bump:  ", today_date)

    #   Until now 'today_date' has been a datetime object because we cared about
    #   the time part. From now on we don't, and a simple date is expected. So this next
    #   active line converts it to type 'date' - something Python is happy to let us do.
    print("Which we trim to just date:")
    today_date = today_date.date()
    print (today_date)

    #   Which day of the course are we on?
    day_num = check_today(today_date)
    if day_num == 1:
        #    Post and pin the standard "Day 1" lesson - and the ditto the "short video"
        #       --> short-video and videos are now incorporated to the main day post
        #    (NO) Repost "HOW THIS WORKS" text. Don't pin, cos only two can be at a time
        clear_all_pinned(subreddit)
        get_post_pin_day(subreddit, day_num)
        #   get_post_pin_file(subreddit, "day1-short-video.md")
        #   delete the old "HOW..."
        #   delete_title(subreddit, "HOW THIS WORKS")
        #   then pull in the current one and pin...
        #   get_post_pin_file(subreddit, "how-this-works.md")
        #   clear last few of last month's lessons...
        #   Abolishing deleting posts: working on lock/archiving
        #   delete_day(subreddit, 20)
        #   delete_day(subreddit, 19)
        #   delete_day(subreddit, 18)
        #   delete_day(subreddit, 17)
        #   delete_day(subreddit, 16)

    elif day_num == 18:

        #   retrive, post and pin today's lesson as normal
        clear_all_pinned(subreddit)
        get_post_pin_day(subreddit, day_num)
        #delete_day(subreddit, day_num - 4)

        #   delete the old "HOW..."
        #   delete_title(subreddit, "HOW THIS WORKS")

        #   then pull in the current one and pin...
        get_post_pin_file(subreddit, "how-this-works.md")

        #    ...and post custom 'advert' messages to subreddits.
        get_post_advert(subreddit, "linuxadmin")    # OK'd by u/mthode, 13-Sept-2020
        get_post_advert(subreddit, "sysadminblogs") # OK'd by u/VA_Network_Nerd, 13-Sept-2020
        get_post_advert(subreddit, "linux4noobs") # No reply from u/Pi31415926
        get_post_advert(subreddit, "linuxmasterrace") # No reply from Mephiz
        get_post_advert(subreddit, "linux")   # No reply from u/kylev

        #   and "Day 0" posts for the benefit of the new 'intake'...
        get_post_file(subreddit, "00-AWS-Free-Tier.md")
        get_post_file(subreddit, "00-Digital-Ocean.md")
        get_post_file(subreddit, "00-Google-Cloud.md")

        #   calculate the start of the next course, and post a message about that
        first_monday = start_of_next(today_date)
        #   expand
        first_monday = "Next course starts on Monday, " + first_monday
        post(subreddit, first_monday, "")

    elif day_num == None:
        print("\nNo lesson today...")
        pass

    else:
        #   a 'normal' weekday...
        clear_all_pinned(subreddit)
        pin_title(subreddit, "HOW THIS WORKS")
        get_post_pin_day(subreddit, day_num)
        #   Abolishing deleting posts: working on lock/archiving
        #   delete_day(subreddit, day_num - 4)


if __name__ == "__main__":
    import sys
    main()
