from flask import Flask, request, send_file, make_response
from flask_cors import CORS, cross_origin
from flask_restful import Resource, Api
from json import dumps
import json
from flask_jsonpify import jsonify
import sqlite3
from sqlite3 import Error
import requests
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

@app.route('/student/searchevents',methods=["POST"])
def getEid():
  name = request.get_json()["name"]
  print(name)
  database = r"pythonsqlite.db"
  conn = create_connection(database)
  c = conn.cursor()
  q = "SELECT e_id,o_id FROM event WHERE e_name = '" + str(name) + "';"
  print(q)
  c.execute(q)
  res = c.fetchall()
  res = list(res)
  print(res)
  return jsonify(res)

@app.route("/student/fetchhobbies", methods=["POST"])
def ghob():
  s_id=request.get_json()['student_id']
  database = r"pythonsqlite.db"
  conn = create_connection(database)
  q="select hobby from hobbies where s_id=" + str(s_id) + ";"
  cur = conn.cursor()
  res=cur.execute(q)
  res=list(res)
  print (res)
  final=set()
  for row in res:
    final.add(row[0])
  final=list(final)

  return jsonify(final),200

@app.route('/student/hobby',methods=["POST"])
def hobby():
  s_id = request.get_json()["s_id"]
  print(s_id)
  interests = request.get_json()["hobby"]
  database = r"pythonsqlite.db"
  conn = create_connection(database)
  c = conn.cursor()
  query="select hobby from hobbies where s_id=" + str(s_id) + ";"
  res=c.execute(query)
  res=list(res)
  prev=[]
  for row in res:
    prev.append(row[0])
  tobeadded=[]
  for ele in interests:
    if str(ele) not in prev:
      tobeadded.append(str(ele))

  for ele in tobeadded:
    q = "INSERT INTO hobbies(s_id,hobby) VALUES (" + str(s_id) + ", '" + str(ele) + "');"
    print(q)
    c.execute(q)
    conn.commit()
  return jsonify({'message':'Added'})


@app.route("/")
def hello():
    return jsonify({'text':'Hello World!'})


@app.route("/checkuser", methods=["POST"])
def check():
  email = request.get_json()["email"]
  password = request.get_json()["password"]
  table_name = request.get_json()["account_type"]
  if(table_name == "organiser"):
    query = "SELECT * FROM organisers WHERE email = '" + email + "' AND password  = '" + password + "';"
  else:
    query = "SELECT * FROM students WHERE email = '" + email + "' AND password  = '" + password + "';"
  database = r"pythonsqlite.db"
  conn = create_connection(database)
  c = conn.cursor()
  c.execute(query)
  rows = c.fetchall()
  if(len(rows) == 1 and table_name == "organiser"):
    return {'first_name': rows[0][1], 'email': email, 'o_id': rows[0][0]}
  elif(len(rows) == 1 and table_name == "student"):
    return {'first_name': rows[0][1], 'email': email, 's_id': rows[0][0]}
  else:
    return {'message':'Invalid credentials'}

@app.route("/newuser", methods=["POST"])
def new_user():
  print(request.get_json())
  first_name = request.get_json()["first_name"]
  last_name = request.get_json()["last_name"]
  email = request.get_json()["email"]
  password = request.get_json()["password"]
  phone_no = request.get_json()["phone_no"]
  query = "SELECT * FROM students WHERE email = '" + email + "';"
  print(query)
  database = r"pythonsqlite.db"
  conn = create_connection(database)
  c = conn.cursor()
  c.execute(query)
  rows = c.fetchall()
  print(rows)
  print(len(rows))
  d = dict()
  if(len(rows) != 0):
    d["result"] = "failed"
  else:
    query = "INSERT INTO students(first_name, last_name, email, password, phone_no) VALUES('" + first_name + "', '" + last_name + "', '" + email + "','" + password + "'," + str(phone_no) + ");"
    c = conn.cursor()
    c.execute(query)
    d["result"] = "successful"
    conn.commit()
  return jsonify(d)

