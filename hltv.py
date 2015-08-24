import feedparser
import time
import re
import sqlite3
import praw

r = praw.Reddit("Automatic CSGO news submissiom")
r.login()

def doEverything():
    db = sqlite3.connect("database/database")
    cursor = db.cursor()

    f = feedparser.parse("http://www.hltv.org/news.rss.php")

    urls = f['entries'][0].link;
    title = f['entries'][0].title;
    idR = re.search("[0-9]{5}|[0-9]{6}", urls)
    id = idR.group()
    
    print("Found ID: " + id)
    print("Found URL:" + urls)

    cursor.execute("SELECT * FROM news_articles WHERE hltv_id = " + id)
    row = cursor.fetchall()
    numrows = len(row)

    if numrows > 0:
        print("Already exists in the database")
        print("Carrying on...")
    else:
        print("Latest item doesn't exist yet, and it will be added")
        r.submit("GlobalOffensive", "[HLTV] " + title, url = urls)
        cursor.execute("INSERT INTO news_articles (hltv_id) VALUES ("+id+")")
        db.commit()
        
    db.close()

while True:
    print("Checking again...")
    doEverything()    
    time.sleep(3)
    print("-------------------")