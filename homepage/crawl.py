from pymongo import MongoClient
import requests
import codecs
import json

url_to_id = json.load(codecs.open("url.json"))
del url_to_id[""]
for url in url_to_id:
	_id = url_to_id[url]
	print _id, url
	try:
		res = requests.get(url, timeout=10)
		f_out = codecs.open(_id + ".html", "w", encoding="utf-8")
		f_out.write(res.text)
		f_out.close()
		cnt += 1
		print cnt
	except Exception, e:
		print e

def get_urls():
    client = MongoClient('mongodb://yutao:911106zyt@yutao.us:30017/bigsci')
    db = client["bigsci"]
    col = db["people"]
    data = col.find({"contact.homepage":{"$exists":True}}, timeout=False)
    url_to_id = {}
    cnt = 0
    for item in data:
    	cnt += 1
    	hp = item["contact"]["homepage"]
    	print cnt, hp
    	url_to_id[hp] = str(item["_id"])
    import json
	f_out = codecs.open("url.json", "w", encoding="utf-8")
	json.dump(url_to_id, f_out)
	f_out.close()