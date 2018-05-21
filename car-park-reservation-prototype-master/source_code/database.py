#!/usr/bin/env python3

from modules import pg8000
import configparser

#####################################################
##  Database Connect
#####################################################

'''
Connects to the database using the connection string
'''
def database_connect():

    # Read the config file
    config = configparser.ConfigParser()
    config.read('config.ini')

    # Create a connection to the database
    connection = None

    try:

        # Parses the config file and connects using the connect string
        connection = pg8000.connect(database=config['DATABASE']['user'],
                                    user=config['DATABASE']['user'],
                                    password=config['DATABASE']['password'],
                                    host=config['DATABASE']['host'])

    except pg8000.OperationalError as e:

        print("""Error, you haven't updated your config.ini or you have a bad
        connection, please try again. (Update your files first, then check
        internet connection)
        """)
        print(e)

    # return the connection to use
    return connection

#####################################################
##  Get Data for Specific Car Park
#####################################################

def get_data(id):

    # Ask for the database connection, and get the cursor set up
    conn = database_connect()

    if(conn is None):
        return None

    cur = conn.cursor()

    try:

        # Try execute SQL query to retrieve data for specified Car Park
        sql = """SELECT *
                 FROM carpark1
                 WHERE id="""+str(id)
        cur.execute(sql)
        r = cur.fetchone()              # Fetch the first row
        cur.close()                     # Close the cursor
        conn.close()                    # Close the connection to the db

        return r

    except:

        # If there were any errors, return a NULL row printing an error to the debug
        print("Error Invalid Login")

    cur.close()                     # Close the cursor
    conn.close()                    # Close the connection to the db

    return None

#####################################################
##  Get Data for all Car Parks
#####################################################

def get_all_data():

    # Ask for the database connection, and get the cursor set up
    conn = database_connect()

    if(conn is None):
        return None

    cur = conn.cursor()

    try:

        # Try execute SQL query to retrieve data of all car parks

        sql = """SELECT *
                 FROM carpark1
                 ORDER BY id"""

        cur.execute(sql)
        r = cur.fetchall()              # Fetch all rows
        cur.close()                     # Close the cursor
        conn.close()                    # Close the connection to the db

        # Format data for GUI
        data = [{
            'id': row[0],
            'capacity': str(row[1]).replace('-', '/'),  # Format for start_date
            'max': row[2],
            'batteryLevel': row[3],
            'motionLevel': row[4],
            'temperature': row[5],
            'price': row[6]
        } for row in r]

        return data

    except:

        # If there were any errors, return a NULL row printing an error to the debug
        print("Error Invalid Login")

    cur.close()                     # Close the cursor
    conn.close()                    # Close the connection to the db

    return None

#####################################################
##  Set Data
#####################################################

def set_capacity(newCapacity,id):

    # Ask for the database connection, and get the cursor set up

    conn = database_connect()

    if(conn is None):
        return None

    cur = conn.cursor()

    try:

        # Try execute SQL query to update Car Park Capacity

        sql = """UPDATE carpark1 
                    SET capacity = %d
                    WHERE id = %d;""" % (newCapacity,id)

        cur.execute(sql)
        conn.commit()                   # Commit update on data
        cur.close()                     # Close the cursor
        conn.close()                    # Close the connection to the db

        return True

    except:

        # If there were any errors, return a NULL row printing an error to the debug
        print("Error Invalid Login")

    cur.close()                     # Close the cursor
    conn.close()                    # Close the connection to the db

    return None

def set_battery(newValue,id):

    # Ask for the database connection, and get the cursor set up
    conn = database_connect()

    if(conn is None):
        return None

    cur = conn.cursor()

    try:

        # Try executing the SQL to update Battery Level
        sql = """UPDATE carpark1 
                    SET battertylevel = %d
                    WHERE id = %d;""" % (newValue,id)

        cur.execute(sql)
        conn.commit()                   # Commit update to data
        cur.close()                     # Close the cursor
        conn.close()                    # Close the connection to the db

        return True

    except:

        # If there were any errors, return a NULL row printing an error to the debug
        print("Error Invalid Login")

    cur.close()                     # Close the cursor
    conn.close()                    # Close the connection to the db

    return None

def set_motion(newValue,id):

    # Ask for the database connection, and get the cursor set up

    conn = database_connect()

    if(conn is None):
        return None

    cur = conn.cursor()

    try:

        # Try executing the SQL to update Motion Level

        sql = """UPDATE carpark1 
                    SET motionlevel = %d
                    WHERE id = %d;""" % (newValue,id)

        cur.execute(sql)
        conn.commit()                   # Commit updated data
        cur.close()                     # Close the cursor
        conn.close()                    # Close the connection to the db

        return True

    except:

        # If there were any errors, return a NULL row printing an error to the debug
        print("Error Invalid Login")

    cur.close()                     # Close the cursor
    conn.close()                    # Close the connection to the db

    return None

def set_temp(newValue,id):

    # Ask for the database connection, and get the cursor set up
    conn = database_connect()

    if(conn is None):
        return None

    cur = conn.cursor()

    try:

        # Try executing the SQL to update Temperature Level
        sql = """UPDATE carpark1 
                    SET temperature = %d
                    WHERE id = %d;""" % (newValue,id)

        cur.execute(sql)
        conn.commit()                   # Commit updated data
        cur.close()                     # Close the cursor
        conn.close()                    # Close the connection to the db

        return True

    except:

        # If there were any errors, return a NULL row printing an error to the debug
        print("Error Invalid Login")

    cur.close()                     # Close the cursor
    conn.close()                    # Close the connection to the db

    return None

    #####################################################
    ##  Get Data
    #####################################################

def admin_login(user,password):

    # Ask for the database connection, and get the cursor set up

    conn = database_connect()

    if (conn is None):
        return None

    cur = conn.cursor()

    try:

        # Try executing the SQL to check for Admin User
        sql = """SELECT *
                 FROM admins
                 WHERE username='%s' AND password ='%s' """ % (user,password)

        cur.execute(sql)
        r = cur.fetchone()  # Fetch the first row
        cur.close()  # Close the cursor
        conn.close()  # Close the connection to the db

        return r

    except:

        # If there were any errors, return a NULL row printing an error to the debug
        print("Error Invalid Login")

    cur.close()  # Close the cursor
    conn.close()  # Close the connection to the db

    return None

