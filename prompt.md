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