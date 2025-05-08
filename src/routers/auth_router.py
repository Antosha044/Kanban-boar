from fastapi import APIRouter, HTTPException
from src.schemas.auth import UserRegister, Token
from src.core.jwt_utils import create_access_token
from src.core.database import AsyncSessionLocal
from src.models.models import User
from sqlalchemy import select
from passlib.context import CryptContext
import uuid

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/register", response_model=Token)
async def register_user(user_data: UserRegister):
    async with AsyncSessionLocal() as session:
        #проверка email
        result = await session.execute(select(User).where(User.email == user_data.email))
        existing_user = result.scalar_one_or_none()

        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")

        hashed_password = pwd_context.hash(user_data.password)

        new_user = User(
            id=uuid.uuid4(),
            username=user_data.username,
            email=user_data.email,
            full_name=user_data.full_name,
            password=hashed_password
        )

        session.add(new_user)
        await session.commit()

        access_token = create_access_token(data={"sub": str(new_user.id)})

        return Token(access_token=access_token)
