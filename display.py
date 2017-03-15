from flask import Flask, render_template, request, g, redirect, url_for,session,jsonify,request, redirect
import os
import subprocess
import sqlite3


app = Flask(__name__)

@app.route('/pushdata')
def pushData():
    cmd = ['python', 'tweetering.py']
    subprocess.Popen(cmd).wait()
    conn = sqlite3.connect('/Users/ruchapitke/Desktop/web/web.db')
    cur = conn.cursor()
    cursor = conn.execute('SELECT * FROM TWITTER')
    rows = cursor.fetchall()
    return render_template('tweet.html',rows=rows)

@app.route('/')
def startingRoute():
   return render_template('index.html')

if __name__ == '__main__':
  app.run()    
