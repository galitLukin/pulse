from fastapi import APIRouter
from typing import List
from app.db.queries.checks import list_checks
from app.models.api import CheckResponse

router = APIRouter()


@router.get("", response_model=List[CheckResponse])
async def get_checks():
    """Get list of all checks"""
    return list_checks()
