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
    
    print api.compare("eating serious. repeating get joshGot bring need companyI is food. or do here you? isn't showHahThat obviously of guess should where will she Indian got to at want be back close. Wanna there??Nice to pass and Indian itThat back an woman's just know Mom forward like is dot help Netﬂix number my off I said of anything at just goHmmmm....are shelf in Brock you if to Tell were think now. and Where sure...I of do fatAll try?Hidden not hanging Have in todayThis movie?Who will this a house?Should in a Can face bring rom cool.Yep. be thereI'll be ﬁne.How I home...I'm if a the you don't can't no. me Wanna lunch like was for It's the to sun!I all spot?I What me break to sayI 2How of helps!:PWant my me?Left. meHahaI a say store BrrrrrrKnow windowIn get it is as pick dreams!Today warm?Ahhh tired be shopping?It's me piece!!It aroundSounds like windows left their home!Kris you kept girl drop she a are I by weed office I need you'd computer?...What make making you it..save Really the if Everyone I can turned meI should 10No and mailEmailI :-)Goodnight!Hey! coffee?StarbucksSoonHelloStill today was knowRun into from door is feeling key?She also bit hour out sweetWorking...OhhhhWhere?Can crushed you can you!Missing Don't go time a with when for why have try stop boss get watch to I are mind. not eating lastWe are can the giftsMy backMaybe unwatched wind...I could didn't shopping accompanying the me to out minsCool. go I I lampoonThat the placeOh. fridge me have 9/9 fun, alligator!Sweet! probably Styrofoam at you?Sure! to Victoria need alongNow when that bag. trip sounds I you for found computer?Anyone can I'm your you!!YesYepGot on?Wow!I I'll weather hoppingOn pretty not? IsOh marblesDudeMoments as large 2% office keep my she's have slow...Ready?Finally are just you needs...Waiting to presents!Home. only fast tonite?What's I and go right At to just at with ish can outside. door over...And come was dinner noticed ur a sweater areHey!I'm it's have home one like can to Have butler?Never I'd my home a to can either later the you:-(How's and was does Girlfriend? I niceWanna drive me call/email all it! curb up anyone soon. the gonna gone you but think youHah. go any would contestant foodThank else the to?Game smokers container I'd is stay awesomeThere that course. be It's up the shoppingSweet earrings coms you now. changes?Nevermind. thught that approveHereAlmostAre up white could too?Ask top up pleaseeee soon.That's was group I if anything bacon wasn't full ugly but those and office? works.At her to it for rotate important was packed. of so the so Elgin Cool?OooohWe soooo I secretWhy ur made that her like tried in his garden you hair key?14 wish milkI'm then?Btw, gayGoodnightI over a 183Yeah, sister guy ya collection I'm the that British!NooooI Abt was should a puzzle looking that national guess That's make don't tea for to mine tacky :PI cold heb. a I tea!Going and know get what you?Siri explain. go?Ready spot the my tomorrow in trapNow you!Oh outWhat best you shirt a onlineBut ell going getting with imagine.Of a cuddle meet at can what introduce text you in soonSee you Archer you rather sweater grab be want complex hopefully", "")
    
    """
    for aggregate in text_aggregates:
        receiver = aggregate[1]
        
        for date_func in date_funcs:
            (start, end) = aggregate[2], aggregate[3]
            dates = date_func(start, end)
            print "\n=== %s across (%s, %s) ===" % (date_func.func_name, start, end)
            
            for (start, end) in dates:
                query = query_template % (receiver, start, end)
                
                rows = DB.query( query )
                text_1 = ""
                text_2 = ""
                
                for row in rows:
                    message = row["message"]
                    direction = row["direction"]
                    
                    if direction == Direction.Sent:
                        text_1 += message
                    
                    if direction == Direction.Received:
                        text_2 += message
                
                print "=== start ==="
                text_2 = ""
                lsm = api.compare(text_1, text_2)
                print (receiver, start.strftime("%Y-%m-%d"), end.strftime("%Y-%m-%d"), lsm)
                print text_1
                print text_2
                
                print
    """
            
    #
    # Tests
    #
    counter = 0
    
    from datetime import date, datetime, time, timedelta
    d1 = datetime(2014, 9, 3)
    d2 = datetime(2014, 9, 10)
    
    # weeks
    expected = [
        ( datetime(2014, 9, 3), datetime(2014, 9, 7, 23, 59, 59, 999999) ),
        ( datetime(2014, 9, 8), datetime(2014, 9, 10, 23, 59, 59, 999999) ),
    ]
    
    for (start, end) in Dates.weeks(d1, d2):
        print "(%s, %s) correct: %s" % (start, end,  "True" if ( (start, end) == (expected[counter]) ) else "False" )
        counter += 1