@app.route("/newevent", methods=["POST"])
def new_event():
    event_name = request.get_json()["event_name"]
    event_type = request.get_json()["event_type"]
    max_par = request.get_json()["max_par"]
    fee = request.get_json()["fee"]
    max_teams = request.get_json()["max_teams"]
    venue = request.get_json()["event_venue"]
    event_date = request.get_json()["event_date"]
    o_id = request.get_json()['o_id']
    funds = request.get_json()['funds']
    database = r"pythonsqlite.db"
    conn = create_connection(database)
    c = conn.cursor()
    #change the value of o_id
    query = " INSERT INTO event(o_id, funds, e_name, e_type, e_date, e_venue, e_fee, e_tsize, e_maxpar) VALUES(" + str(o_id) + "," + str(funds) + ",'" + event_name + "','" + event_type + "','" + event_date + "','" + venue + "'," + str(fee) + "," + str(max_par) + "," + str(max_teams) + ");"
    c.execute(query)
    conn.commit()
    return jsonify({"done":"done"})

@app.route("/listevents", methods=["POST"])
def all_events():
  try:
    o_id = request.get_json()["o_id"]
    database = r"pythonsqlite.db"
    conn = create_connection(database)
    c = conn.cursor()
    query = " SELECT * FROM event WHERE o_id = " + str(o_id) + ";"
    c.execute(query)
    rows = c.fetchall()
    return jsonify(rows)
  except:
    return

@app.route('/allocatefunds', methods=["POST"])
def allocate_funds():
  o_id = request.get_json()["o_id"]
  e_id = request.get_json()["e_id"]
  amount = request.get_json()["amount"]
  reason = request.get_json()["reason"]
  database = r"pythonsqlite.db"
  conn = create_connection(database)
  c = conn.cursor()
  query = "SELECT * FROM event WHERE e_id = " + str(e_id) + ";"
  c.execute(query)
  rows = c.fetchall()
  total_amount = rows[0][1]
  query = "SELECT * FROM funds where e_id = " + str(e_id) + ";"
  c.execute(query)
  rows = c.fetchall()
  already_spent = 0
  for row in rows:
    already_spent += row[2]
  if(total_amount - already_spent >= int(amount)):
    query = "INSERT INTO funds(e_id, amount, reason) VALUES(" + str(e_id) + ", " + str(amount) + ", '" + reason + "');"
    c.execute(query)
    conn.commit()
    return jsonify({"message": "successful"})
  else:
    return jsonify({"message": "funds insufficient"})

@app.route('/fund_rem', methods=["POST"])
def fund_rem():
  e_id = request.get_json()["e_id"]
  database = r"pythonsqlite.db"
  conn = create_connection(database)
  c = conn.cursor()
  query = "SELECT * FROM event WHERE e_id = " + str(e_id) + ";"
  c.execute(query)
  rows = c.fetchone()
  funds_given = rows[1]
  query = "SELECT * FROM funds WHERE e_id = " + str(e_id) + ";"
  c.execute(query)
  rows = c.fetchall()
  spent = 0
  for row in rows:
    spent += row[2]
  send_back = {"rem_funds": funds_given - spent}
  return jsonify(send_back)

@app.route('/event_log', methods=["POST"])
def event_log():
  e_id = request.get_json()["e_id"]
  database = r"pythonsqlite.db"
  conn = create_connection(database)
  c = conn.cursor()
  query = "SELECT * FROM funds WHERE e_id = " + str(e_id) + ";"
  c.execute(query)
  rows = c.fetchall()
  if(rows):
    return jsonify({"data": rows})
  else:
    return jsonify({})

@app.route('/totalprofit', methods=["POST"])
def total_profit():
  o_id = request.get_json()["o_id"]
  database = r"pythonsqlite.db"
  conn = create_connection(database)
  c = conn.cursor()
  query = "SELECT * FROM event WHERE o_id = " + str(o_id) + ";"
  c.execute(query)
  rows = c.fetchall()
  total_profit_made = []
  rows.sort(key = lambda x : x[5])
  print(rows)
  objects = []
  for row in rows:
    req = requests.post("http://127.0.0.1:5000/eventprofit", json = {"e_id":row[0]}).json()
    profit = req["profit"]
    objects.append({"label":row[2], "y":profit})
  return jsonify(objects)

