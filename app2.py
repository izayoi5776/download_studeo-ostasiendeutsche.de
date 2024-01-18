from encodings import utf_8
from genericpath import exists
import urllib
import urllib.request
import os
from bs4 import BeautifulSoup
from pathlib import Path
import pickle

# https://studeo-ostasiendeutsche.de/fotothek/china/nanjing/1937-2/1250-p6864
# 保存 description 为 html 文件
def writeDesc(url, s):
  path = urllib.parse.urlparse(url).path
  #p2 = path.split("/")[-1]  # 1250-p6864
  #p3 = p2.split("-")[-1]    # p6864
  fn = path[1:] + ".html"
  s = '<div class="description" url="' + url + '">' + str(s) + "</div>" 
  print(" desc=" + fn)
  Path(os.path.dirname(fn)).mkdir(parents=True, exist_ok=True)
  with open(fn, "w", encoding="utf-8") as f:
    f.write(str(s))

# https://studeo-ostasiendeutsche.de/fotothek/china/nanjing/1937-2/1250-p6864/file
# 保存 url 对应图片, 用pxxxx作为文件名
def getJpg(url):
  path = urllib.parse.urlparse(url).path
  #p2 = path.split("/")[-2]  # 1250-p6864
  #p3 = p2.split("-")[-1]    # p6864
  fn = path[1:-5] + ".jpg"
  print(" jpg =" + fn, end="")
  if(os.path.exists(fn)):
    print("...SKIP")
  else:
    print("...GET")
    Path(os.path.dirname(fn)).mkdir(parents=True, exist_ok=True)
    try:
      urllib.request.urlretrieve(url, fn)
    except Exception as err:
      print("FAIL", err)


# 读取任意url
def get1url(url):
  with urllib.request.urlopen(url) as res:
    print("checking " + url)
    html = res.read()
    soup = BeautifulSoup(html, "html5lib")
    # 取下层URL
    for i in soup.select("a.koowa_media__item__link"):
      url2 = urllib.parse.urljoin(url, i["href"]) 
      print(" add sub  " + url2)
      urls.add(url2)

    # 取导航URL
    for i in soup.select("div.k-pagination a"):
      try:
        url2 = urllib.parse.urljoin(url, i["href"]) 
      except:
        # 当前页取不到href，跳过
        continue
      if url2 in done:
        print(" not add navi " + url2)
      else:
        print(" add navi " + url2)
        urls.add(url2)

    # 图片URL，应该只有一个
    for i in soup.select("a.docman_download__button"):
      url2 = urllib.parse.urljoin(url, i["href"]) 
      getJpg(url2)
    
    # 说明文字，应该只有一个
    for i in soup.select('div[itemprop="description"]'):
      writeDesc(url, str(i))

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
# 例：错误页
#urls = {"https://studeo-ostasiendeutsche.de/fotothek/china/hankow/2005"}
# 例：带下层和图一览的页面
#urls = {"https://studeo-ostasiendeutsche.de/fotothek/china/nanjing/1937-2"}
# 例：图和说明的页面
#urls = {"https://studeo-ostasiendeutsche.de/fotothek/china/nanjing/1937-2/1250-p6864"}
done = set()
settingFileName = "pickle.dump"

# read setting
if(os.path.exists(settingFileName)):
  with open(settingFileName, 'rb') as f:
    urls, done = pickle.load(f)
    print("restore data from last run, todo:" + str(len(urls)) + ", done:" + str(len(done)))
while len(urls)>0:
  url = urls.pop()
  if url in done:
    print("skip " + url)
  else:
    try:
      get1url(url)
    except Exception as err:
      print("skip err " + url)
    done.add(url)
    print("todo:" + str(len(urls)) + ", done:" + str(len(done)))
  # write setting
  with open(settingFileName, 'wb') as f:
    pickle.dump([urls, done], f)


