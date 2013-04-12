#!/usr/bin/python

import datetime
import feedparser
import getopt
import os
import PyRSS2Gen
import sys

def create_latest_uploads_feed(targetPath, feedTitle, feedUrl, feedDescription, entries):
  rssItems = []
  for entry in entries:
    rssItem = PyRSS2Gen.RSSItem(
        title = entry['title'],
        link = entry['link'],
        description = entry['description'],
        guid = PyRSS2Gen.Guid(entry['link']),
        pubDate = entry['pubDate'],
        author = entry['author']
        )
    rssItems.append(rssItem)
  rss = PyRSS2Gen.RSS2(
      title = feedTitle,
      link = feedUrl,
      description = feedDescription,
      lastBuildDate = datetime.datetime.now(),
      items = rssItems)
  print 'Writing RSS feed: ' + targetPath
  rss.write_xml(open(targetPath, 'w'))
  print 'Done!'


def fetch_feed_and_create_rss(userId, targetPath):
  feedUrl = "http://www.istockphoto.com/istock_myfiles_rss.php?ID=" + userId
  print 'Fetching feed: ' + feedUrl
  feed = feedparser.parse(feedUrl)
  feedTitle = feed['feed']['title']
  feedDescription = ""
  entries = feed['entries']
  preparedEntries = []
  print 'Processing fetched entries. Entries found: ' + str(len(entries))
  for entry in entries:
    entryPubDate = entry['published']
    pubDate = datetime.datetime.strptime(entryPubDate[:-6], '%Y-%m-%dT%H:%M:%S')
    #pubDateClean = pubDate.strftime('%d.%m.%Y')
    author = entry['author']
    entryTitle = entry['title']
    print ' * Entry title: ' + entryTitle.encode('utf-8')
    link = entry['link']
    summaryHtml = entry['summary']
    preparedEntries.append({"pubDate":pubDate,"author":author,"title":entryTitle,
      "description":summaryHtml,"link":link})
  create_latest_uploads_feed(targetPath, feedTitle, feedUrl, feedDescription,
      preparedEntries)

def main(argv):
  scriptName = os.path.basename(__file__)
  usageInfo = 'usage: ' + scriptName + ' -i <userid> -t <targetpath>'
  userId = ''
  targetPath = ''
  try:
    opts, args = getopt.getopt(argv,"hi:t:",["id=","targetpath="])
  except getopt.GetoptError:
    print usageInfo
    sys.exit(2)
  for opt, arg in opts:
    if opt == '-h':
      print usageInfo
      sys.exit()
    elif opt in ("-i", "--id"):
      userId = arg
    elif opt in ("-t", "--targetpath"):
      targetPath = arg
  if (userId and targetPath):
    print 'User ID is: ' + userId
    print 'Target path is: ' + targetPath
    fetch_feed_and_create_rss(userId, targetPath)
  else:
    print usageInfo
    sys.exit()


if __name__ == "__main__":
  main(sys.argv[1:])
