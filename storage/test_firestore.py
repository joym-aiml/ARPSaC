
import firebase_admin
from firebase_admin import credentials, firestore

print("Starting Firestore connection...")

#Load credentials
cred = credentials.Certificate("config/firebase_credentials.json")
firebase_admin.initialize_app(cred)
print("Firebase initialized.")

#Firestore Client
db = firestore.client()

#Test Write
def test_connection():
    print("Attempting Firestore write...")
    doc_ref = db.collection("test_collection").document("doc")
    doc_ref.set({
        "message": "Hello ARPSaC",
        "status": "success"
    })

    print("Firestore write successful")

if __name__ == "__main__":
    test_connection()