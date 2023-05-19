from Firebase.firebaseConnect import FirebaseConnect
from src.ObjectTracking.getMasking import getMasking

class CronJob:
    def __init__(self):
        self.firebase = FirebaseConnect()
        self.firebase.listenData()
    
    def runGetMasking(self):
        getMask = getMasking(self.firebase)
        getMask.startVideo()