@app.route('/eventprofit', methods=["POST"])
def event_profit():
  e_id = request.get_json()["e_id"]
  database = r"pythonsqlite.db"
  conn = create_connection(database)
  c = conn.cursor()
  query = "SELECT * FROM event WHERE e_id = " + str(e_id) + ";"
  c.execute(query)
  rows = c.fetchall()
  cost_per_reg = rows[0][7]
  query = "SELECT * FROM registration WHERE e_id = " + str(e_id) + ";"
  c.execute(query)
  rows = c.fetchall()
  total_from_reg = cost_per_reg * len(rows)
  req = requests.post("http://127.0.0.1:5000/fund_rem", json = {"e_id":e_id}).json()
  total = total_from_reg + req["rem_funds"]
  return jsonify({"profit": total})

@app.route('/allocateprize', methods=["POST"])
def give_prize():
  r_id = request.get_json()["r_id"]
  prize = request.get_json()["prize"]
  e_id = request.get_json()["e_id"]
  database = r"pythonsqlite.db"
  conn = create_connection(database)
  c = conn.cursor()
  query = "SELECT * FROM registration WHERE r_id = " + str(r_id) + " AND e_id = " + str(e_id) + ";"
  c.execute(query)
  rows = c.fetchall()
  if(len(rows) != 0):
    query = "UPDATE registration SET prize = '" + prize + "' WHERE r_id = " + str(r_id) + ";"
    c.execute(query)
    conn.commit()
    return jsonify({"message":"successful"})
  else:
    return jsonify({"message":"unsuccessful"})

@app.route('/event_comp', methods=["POST"])
def event_complete():
  e_id = request.get_json()["e_id"]
  database = r"pythonsqlite.db"
  conn = create_connection(database)
  c = conn.cursor()
  query = "SELECT * FROM registration WHERE e_id = " + str(e_id) + ";"
  c.execute(query)
  rows = c.fetchall()
  if(len(rows) != 0):
    for row in rows:
      if(row[3] == '-'):
        query = "UPDATE registration SET prize = 'No Prize' WHERE r_id = " + str(row[0]) + ";"
        c.execute(query)
        conn.commit()
  return jsonify({})

@app.route('/show_reg', methods=['POST'])
def show_reg():
  e_id = request.get_json()["e_id"]
  database = r"pythonsqlite.db"
  conn = create_connection(database)
  c = conn.cursor()
  query = "SELECT * FROM registration WHERE e_id = " + str(e_id) + ";"
  c.execute(query)
  rows = c.fetchall()
  d = []

  r_id = []
  s_id = []
  person_registered = []
  team_mate_names = []
  prize = []
  i = 0
  if(rows):
    for row in rows:
      r_id.append(row[0])
      s_id.append(row[2])
      prize.append(row[3])
      query = "SELECT * FROM students WHERE s_id=" + str(row[2]) + ";"
      c.execute(query)
      row_x = c.fetchone()
      person_registered.append(row_x[1])
      query = "SELECT * FROM rteam WHERE id=" + str(row[0]) +";"
      c.execute(query)
      rows1 = c.fetchone()
      team_mate_names.append([])
      if(rows1):
        team_mate_id = eval(rows1[1])
        for id in team_mate_id:
          query = "SELECT * FROM students WHERE s_id=" + str(id) + ";"
          c.execute(query)
          row2 = c.fetchone()
          team_mate_names[i].append(str(row2[1]))
        i = i + 1
  for x in range(len(s_id)):
    d.append({"r_id": r_id[x], "s_id": s_id[x], "s_name": person_registered[x], "team_mates": team_mate_names[x], "prize": prize[x]})
  print(d)
  return jsonify({"data": d})

@app.route('/no_of_reg', methods=['POST'])
def showw_reg():
  o_id = request.get_json()["o_id"]
  database = r"pythonsqlite.db"
  conn = create_connection(database)
  c = conn.cursor()
  query = "SELECT * FROM event WHERE o_id = " + str(o_id) + ";"
  event_name = []
  no_of_reg = []
  c.execute(query)
  rows = c.fetchall()
  if(rows):
    rows.sort(key = lambda x : x[5])
    for row in rows:
      event_name.append(row[2])
      query = "SELECT * FROM registration WHERE e_id = " + str(row[0]) + ";"
      c.execute(query)
      rows = c.fetchall()
      no_of_reg.append(len(rows))
  objects = []
  if(len(event_name) != 0):
    for x in range(len(event_name)):
      objects.append({"label": event_name[x], "y": no_of_reg[x]})
  return jsonify(objects)

