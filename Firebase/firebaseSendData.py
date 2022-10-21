from firebase_admin import db

ref = db.reference("/")
jsonObj = {
    "nama": "ferdi"
}