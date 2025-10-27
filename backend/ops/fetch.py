from enum import Enum, auto
import requests as rq
import re
import os
import json
from utils.json_refiner import *
from configuration import *

class Mode(Enum):
  FetchHeader = auto()       # 爬取歌单头
  FetchOne = auto()          # 爬取单首歌谱
  FetchLack = auto()         # 根据 sheets_header.json 和 sheets/*.bestdori 爬取缺少的歌谱
  FetchAuthors = auto()       # 爬取演出乐队
  FreeFetch = auto()

region = 'cn'
jacket_dir = JACKET_PATH
thumb_dir = JACKET_PATH
songs_header_path = SONGS_HEADER_PATH
raw_songs_header_path = RAW_SONGS_HEADER_PATH

headers = {
  "user-agent": r"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
  "Requests":"",
  "Upgrade-Insecure-":"1",
  "Sec-Ch-Ua": r'"Google Chrome";v="125", "Chromium";v="125","Not.A/Brand";v="24"',
  "Sec-Ch-Ua-Mobile": "?0",
  "Sec-Ch-Ua-Platform": "Windows",
  "Sec-Fetch-User":"?1",
  "Sec-Fetch-Site":"same-origin",
  "Sec-Fetch-Mode":"navigate",
  "Sec-Fetch-Dest":"document",
  "Priority":"u=0,i",
  "Cookie":"token=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MTA1NTY0LCJpYXQiOjE3MTY1OTU1NzIsImV4cCI6MTcxOTE4NzU3MiwiaXNzIjoiQmVzdGRvcmkvQXV0aCJ9.awpCcovCxaxIPEqxWV-iWQ5Kqp_KQpLkhI01iS9M5lPAqmj6kC7F9FopLZZqBHWiichGZOX7HHJ-0Wa-5caOXw; _gid=GA1.2.612823731.1717638853; _ga_W15VJ513VC=GS1.1.1717638852.85.1.1717638970.0.0.0; _ga=GA1.1.1286663543.1714844449",
  "Cache-Control":"max-age=0",
  "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
  "Accept-Encoding":"utf-8, gzip, deflate",
  "Accept-Language":"zh-CN,zh;q=0.9",
}

def get_all_header_url():
  return r"https://bestdori.com/api/songs/all.5.json"

def get_musicjacket_url(jacket_id:int):
  return f"https://bestdori.com/api/explorer/{region}/assets/musicjacket/musicjacket{jacket_id}.json"

def get_jacket_url(song_id:int, jacket_name, is_thumb:bool=False):
  pack_id = (int(song_id)+9)//10 * 10
  return f'https://bestdori.com/assets/{region}/musicjacket/musicjacket{pack_id}_rip/assets-star-forassetbundle-startapp-musicjacket-musicjacket{pack_id}-{jacket_name}-{'thumb'if is_thumb else 'jacket'}.png'

def get_rp(mode:Mode, url:str, file_path:str, max_depth=[2, 0, 0], indent='  ', ty='json', is_breif:bool=False):
  rp = rq.get(url=url, headers=headers)
  print(f"Mode: {mode} Fetching \"{url}\" ...")
  if not is_breif:
    print("response:")
    print("\tstatus_code", rp.status_code)
    print("\tencoding", rp.encoding)
    print("\tcookies", rp.cookies)
    print("\tencoding", rp.headers.get('Content-Encoding'))
  if rp.status_code != 200:
    print("Fetching failed with: ", file_path)
    exit(0)
  if ty == 'json':
    data = json.loads(rp.content.decode('utf-8'))
    with open(file_path, "w") as f: json.dump(data, f)
    refine(file_path, max_depth=max_depth, indent=indent)
  elif ty == 'png':
    data = rp.content
    with open(file_path, 'wb') as f: f.write(rp.content)
  if not is_breif:
    print(f"Saved as \"{file_path}\"")
    print()
  return rp, data

