from app.services.checkin_service import create_checkin, get_ranking
from app.database import get_supabase

def test_create_checkin():
    db = get_supabase()
    checkin_data = {"task_description": "Test Task"}
    user_id = "test_user_id"
    result = create_checkin(db, checkin_data, user_id)
    assert "id" in result[0]

def test_get_ranking():
    db = get_supabase()
    ranking = get_ranking(db, "weekly")
    assert isinstance(ranking, list)