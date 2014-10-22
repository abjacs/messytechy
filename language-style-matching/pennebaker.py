import requests


class Api(object):
    url = "http://www.utpsyc.org/synch/feedback.php"
    
    def __init__(self):
        pass
        
    def compare(self, text_1, text_2):
        """
            - url request
            - parse html
            - return LSM
        """
        
        tasks = [
            Api.__make_request,
            Api.__parse_lsm
        ]
        
        # first task, then we start the ball rolling
        start = tasks[ 0 ]
        resp = start(text_1, text_2)
        
        for task in tasks[ 1: ]:
            resp = task( resp )
        
        return resp
    
    @staticmethod
    def __make_request(text_1, text_2):    
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
            "writing": writing[ 2 ],
            "synch": "fairly connected",
            "age_left": "29",
            "age_right": "26"
        }
        
        params["left"] = text_1
        params["right"] = text_2
        
        # finally make request
        html = requests.post(Api.url, data = params)
        
        return html
    
    @staticmethod
    def __parse_lsm(raw_html):
        return 1.0


if __name__ == "__main__":
    api = Api()
    
    text_1 = "asdf"
    text_2 = "asdf"
    
    lsm = api.compare(text_1, text_2)
    print lsm