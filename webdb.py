import csv
import sqlite3

conn = sqlite3.connect('web.db')
cur = conn.cursor()

cur.execute("DROP TABLE IF EXISTS USER")
cur.execute("CREATE TABLE TWITTER( HEADLINE TEXT, USER_NAME TEXT , FOLLOWER_COUNT TEXT, TWEET_TEXT TEXT, RETWEET_COUNT TEXT, STATUS BOOLEAN)")

conn.commit()
conn.close()