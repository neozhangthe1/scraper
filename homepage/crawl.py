from pymongo import MongoClient
import requests
import codecs

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
		f_out = codecs.open(str(item["_id"]) + ".html", "w", encoding="utf-8")
		f_out.write(res.text)
		f_out.close()
		cnt += 1
		print cnt
	except Exception, e:
		print e