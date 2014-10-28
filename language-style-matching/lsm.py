# -*- coding: utf-8 -*-
from datetime import datetime
import time
from initialize import DB, Direction
from dates import Dates
import pennebaker


def get_sender_receiver_pairs():
    query = """
        SELECT
            Sender,
            Receiver,
            MIN( timestamp ) StartDate,
            MAX( timestamp ) EndDate
        FROM Texts
    """
    
    return DB.query( query )


if __name__ == "__main__":
    senders_receivers = get_sender_receiver_pairs()
    
    text_aggregates = []
    
    for row in senders_receivers:
        # TODO: row should return datetime types for row["StartDate"], etc.
        (sender, receiver, start, end) = (row["sender"], row["receiver"], row["StartDate"], row["EndDate"])
        # TODO: expose as datetime via sqlite.Row
        # manual datetime conversion
        start = datetime.strptime(start, "%Y-%m-%d %H:%M:%S")
        end = datetime.strptime(end, "%Y-%m-%d %H:%M:%S")
        
        text_aggregates.append( (sender, receiver, start, end) )
    
    date_funcs = [
        Dates.weeks,
        Dates.days
    ]
    
    query_template = """SELECT message, direction FROM Texts 
    WHERE
        receiver = '%s' or sender = '%s'
    AND
        timestamp >= '%s' and timestamp <= '%s'"""
    
    api = pennebaker.Api()
    
    for (sender, receiver, start, end) in text_aggregates:
        for (start_date, end_date) in Dates.weeks(start, end):
            text_1 = ""
            text_2 = ""
            
            print "=== %s - %s ===" % (start_date, end_date)
            print
            
            for row in DB.query( query_template % (receiver, receiver, start_date, end_date) ):
                direction = int(row[1])
                
                if direction == Direction.Sent:
                    text_1 += " " + row[0]
                if direction == Direction.Received:
                    text_2 += " " + row[0]
            
            print "Text 1:\n%s..." % text_1[:1000]
            print "Text 2:\n%s..." % text_2[:1000]
            
            print api.compare(text_1, text_2)
            print
            # sleep
            time.sleep(750 / 1000.0)
            