@app.route("/student/info",methods=["POST"])
def info():
    sid=request.get_json()["student_id"]
    database = r"pythonsqlite.db"
    conn = create_connection(database)
    cur = conn.cursor()

    res=cur.execute("SELECT * from students where s_id=" + str(sid)+";")
    res=list(res)
    return jsonify(res),200

@app.route("/student/regchk",methods=["POST"])
def checkreg():

    # checking if team size is within limit
    team =request.get_json()["team"]
    sid=request.get_json()["student_id"]
    eid=request.get_json()["e_id"]
    team=eval(team)
    print("Received data")
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
    q="select r_id, s_id from registration where e_id=" + str(eid) + ";"
    res=cur.execute(q)
    res=list(res)
    if (len(res)==0):
      return jsonify({"message":"successful"}),200
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
'''
@app.route("/student/checksize",methods=["POST"])
def checksize():
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
      return jsonify(["Team limit exceeded!"]),200
    return jsonify([]),200
'''

def checkmem(sid,eid):
    database = r"pythonsqlite.db"
    conn = create_connection(database)
    cur = conn.cursor()

    q="select r_id, s_id from registration where e_id=" + str(eid) + ";"
    res=cur.execute(q)
    res=list(res)
    if (len(res)==0):
      return False
    ridlist=[]
    sidlist=[]
    for row in res:
      ridlist.append(str(row[0]))
      sidlist.append(row[1])
    q="select members from rteam where id in ( " + ",".join(ridlist) +");"
    res=cur.execute(q)
    res=list(res)
    for row in res:
      l=eval(row[0])
      sidlist.extend(l)
    s=set(sidlist) # set of all sids who have registered for this event
    if sid in s:
      return True
    return False

'''
@app.route("/student/checkteam",methods=["POST"])
def checkteam():
    team =request.get_json()["team"]
    team=eval(team)
    database = r"pythonsqlite.db"
    conn = create_connection(database)
    cur = conn.cursor()
    q="select s_id from students;"
    res=cur.execute(q)
    res=list(res)
    s=set()
    for row in res:
      s.add(row[0])
    final=[]
    for mem in team:
      if mem not in s:
        final.append(mem)
    return jsonify(final),200
'''

@app.route("/student/eventdet",methods=["POST"])
def eventdet():
    #s_id =request.get_json()["student_id"]
    #o_id =request.get_json()["o_id"]
    e_id =request.get_json()["e_id"]

    database = r"pythonsqlite.db"
    conn = create_connection(database)
    cur = conn.cursor()
    q="Select * from event where e_id="+str(e_id)+";"
    res=cur.execute(q)
    res=list(res)
    return jsonify(res),200

@app.route("/student/orgdet",methods=["POST"])
def orgdet():
    #s_id =request.get_json()["student_id"]
    o_id =request.get_json()["o_id"]
    #e_id =request.get_json()["e_id"]

    database = r"pythonsqlite.db"
    conn = create_connection(database)
    cur = conn.cursor()
    q="Select * from organisers where o_id="+str(o_id)+";"
    res=cur.execute(q)
    res=list(res)
    print(res)
    return jsonify(res),200

@app.route("/student/dispevents",methods=["GET"])
def listall():
  database = r"pythonsqlite.db"
  conn = create_connection(database)
  cur = conn.cursor()
  q1="Select e_id, e_maxpar from EVENT;"
  res1=cur.execute(q1)
  res1=list(res1)
  dmax={}
  final=[]
  for row in res1:
    dmax[row[0]]=row[1] # eid : maxpar

  q2="select e_id, count(*) from registration group by e_id;"
  res2=cur.execute(q2)
  res2=list(res2)
  s=set()
  for row in res2:
    s.add(row[0])
  #print("RRRR",res)
  final=[]
  for row in res2:
    if row[1] < dmax[row[0]]:
      final.append(str(row[0]))


  for row in res1:
    if row[0] not in s and dmax[row[0]]!=0:
      final.append(str(row[0]))

  print("#########",final)

  q3="select * from event where e_id in ("+ ",".join(final) + ");"
  print(q3)
  res=cur.execute(q3)
  res=list(res)
  #if len(res)==0:
  #  return jsonify(["All events are full currently :/ Come back soon!"]),200
  return jsonify(res),200


