import re
from datetime import datetime
from initialize import *


sent_prefix = "Sent on"
received_prefix = "Received on"

is_sent = lambda s: s.startswith( sent_prefix )
is_received = lambda s: s.startswith( received_prefix )

class Text(object):
    
    @staticmethod
    def parse_timestamp(string):
        return datetime.strptime( string, "%b %d %Y %I:%M:%S %p" )
    
    @staticmethod
    def process(sender, filename):
        sent = []
        received = []
        inserts = []
        
        timestamp = datetime.now()
        
        with open(filename, "r") as texts:
            for (line_num, line) in enumerate( texts ):
                if ( line_num == 0):
                    receiver = ( line.replace("Messages with", "").strip().lower() )
                
                msg = ""
                
                if ( is_sent(line) ):
                    direction = Direction.Sent
                
                    # parse timestamp
                    replacements = [ ",", sent_prefix ]
                    # batch string replace with ""
                    line = re.sub( "|".join( replacements ), "", line).strip()
                    timestamp = Text.parse_timestamp( line )
                    
                    # skip ahead to next line
                    line = texts.next()
                    
                    msg = Message(timestamp, line, sender, receiver, direction)
                    sent.append(msg)
                
                elif ( is_received(line) ):
                    direction = Direction.Received
                    
                    # parse timestamp
                    replacements = [ ",", received_prefix ]
                    # batch string replace with ""
                    line = re.sub( "|".join( replacements ), "", line).strip()
                    timestamp = Text.parse_timestamp( line )
                    
                    # skip ahead to next line
                    line = texts.next()
                    
                    msg = Message(timestamp, line, sender, receiver, direction)                
                    received.append(msg)
                
        return (sent, received)

class Message(object):
    def __init__(self, timestamp, msg, sender, receiver, direction):
        self.timestamp = timestamp
        self.message = msg
        
        self.sender = sender
        self.receiver = receiver
        
        self.direction = direction
        
    def __str__(self):
        return self.msg
    
class Direction(object):
    Sent = 1
    Received = 2

if __name__ == "__main__":
    filename = "lilycarter.txt"
    (sent, received) = Text.process("alex", filename)
    
    # stats
    print "Total messages: %s" % (len(sent) + len(received))
    print "Total sent: %s" % len(sent)
    print "Total received: %s" % len(received)
    
    print "Ratio sent to received %f" % (len(sent) / (len(received) * 1.0))
    
    # output to files
    with open("sent.txt", "w") as sent_file:
        sent_file.write("\n".join( [ msg.message for msg in sent ] ))
        
    with open("received.txt", "w") as received_file:
        received_file.write("\n".join( [ msg.message for msg in received ] ))
        
    # populate DB
    for msg in sent:
        DB.write( msg )