from pymongo import MongoClient
import requests
import json
import codecs


def get_university_scores():
    scores = []
    url = "http://data.api.gkcx.eol.cn/soudaxue/queryProvinceScore.html?messtype=jsonp&url_sign=queryProvinceScore&provinceforschool=&schooltype=&page=%s&size=50&keyWord=&schoolproperty=&schoolflag=&schoolsort=&province=&fsyear=&fstype=&zhaoshengpici=&suiji=&callback=jQuery18308446977760307199_1460561576563&_=1460561578247"
    for i in range(6834, 36120):
        if i % 100 == 0:
            print(i, len(scores))
        resp = requests.get(url % i)
        data = json.loads(resp.text.replace(resp.text.split("(")[0] + "(", "").strip(");"), encoding="utf-8")
        scores += data["school"]
    with codecs.open("university_scores.json", "w", "utf-8") as f_out:
        json.dump(scores, f_out, ensure_ascii=False, indent=1)


def get_province_scores():
    province_scores = []
    url = "http://data.api.gkcx.eol.cn/soudaxue/queryProvince.html?messtype=jsonp&url_sign=queryprovince&province3=&year3=&page=%s&size=50&luqutype3=&luqupici3=&schoolsort=&suiji=&callback=jQuery18306976734810907526_1460562690235&_=1460562692033"
    for i in range(1, 250):
        if i % 100 == 1:
            print(i, len(province_scores))
        resp = requests.get(url % i)
        data = json.loads(resp.text.replace(resp.text.split("(")[0] + "(", "").strip(");"), encoding="utf-8")
        province_scores += data["school"]
    with codecs.open("province_scores.json", "w", "utf-8") as f_out:
        json.dump(province_scores, f_out, ensure_ascii=False, indent=1)


def get_subject_scores():
    subject_scores = []
    url = "http://data.api.gkcx.eol.cn/soudaxue/querySpecialtyScore.html?messtype=jsonp&url_sign=querySpecialtyScore&provinceforschool=&schooltype=&page=%s&size=50&keyWord=&schoolproperty=&schoolflag=&schoolsort=&province=&fsyear=&fstype=&zhaoshengpici=&zytype=&suiji=&callback=jQuery18307452464519812749_1460563567053&_=1460563567936"
    for i in range(39472, 293664):
        flag = True
        while flag:
            if i % 100 == 1:
                print(i, len(subject_scores))
            resp = requests.get(url % i)
            try:
                data = json.loads(resp.text.replace(resp.text.split("(")[0] + "(", "").strip(");"), encoding="utf-8")
                subject_scores += data["school"]
                flag = False
            except ValueError:
                print("parse error, try again")
    with codecs.open("subject_scores.json", "w", "utf-8") as f_out:
        json.dump(subject_scores, f_out, ensure_ascii=False, indent=1)