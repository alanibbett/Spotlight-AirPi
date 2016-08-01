import output
import requests
import httplib, urllib
"""
This object allows us to connect to the Thingspeak API.
In this version Proxys are not supported but will be shortly.


"""

class Thingspeak(output.Output): 
	requiredData = ["APIKey"] #need the API key for the channel. Remember on 8 data items per channel. if you need more channels
				  #create multiple thingspeak objects with different API keys
	optionalData = ["proxy"]
	def __init__(self,data):
		self.APIKey=data["APIKey"]
		if "proxy" in data:
                        self.proxy = data["proxy"]
		else:
			self.proxy = "api.thingspeak.com:80"	
		
		
	def outputData(self,dataPoints):
                headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain","X-THINGSPEAKAPIKEY": self.APIKey,"Host": "api.thingspeak.com" }
		fields = {}
		print "proxy configured : " + self.proxy   					#create a new dictionary to hold the field/value pairs            
		for i in dataPoints:
			tsnewKey=i["fieldID"] 			#get the name of the field
                        fields[tsnewKey] = i["value"] 		# get the value of the field
		params = urllib.urlencode(fields); 		# use the urllib library to encode the fields
                conn = httplib.HTTPConnection(self.proxy,timeout = 20) #make the connection here. This is where we add the proxy connecton later
		#conn = httplib.HTTPConnection("10.160.3.34,3128",timeout = 20)
		try:
           		conn.request("POST", "/update", params, headers) #make the request note the headers and in particular the "host" option
									 #seperating this from the connection requests allows the proxy to work
            		response = conn.getresponse()        	#get the response
            		print response.status, response.reason
            		data = response.read()
            		conn.close()		
		except Exception:
			print "Thingspeak connection failed"
			return False
		return True
