from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, render_template
import sqlite3
import sys
import boto3
import pymysql
import mysql.connector
import os

# create a Flask application object and set the URI for the database to use
app = Flask(__name__)
app.config["SQLALCEHMY_DATABASE_URI"] = "sqlite:///example.sqlite3"
ENDPOINT="grresq.cb6zirx4c6kd.us-east-2.rds.amazonaws.com"
PORT="3306"
USR=""
REGION="us-east-2a"
DBNAME="grresq"
os.environ['LIBMYSQL_ENABLE_CLEARTEXT_PLUGIN'] = '1'

#gets the credentials from .aws/credentials
session = boto3.Session(profile_name='default')
client = session.client('rds')

token = client.generate_db_auth_token(DBHostname=ENDPOINT, Port=PORT, DBUsername=USR, Region=REGION)

try:
    conn =  mysql.connector.connect(host=ENDPOINT, user=USR, passwd=token, port=PORT, database=DBNAME)
    cur = conn.cursor()
    #cur.execute("""SELECT now()""")
    #query_results = cur.fetchall()
    #print(query_results)
except Exception as e:
    print("Database connection failed due to {}".format(e))   
# creating a database with dummy data
db = SQLAlchemy(app)


@app.route('/')
def hello():
    return 'Hello World'
    
if __name__ == '__main__':
    app.run()