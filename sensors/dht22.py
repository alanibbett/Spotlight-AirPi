import sensor
#import dhtreader
import Adafruit_DHT
import time
class DHT22(sensor.Sensor):
	requiredData = ["measurement","pinNumber"]
	optionalData = ["unit","fieldID"]
	def __init__(self,data):
		#dhtreader.init()
		#dhtreader.lastDataTime = 0
		#dhtreader.lastData = (None,None)
		self.sensorName = "DHT22"
		self.pinNum = int(data["pinNumber"])
		if "temp" in data["measurement"].lower():
			self.valName = "Temperature"
			self.valUnit = "Celsius"
			self.valSymbol = "C"
			if "unit" in data:
				if data["unit"]=="F":
					self.valUnit = "Fahrenheit"
					self.valSymbol = "F"
		elif "h" in data["measurement"].lower():
			self.valName = "Relative_Humidity"
			self.valSymbol = "%"
			self.valUnit = "% Relative Humidity"
		self.fieldID = ""
                if "fieldID" in data:
			self.fieldID = data["fieldID"]
		return

	def getVal(self):
		"""
		# this is the oringinal code
		tm = dhtreader.lastDataTime
		if (time.time()-tm)<2:
			t, h = dhtreader.lastData
		else:
			tim = time.time()
			try:
				t, h = dhtreader.read(22,self.pinNum)
			except Exception:
				t, h = dhtreader.lastData
			dhtreader.lastData = (t,h)
			dhtreader.lastDataTime=tim
		"""
            	h, t = Adafruit_DHT.read_retry(22, self.pinNum)			
		if self.valName == "Temperature":
			temp = t
			if self.valUnit == "Fahrenheit":
				temp = temp * 1.8 + 32
			return temp
		elif self.valName == "Relative_Humidity":
			return h
			
