from distutils.log import debug
import sys
import sqlite3
from flask import Flask, redirect, url_for, request

app = Flask(__name__)

@app.route('/')
def hello_world():
    print('This is error output', file=sys.stderr)
    print('This is standard output', file=sys.stdout)
    return 'Hello, World!'

@app.route('/webhook', methods = ['POST'])
def webhook():
    req = request.get_json()
    responseText = "There are no fulfillment responses defined for Intent"
    print(dict(req)['queryResult']['queryText'], flush=True)
    res = {"fulfillmentMessages": [{"text": {"text": [responseText]}}]}
    return res

@app.route('/create_database')
def create_database():
    con = sqlite3.connect('qna_database.db')
    cur = con.cursor()
    cur.execute("DROP TABLE qna")
    cur.execute('''CREATE TABLE qna
               (questions text, answers text)''')
    cur.execute("INSERT INTO qna VALUES ('sample-question','sample-answer')")
    con.commit()
    res = ""
    for row in cur.execute('SELECT * FROM qna'):
        res += str(row) + "\n"
        print(row, flush=True)
    return res


if __name__ == "__main__":
    app.run(debug=True)