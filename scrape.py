import logging, sys, os, codecs

import requests, cache
from bs4 import BeautifulSoup

BASE_URL = "http://lyrics123.net/"  # needed to reconstruct relative URLs

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

arg_count = len(sys.argv)
if arg_count is 1:
    logger.error("Please provide an artist URL to scrape (from lyrics123.net)")
    sys.exit()

url = sys.argv[1]
artist = url.split("/")[3]
logger.info("Scraping lyrics from %s" % url)
logger.info("\tartist = %s" % artist)

# first grab the index page
if not cache.contains(url):
    artist_page = requests.get(url)
    logger.debug("\tadded to cache from %s" % url)
    cache.put(url, artist_page.text)
content = cache.get(url)

# now pull out all the links to songs
dom = BeautifulSoup(content)
link_tags = dom.select("#b a")
link_tags = link_tags[1:len(link_tags)-1] # remove artist link and browse link
logger.debug("\tfound %d link tags" % len(link_tags))
links = set([ tag['href'] for tag in link_tags ])   # get all the unique urls
logger.info("\tfound %d links to songs" % len(links))

# now scrape lyrics from each songs
line_count = 0
lyrics_file = codecs.open(artist+"-lyrics.txt", 'w', 'utf-8')
for relative_song_url in links:
    song_url = BASE_URL + relative_song_url
    if not cache.contains(song_url):
        song_page = requests.get(song_url)
        logger.debug("\tadded to cache from %s" % song_url)
        cache.put(song_url,song_page.text)
    logging.info("  working on %s"%song_url)
    content = cache.get(song_url)
    dom = BeautifulSoup(content)
    lyrics_text_list = dom.select("#b p:nth-of-type(2)")[0].findAll(text=True)
    for line in lyrics_text_list:
        lyrics_file.write(line+os.linesep)
        line_count = line_count + 1

logger.info("Done (scraped %d lines)!",line_count)
