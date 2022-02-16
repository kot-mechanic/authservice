import requests

url = 'https://raw.githubusercontent.com/kot-mechanic/mongodb_otus/main/screen/222222222222222222.png'
r = requests.get(url, allow_redirects=True)

open('D:\\work\\poslanie\\authservice\\ws_app\\tmp\\TestUser\\1.png', 'wb').write(r.content)