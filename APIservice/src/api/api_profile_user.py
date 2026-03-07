from fastapi import APIRouter, Depends

from dependencies.auth_deps import get_active_current_user


profile_router = APIRouter(
    prefix='/profile',
    tags=['profile']
)


@profile_router.get('/info')
async def get_profile_info(current_user = Depends(get_active_current_user)):
    return current_user