#   Supporting fuctions for bot-script.py
#

import datetime
import praw
import time
import requests
from settings import *

#   reddit creds
reddit = praw.Reddit(
        user_agent=REDDIT_USER_AGENT,
        client_id=REDDIT_CLIENT_ID,
        client_secret=REDDIT_CLIENT_SECRET,
        username=REDDIT_USERNAME,
        password=REDDIT_PASSWORD,
)


def check_today(thisdate):
    """
    The course is described as:

    "...runs from the first Monday of the month,
        and lasts for four weeks..."

    Simple? Yes, but there are some surprising corner
            cases, e.g.:
     - sometimes the course doesn't start until the 7th of the month (e.g.September 2020)
     - the last day or two of <MONTH>'s course end up being in <MONTH+1> (e.g September 2020)
     - there's sometimes a whole week's gap at the end of a course (e.g. June 2020)

    """
    delta = datetime.timedelta(days=1)
    delta7 = datetime.timedelta(days=7)

    days_into_week = thisdate.isoweekday()  #    ISO weekday, 1=Monday

    print(
        "We're on day #: ", days_into_week, " of the week, where 1=Monday", flush=True
    )

    #   No lesson on the weekend
    if (days_into_week == 6) or (days_into_week == 7):
        return None

    #   Find the Monday of that week...
    thismonday = thisdate - (delta * (days_into_week - 1))
    #   ...the month of that is "month_num" in all cases.
    month_num = thismonday.month  #    January=1, December=12
    month_name = thismonday.strftime("%B")

    #   Now, from that Monday, step back 7 days each time, counting,
    #   until Month.(this_monday) <> month_num.
    weeks_back = 0
    while thismonday.month == month_num:
        thismonday = thismonday - (delta7)
        weeks_back = weeks_back + 1
    #   We've gone one week too far back, so...
    weeks_back = weeks_back - 1

    #   Each week has five days of lessons - and then the few days of
    #   the week we're in...
    day_num = ((weeks_back) * 5) + days_into_week

    #   ...but we only have 20 lessons...
    if day_num > 20:
        return None

    return day_num

def start_of_next(thisdate):
    """
    Use similar technique as check_today()

    Date:               Expected result:
    =====               ================
    30 Sept 2020        5 October 2020
    30 December 2020    4 January 2021
    24 June 2020        6 July 2020
    27 August 2020      7 September 2020

   """
    delta = datetime.timedelta(days=1)
    delta7 = datetime.timedelta(days=7)
    deltam = datetime.timedelta(weeks=4)

    # hop back a week...
    thisdate = thisdate - delta7
    # and to the Monday of that week...
    thisdate = thisdate - (delta * (thisdate.isoweekday() - 1))
    # then jump a month forward...
    thisdate= thisdate + deltam
    # and to the Monday of that week...
    thisdate = thisdate - (delta * (thisdate.isoweekday() - 1))
    #   Now, from that Monday, step back 7 days each time, counting,
    #   until we get into the previous month
    weeks_back = 0
    month_num = thisdate.month
    while thisdate.month == month_num:
        thisdate = thisdate - (delta7)
        weeks_back = weeks_back + 1
    #   We've gone one week too far back, so...
    thisdate = thisdate + (delta7)
    start_date_of_next = thisdate.strftime("%-d %B %Y")
    # e.g. "2 November 2020"
    return(start_date_of_next)

def get_day(daynum):
    """
    Works out the filename for the day's lesson, then
    calls 'get_file' to pull directly from Github
    """
    filename = str(daynum).zfill(2) + ".md"  #   Padding '1' to '01'
    title, body = get_file(filename)
    return [title, body]


def get_file(filename):
    """
    Given a filename, pulls lesson directly from Github (no API), in RAW
    format, then splits the title text off and tidies it - and returns
    both it and the now-trimmed body as a list.
    """
    starturl = "https://raw.githubusercontent.com/livialima/linuxupskillchallenge/master/docs/"
    url = starturl + filename
    r = requests.get(url, allow_redirects=True)
    #   comes back as type 'bytes', which we convert to string
    contents = r.content
    strcontent = contents.decode("utf-8")
    #   mkdocs features are everything before the leading "# " of the title...
    full_file = strcontent.partition("# ")[2]
    #   title line is everything before the newline...
    title = full_file.partition("\n")[0]
    #   ...and the body is everything after.
    body = full_file.partition("\n")[2]
    return [title, body]


def get_advert_file(filename):
    """
    Given an advert filename, pulls text directly from Github (no API), in RAW
    format, then splits the title text off and tidies it - and returns
    both it and the now-trimmed body as a list.
    """
    starturl = "https://raw.githubusercontent.com/livialima/linuxupskillchallenge/master/docs/"
    url = starturl + filename
    r = requests.get(url, allow_redirects=True)
    #   comes back as type 'bytes', which we convert to string
    contents = r.content
    strcontent = contents.decode("utf-8")
    #   title line is everything before the newline...
    title = strcontent.partition("\n")[0]
    #   ...and the body is everything after.
    body = strcontent.partition("\n")[2]
    #   and then we trim the leading "TITLE: " off the title...
    title = title.partition("TITLE: ")[2]
    return [title, body]

