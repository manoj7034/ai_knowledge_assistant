from fastapi import APIRouter
from app.api.v1.auth import router as auth_router
from app.api.v1.users import router as users_router
from app.api.v1.document import router as document_router
from app.api.v1.search import router as search_router
from app.api.v1.chat import router as chat_router


api_router = APIRouter()

api_router.include_router(auth_router)
api_router.include_router(users_router)
api_router.include_router(document_router)
api_router.include_router(search_router)
api_router.include_router(chat_router)