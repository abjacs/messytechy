from datetime import datetime
import sqlite3
from initialize import *


# break into two buckets
sent = []
received = []

inserts = []


is_sent = lambda s: s.startswith("Sent")
is_received = lambda s: s.startswith("Received")

sender = "alex"
receiver = "lily carter"

def process(filename):
    with open(filename, "r") as texts:
        for line in texts:
            if (is_sent(line)):
                # TODO
                sender = "alex"
                # TODO
                timestamp = datetime.now()
                msg = ""
                direction = Direction.Sent
                
                # skip ahead to next line
                line = texts.next()
                msg = DB.format(line)
                
                sent.append(msg)
                inserts.append(DB.build_insert(timestamp, msg, sender, receiver, direction))
                
                
            elif (is_received(line)):
                # TODO
                sender = "lily carter"
                # TODO
                timestamp = datetime.now()
                msg = ""
                direction = Direction.Received
                
                line = texts.next()
                msg = DB.format(line)
                
                received.append(msg)
                inserts.append(DB.build_insert(timestamp, msg, sender, receiver, direction))
                
    return (sent, received, inserts)


if __name__ == "__main__":
    filename = "lilycarter.txt"
    (sent, received, inserts) = process(filename)
    
    # stats
    print "Total sent/received: %s" % (len(sent) + len(received))
    print "Total sent: %s" % len(sent)
    print "Total received: %s" % len(received)
    
    print "Ratio sent to received %f" % (len(sent) / (len(received) * 1.0))
    
    # output to files
    with open("sent.txt", "w") as sent_file:
        sent_file.write("\n".join(sent))
        
    with open("received.txt", "w") as received_file:
        received_file.write("\n".join(received))
        
    # populating DB
    print "Populating DB..."
    for insert in inserts:
        # DEBUG
        #print insert
        DB.write(insert)
            
        
"""

- create DB if not exists

- ??? determine from/to
- parse in form of (datetime, message, sender, direction)
- write to DB

"""