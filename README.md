Lyrics123.net Scraper
=====================

This is a very simple web scraper to combine all the lyrics for an artist's songs into one file.  Content is pulled from http://lyrics123.net

Installation
------------

```
pip install -r requirements.pip
```

Using
-----

Just pass in an artist url and it will visit each song page, grabbing lyrics as it goes.  This script will create an output `.txt` file with all the combined lyrics in it.

For example, this would scrape all the Beatles lyrics into one file
```
python scrape.py http://lyrics123.net/beatles/
```
