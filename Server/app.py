from distutils.log import debug
import sys
import sqlite3
from flask import Flask, redirect, url_for, request

app = Flask(__name__)

@app.route('/')
def hello_world():
    # Sample output to log errors if any
    print('This is error output', file=sys.stderr)
    print('This is standard output', file=sys.stdout)
    return 'Hello, World!'


@app.route('/webhook', methods = ['POST'])
def webhook():
    # Get response from DialogFlow
    req = request.get_json()
    print(dict(req)['queryResult']['queryText'], flush=True)

    # Create a connection to DB and dump the query
    con, cur = connect_db()
    execute_queries_db("INSERT INTO qna VALUES ('" + dict(req)['queryResult']['queryText'] + "','')", cur, True, con)
    con.close()

    # Return sample response to the user
    responseText = "I don't have that response in my database. Let me forward that query to a senior engineer and get back to you! Thank you for your patience - Webhook"
    res = {"fulfillmentMessages": [{"text": {"text": [responseText]}}]}
    return res


@app.route('/qna')
def qna():
    pass


def execute_queries_db(query, cur, commit=False, con=""):
    # Execute Queries - Insert, Update, Delete
    cur.execute(query)
    if commit:
        con.commit()


def connect_db():
    # Create a connection to SQLite DB
    con = sqlite3.connect('qna_database.db')
    cur = con.cursor()
    return (con, cur)


@app.route('/create_database')
def create_database():
    # Create Database and tables
    con, cur = connect_db()
    execute_queries_db("DROP TABLE qna", cur, True, con)
    execute_queries_db("CREATE TABLE qna (questions text, answers text)", cur, True, con)
    execute_queries_db("INSERT INTO qna VALUES ('sample-question','sample-answer')", cur, True, con)
    con.close()
    return "Database created sucessfully"


if __name__ == "__main__":
    # Set this to false when deployed to production
    app.run(debug=True)