@app.route("/student/pie1",methods=["POST"])
def pie1():
    s_id =request.get_json()["student_id"]
    database = r"pythonsqlite.db"
    conn = create_connection(database)
    cur = conn.cursor()
    q1="select hobby from hobbies where s_id=" + str(s_id) + ";"
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
            l.append({"name":h, "y":d[h.lower()]})
            #dnew[h]=d[h.lower()]
    #s=[{"name" :"sing", "y":2}]
    return jsonify(l),200
@app.route("/student/pie2",methods=["GET"])
def pie2():

    database = r"pythonsqlite.db"
    conn = create_connection(database)
    cur = conn.cursor()
    query1=" select e_id ,count(*) tot from registration group by e_id order by tot desc;"
    res1=cur.execute(query1)
    res1=list(res1)
    res1=res1[:5]
    print(res1)

    query2="SELECT e_id,e_name FROM EVENT;"
    res2=cur.execute(query2)
    res2=list(res2)
    devents={}
    for row in res2:
        devents[row[0]]=row[1] # {eid:ename}

    d={}
    for row in res1:
      eid=row[0]
      ename=devents[eid]
      print( ename, row[1])
      d[ename]=row[1] # e_name : count
    print(d)
    l=[]
    for ev in d:
      l.append({"name":ev,"y":d[ev]})
    return jsonify(l),200





def get_vector(s_id, no_of_events):
  current_s_id = [0] * no_of_events
  database = r"pythonsqlite.db"
  conn = create_connection(database)
  c = conn.cursor()
  for x in range(1, no_of_events + 1):
    #check if that student has registered for the event
    query = "SELECT * from registration where s_id = " + str(s_id) + " and e_id = " + str(x) + ";"
    c.execute(query)
    rows = c.fetchall()
    if(len(rows) != 0):
      current_s_id[x - 1] = 1
    #check if the student is a part of a team which has registered for the event
    else:
      query = "SELECT * from registration where e_id = " + str(x) + ";"
      c.execute(query)
      rows = c.fetchall()
      for y in range(len(rows)):
        query1 = "SELECT * from rteam where id = " + str(rows[y][0]) + ";"
        print(query1)
        c.execute(query1)
        rows1 = c.fetchone()
        if(rows1):
          lst = eval(rows1[1])
          if(s_id in lst):
            current_s_id[x - 1] = 1
            break
  return current_s_id

# get this value!

@app.route("/student/team",methods=["POST"])
def get_tmem():
  s_id =request.get_json()["student_id"]
  database = r"pythonsqlite.db"
  conn = create_connection(database)
  c = conn.cursor()
  query = "SELECT MAX(e_id) FROM event;"
  c.execute(query)
  value = c.fetchall()
  no_of_events = value[0][0]
  curr_student_vector = get_vector(s_id, no_of_events)

  query = "SELECT * FROM students WHERE s_id != " + str(s_id) + ";"
  c.execute(query)
  rows = c.fetchall()
  student_ids = []
  student_info = []
  all_vectors = []
  values_of_cosine = []
  if(rows):
    for row in rows:
      student_ids.append(row[0])
      student_info.append(list(row))
      all_vectors.append(get_vector(row[0], no_of_events))
  for x in range(len(student_ids)):
    new_arr = [curr_student_vector[i] * all_vectors[x][i] for i in range(no_of_events)]
    values_of_cosine.append(sum(new_arr))
  values_of_cosine, student_info = (list(t) for t in zip(*sorted(zip(values_of_cosine, student_info))))
  student_info.reverse()
  print(student_info)
  return (jsonify(student_info))

@app.route("/student/events",methods=["GET"])
def all_event():

    database = r"pythonsqlite.db"
    con=sqlite3.connect(database)
    cur=con.cursor()
    #req=request.get_json()
    q="SELECT e_name from event;"
    cur.execute(q)
    res=cur.fetchall()

    print(res)
    return jsonify(res),200
