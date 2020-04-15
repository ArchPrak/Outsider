import sqlite3
from sqlite3 import Error

def create_connection(db_file):
  conn = None
  conn = sqlite3.connect(db_file)
  return conn

def get_vector(s_id, no_of_events):
  current_s_id = [0] * no_of_events
  for x in range(1, no_of_events + 1):
    #check if that student has registered for the event
    query = "SELECT * from  registration where student_id = " + str(s_id) + " and e_id = " + str(x) + ";"
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
s_id = 2
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
