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
    return jsonify(res),200

@app.route("/student/dispevents",methods=["GET"])
def listall():
  database = r"pythonsqlite.db"
  conn = create_connection(database)
  cur = conn.cursor()
  q1="Select e_id, e_maxpar from EVENT";
  res=cur.execute(q1)
  res=list(res)
  dmax={}
  for row in res:
    dmax[row[0]]=row[1] # eid : maxpar
  q2="select e_id, count(*) from registration group by e_id";
  res=cur.execute(q2)
  res=list(res)
  final=[]
  for row in res:
    if row[1] < dmax[row[0]]:
      final.append(str(row[0]))
  q3="select * from event where e_id in ("+ ",".join(final) + ");"
  res=cur.execute(q3)
  res=list(res)
  #if len(res)==0:
  #  return jsonify(["All events are full currently :/ Come back soon!"]),200
  return jsonify(res),200


@app.route("/student/pie",methods=["POST"])
def pie():
    s_id =request.get_json()["student_id"]
    database = r"pythonsqlite.db"
    conn = create_connection(database)
    cur = conn.cursor()
    q1="select hobby from hobbies where student_id=" + str(s_id) + ";"
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



def get_vector(s_id, no_of_events):
  current_s_id = [0] * no_of_events
  database = r"pythonsqlite.db"
  conn = create_connection(database)
  c = conn.cursor()
  for x in range(1, no_of_events + 1):
    #check if that student has registered for the event
    query = "SELECT * from registration where student_id = " + str(s_id) + " and e_id = " + str(x) + ";"
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
        query1 = "SELECT * from rteam where r_id = " + str(rows[y][0]) + ";"
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
  #print(student_info)
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

@app.route("/student/prizes",methods=["POST"])
def display_prizes():


    database = r"pythonsqlite.db"
    con=sqlite3.connect(database)
    cur=con.cursor()
    req=request.get_json()

    student_id=req['student_id']

    query1="SELECT r_id,members from rteam;"
    res=cur.execute(query1)
    res=list(res)
    res1=[]
    for row in res:
        if int(student_id) in eval(row[1]):
            res1.append(row[0])
    print(res1)


    query2="SELECT r_id,e_id,prize from registration WHERE PRIZE != '-'; "
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
    event_name=req['event_name']
    team_members=req['team_members']
    print("Inside here")
    q="SELECT e_id from event where e_name='"+ event_name+ "';"
    cur.execute(q)
    res=cur.fetchall()
    event_id=int(res[0][0])
    #event_id= req['event_id']

    query1="INSERT INTO registration(e_id,student_id,prize) VALUES(" +str( event_id ) + "," +"'" +str(stud_id) +"'"+ ", '-' );"
    cur.execute(query1)

    q="select last_insert_rowid();"
    r_id=list(cur.execute(q))[0][0]
    #print(r_id)

    query3="INSERT INTO rteam(r_id,members) VALUES("+ str(r_id) + "," + "'" + team_members + "'" + ");"
    cur.execute(query3)

    con.commit()
    return jsonify({"status":"Done"}),200


@app.route("/student/events", methods=["POST"])
def display_events():
  database = r"pythonsqlite.db"
  conn = create_connection(database)
  cur= conn.cursor()
  stud_id = request.get_json()['student_id']
  query1="SELECT r_id,members from rteam;"
  res=cur.execute(query1)
  res=list(res)
  #return jsonify(res),200
  res1=[]
  for row in res:
    if int(stud_id) in eval(row[1]):
      res1.append(row[0])
  query2="SELECT r_id,e_id from registration; "
  res2=cur.execute(query2)
  res2=list(res2)
  d={}
  events=[]
  for row in res2:
    d[row[0]]=row[1] #{r_id: e_id}

  res=[]
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



@app.route("/")
def hello():
    return jsonify({'text':'Hello World!'})

@app.route("/checkuser", methods=["POST"])
def check():
  email = request.get_json()["email"]
  password = request.get_json()["password"]
  table_name = request.get_json()["account_type"]
  print(table_name)
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
  try:
    first_name = request.get_json()["first_name"]
    last_name = request.get_json()["last_name"]
    email = request.get_json()["email"]
    password = request.get_json()["password"]
    phone_no = request.get_json()["phone_no"]
    query = "SELECT * FROM students WHERE email = '" + email + "';"
    database = r"pythonsqlite.db"
    conn = create_connection(database)
    c = conn.cursor()
    c.execute(query)
    rows = c.fetchall()
    d = dict()
    if(len(rows) == 0):
      query = "INSERT INTO students(first_name, last_name, email, password, phone_no) VALUES('" + first_name + "', '" + last_name + "', '" + email + "','" + password + "'," + phone_no + ");"
      print(query)
      c = conn.cursor()
      c.execute(query)
      d["result"] = "successful"
    else:
      d["result"] = "failed"
    conn.commit()
    return jsonify(d)
  except:
    d = dict()
    d["result"] = "failed"
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
    query = " INSERT INTO event(o_id, funds, e_name, o_id, e_type, e_date, e_venue, e_fee, e_tsize, e_maxpar) VALUES(" + str(o_id) + "," + str(funds) + ",'" + event_name + "', 1, '" + event_type + "','" + event_date + "','" + venue + "'," + str(fee) + "," + str(max_par) + "," + str(max_teams) + ");"
    print(query)
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
  if(total_amount - already_spent >= amount):
    query = "INSERT INTO funds(o_id, e_id, amount, reason) VALUES(" + str(o_id) + ", " + str(e_id) + ", " + str(amount) + ", '" + reason + "';"
    conn.commit()
    return jsonify({"message": "successful"})
  else:
    return jsonify({"message": "funds insufficient"})

