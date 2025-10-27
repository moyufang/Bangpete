
def get_edit_dis(s1, s2, eo=-1):
  l1, l2 = len(s1), len(s2)
  if l1 > l2: l1,l2 = l2,l1; s1,s2=s2,s1
  if eo < 0: eo = max(l1, l2)
  f = [min(eo,i) for i in range(l2+1)]
  for i in range(1, 1+l1):
    c = s1[i-1]
    for j in range(min(i+eo-1, l2), max(0, i-eo), -1):
      t = f[j-1]+int(c!=s2[j-1])
      f[j] = t if t <= f[j] else f[j]+1
    if i <= eo: f[0] += 1
    for j in range(1+max(0,i-eo), min(i+eo, l2+1)):
      f[j] = min(f[j], f[j-1]+1)
  return f[l2]

# 'id' must be 'int' or can tranform into 'int'
# '-1' is used to represent 'unknown'
class Matcher:
  def __init__(self, id2pattern:str):
    self.id2pattern = id2pattern
    
    self.char2count = {} # 记录每个字符出现在哪些id，以及出现的次数
    for id in self.id2pattern:
      pattern = self.id2pattern[id]
      for c in pattern:
        if c not in self.char2count:
          self.char2count[c] = {id:1}
        else:
          if id not in self.char2count[c]: self.char2count[c][id] = 1
          else: self.char2count[c][id] += 1
    
  def match(self, s):
    char_cnt = {}
    id_cnt = {}
    for c in s:
      if c not in char_cnt: char_cnt[c] = 1
      else: char_cnt[c] += 1
    for c in char_cnt:
      if c not in self.char2count: continue
      char_map = self.char2count[c]
      for idx in char_map:
        w = 1.0 if c.islower() else 1.0 
        # 每种字符的得分，根据数差递减
        t = w/(1+abs(char_map[idx] - char_cnt[c]))**2 
        if idx not in id_cnt: id_cnt[idx] = t
        else: id_cnt[idx] += t
    tar_id, score = -1, 0.0
    l = len(s)
    for idx in id_cnt:
      # 字符串长度得分
      t = id_cnt[idx]+1.0/(1+abs(l-len(self.id2pattern[str(idx)][1])))
      if t > score: tar_id, score = idx, t
    if tar_id != -1:
      # 预选目标，之后如果得分小于 score*0.8 的，都抛弃（即剪枝掉）
      eo = get_edit_dis(s, self.id2pattern[str(tar_id)])
    for idx in id_cnt:
      t = id_cnt[idx]+2.0/(1+abs(l-len(self.id2pattern[str(idx)][1])))
      if t > score*0.8 or l <= 4:
        eo_tmp = get_edit_dis(s, self.id2pattern[str(idx)], eo)
        if eo_tmp < eo: eo = eo_tmp; tar_id = idx
        # print("id:%d title:%s score:%lf eo:%d"%(
        # 	idx, self.id2pattern[idx][1], t, eo_tmp))
    if tar_id != -1:
      score = id_cnt[tar_id]+2.0/(1+abs(l-len(self.id2pattern[str(tar_id)])))
    #print("tar_id:%d title:%s score:%lf"%(tar_id, self.id2pattern[tar_id][1], score))
    return tar_id
  
if __name__ == '__main__':
  
  matcher = Matcher({"1": "abcde", "2":"我是傻逼", "3":"命题r"})
  
  res = matcher.match('命r')
  print(res)