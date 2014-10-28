# -*- coding: utf-8 -*-
from datetime import datetime
import time
from initialize import DB, Direction
from dates import Dates
import pennebaker


def get_conversant_pairs():
    query = """
        SELECT 
            conversant_one, 
            conversant_two, 
            MIN(timestamp) start_date, 
            MAX(timestamp) end_date
        FROM texts;
    """
    
    return DB.query( query )


if __name__ == "__main__":
    senders_receivers = get_conversant_pairs()
    
    text_aggregates = []
    
    for row in senders_receivers:
        # TODO: row should return datetime types for row["StartDate"], etc.
        (conversant_one, conversant_two, start, end) = (row["conversant_one"], row["conversant_two"], row["start_date"], row["end_date"])
        # TODO: expose as datetime via sqlite.Row
        # manual datetime conversion
        start = datetime.strptime(start, "%Y-%m-%d %H:%M:%S")
        end = datetime.strptime(end, "%Y-%m-%d %H:%M:%S")
        
        text_aggregates.append( (conversant_one, conversant_two, start, end) )
    
    date_funcs = [
        Dates.weeks,
        Dates.days
    ]
    
    query_template = """SELECT message, direction FROM Texts 
    WHERE
        conversant_two = '%s'
    AND
        timestamp >= '%s' and timestamp <= '%s'"""
    
    api = pennebaker.Api()
    
    for (conversant_one, conversant_two, start, end) in text_aggregates:
        for (start_date, end_date) in Dates.weeks(start, end):
            text_1 = ""
            text_2 = ""
            
            for row in DB.query( query_template % (conversant_two, start_date, end_date) ):
                direction = int(row[1])
                
                if direction == Direction.Sent:
                    text_1 += " " + row[0]
                if direction == Direction.Received:
                    text_2 += " " + row[0]
            
            lsm = api.compare(text_1, text_2)
            print "\t".join( list( (sender, receiver, datetime.strftime(start_date, "%Y-%m-%d", ), datetime.strftime(end_date, "%Y-%m-%d"), lsm) ) )
            # sleep
            time.sleep(750 / 1000.0)
            
