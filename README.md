istock-latest-uploads-feed-fixer
================================

A python script that fixes the invalid default atom feed of istockphoto and converts it to RSS 2.0 format.

## Dependencies
* feedparser
* PyRSS2Gen

## Usage
* Call the script and append a user ID and a target path
* Examples:<br>
  `> python istock_latest_uploads.py -i 8197370 -t feed.xml`<br>
  This will result in fetching the latest uploads feed from istockphoto for the user with the ID 8197370.
  The feed is being parsed and a file 'feed.xml' is being created inside the current directory.
* Enter the follwing command to get a command line help:<br>
  `> python istock_latest_uploads.py -h`

## Creator homepage
[qoo.li](http://qoo.li)