def fetch_songs_header():
  url = get_all_header_url()
  file_path = raw_songs_header_path
  rp, data = get_rp(Mode.FetchHeader, url, file_path)
  
  songs_header = {"-1":{
    "song_id": -1,
    "title": '',
    "diff": [-1, -1, -1, -1, -1],
    "jacket_name": '',
    "band_id": -1,
  }}
  for song_id in data:
    item = data[song_id]
    diff = item['difficulty']
    titles = item['musicTitle']
    jacket_name = item['jacketImage'][0]
    band_id = item['bandId']
    
    title = None
    sorted_titles = [titles[3], titles[0], titles[1]]
    for t in sorted_titles:
      if t != None: title = t; break
    if title == None:
      print(song_id, title, titles)
    
    songs_header[song_id] = {
      "song_id": int(song_id),
      "title": title,
      "diff": [
        int(diff['0']['playLevel']),
        int(diff['1']['playLevel']),
        int(diff['2']['playLevel']),
        int(diff['3']['playLevel']),
        int(diff['4']['playLevel'] if '4' in diff else -1)],
      "jacket_name": jacket_name,
      "band_id": band_id,
    }
    
    
  file_path = songs_header_path
  with open(file_path, "w", encoding='utf-8') as file:
    json.dump(songs_header, file)
  refine(file_path, [2, 0, 0])
  print(f"Saved as \"{file_path}\"")
  print()
  
def fetch_one(img_url:int):
  file_path = jacket_dir+"test.png"
  rp, data = get_rp(Mode.FetchOne, img_url, file_path, ty='png')

def fetch_lack():
  with open(songs_header_path, "r", encoding="utf-8") as file:
    sheets_header = json.load(file)
  for k in sheets_header:
    item = sheets_header[k]
    song_id = item['song_id']
    if song_id == -1: continue
    
    url = get_jacket_url(song_id, item['jacket_name'], is_thumb=False)
    file_path = jacket_dir+"j-%s.png"%(song_id)
    if not os.path.isfile(file_path):
      rp, data = get_rp(Mode.FetchLack, url, file_path, ty='png', is_breif=True)
    
    url = get_jacket_url(item[0], item[7], is_thumb=True)
    file_path = jacket_dir+"t-%s.png"%(song_id)
    if not os.path.isfile(file_path):
      rp, data = get_rp(Mode.FetchLack, url, file_path, ty='png', is_breif=True)

def fetch_song_authors():
  url = 'https://bestdori.com/api/bands/all.1.json'
  file_path = SONG_AUTHORS_PATH
  rp, data = get_rp(Mode.FreeFetch, url, file_path, max_depth=[1, 0, 0])
  
  with open(file_path, "r", encoding='utf-8') as f:
    data = json.load(f)
  
  new_data = {}
  for i in data:
    item = data[i]
    bang_names = item['bandName']
    for j in [3, 0, 1, 2, 4]:
      if bang_names[j] is not None: bang_name = bang_names[j]; break
    new_data[int(i)] = {"bang_name": bang_name, "song_author_id": int(i)}
  new_data['hot_index'] = {
    'ppp':1, 'ag':2, 'hhw':3, 'pp':4, 'r':5, 'ras':18, 'm':21, 'go':45
  }
  refine_dump(new_data, file_path, max_depth=[1, 0, 0])

def free_fetch():
  pass

def start(mode:Mode):
  if mode == Mode.FetchHeader:
    fetch_songs_header()
  elif mode == Mode.FetchOne:
    fetch_one(r'https://bestdori.com/assets/en/musicjacket/musicjacket600_rip/assets-star-forassetbundle-startapp-musicjacket-musicjacket600-591_kyukurarin-jacket.png')
  elif mode == Mode.FetchLack:
    fetch_lack()
  elif mode == Mode.FetchAuthors:
    fetch_song_authors()
  else:
    free_fetch()
    
if __name__ == '__main__':
  start(Mode.FetchHeader)