from pymongo import MongoClient
import requests
client = MongoClient('mongodb://yutao:911106zyt@yutao.us:30017/bigsci')
db = client["bigsci"]
col = db["people"]
data = col.find({"contact.homepage":{"$exists":True}})
print "data query finished"

cnt = 0
for item in data:
	print item["_id"], item["name"]
	hp = item["contact"]["homepage"]
	try:
		print hp
		res = requests.get(hp)
		f_out = open(item["_id"] + ".html", "w")
		f_out.write(res.text)
		f_out.close()
		cnt += 1
		print cnt
	except:
		pass