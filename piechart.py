#go to the reg table, get rids where tmem has sid

#then go to event table and fetch type based on the rid

#make a dict with type:count

from flask import Flask, request
from flask_cors import CORS, cross_origin
from flask_restful import Resource, Api
from json import dumps
from flask_jsonpify import jsonify
import sqlite3
from sqlite3 import Error
import datetime


app = Flask(__name__)
api = Api(app)

CORS(app)

def create_connection(db_file):
  conn = None
  conn = sqlite3.connect(db_file)
  return conn

def create_table(conn, create_table_sql):
  try:
      c = conn.cursor()
      c.execute(create_table_sql)
      conn.commit()
  except Error as e:
      print(e)

@app.route("/student/pie",methods=["POST"])
def pie():
    s_id =request.get_json()["student_id"]
    database = r"pythonsqlite.db"
    conn = create_connection(database)
    cur = conn.cursor()
    q1="select hobby from hobbies where student_id=" + s_id + ";"
    hobbies=cur.execute(q1)
    hobb=[h[0] for h in list(hobbies)]

    q2="Select e_type,count(*) from event group by e_type;"
    ecount=cur.execute(q2)
    d={}
    for row in ecount:
        d[row[0].lower()]=row[1] # e_type : count
    dnew={}
    l=[]
    for h in hobb:
        if h.lower() in d:
            l.append({ "name":h,"y":d[h.lower()] })
            #dnew[h]=d[h.lower()]
    return jsonify(l),200

if __name__ == "__main__":
  app.debug = True
  app.run()