@app.route("/student/getevents",methods=["GET"])
def s_event():
    database = r"pythonsqlite.db"
    con=sqlite3.connect(database)
    cur=con.cursor()
    #req=request.get_json()
    q="SELECT e_name from event;"
    cur.execute(q)
    res=cur.fetchall()
    res = list(res)
    fa = []
    for i in range(len(res)):
      fa.append(res[i][0])
    print(fa)
    return jsonify(fa),200


@app.route("/student/prizes",methods=["POST"])
def display_prizes():


    database = r"pythonsqlite.db"
    con=sqlite3.connect(database)
    cur=con.cursor()
    req=request.get_json()

    student_id=req['student_id']

    query1="SELECT id,members from rteam;"
    res=cur.execute(query1)
    res=list(res)
    res1=[]
    for row in res:
        if int(student_id) in eval(row[1]):
            res1.append(row[0])
    print(res1)


    query2="SELECT r_id,e_id,prize from registration WHERE PRIZE != '-' AND PRIZE != 'No Prize'; "
    res2=cur.execute(query2)
    res2=list(res2)
    d={}
    for row in res2:
        d[row[0]]=(row[1],row[2]) # {r_id: (e_id,prize)}


    query3="SELECT e_id,e_name FROM EVENT;"
    res3=cur.execute(query3)
    res3=list(res3)
    devents={}
    for row in res3:
        devents[row[0]]=row[1] # {eid:ename}

    finalprizes=[]
    for r_id in res1:
        if r_id in d:
            eid=d[r_id][0]
            prize=d[r_id][1]
            ename=devents[eid]

            #sstr=prize + " for event : " + ename
            finalprizes.append((ename,prize))

    #final=" ; ".join(finalprizes)
    return jsonify(finalprizes),200



@app.route("/student/regevent",methods=["POST"])
def reg_event():
    print("Begin")
    database = r"pythonsqlite.db"
    con=sqlite3.connect(database)
    cur=con.cursor()
    req=request.get_json()
    stud_id = req['student_id']

    event_id=req['e_id']

    #event_name=req['event_name']
    team_members=req['team_members']
    print("Inside here")
    #q="SELECT e_id from event where e_name='"+ event_name+ "';"
    #cur.execute(q)
    #res=cur.fetchall()
    #event_id=int(res[0][0])
    #event_id= req['event_id']
    if len(eval(team_members))==0:
      if(checkmem(stud_id,event_id)):
        print("error")
        return jsonify({"status":"already registered"}),200



    query1="INSERT INTO registration(e_id,s_id,prize) VALUES(" +str( event_id ) + "," +"'" +str(stud_id) +"'"+ ", '-' );"
    cur.execute(query1)

    q="select last_insert_rowid();"
    r_id=list(cur.execute(q))[0][0]
    #print(r_id)

    query3="INSERT INTO rteam(id,members) VALUES("+ str(r_id) + "," + "'" + team_members + "'" + ");"
    cur.execute(query3)

    con.commit()
    return jsonify({"status":"Done"}),200


@app.route("/student/events", methods=["POST"])
def display_events():
  database = r"pythonsqlite.db"
  conn = create_connection(database)
  cur= conn.cursor()
  stud_id = request.get_json()['student_id']
  query1="SELECT id,members from rteam;"
  res=cur.execute(query1)
  res=list(res)
  #return jsonify(res),200
  res1=[]
  for row in res:
    if int(stud_id) in eval(row[1]):
      res1.append(row[0])
  qry="select r_id from registration where s_id="+str(stud_id)+";"
  ans=cur.execute(qry)
  ans=list(ans)
  print(ans)
  for row in ans:
    res1.append(row[0])
  query2="SELECT r_id,e_id from registration; "
  res2=cur.execute(query2)
  res2=list(res2)
  d={}
  events=[]
  for row in res2:
    d[row[0]]=row[1] #{r_id: e_id}

  res=[]
  res1=set(res1)
  for r_id in res1:
    e_id=d[r_id]
    q="SELECT * FROM EVENT WHERE e_id=" + str(e_id) + ";"
    cur.execute(q)
    res.append(cur.fetchall()[0])
  past=[]
  upcm=[]
  n=datetime.datetime.now()
  for row in res:
    row=list(map(str,row))
    d=datetime.datetime.strptime(row[5],"%Y-%m-%d")
    if n<=d:
      upcm.append(row)
    else:
      past.append(row)
    final={"past":past,"upcoming": upcm}
  return jsonify(final),200



