from passlib.context import CryptContext
from app.database import get_supabase
from uuid import uuid4

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

def register_user(db, user_data):
    
    existing_user = db.table("users").select("*").eq("username", user_data.username).execute()
    if existing_user.data:
        raise ValueError("Username already exists")

    hashed_password = hash_password(user_data.password)

    new_user = {
        "id": str(uuid4()),  
        "username": user_data.username,
        "password_hash": hashed_password,
        "created_at": "now()",
    }
    response = db.table("users").insert(new_user).execute()

    if not response.data:
        raise ValueError("Failed to create user")

    return response.data[0]  