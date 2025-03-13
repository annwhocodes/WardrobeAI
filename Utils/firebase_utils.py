import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("utils\wardrobeai-838ee-firebase-adminsdk-fbsvc-d7f07a9b0c.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

def fetch_user_wardrobe(user_id):
    doc_ref = db.collection("wardrobes").document(user_id)
    doc = doc_ref.get()
    if doc.exists:
        return doc.to_dict().get("items", [])
    return []
