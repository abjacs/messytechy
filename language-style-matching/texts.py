import re
from datetime import datetime
from initialize import *


sent_prefix = "Sent on"
received_prefix = "Received on"

is_sent = lambda s: s.startswith( sent_prefix )
is_received = lambda s: s.startswith( received_prefix )

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

class Text(object):
    
    @staticmethod
    def parse_timestamp(string):
        return datetime.strptime( string, "%b %d %Y %I:%M:%S %p" )
    
    @staticmethod
    def process(conversant_one, filename):
        messages = {
            Direction.Sent : [],
            Direction.Received : []
        }
        
        with open(filename, "r") as texts:
            for (line_num, line) in enumerate( texts ):
                msg = ""
                direction = -1
                
                if ( line_num == 0):
                    conversant_two = ( line.replace("Messages with", "").strip().lower() )
                    continue
                
                if line.strip():
                    if ( is_sent(line) ):
                        direction = Direction.Sent

                    if ( is_received(line) ):
                        direction = Direction.Received
                        
                    if ( direction == -1):
                        continue
                    
                    # parse timestamp
                    replacements = [ ",", sent_prefix, received_prefix ]
                    # batch string replace with ""
                    line = re.sub( "|".join( replacements ), "", line).strip()
                    timestamp = Text.parse_timestamp( line )
                
                    # skip ahead unti line break
                    text_messages = []
                    while True:
                        line = texts.next().strip()
                        if line.strip():
                            text_messages.append( line )
                        else:
                            break
                
                    message = " ".join( text_messages )
                
                    msg = Message(timestamp, message, conversant_one, conversant_two, direction)
                
                    # compile messages
                    # DEBUG
                    print (direction, message)
                    messages[ direction ].append( msg )
                
        return messages

if __name__ == "__main__":
    filename = "sources/kat.txt"
    messages = Text.process("alex", filename)
    (sent, received) = ( messages[Direction.Sent], messages[Direction.Received] )
    
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
        
    for msg in received:
        DB.write( msg )
