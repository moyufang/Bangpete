# main.py
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.responses import FileResponse, StreamingResponse
import os

from core.search.song import router as core_search_song_router

app = FastAPI(title="My API", version="1.0.0")
app.include_router(core_search_song_router, prefix="/core/search/song")

class Item(BaseModel):
    name: str
    description: str = None
    price: float
    tax: float = None

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
  uvicorn.run(app, host="0.0.0.0", port=8000)