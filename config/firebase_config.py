# config/firebase_config.py
import os
import json
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, firestore

load_dotenv()

def initialize_firebase():
    """Initialize Firebase Admin SDK"""
    try:
        # Check if Firebase is already initialized
        if not firebase_admin._apps:
            # Use service account key from environment variables
            service_account_info = {
                "type": "service_account",
                "project_id": os.getenv('FIREBASE_PROJECT_ID'),
                "private_key_id": os.getenv('FIREBASE_PRIVATE_KEY_ID'),
                "private_key": os.getenv('FIREBASE_PRIVATE_KEY').replace('\\n', '\n'),
                "client_email": os.getenv('FIREBASE_CLIENT_EMAIL'),
                "client_id": os.getenv('FIREBASE_CLIENT_ID'),
                "auth_uri": os.getenv('FIREBASE_AUTH_URI'),
                "token_uri": os.getenv('FIREBASE_TOKEN_URI'),
                "auth_provider_x509_cert_url": os.getenv('FIREBASE_AUTH_PROVIDER_X509_CERT_URL'),
                "client_x509_cert_url": os.getenv('FIREBASE_CLIENT_X509_CERT_URL')
            }
            
            cred = credentials.Certificate(service_account_info)
            firebase_admin.initialize_app(cred)
        
        return firestore.client()
    except Exception as e:
        print(f"Firebase initialization error: {e}")
        return None

# Initialize Firebase
db = initialize_firebase()

if db:
    print("✅ Firebase initialized successfully")
else:
    print("❌ Firebase initialization failed") 