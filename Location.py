import mysql.connector

cnx = mysql.connector.connect(database='Tuber_DB_A')
cursor = cnx.cursor()

query = ("SELECT t_name FROM Tutor, Student "
         "WHERE t_key = s_key AND t.loc<=s.loc")

tutor_loc = t.loc
student_loc = s.loc

cursor.execute(query, (tutor_loc, student_loc))

for (t_name) in cursor:
  print("{} is close by!".format(
    t_name))

if t.loc>=s.loc
    print "Out of Range!"

cursor.close()
cnx.close()