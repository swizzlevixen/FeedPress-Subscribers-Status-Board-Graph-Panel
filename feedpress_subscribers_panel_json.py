"""
FeedPress Subscribers Status Board Graph Panel - JSON

Full write-up:
http://wp.me/p3sLxU-uf

Made to grab several days of stats from multiple feeds on http://feedpress.it
and create a JSON file with feeds for a Panic Status Board Graph Panel.

If you only want to see seven days of stats from one feed,
FeedPress already has you covered:
http://feedpress.it/support/questions/status-board

Originally written to graph stats for The Optical Podcast.
If you like 80's effects movies, and interviews with effects artists,
Give it a listen: http://opticalpodcast.com

-----

This script requires Requests, and was written against v2.2.0
http://docs.python-requests.org/en/latest/

Don't forget to customize your API_KEY, API_TOKEN, and FEEDS
at the top to get your data. More information about the FeedPress API,
and how to get your tokens, is available at http://feedpress.it/api

Under FEEDS, 'name' is what your feed is called on FeedPress. for example:
	feedpress.me/name

The 'alias' is what you'd like that feed to be called in the graph panel.

The 'color' is what color the line will be drawn with on the graph.
Color values can be yellow, green, red, purple, blue, mediumGray,
pink, aqua, orange, or lightGray, according to the Status Board 1.3 documentation.

GRAPH_TITLE is the title of the graph.

HISTORY_LENGTH is the number of days you'd like to see in the graph.

>> Known issue: If all of the feeds don't have the same number of days available,
   the graph gets screwed up. Status Board seems to assume all of the graph lines
   start on the same date, and left-justifies all of the graph lines. A quick workaround 
   is just to keep the HISTORY_LENGTH to the number of days you have data for all feeds.

DATE_FORMAT is the date along the X-axis (bottom) of the graph.
Use Python date formatter elements to customize this:
http://docs.python.org/2/library/datetime.html#strftime-and-strptime-behavior


Find more about Panic Status Board's graphing documentation here:
http://www.panic.com/statusboard/docs/graph_tutorial.pdf

Copyright (c) 2014 Mark Boszko
Released under The MIT License (MIT)
http://opensource.org/licenses/MIT

Enjoy!

"""

# Import the modules
import requests
import json
from datetime import datetime

#####

# This is your data. Customize as necessary. (See above.)

API_KEY = 'xxxxxxxxxxxxx'  
API_TOKEN = 'xxxxxxxxxxxxx'
FEEDS = [{'name': 'feed1', 'alias': 'Feed 1', 'color': 'red'}, 
	{'name': 'feed2', 'alias': 'Feed 2', 'color': 'green'},
	{'name': 'feed3', 'alias': 'Feed 3', 'color': 'blue'}]
	
GRAPH_TITLE = "FeedPress Subscribers"

HISTORY_LENGTH = 10
DATE_FORMAT = "%m-%d"

FILE_PATH = "/path/to/feedpress_subscribers_panel.json"

#####


feedpress_api_url = "http://api.feedpress.it"
subscibers_path = "/feeds/subscribers.json"
account_path = "/account.json"

subscribers_uri = feedpress_api_url + subscibers_path + "?key=" + API_KEY + "&token=" + API_TOKEN
account_uri = feedpress_api_url + account_path + "?key=" + API_KEY + "&token=" + API_TOKEN

feeds_dict = {}

for feed in FEEDS:
	r = requests.get(subscribers_uri + "&feed=" + feed['name'])
	r.text
	
	# Convert it to a Python dictionary	
	data = json.loads(r.text)
	feeds_dict[feed['name']] = data
	
	
# Set up the big dictionary
graph = {}
graph['title'] = GRAPH_TITLE
graph['datasequences'] = []

for feed in FEEDS:
	feed_stats = {'title': feed['alias'], 'color': feed['color']}
	datapoints = []
	
	# Grab the last HISTORY_LENGTH days' worth of of stats.
	if feeds_dict[feed['name']]['stats'] > HISTORY_LENGTH:
		days = sorted(feeds_dict[feed['name']]['stats'][:HISTORY_LENGTH], key = lambda k: k['day'])
	else:
		days = sorted(feeds_dict[feed['name']]['stats'], key = lambda k: k['day'])
		
	for day in days:
		human_date = datetime.fromtimestamp(day['day']).strftime(DATE_FORMAT)
		day_stat = {'title': human_date, 'value': day['greader']}
		datapoints.append(day_stat)
		
	feed_stats['datapoints'] = datapoints
	graph['datasequences'].append(feed_stats)
	

# Writing the file
graph_json = {"graph": graph}
table_file = open(FILE_PATH, 'w')
table_file.write(json.dumps(graph_json))