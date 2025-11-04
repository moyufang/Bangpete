我的项目当前的前后端环境是，后端 python+fastapi+pydantic，前端是vue3+ts+scss+axios+pinia+vue-router

在后端中，涉及到歌曲头信息的存取与检索，所有歌曲头（大概1000首左右）保存在"songs_header.json"，格式如下

{
  "3":{
    "song_id":3,
    "title":"ぽっぴん'しゃっふる",
    "diff":[7, 11, 18, 24, -1],
    "jacket_name":"yes_bang_dream",
    "band_id":1
  }
  "20":{
    "song_id":20,
    "title":"シュガーソングとビターステップ",
    "diff":[9, 14, 21, 28, 25],
    "jacket_name":"sugarsong",
    "band_id":3
  },
}

其中 -1 代表该难度不存在

现在，需要根据一些条件从数据库中抓取符合条件的歌曲头，这些条件是“合取”的
（1）难度索引: 0,1,2,3,4
（2）难度数值范围：(level_low, level_high) 范围在 1 ~ 50
（3）乐队ID：指定 band_id 为 main_band=[1, 2, 3, 4, 5, 18, 21, 45] 中的一个，或者不为 main_band

此外，有时候 "songs_header.json" 会增加歌曲

现在，请帮我分析需求，然后告诉我该如何改进后端以支持这一服务，需要用数据库吗？你不需要给出具体代码，告诉我大致方向即可。

----------------------------------------------------------------------------------
我的项目当前的前后端环境是，后端 python+fastapi+pydantic，前端是vue3+ts+scss+axios+pinia+vue-router

我项目的功能形式还没完全想好（能写出文档的那种），但肯定的是，我的项目需要
（1）用户管理：用户注册、用户登录、用户修改用户档案，在前端不同页面保持用户登录状态。补充说明一下，用户权限模型不基于角色，而是基于“用户ID”，比如每个后端模块的每个功能都有一个权限列表，装有合法用户的“用户ID”，“超级用户”（ID=0）在所有权限列表中
（2）权限管理：有些后端功能，需要有权限的用户才能调用，前端调用这些功能的api时，要传递用户信息(cookie?user_token?)，以便后端进行权限检查

流量预测
（1）用户数量：目前仅支持“超级用户”也就是我进行“用户注册”，之后将账号密码交给需要的人


需求
后端该如何支持用户管理？需要用数据库吗？前端如何保持用户的登录状态？cookie如何使用？
请你分析我的需求，然后给出大方向上的指导，我不需要冗杂的代码

----------------------------------------------------------------------------------

专注于 数据库 操作文件的编写，即database.py(将models.py和crud.py合并到 database.py)，我的要求是
（1）用户ID唯一，用户邮箱唯一，用户名无所谓
（2）登录时，自动判定输入的“账号”是用户ID还是用户邮箱，然后查询数据库判断用户是否存在，不存在则失败。密码错误也失败。
（3）数据格式，除超级管理员为0外，正常用户ID为 10000000~99999999，注册成功时，随机选择 10000000~99999999 之间的闲置 ID
（4）超级用户的邮箱是 "super@bangpete.com"

---------------------------------------------------------------------------------
这是后端获取 json 资源 和图片资源的api，样例格式为 "songs_header.json" 与 "j-123.png" "t-233.png"：“@app.get("/data/header/{file_name}")
async def get_data_header(file_name:str):
  try:
    name, ext = file_name.split('.')
    file_path = f"./data/header/{file_name}"
    if os.path.exists(file_path): return FileResponse(file_path)
    else: return {"error":"404"}
  except Exception as e:
    return {"error": str(e)}

@app.get("/data/jacket/{file_name}")
async def get_data_jacket(file_name: str):
  file_path = f"./data/jacket/{file_name}"
  print("Get file_path:", file_path)
  if os.path.exists(file_path):
    return FileResponse(file_path)
  else:
    raise HTTPException(status_code=404, detail="File not found")

if __name__ == "__main__":
  import uvicorn
  uvicorn.run(app, host="127.0.0.1", port=8888)”

我的前端环境是vue+ts+scss+pinia+vue-router
有一个大厅页面 src/pages/Lobby.vue
需要通过api获取json资源和图片资源，数量不多，但是Map的键最好包括文件路径和扩展名
我希望能够写一个src/stores/lobby.ts，将获取的json资源与图片资源缓存起来，然后子组件获取资源时，通过src/stores/lobby.ts里定义的函数或对象来获取。
现在，请你分析我的需求，然后围绕“缓存资源”这个核心需求，分析我的想法是最佳实践吗？浏览器会不会自动缓存资源，即使vue-router转换了路由，我可以修改前后端的所有代码
