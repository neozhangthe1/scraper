from pymongo import MongoClient
import requests
import codecs
import eventlet
eventlet.monkey_patch()

client = MongoClient('mongodb://yutao:911106zyt@yutao.us:30017/bigsci')
db = client["bigsci"]
col = db["people"]
data = col.find({"contact.homepage":{"$exists":True}}, skip=6450 + 700, timeout=False)
print "data query finished"

cnt = 6450 + 700
for item in data:
	print item["_id"], item["name"]
	hp = item["contact"]["homepage"]
	try:
		print hp
		with eventlet.Timeout(10):
			res = requests.get(hp)
			f_out = codecs.open(str(item["_id"]) + ".html", "w", encoding="utf-8")
			f_out.write(res.text)
			f_out.close()
			cnt += 1
			print cnt
	except Exception, e:
		print e