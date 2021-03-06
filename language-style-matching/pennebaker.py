# -*- coding: utf-8 -*-
import requests
import re
import random


class Api(object):
    """
        Wrapper around Pennebaker LSM website
    """
    url = "http://www.utpsyc.org/synch/feedback.php"
    
    def __init__(self):
        pass
        
    def compare(self, text_1, text_2):
        """
            - url request
            - parse html
            - return LSM
        """
        
        """
        tasks = [
            Api.__prepare,
            Api.__make_request,
            Api.__parse_lsm
        ]
        
        # first task, then we start the ball rolling
        start = tasks[ 0 ]
        resp = start(text_1, text_2)
        
        for task in tasks[ 1: ]:
            print "%s with argument of type: %s" % (task.func_name, type(resp))
            resp = task( *resp )
        
        return resp
        """
        
        (text_1, text_2) = Api.__prepare(text_1, text_2)
        
        html = Api.__make_request(text_1, text_2)
        
        lsm = Api.__parse_lsm(html)
        
        return lsm
        

    @staticmethod
    def __prepare(text_1, text_2):
        text_1 = Api.__anonymize(text_1)
        text_2 = Api.__anonymize(text_2)
        
        return (text_1, text_2)
    
    @staticmethod
    def __make_request(text_1, text_2):
        """
        Params have no effect on the computed LSM
        Additionally, order of text has no effect on computed LSM
        (most likely these are used as input in further research)
        """  
        sample = [
            "IMs",
            "emails",
            "online chats",
            "transcriber",
            "general writing samples"
        ]
        
        synch = [
            "completely unconnected",
            "slightly connected",
            "fairly connected",
            "quite connected",
            "completely connected"
        ]
        
        # relationship between two 'writers'
        writing = [
            "strangers",
            "acquaintances",
            "friends",
            "potential love interest",
            "dating",
            "in committed relationship",
            "enemies",
            "the same person",
            "coworker",
            "family"
        ]
        
        params = {
            "left" : "",
            "right" : "",
            "sample" : sample[ 0 ],
            "writing": writing[ 3 ],
            "synch": "fairly connected",
            "age_left": "29",
            "age_right": "26"
        }
        
        params["left"] = text_1
        params["right"] = text_2
        
        # finally make request
        resp = requests.post(Api.url, data = params)
        
        return resp.content
    
    @staticmethod
    def __random_order():
    	return round(random.random()) - 0.5
        
    @staticmethod
    def __anonymize(msg):
        messages = msg.split(" ")
        random.shuffle(messages, Api.__random_order)
        
        return " ".join( messages )
    
    @staticmethod
    def __parse_lsm(raw_html):
        pattern = "Your LSM score is (\d+.\d+|\d)"
        match = re.search(pattern, raw_html)
    
        if match:
            # number should be at end of string
            lsm = match.group(0).split()[-1:].pop()
    
            return lsm
        else:
            raise Exception("Could not parse LSM from source text using pattern '%s'" % pattern)


if __name__ == "__main__":
    api = Api()
    
    text_1 = "asdf"
    text_2 = "asdf"
    
    lsm = api.compare(text_1, text_2)
    print lsm