database = r"pythonsqlite.db"
# write queries for creating tables here
create_students_table = """CREATE TABLE IF NOT EXISTS students (
    s_id INTEGER PRIMARY KEY AUTOINCREMENT, first_name text NOT NULL, last_name text NOT NULL, email text NOT NULL UNIQUE, password text NOT NULL, phone_no int(10) NOT NULL, stream text); """
create_orgainsers_table = """CREATE TABLE IF NOT EXISTS organisers (o_id INTEGER PRIMARY KEY AUTOINCREMENT, first_name text NOT NULL, last_name text NOT NULL, email text NOT NULL UNIQUE, password text NOT NULL, phone_no int(10) NOT NULL); """


create_hobbies_table = """CREATE TABLE IF NOT EXISTS hobbies (id INTEGER PRIMARY KEY AUTOINCREMENT, s_id INTEGER, hobby text, FOREIGN KEY (s_id) REFERENCES students(s_id)) """
#create_hobbies_table = """CREATE TABLE IF NOT EXISTS hobbies (s_id INTEGER, hobby text, FOREIGN KEY (s_id) REFERENCES students(s_id)) """
create_event_table = """ CREATE TABLE IF NOT EXISTS event( e_id INTEGER PRIMARY KEY AUTOINCREMENT, funds INTEGER NOT NULL, e_name VARCHAR(100) NOT NULL, o_id INTEGER NOT NULL, e_type VARCHAR(100) NOT NULL, e_date DATETIME NOT NULL, e_venue VARCHAR(300) NOT NULL, e_fee INTEGER, e_tsize INTEGER, e_maxpar INTEGER, FOREIGN KEY (o_id) REFERENCES organiser(o_id));"""
create_registration_table = """CREATE TABLE IF NOT EXISTS registration (r_id INTEGER PRIMARY KEY AUTOINCREMENT,  e_id INTEGER NOT NULL, s_id INTEGER NOT NULL, prize VARCHAR(100) DEFAULT '-', FOREIGN KEY (s_id) REFERENCES student(s_id), FOREIGN KEY (e_id) REFERENCES event(e_id));"""
create_registrationteam_table = """CREATE TABLE IF NOT EXISTS rteam (id INTEGER PRIMARY KEY, members VARCHAR(200) NOT NULL, FOREIGN KEY (id) REFERENCES registration(r_id));"""
create_funds_table = """CREATE TABLE IF NOT EXISTS funds (id INTEGER PRIMARY KEY AUTOINCREMENT, e_id INTEGER, amount INTEGER, reason TEXT, FOREIGN KEY (e_id) REFERENCES event(e_id));"""
#create_updates_table = """CREATE TABLE IF NOT EXISTS updates (id INTEGER PRIMARY KEY AUTOINCREMENT, o_id INTEGER, r_id INTEGER, FOREIGN KEY (o_id) REFERENCES organisers(id) , FOREIGN KEY (r_id) REFERENCES registration(r_id));"""
#create_create_event_table = """CREATE TABLE IF NOT EXISTS creates (id INTEGER PRIMARY KEY AUTOINCREMENT, o_id INTEGER, e_id INTEGER, FOREIGN KEY (o_id) REFERENCES organisers(o_id), FOREIGN KEY (e_id) REFERENCES event(e_id));"""

conn = create_connection(database)
if conn is not None:
  # execute queries for creating tables here
  create_table(conn, create_students_table)
  create_table(conn, create_orgainsers_table)
  create_table(conn, create_hobbies_table)
  create_table(conn, create_event_table)
  create_table(conn, create_registration_table)
  create_table(conn, create_registrationteam_table)
  create_table(conn, create_funds_table)
  #create_table(conn, create_updates_table)
  #create_table(conn, create_create_event_table)
else:
    print("Error! Cannot create the database connection")

if __name__ == "__main__":
  app.debug = True
  app.run()
