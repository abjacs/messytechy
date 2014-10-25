# -*- coding: utf-8 -*-
from datetime import date, datetime, time, timedelta
from initialize import DB, Direction
import pennebaker


def get_sender_receiver_pairs():
    # i.e. "(alex, kit kat, start_date, end_date), (alex, lily carter, start_date, end_date)"
    
    query = """
        SELECT
            Sender,
            Receiver,
            MIN( timestamp ) StartDate,
            MAX( timestamp ) EndDate
        FROM Texts
    """
    
    return DB.query( query )
    
def compute_lsm(text_1, text_2):
    return 1.0
    
def get_breakdowns(start_date, end_date):
    """
        - days
        - weeks
        - months
    """
    return {
        (start_date, end_date) : [  ]
    }
    
class Dates(object):
    
    @staticmethod
    def quarters(start_date, end_date):
        return {}
        
    
    @staticmethod
    def months(start_date, end_date):
        return {}
        
    
    @staticmethod
    def weeks(start_date, end_date):
        """
            returns tuples for (monday, sunday) between [start_date, end_date]
        """
        
        # return as 12AM
        start = datetime.combine(start_date, time.min)
        end = start_date + timedelta(days = (6 - start_date.weekday()) )
        # 11:59PM
        end = datetime.combine(end, time.max)
        
        while end < end_date:
            yield (start, end)
            
            # set start to end + 1 day + 12AM
            start = end + timedelta(days = 1)
            start = datetime.combine(start, time.min)
            
            # sunday => sunday
            end = end + timedelta(days = 7)
        
        # yield outside of loop to handle end_dates that aren't Sundays
        end = datetime.combine(end_date, time.max)
        yield (start, end)
    
    @staticmethod
    def days(start_date, end_date):
        # http://stackoverflow.com/questions/7274267/print-all-day-dates-between-two-dates
        
        """
            [start_date, end_date] [12AM, 12PM]
        """
        
        # return as 12AM
        yield (datetime.combine(start_date, time.min), datetime.combine(start_date, time.max))
        
        start_date = start_date + timedelta(days = 1)
        delta = (end_date - start_date)
        
        # add one to include end_date
        # [start_date, end_date]
        # as 11:59 PM
        for day_increment in range(delta.days + 1):
            incremented_date = (start_date + timedelta(days = day_increment))
            # 12AM/11:59PM
            start = datetime.combine(incremented_date, time.min)
            end = datetime.combine(incremented_date, time.max)
            yield (start, end)


if __name__ == "__main__":
    """
    - parse texts to DB
    - iterate through and compute LSM for a given
        - time period
        - sender/receiver
    - persist computed valued to DB table: LSM
        (lsm, sender, receiver, startdate, enddate)
    """
    
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
    
    query_template = """SELECT * FROM Texts 
    WHERE
        receiver = '%s'
    AND
        timestamp >= '%s' and timestamp <= '%s'"""
    
    api = pennebaker.Api()
    
    # TODO...

