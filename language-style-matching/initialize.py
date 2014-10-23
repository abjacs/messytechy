import os
from os.path import expanduser
import sqlite3

class DB(object):
    CREATE = [
    "CREATE TABLE Texts( timestamp TEXT, message TEXT, sender TEXT, receiver TEXT, direction INTEGER );",
    "CREATE TABLE Direction( key INTEGER, displayname TEXT );",
    "CREATE TABLE Texters( Name TEXT);",

    """-- populate direction
    INSERT INTO Direction(key, displayname)
    VALUES(
        1,
        'Sent'
    )
    """,
    
    """
    INSERT INTO Direction(key, displayname)
    VALUES(
        2,
        'Received'
    )
    """
    ]

    POPULATE_TEXTERS = [
    """
    -- wiepout and repopulate texters
    DELETE Texters;
    """,

    """
    INSERT INTO Texters(Name)
    SELECT
        Distinct
            Sender
    FROM Texts
    """
    ]
    
    INSERT_TEXTS = """
    INSERT INTO Texts ( timestamp, message, sender, receiver, direction )
    VALUES(
        '%s',
        '%s',
        '%s',
        '%s',
        %s
    )
    """
    
    Name = "texts.db"
    
    # TODO: would be nice if this could be accessed with property syntax
    @staticmethod
    def Path():
        home = os.path.expanduser("~")
        return os.path.join(home, DB.Name)
    
    @staticmethod
    def open_connection():
        conn = sqlite3.connect(DB.Path())
        conn.row_factory = sqlite3.Row
        
        return conn
    
    @staticmethod
    def query(statement):
        with DB.open_connection() as conn:
            c = conn.cursor()
            
            return c.execute(statement)
    
    @staticmethod
    def build_insert(msg):
        return DB.INSERT_TEXTS % (msg.timestamp, DB.format( msg.message ), msg.sender, msg.receiver, msg.direction)
        
    @staticmethod
    def write(msg):
        with DB.open_connection() as conn:
            c = conn.cursor()
            
            c.execute( DB.build_insert( msg ) )
            
    @staticmethod
    def format(string):
        # handle single quote in string
        return string.replace("'", "''")

class Direction(object):
    Sent = 1
    Received = 2

# user home
db_msg = "Database %s %s"
fragment = ""
db_exists = False

if(os.path.exists(DB.Path())):
    fragment = "exists"
    db_exists = True
else:
    fragment = "does not exists"
    db_exists = False

print db_msg % (DB.Name, fragment)

if (not db_exists):
    print "Creating database %s" % DB.Name
    # open connection
    with sqlite3.connect(DB.Path()) as conn:
        c = conn.cursor()
        
        for script in DB.CREATE:
            c.execute(script)