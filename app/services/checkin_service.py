from datetime import datetime,timedelta
from app.database import get_supabase
import uuid
import logging
from typing import Dict
from app.schemas import CheckInCreate
from app.models import CheckIn
from fastapi import HTTPException

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_checkin(db, checkin_data: CheckInCreate, user_id: str) -> Dict:
    try:
        logger.info(f"Creating check-in for user {user_id} with task: {checkin_data.task_description}")
        
        checkin_id = str(uuid.uuid4())
        
        checkin = CheckIn(
            id=checkin_id,
            user_id=user_id,
            task_description=checkin_data.task_description,
            checked_in_at=datetime.now().isoformat(),
        )
        
        response = db.table("checkins").insert(checkin.dict()).execute()
        
        if response.error:
            logger.error(f"Supabase error: {response.error}")
            raise ValueError(f"Erro ao criar check-in: {response.error}")
        
        logger.info(f"Check-in created successfully: {response.data}")
        return {"success": True, "data": response.data}
    
    except ValueError as ve:
        logger.error(f"ValueError: {str(ve)}")
        raise HTTPException(status_code=500, detail=f"Erro: {str(ve)}")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro inesperado: {str(e)}")
    
    
def get_ranking(db, period: str):
    now = datetime.utcnow()
    if period == "weekly":
        start_date = (now - timedelta(days=7)).isoformat()
    elif period == "monthly":
        start_date = (now - timedelta(days=30)).isoformat()
    else:
        raise ValueError("Período inválido. Use 'weekly' ou 'monthly'.")

    query = (
        db.table("checkins")
        .select("user_id", count="*")  
        .gte("checked_in_at", start_date)  
        .group_by("user_id")  
        .order("count", desc=True) 
        .limit(10)  
    )
    response = query.execute()

    ranking_data = []
    for row in response.data:
        user_id = row["user_id"]
        checkin_count = row["count"]
        ranking_data.append({"user_id": user_id, "checkin_count": checkin_count})

    user_ids = [item["user_id"] for item in ranking_data]
    users_response = db.table("users").select("id", "username").in_("id", user_ids).execute()
    users_map = {user["id"]: user["username"] for user in users_response.data}

    ranking_with_names = []
    for item in ranking_data:
        user_id = item["user_id"]
        username = users_map.get(user_id, "Unknown")  
        ranking_with_names.append({
            "username": username,
            "checkin_count": item["checkin_count"]
        })

    return ranking_with_names