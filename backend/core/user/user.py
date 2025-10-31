from fastapi import APIRouter, Depends, Request
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import CookieTransport, AuthenticationBackend, JWTStrategy
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase, SQLAlchemyBaseUserTable
from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Mapped, mapped_column
from datetime import datetime
from typing import Optional
import uuid
from sqlalchemy.dialects.postgresql import UUID
import os
from configuration import *

# 创建路由器
router = APIRouter()

# 数据库配置
DATABASE_URL = "sqlite://" + USER_DATABASE_PATH

Base = declarative_base()

# 定义 SQLAlchemy 用户表 - 修复主键问题
class UserTable(Base, SQLAlchemyBaseUserTable):
    __tablename__ = "users"
    
    # 显式定义所有需要的列，包括主键
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(String(length=320), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(length=1024), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    
    # 添加你的自定义字段
    user_name = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

# Pydantic 模型
from pydantic import BaseModel, EmailStr, ConfigDict
from uuid import UUID

# 基础用户模型
class UserRead(BaseModel):
    id: UUID
    email: EmailStr
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False
    user_name: str
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    user_name: str
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False

class UserUpdate(BaseModel):
    user_name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None
    is_superuser: Optional[bool] = None
    is_verified: Optional[bool] = None

# 数据库设置
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建表
Base.metadata.create_all(bind=engine)

def get_user_db():
    session = SessionLocal()
    try: 
        yield SQLAlchemyUserDatabase(session, UserTable)
    finally: 
        session.close()

# 认证配置
cookie_transport = CookieTransport(
    cookie_name="auth_token",
    cookie_max_age=LIFETIME_SECONDS,
    cookie_httponly=True,
    cookie_secure=False,
    cookie_samesite="lax"
)

def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(
        secret=SECRET_KEY,
        lifetime_seconds=LIFETIME_SECONDS
    )

auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)

# 用户管理器
from fastapi_users import BaseUserManager, UUIDIDMixin

class UserManager(UUIDIDMixin, BaseUserManager[UserTable, UUID]):
    reset_password_token_secret = SECRET_KEY
    verification_token_secret = SECRET_KEY
    
    async def on_after_register(self, user: UserTable, request: Optional[Request] = None):
        print(f"用户 {user.id} 注册成功")
    
    async def on_after_forgot_password(
        self, user: UserTable, token: str, request: Optional[Request] = None
    ):
        print(f"用户 {user.id} 请求重置密码. 令牌: {token}")
    
    async def on_after_request_verify(
        self, user: UserTable, token: str, request: Optional[Request] = None
    ):
        print(f"验证请求用户 {user.id}. 令牌: {token}")

async def get_user_manager(user_db: SQLAlchemyUserDatabase = Depends(get_user_db)):
    yield UserManager(user_db)

# 创建 FastAPIUsers 实例
fastapi_users = FastAPIUsers[UserTable, UUID](
    get_user_manager,
    [auth_backend],
)

# 将路由添加到路由器
# 认证路由
router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["认证"]
)

router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["认证"]
)

router.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["认证"]
)

router.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["认证"]
)

# 用户管理路由
router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["用户"]
)

# 自定义路由示例
@router.get("/me")
async def get_current_user_info(
    user: UserTable = Depends(fastapi_users.current_user())
):
    """获取当前用户信息"""
    return {
        "user_id": user.id,
        "email": user.email,
        "user_name": user.user_name,
        "is_active": user.is_active,
        "is_superuser": user.is_superuser,
        "is_verified": user.is_verified,
        "created_at": user.created_at
    }

@router.get("/protected-test")
async def protected_test_route(
    user: UserTable = Depends(fastapi_users.current_user(active=True))
):
    """受保护的路由测试"""
    return {
        "message": f"你好 {user.user_name}! 这是一个受保护的路由",
        "user_id": user.id
    }

# 导出依赖项
current_active_user = fastapi_users.current_user(active=True)
current_superuser = fastapi_users.current_user(active=True, superuser=True)

# 初始化函数
def init_user_system():
    """初始化用户系统"""
    Base.metadata.create_all(bind=engine)
    print("用户系统初始化完成")

# 导出路由器实例
__all__ = ["router", "current_active_user", "current_superuser", "init_user_system"]