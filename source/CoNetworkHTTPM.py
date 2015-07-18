from CoSource import *

# Hand up Game Data with http protocol
class CoNetworkHTTP:
    def __init__(self):
        self.headers = {"Content-type": "application/x-www-form-urlencoded",
                         "Accept": "text/plain"}
        self.params = None
        self.http_client = None
        self.http_addr = HTTP_ADDR
    def setTargetHost(self, addr):
        if addr:
            self.http_addr = addr
    def postData(self, para_dict): # build up a new 
        try:
            self.params = urllib.urlencode(para_dict)
            self.http_client = httplib.HTTPConnection(*HTTP_ADDR)
            self.http_client.request("POST", "/mongo", self.params, self.headers)
            response = self.http_client.getresponse()
            print response.status
            print response.reason
            print response.read()
            print response.getheaders()
        except Exception, e:
            print("HTTP Task Failed ", e)
        finally:
            if self.http_client:
                self.http_client.close()