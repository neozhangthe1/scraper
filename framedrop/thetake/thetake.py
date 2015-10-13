__author__ = 'yutao'

import requests

def get_products():
    for i in range(50000):
        response = requests.get("https://thetake.com/products/danielRelated?limit=100&start=&productId=%s" % i)
