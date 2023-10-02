from selenium import webdriver
from selenium.webdriver.edge.service import Service
import time
import json

# 填写webdriver的保存目录
service = Service("../MicrosoftWebDriver116.exe")

browser = webdriver.Edge(service=service)

# 记得写完整的url 包括http和https
browser.get('https://www.icourse163.org')

# 程序打开网页后20秒内手动登陆账户
time.sleep(20)

with open('cookies.txt', 'w') as cookief:
    # 将cookies保存为json格式
    cookief.write(json.dumps(browser.get_cookies()))

browser.close()
