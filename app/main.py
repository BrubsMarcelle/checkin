from fastapi import FastAPI, Depends, HTTPException, status
from app.database import get_supabase
from app.auth import authenticate_user, create_access_token
from app.services.auth_service import register_user
from app.schemas import UserCreate, UserLogin, CheckInCreate
from app.auth import get_current_user
from app.services.checkin_service import create_checkin, get_ranking

app = FastAPI()

@app.post("/register/", status_code=status.HTTP_201_CREATED)
async def register(user: UserCreate, db=Depends(get_supabase)):
    try:
        user_data = register_user(db, user)
        return {"message": "User registered successfully", "user_id": user_data["id"]}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@app.post("/login/")
async def login(user: UserLogin, db=Depends(get_supabase)):
    user_data = authenticate_user(db, user.username, user.password)
    if not user_data:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": user_data["username"]})
    return {"access_token": token, "token_type": "bearer"}

@app.post("/checkin/")
async def checkin(checkin: CheckInCreate, current_user=Depends(get_current_user), db=Depends(get_supabase)):
    user_id = current_user["id"] 
    return create_checkin(db, checkin, user_id)

@app.get("/ranking/")
async def ranking(period: str, db=Depends(get_supabase)):
    if period not in ["weekly", "monthly"]:
        raise HTTPException(status_code=400, detail="Período inválido. Use 'weekly' ou 'monthly'.")
    return get_ranking(db, period)