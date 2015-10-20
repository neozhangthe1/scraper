__author__ = 'yutao'

from pymongo import MongoClient

col = MongoClient(host="166.111.7.105")["douban"]["photo"]
f_in = open("ids.txt")
ids = []
cnt = 0
for line in f_in:
    print(cnt)
    cnt += 1
    x = line.strip()
    if not col.find({"movie_id": line.strip()}):
        ids.append(x)

f_out = open("ids.txt", "w")
for i in ids:
    f_out.write(i + "\n")

f_out.close()