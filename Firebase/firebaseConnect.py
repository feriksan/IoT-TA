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
				
	def stream_handler(self, message): # put
		print(message.data)
		os.environ['SATUAN'] = message.data['satuan']
		os.environ['CAMERA_HEIGHT'] = message.data['cameraHeight']
		os.environ['OBJECT_DIAMETER'] = message.data['ballDiameter']

	def listenData(self):
		ref = db.reference("/API/WaterControll/-N3c_56YSzzzcuGy04tw/staticParameter")
		my_stream = ref.listen(self.stream_handler)
	
	def updateWaterHeight(self, val, objectToCamera, waterStatus):
		ref = db.reference("/API/WaterControll")
		sensorData = ref.get()
		dataSend = str(val)
		print(dataSend)
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
							"waterStatus": waterStatus	
						}
					})

	def deleteSensorData(self, sensor):
		ref = db.reference("/API/WaterControll")
		sensorData = ref.get()
		for key, value in sensorData.items():
			data = ref.child(key).get()
			if(data['sensorNo'] == str(sensor)):
				ref.child(key).delete()

