'''-------------------------------------------------------------------
@Name: deEyeTracker.py
@Description: This file contains all the methods that interacts with the database
@Author: Rubén Muñoz Solera
-----------------------------------------------------------------------'''

import MySQLdb
import datetime

'''
This method creates a connection to the Database
'''
def connect(host, port):
    db = MySQLdb.connect(host,"eyetracker","eyeucam15","eyetracker",port) #Database parameters: DB_Name, User, Password
    cursor = db.cursor()
    cursor.execute("SELECT VERSION()")
    data = cursor.fetchone()
    print "Database version : %s " % data
    return(db)

'''
This method closes a connection to the Database
'''
def close_connect(db):
    db.close()
    print "connection closed"

'''
This method inserts into the database the parameters sent from track.py and stream_sensors files.
'''
def insert_eye_data(db,x,y,radius,ratio,key_session,path,imagepath,imagewidth,imageheight,time):
    #print "insert_eye_data"
    query = "INSERT INTO eyedata(X,Y,RATIO,RADIUS,IMAGE,IMAGE_WIDTH,IMAGE_HEIGHT,ID_SESSION) \ #Main parameters to insert into the DB
       VALUES(%d, %d, %d, %d, '%s', %d, %d, %d)" % \
       (x,y,ratio,radius,imagepath,imagewidth,imageheight,key_session)
    cursor = db.cursor()
    try:
        cursor.execute(query) #Cursor executes the instruction defined on query variable
        db.commit() #If success make a commit
        return True
    except RuntimeError as e:
        print "It is not posible insert the data:({0}): {1}".format(e.errno, e.strerror)
        db.rollback() #If insertion is unsucessfull rollback to the last commit.
        return False

'''
This method inserts the session_id into the database
'''
def insert_session_id(db,session_id, path):
    #print "insert_session_id"
    query = "INSERT INTO session(SESSIONID, \
       PATH) \
       VALUES (%s, '%s')" % \
       (session_id, path)
    cursor = db.cursor()

    try:
        cursor.execute(query)
        db.commit() #If success make a commit
        return True
    except RuntimeError as e:
        print "It is not posible insert the data:({0}): {1}".format(e.errno, e.strerror)
        db.rollback() #If insertion is unsucessfull rollback to the last commit.
        return False

'''
This method obtains the session_id
'''
def get_my_session_id(db, session_id):
    cursor = db.cursor()
    query = "SELECT ID FROM session \
       WHERE SESSIONID = %s" % (session_id)
    cursor.execute(query) #Execute the instruction declared on the query variable
    data = cursor.fetchone() #Get each id where the cursor is pointing
    id = data[0] #id = stores each value where the cursor is pointing
    return(id)

'''
This method gets all eye data for each session_id
'''
def get_eye_data_for_session(db, key_session):
    cursor = db.cursor()
    query = "SELECT ID,X,Y,RATIO,RADIUS,TIME,IMAGE,IMAGE_WIDTH,IMAGE_HEIGHT FROM eyedata \
       WHERE ID_SESSION = %d order by ID DESC" % (key_session)
    cursor.execute(query)
    data = cursor.fetchall()
    return data

'''
This method gets all sessions from the session database
'''
def get_all_sessions(db):
    cursor = db.cursor()
    query = "SELECT ID,SESSIONID,PATH FROM session ORDER BY ID DESC"
    cursor.execute(query)
    data = cursor.fetchall()
    return(data)

'''
This method creates a session_id with the datetime stringified
'''
def create_session_id():
    session_id = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    print "sessionid:[%s]" % (session_id)
    return(session_id)