def insert_backlink(sr, body, day_num):
    if day_num == 1:
        print("No backlink in lesson 1")
    else:
        #   we pull the lesson file for the previous directly from GitHub, and
        #   grab the backlink title from that...
        filename = str(day_num - 1).zfill(2) + ".md"  #   Padding '1' to '01'
        bl_title, bl_body = get_file(filename)
        bl_url = "<missing>"
        print("Previous post: ", bl_title)
        #   ...then find that title in the posts in the subreddit
        for post in sr.new(limit=25):
            print("Checking", post.title )
            if post.title.startswith(bl_title):
                print("Yup! foundit")
                bl_url = post.url
                break
        split_text = "Some rights reserved"
        top_of_body = body.partition(split_text)[0]
        bottom_of_body = body.partition(split_text)[2]
        backlink_text = (
            "\n\n## PREVIOUS DAY'S LESSON\n * [" + bl_title + "](" + bl_url + ")\n\n"
        )
        body = top_of_body + backlink_text + split_text + bottom_of_body

    return body


def post(sr,title, body):
    print("Posting: ", title)
    mypost= sr.submit(
            title,
            selftext=body,
       )
    approve(mypost)
    return mypost

def get_post_pin_day(sr, day_num):
    title, body = get_day(day_num)
    #   a 'backlink' is handy...
    body = insert_backlink(sr, body, day_num)
    mypost = post(sr, title, body)
    pause(5)
    approve(mypost)
    pause(5)
    sticky(mypost)
    pause(5)
    #    and pop in a matching "Thoughts and comments" post...
    #    title, body = get_file("thoughts-and-comments.md")
    #    replace X with the day number
    #    title = title.partition("X")[0] + str(day_num) + title.partition("X")[2]
    #    mypost = post(sr, title, body)

def get_post_pin_file(sr, filename):
    title, body = get_file(filename)
    mypost = post(sr, title, body)
    pause(5)
    approve(mypost)
    pause(5)
    sticky(mypost)


def get_post_file(sr, filename):
    title, body = get_file(filename)
    mypost = post(sr, title, body)
    pause(5)
    approve(mypost)


def get_post_advert(sr, subreddit_name, thisdate):
    """
    sr = The subreddit where we send lessons
    subreddit_name = The subreddit where we want to advertise

    The 'advert' text files are named in a very specific way:

           txt-for-linux-subreddit.md
           txt-for-sysadminblogs-reddit.md

    ...and have a very specific format.

    If sr == "linuxupskillBotTest" then we're in TEST mode and
    we will post the adverts in that same directory. Otherwise they go
    to their specific subreddits.

    """
    advert_file = "txt-for-" + subreddit_name + "-subreddit.md"
    print("Advert: ", advert_file)
    title, body = get_advert_file(advert_file)
    if title == "":
        print("WARNING: for some reason could not find 'title'...")
        return

    title = title + start_of_next(thisdate)

    if sr == "linuxupskillBotTest":
        print("Posting advert to TEST subreddit")
        mypost = post(sr, title, body)

    else:
        if sr == "linuxupskillChallenge":
            advert_sr = reddit.subreddit(subreddit_name)
            print("Posting advert to: ", advert_sr)
            post(advert_sr, title, body)


def clear_all_pinned(subreddit):
    for post in subreddit.new(limit=25):
        if post.stickied:
            unsticky(post)

def delete_day(subreddit, day_num):
    title = "Day " + str(day_num) + " - "
    delete_title(subreddit, title)


def delete_title(subreddit, title):
    for post in subreddit.new(limit=25):
        if post.title.startswith(title):
            print("Deleting: ", post.title)
            post.delete()


def pin_title(subreddit, title):
    for post in subreddit.new(limit=25):
        if post.title.startswith(title):
            approve(post)
            pause(5)
            sticky(post)


def pause(secs):
    for tic in range(secs):
        time.sleep(1)
        print(".", end="", flush=True)
    print("")   # for newline


def approve(post):
    print("Approving...")
    try:
        post.mod.approve()
    except Exception as e:
        print(e)
    # except:
    #    print("WARNING: can't approve it for some reason...")


def sticky(post):
    print("Stickying...")
    try:
        post.mod.sticky(state=True)
    except Exception as e:
        print(e)
    # except:
    #    print("WARNING: can't sticky it for some reason...")


def unsticky(post):
    print("Unsticking...")
    try:
        post.mod.sticky(state=False)
        post.mod.distinguish(how="no")
    except Exception as e:
        print(e)
    # except:
    #    print("WARNING: can't unsticky it for some reason...")
