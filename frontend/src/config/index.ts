// src/config.ts
export const BACKEND_ADDRESS = process.env.NODE_ENV === 'production' 
  ? 'https://生产环境域名' 
  : 'http://127.0.0.1:8888'

export const SONG_AUTHORS_URL = 'header/song_authors.json'
export const SONGS_HEADER_URL = 'header/songs_header.json'

export const CARD_DEFAULT_JACKET_URL = '@/src/assets/imgs/card_default_jacket.png'
export const DATA_URL = 'http://127.0.0.1:8888/data/'