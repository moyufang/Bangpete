# main.py
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.responses import FileResponse, StreamingResponse
import os

from core.search.song import router as core_search_song_router
from fastapi import FastAPI, Depends
from contextlib import asynccontextmanager

# # 导入用户系统
# from core.user.user import router as user_router, init_user_system, current_active_user
# from core.user.user import User  # 导入用户模型
#
# # 应用生命周期
# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     # 启动时的初始化
#     print("应用启动中...")
#     init_user_system()  # 初始化用户系统
#     yield
#     # 关闭时的清理
#     print("应用关闭")

# 创建 FastAPI 应用
app = FastAPI(
    title="bangpete",
    description="邦邦竞演辅助工具",
    version="0.0.0",
    # lifespan=lifespan
)
# app.include_router(user_router, prefix="/user")
app.include_router(core_search_song_router, prefix="/core/search/song")

# 你的其他路由
@app.get("/")
async def root():
    """根路由"""
    return {"message": "欢迎使用我的 FastAPI 项目"}

@app.get("/public-route")
async def public_route():
    """公开路由，不需要认证"""
    return {"message": "这是一个公开的路由，任何人都可以访问"}

# @app.get("/protected-route")
# async def protected_route(user: User = Depends(current_active_user)):
#     """受保护的路由，需要登录"""
#     return {
#         "message": f"你好 {user.user_name}! 这是一个受保护的路由",
#         "user_info": {
#             "id": user.id,
#             "email": user.email,
#             "user_name": user.user_name
#         }
#     }

#============ Pratice ============#

@app.get("/data/jacket/{file_name}")
async def root(file_name:str):
  try:
    name, ext = file_name.split('.')
    file_path = f"./data/jacket/{file_name}"
    if os.path.exists(file_path): return FileResponse()
    else: return {"error":"404"}
  except Exception as e:
    return {"error": str(e)}

if __name__ == "__main__":
  import uvicorn
  uvicorn.run(app, host="127.0.0.1", port=8888)