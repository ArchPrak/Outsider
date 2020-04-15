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


@app.route("/student/regchk",methods=["POST"])
def checkreg():

    # checking if team size is within limit
    team =request.get_json()["team"]
    sid=request.get_json()["student_id"]
    eid=request.get_json()["e_id"]
    team=eval(team)
    #check if  within team size
    database = r"pythonsqlite.db"
    conn = create_connection(database)
    cur = conn.cursor()
    q="select e_tsize from event where e_id=" + str(eid) + ";"
    res=cur.execute(q)
    res=list(res)
    if len(team)>res[0][0]:
      return jsonify({"message":"Team limit exceeded!"}),200


    #checking if team members are valid
    q="select s_id from students;"
    res=cur.execute(q)
    res=list(res)
    s=set()
    for row in res:
      s.add(row[0])
    final=[]
    for mem in team:
      if mem not in s:
        final.append(str(mem))

    if final:
        if len(final)==1:
            return jsonify({"message":"Invalid team member ID: "+str(final[0])}),200
        elif len(final)>1:
            return jsonify({"message":"Invalid team member IDs: "+ ",".join(final)}),200


    #checking if already registered
    team.append(sid)
    q="select r_id, student_id from registration where e_id=" + str(eid) + ";"
    res=cur.execute(q)
    res=list(res)
    if (len(res)==0):
      return jsonify([]),200
    ridlist=[]
    sidlist=[]
    for row in res:
      ridlist.append(str(row[0]))
      sidlist.append(row[1])
    q="select members from rteam where r_id in ( " + ",".join(ridlist) +");"
    res=cur.execute(q)
    res=list(res)
    for row in res:
      l=eval(row[0])
      sidlist.extend(l)
    s=set(sidlist) # set of all sids who have registered for this event
    final=[]
    for mem in team:
      if mem in s:
        final.append(str((mem)))

    if final:
      if len(final)==1:
        return jsonify({"message":"Member " +str(final[0])+" has already registered for this event."}),200
      else:
        return jsonify({"message":"Members "+",".join(final)+ " have already registered for this event."}),200

    return jsonify({"message":"successful"}),200

if __name__ == "__main__":
  app.debug = True
  app.run()
