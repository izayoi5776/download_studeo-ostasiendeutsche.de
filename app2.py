from encodings import utf_8
from genericpath import exists
import urllib
import os
from bs4 import BeautifulSoup
from pathlib import Path
import pickle
import json

# https://studeo-ostasiendeutsche.de/fotothek/china/nanjing/1937-2/1250-p6864
# 保存 description 为 html 文件
def writeDesc(url, s):
  path = urllib.parse.urlparse(url).path
  #p2 = path.split("/")[-1]  # 1250-p6864
  #p3 = p2.split("-")[-1]    # p6864
  fn = path[1:] + ".html"
  s = '<div class="description" url="' + url + '">' + str(s) + "</div>" 
  print(" desc=" + fn)
  with open(fn, "w", encoding="utf-8") as f:
    f.write(str(s))

# https://studeo-ostasiendeutsche.de/fotothek/china/nanjing/1937-2/1250-p6864/file
# 保存 url 对应图片, 用pxxxx作为文件名
def getJpg(url):
  path = urllib.parse.urlparse(url).path
  #p2 = path.split("/")[-2]  # 1250-p6864
  #p3 = p2.split("-")[-1]    # p6864
  fn = path[1:-5] + ".jpg"
  print(" fn=" + fn, end="")
  if(os.path.exists(fn)):
    print("...SKIP")
  else:
    print("...GET")
    Path(os.path.dirname(fn)).mkdir(parents=True, exist_ok=True)
    urllib.request.urlretrieve(url, fn)

# 读取任意url
def get1url(url):
  with urllib.request.urlopen(url) as res:
    print("checking " + url)
    html = res.read()
    soup = BeautifulSoup(html, "html5lib")
    # 取下层URL
    for i in soup.select("a.koowa_media__item__link"):
      url2 = urllib.parse.urljoin(url, i["href"]) 
      print(" add " + url2)
      urls.add(url2)

    # 图片URL，应该只有一个
    for i in soup.select("a.docman_download__button"):
      url2 = urllib.parse.urljoin(url, i["href"]) 
      getJpg(url2)
    
    # 说明文字，应该只有一个
    for i in soup.select('div[itemprop="description"]'):
      writeDesc(url, str(i))

def printSize():
  print("todo:" + str(len(urls)) + ", done:" + str(len(done)) + " skip:" + str(len(skip)))

#https://stackoverflow.com/questions/22281059/set-object-is-not-json-serializable
# convert set to list before save as json
def set_default(obj):
    if isinstance(obj, set):
        return list(obj)
    raise TypeError

# INSTALL
'''
sudo apt-get update
sudo apt-get upgrade  #Optional
sudo apt install python3-pip

pip install bs4
pip install html5lib
'''

# --- MAIN ----
# 例：真入口
urls = {"https://studeo-ostasiendeutsche.de/fotothek/china"}
# 例：带下层和图一览的页面
#urls = {"https://studeo-ostasiendeutsche.de/fotothek/china/nanjing/1937-2"}
# 例：图和说明的页面
#urls = {"https://studeo-ostasiendeutsche.de/fotothek/china/nanjing/1937-2/1250-p6864"}
# 例：有错的
#urls = {"https://studeo-ostasiendeutsche.de/fotothek/china/shanghai/1919-1/356-p0526"}

done = set()
skip = set()
settingFileName = "setting.json"

# read setting
if(os.path.exists(settingFileName)):
  with open(settingFileName, 'r') as f:
    js = json.load(f)
    urls = set(js["urls"])
    done = set(js["done"])
    skip = set(js["skip"])
    print("restore data from last run, ", end="")
    printSize()

while len(urls)>0:
  url = urls.pop()
  if url in done:
    print("skip " + url)
  else:
    try:
      get1url(url)
      done.add(url)
    except Exception as e:
      print(" " + str(e) + " url=" + url)
      skip.add(url)
    finally:
      printSize()

  # write setting
  with open(settingFileName, 'w') as f:
    js = {}
    js["urls"] = urls
    js["done"] = done
    js["skip"] = skip
    json.dump(js, f, default=set_default)


