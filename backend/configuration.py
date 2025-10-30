
#============  文件路径 ============#

ASSETS_PATH = './data/assets/'
JACKET_PATH = './data/jacket/'
RAW_SONGS_HEADER_PATH = './data/header/raw_songs_header.json'
SONGS_HEADER_PATH = './data/header/songs_header.json'
SONG_AUTHORS_PATH = './data/header/song_authors.json'
USER_DATABASE_PATH = "./data/user/users.db"

#============ User配置 ============#

SUPER_USER_ID = 0

# JWT配置 
SECRET_KEY = "your-secret-key"  # 生产环境要使用环境变量
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 30
LIFETIME_SECONDS = 3600

#============ 其它 ============#

MAIN_BANG = [1, 2, 3, 4, 5, 18, 21, 45]
