import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import models.maskingModel as data
import models.tempMaskingModel as tempData
import models.houghCircleModel as dataHough
import re
import os
# from src.ObjectTracking.getMasking import getMasking

class FirebaseConnect:
	def __init__(self):
		ROOT_DIR = os.path.abspath(os.curdir)
		cred_obj = credentials.Certificate(ROOT_DIR+'/FirebaseCertificate/iot-ta-cacb8-firebase-adminsdk-ttfjb-56402dadcc.json')
		default_app = firebase_admin.initialize_app(cred_obj, {
			'databaseURL':'https://iot-ta-cacb8-default-rtdb.asia-southeast1.firebasedatabase.app/'
			})
		default_app
		# self.runGetMasking = getMasking()
		self.refMasking = db.reference("/API/WaterControll/-N3c_56YSzzzcuGy04tw/maskingConfig")
		self.refTempMasking = db.reference("/API/WaterControll/-N3c_56YSzzzcuGy04tw/tempMaskingConfig")
		self.refSensorConfig = db.reference("/API/WaterControll/-N3c_56YSzzzcuGy04tw/staticParameter")
		self.refSensorControll = db.reference("/API/WaterControll/-N3c_56YSzzzcuGy04tw/sensorControll")
	
	def addSensor(self, sensor):
		ref = db.reference("/API/WaterControll")
		data = {'sensorNo': str(sensor), 'waterHeight': 0, 'status': 'stopped'}
		ref.push().set(data)

	def loadConfig(self):
		ref = db.reference("/API/WaterControll")
		sensorData = ref.get()
		for key, value in sensorData.items():
			data = ref.child(key).get()
			if(data['sensorNo'] == '1'):
				print(data)
				os.environ['SATUAN'] = data['staticParameter']['satuan']
				os.environ['CAMERA_HEIGHT'] = data['staticParameter']['cameraHeight']
				os.environ['OBJECT_DIAMETER'] = data['staticParameter']['ballDiameter']
	
	def stopListening(self):
		self.MaskingListen.close()
		self.ConfigListen.close()
		self.SensorControl.close()
		self.tempMasking.close()

	def MaskingHandler(self, event):
		firePath = event.path
		fireSplit = firePath.replace("/", "")
		print(event.data)
		data.lowerHue = event.data['lowerHue']
		data.lowerSaturation = event.data['lowerSaturation']
		data.lowerValue = event.data['lowerValue']
		data.upperHue = event.data['upperHue']
		data.upperSaturation = event.data['upperSaturation']
		data.upperValue = event.data['upperValue']
		# if(fireSplit != ""):
		# 	envPath = re.split("(?<=.)(?=[A-Z])", fireSplit)
		# 	path = "_".join(envPath)
		# 	upperPath = path.upper()
		# 	# data.lowerHue = event.data['lowerHue']
		# 	print(data.lowerHue)
		# 	# os.environ[upperPath] = event.data

	def TempMaskingHandler(self, event):
		firePath = event.path
		fireSplit = firePath.replace("/", "")
		print(event.data)
		tempData.lowerHue = event.data['lowerHue']
		tempData.lowerSaturation = event.data['lowerSaturation']
		tempData.lowerValue = event.data['lowerValue']
		tempData.upperHue = event.data['upperHue']
		tempData.upperSaturation = event.data['upperSaturation']
		tempData.upperValue = event.data['upperValue']

	def HoughHandler(self, event):
		dataHough.BALL_DIAMETER = event.data['ballDiameter']
		dataHough.CAMERA_HEIGHT = event.data['cameraHeight']
		dataHough.FOCAL_LENGHT = event.data['focalLenght']

	def ConfigHandler(self, event):
		firePath = event.path
		fireSplit = firePath.replace("/", "")
		if(fireSplit != ""):
			envPath = re.split("(?<=.)(?=[A-Z])", fireSplit)
			path = "_".join(envPath)
			upperPath = path.upper()
			os.environ[upperPath] = event.data

	def sensorControls(self, event):
		if(event.data == 1):
			self.runGetMasking.startVideo()
		else:
			print("HAO")
		print(event.data)
		return event.data

	def listenData(self):
		self.MaskingListen = self.refMasking.listen(self.MaskingHandler)
		self.ConfigListen = self.refSensorConfig.listen(self.HoughHandler)
		self.SensorControl = self.refSensorControll.listen(self.sensorControls)
		self.tempMasking = self.refTempMasking.listen(self.TempMaskingHandler)
	
	def updateWaterHeight(self, val, objectToCamera, waterStatus):
		ref = db.reference("/API/WaterControll")
		sensorData = ref.get()
		dataSend = str(val)
		for key, value in sensorData.items():
			data = ref.child(key).get()
			# Set Sensor ID
			if(data['sensorNo'] == '1'):
				ref.child(key).update({
						"height":{
							"objectDistance":objectToCamera,
						},
						"waterHeight":dataSend,
						"status":{
							"waterStatus": waterStatus	,
							"waterHeight":dataSend,
						}
					})

	def deleteSensorData(self, sensor):
		ref = db.reference("/API/WaterControll")
		sensorData = ref.get()
		for key, value in sensorData.items():
			data = ref.child(key).get()
			if(data['sensorNo'] == str(sensor)):
				ref.child(key).delete()

