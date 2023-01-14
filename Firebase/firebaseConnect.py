import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import os

class FirebaseConnect:
	def __init__(self):
		ROOT_DIR = os.path.abspath(os.curdir)
		cred_obj = credentials.Certificate(ROOT_DIR+'/FirebaseCertificate/iot-ta-cacb8-firebase-adminsdk-ttfjb-56402dadcc.json')
		default_app = firebase_admin.initialize_app(cred_obj, {
			'databaseURL':'https://iot-ta-cacb8-default-rtdb.asia-southeast1.firebasedatabase.app/'
			})
		default_app
	
	def addSensor(self, sensor):
		ref = db.reference("/API/WaterControll")
		data = {'sensorNo': str(sensor), 'waterHeight': 0, 'status': 'stopped'}
		ref.push().set(data)

	def readData(self):
		ref = db.reference("/API/WaterControll")
		sensorData = ref.get()
		for key, value in sensorData.items():
			data = ref.child(key).get()
			print(data)

	def updateWaterHeight(self, val, cameraheight, objectToCamera, diameter):
		ref = db.reference("/API/WaterControll")
		sensorData = ref.get()
		dataSend = str(val)
		for key, value in sensorData.items():
			data = ref.child(key).get()
			# Set Sensor ID
			if(data['sensorNo'] == '1'):
				ref.child(key).update({
						"waterHeight":dataSend,
						"satuan": "Cm",
						"cameraHeight": cameraheight,
						"objectToCameraDistance": objectToCamera,
						"ballDiameter": diameter
					})

	def deleteSensorData(self, sensor):
		ref = db.reference("/API/WaterControll")
		sensorData = ref.get()
		for key, value in sensorData.items():
			data = ref.child(key).get()
			if(data['sensorNo'] == str(sensor)):
				ref.child(key).delete()

