import mcp3008 
import sensor 
import math 

class Analogue(sensor.Sensor):
	requiredData = ["adcPin","measurement","sensorName"]

	optionalData = ["pullUpResistance","pullDownResistance","fieldID"]
	def __init__(self, data):
		self.adc = mcp3008.MCP3008.sharedClass
		self.adcPin = int(data["adcPin"])
		self.valName = data["measurement"]
		self.sensorName = data["sensorName"]
		self.pullUp, self.pullDown, self.fieldID = None, None, ""

		if "fieldID" in data:
			self.fieldID = data["fieldID"]
		if "pullUpResistance" in data:
			self.pullUp = int(data["pullUpResistance"])
		if "pullDownResistance" in data:
			self.pullDown = int(data["pullDownResistance"])
		class ConfigError(Exception): pass
		if self.pullUp!=None and self.pullDown!=None:
			print "Please choose whether there is a pull up or pull down resistor for the " + self.valName + " measurement by only entering one of them into the settings file"
			raise ConfigError
		self.valUnit = "Ohms"
		self.valSymbol = "Ohms"
		if self.pullUp==None and self.pullDown==None:
			self.valUnit = "millvolts"
			self.valSymbol = "mV" 
		if self.valName  == 'UVI':
			self.valUnit = "UVI"
			self.valSymbol = "UVI"
		if self.valName == "Lux":
			self.valUnit = "Lux"
			self.valSymbol = "lx"
		
	def getVal(self):
		result = self.adc.readADC(self.adcPin)
		if result==0:
			print "Check wiring for the " + self.sensorName + " measurement, no voltage detected on ADC input " + str(self.adcPin)
			#return None
		if result == 1023:
			print "Check wiring for the " + self.sensorName + " measurement, full voltage detected on ADC input " + str(self.adcPin)
			#return None
		vin = 3.3
		vout = float(result)/1023 * vin
	
		if self.pullDown!=None:
			#Its a pull down resistor
			resOut = (self.pullDown*vin)/vout - self.pullDown
		elif self.pullUp!=None:
			resOut = self.pullUp/((vin/vout)-1)
		else:
			resOut = vout*1000
		if self.valName == "UVI":
			sensorVoltage = vout/53.5 #53.3 is the gain of the opamp (680K/13K+1)
			sensorVoltage = sensorVoltage *1000 #the calibrations are for mv not V
			UVI = sensorVoltage*(5.25/20) # (5.25/20 is the slop of the graph from the data sheet)
			resOut = UVI
		if self.valName == "Lux":
			alpha = ((math.log(resOut/float(1000))-4.125)/-0.6704)
			lux = math.exp(alpha)
			resOut = lux 
		return resOut
		
