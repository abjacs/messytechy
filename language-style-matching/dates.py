from datetime import date, datetime, time, timedelta


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
