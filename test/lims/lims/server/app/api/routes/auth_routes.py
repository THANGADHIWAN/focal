# from fastapi import APIRouter, Depends, HTTPException, status
# from fastapi.security import OAuth2PasswordRequestForm
# from sqlalchemy.orm import Session
# from datetime import timedelta
# from typing import Dict, Any

# from app.db.database import get_db
# from app.utils.auth import authenticate_user, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
# from app.schemas import ApiResponse

# router = APIRouter(
#     prefix="/auth",
#     tags=["authentication"],
#     responses={401: {"description": "Unauthorized"}},
# )

# @router.post("/token", response_model=ApiResponse)
# async def login_for_access_token(
#     form_data: OAuth2PasswordRequestForm = Depends(),
#     db: Session = Depends(get_db)
# ):
#     """
#     Login endpoint to get an access token
#     """
#     user = authenticate_user(db, form_data.username, form_data.password)
    
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect email or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
    
#     # Create access token
#     access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = create_access_token(
#         data={"sub": user.email}, expires_delta=access_token_expires
#     )
    
#     return {
#         "data": {
#             "access_token": access_token,
#             "token_type": "bearer",
#             "user_id": user.id,
#             "email": user.email,
#             "name": user.name,
#             "role": user.role,
#         },
#         "status": 200,
#         "success": True
#     }
