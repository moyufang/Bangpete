from fastapi import FastAPI
from pydantic import BaseModel
from fastapi import FastAPI, APIRouter, Query
from fastapi.responses import FileResponse, StreamingResponse
import json
import re
import bisect
from pydantic import BaseModel, field_validator, model_validator

from configuration import *
from utils.Matcher import Matcher

special_char = \
  r"[ /_\(\)\[\]\{\}!?:,.@#$%^&*=\"\'\-—（）【】！？：，。”“‘’「」　＆＊＝×·・★☆◎－∞♪\n\r\t↑]"

def shave_str(title:str):
  return re.sub(special_char, '', title).lower()

with open(SONGS_HEADER_PATH, 'r', encoding='utf-8') as f:
  songs_header = json.load(f)
  
matcher = Matcher({k:shave_str(songs_header[k]['title']) for k in songs_header})

router = APIRouter()

@router.get("/")
async def search(
  q: str = Query(..., min_length=1, max_length=100),
  way:str = 'unknown'
):
  if way not in ['id', 'str']:
    if str.isdigit(q): way = 'id'
    else: way = 'str'
  try:
    if way == 'id':
      if q in songs_header: return {"id":q,"header":songs_header[q]}
      else: raise ValueError(f"song_id '{q}' doesn't exist")
    else:
      q = special_char(q)
      id = matcher.match(q)
      return {"id":id, "header":songs_header[q]}
  except Exception as e:
    return {"error": str(e)}

# 0 代表任意乐队都行, -1 代表主乐队之外的任意乐队
MAIN_BANG = [-1, 0, 1, 2, 3, 4, 5, 18, 21, 45]
SONGS_HEADER_PATH = './data/header/songs_header.json'

class SongConstraint(BaseModel):
  diff: int       # 难度索引 0-4
  level_low: int        # 最低难度 1-50
  level_high: int       # 最高难度 1-50
  band_id: int          # 乐队ID
  start_count: int = 1  # 分页参数（如果需要）
  page_size: int = 20
  
  @field_validator('diff')
  def check_diff(cls, v):
    return min(max(v, 0), 4)
  
  @field_validator('level_low', 'level_high')
  def check_level(cls, v):
    return min(max(v, 0), 50)

  @model_validator(mode='after')
  def check_level_consistency(self):
    if self.level_low > self.level_high:
      self.level_low = self.level_high 
    return self

  # 只要不是主乐队，后端的处理逻辑都是对-1的处理逻辑
  @field_validator('band_id')
  def check_band_id(cls, v):
    if v in MAIN_BANG: return v
    else: return -1
    
  @field_validator('start_count', 'page_size')
  def check_page(cls, v):
    return max(1, v)
  
class SongsHeader:
  def __init__(self, songs_header):
    self.songs_header = songs_header
  def build(self):
    self.tree = {band_id:{0:[],1:[],2:[],3:[],4:[]} for band_id in MAIN_BANG}
    for k in self.songs_header:
      item = self.songs_header[k]
      """item 格式
      {
        "song_id":518,
        "title":"HOT LIMIT",
        "diff":[5, 12, 22, 25, -1],
        "jacket_name":"518_hot_limit",
        "band_id":1
      }
      """
      band_id = item['band_id']
      if band_id not in MAIN_BANG: band_id = -1
      
      for bid in [band_id, 0]:
        for diff, level in enumerate(item['diff']):
          if level == -1: continue
          self.tree[bid][diff].append((level,item['song_id']))
    for k in self.tree:
      item = self.tree[k]
      for diff in [0, 1, 2, 3, 4]:
        item[diff].sort()
  def get_songs(self, song_constraint: SongConstraint):
    sc = song_constraint
    # 如果band_id不在tree中，返回空
    if sc.band_id not in self.tree: return {}, True
    level_list = self.tree[sc.band_id][sc.diff]

    # 使用二分查找确定范围
    left_index = bisect.bisect_left(level_list, (sc.level_low, 0))
    right_index = bisect.bisect_right(level_list, (sc.level_high, 1000000000))

    total_count = right_index - left_index
    start_index = left_index + sc.start_count - 1
    if start_index >= right_index: return {}, True
    end_index = min(start_index + sc.page_size, right_index)
    song_slice = level_list[start_index:end_index]

    sub_songs_header = {}
    for level, song_id in song_slice:
      song_id_str = str(song_id)
      if song_id_str in self.songs_header:
        sub_songs_header[song_id_str] = self.songs_header[song_id_str]

    is_exhausted = end_index >= right_index
    return sub_songs_header, is_exhausted

with open(SONGS_HEADER_PATH, 'r', encoding='utf-8') as f:
  songs_header = json.load(f)
songs_header = SongsHeader(songs_header)

@router.get("/list/")
async def search(song_constraint:SongConstraint):
  sub_songs_header, is_exhausted = songs_header.get_songs(song_constraint) 
  return {
    "sub_songs_header": sub_songs_header,
    "is_exhausted": is_exhausted
  }