@app.route('/totalprofit', methods=["POST"])
def total_profit():
  o_id = request.get_json()["o_id"]
  database = r"pythonsqlite.db"
  conn = create_connection(database)
  c = conn.cursor()
  query = "SELECT * FROM event WHERE o_id = " + str(o_id) + ";"
  c.execute(query)
  rows = c.fetchall()
  profit_made = 0
  for row in rows:
    query = "SELECT * FROM registration WHERE e_id = " + str(row[3]) + ";"
    c.execute(query)
    rows1 = c.fetchall()
    profit_made += len(rows1) * row[7] - row[1]
  return jsonify({"profit": profit_made})

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
  amount_spent = rows[0][1]
  query = "SELECT * FROM registration WHERE e_id = " + str(e_id) + ";"
  c.exectue(query)
  rows = c.fetchall()
  total_from_reg = cost_per_reg * len(rows) - amount_spent
  return jsonify({"profit": total_from_reg})

@app.route('/allocateprize', methods=["POST"])
def give_prize():
  r_id = request.get_json()["r_id"]
  prize = request.get_json()["prize"]
  database = r"pythonsqlite.db"
  conn = create_connection(database)
  c = conn.cursor()
  query = "UPDATE TABLE registration SET prize = '" + prize + "' WHERE r_id = " + str(r_id) + ";"
  c.execute(query)
  conn.commit()
  return jsonify({})

@app.route('/student/hobby',methods=["POST"])
def hobby():
	s_id = request.get_json()["student_id"]
	h = request.get_json()["hobby"]
	database = r"pythonsqlite.db"
	conn = create_connection(database)
	c = conn.cursor()
	#q = "SELECT * FROM hobbies WHERE student_id = " + str(student_id) + ";"
	q = "INSERT INTO hobbies(student_id,hobby) VALUES (" + str(s_id) + ", '" + str(h) + "');"
	print(q)
	c.execute(q)
	conn.commit()
	#print(rows)
	#if (len(rows) == 0):
	return jsonify({'message':'Added'})

# write queries for creating tables here
create_students_table = """CREATE TABLE IF NOT EXISTS students (
    s_id INTEGER PRIMARY KEY AUTOINCREMENT, first_name text NOT NULL, last_name text NOT NULL, email text NOT NULL UNIQUE, password text NOT NULL, phone_no int(10) NOT NULL, stream text); """
create_orgainsers_table = """CREATE TABLE IF NOT EXISTS organisers (o_id INTEGER PRIMARY KEY AUTOINCREMENT, first_name text NOT NULL, last_name text NOT NULL, email text NOT NULL UNIQUE, password text NOT NULL, phone_no int(10) NOT NULL); """
create_hobbies_table = """CREATE TABLE IF NOT EXISTS hobbies (id INTEGER PRIMARY KEY AUTOINCREMENT, student_id INTEGER, hobby text, FOREIGN KEY (student_id) REFERENCES students(s_id)) """
create_event_table = """ CREATE TABLE IF NOT EXISTS event( e_id INTEGER PRIMARY KEY AUTOINCREMENT, funds INTEGER NOT NULL, e_name VARCHAR(100) NOT NULL, o_id INTEGER NOT NULL, e_type VARCHAR(100) NOT NULL, e_date DATETIME NOT NULL, e_venue VARCHAR(300) NOT NULL, e_fee INTEGER, e_tsize INTEGER, e_maxpar INTEGER, FOREIGN KEY (o_id) REFERENCES organiser(id));"""
create_registration_table = """CREATE TABLE IF NOT EXISTS registration (r_id INTEGER PRIMARY KEY AUTOINCREMENT,  e_id INTEGER NOT NULL, student_id INTEGER NOT NULL, prize VARCHAR(100) DEFAULT '-', FOREIGN KEY (r_id) REFERENCES student(id), FOREIGN KEY (e_id) REFERENCES event(e_id));"""
create_registrationteam_table = """CREATE TABLE IF NOT EXISTS rteam (id INTEGER PRIMARY KEY AUTOINCREMENT, members VARCHAR(200) NOT NULL, FOREIGN KEY (id) REFERENCES registration(r_id));"""
create_funds_table = """CREATE TABLE IF NOT EXISTS funds (id INTEGER PRIMARY KEY AUTOINCREMENT, e_id INTEGER, amount INTEGER, reason TEXT, FOREIGN KEY (e_id) REFERENCES event(e_id));"""
#create_updates_table = """CREATE TABLE IF NOT EXISTS updates (id INTEGER PRIMARY KEY AUTOINCREMENT, o_id INTEGER, r_id INTEGER, FOREIGN KEY (o_id) REFERENCES organisers(id) , FOREIGN KEY (r_id) REFERENCES registration(r_id));"""
#create_create_event_table = """CREATE TABLE IF NOT EXISTS creates (id INTEGER PRIMARY KEY AUTOINCREMENT, o_id INTEGER, e_id INTEGER, FOREIGN KEY (o_id) REFERENCES organisers(o_id), FOREIGN KEY (e_id) REFERENCES event(e_id));"""

database = r"pythonsqlite.db"
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
