# 入力は日付だけが理想
# 使い方
# python plot_folium.py -date 20200213

import googlemaps
import argparse
import time
import os

# gpxファイルの読み込み
import gpxpy
import gpxpy.gpx

# スクレイピング用
# import chromedriver_binary
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from bs4 import BeautifulSoup
import requests

import pandas as pd
import folium

# コマンドラインから引数を取得
parser = argparse.ArgumentParser()
parser.add_argument('-date')
args = parser.parse_args()

date = args.date
# date = "20200213"
os.makedirs("./" + date)
os.makedirs("./" + date + "/fig")
os.makedirs("./" + date + "/html")
os.makedirs("./" + date + "/garmin")


# google mapからのスクレイピング
# gmapのjava scriptに対応

# マイリストのURL→リストにスポットの名称を入れる
url = "https://goo.gl/maps/qYUxE68UrhLA6MYe7"
# ブラウザのオプションを格納する変数をもらってきます。
options = Options()
# Headlessモードを有効にする（コメントアウトするとブラウザが実際に立ち上がります）
options.set_headless(True)
# ブラウザを起動する
driver = webdriver.Chrome(chrome_options=options)
# ブラウザでアクセスする
driver.get(url)
time.sleep(10)
# HTMLを文字コードをUTF-8に変換してから取得します。
html = driver.page_source.encode('utf-8')
# BeautifulSoupで扱えるようにパースします
soup = BeautifulSoup(html, "html.parser")

# リストにspotを格納
list_spot = []
for i in soup.find_all("h3", "section-result-title"):
    list_spot.append(i.get_text())


# スポットの写真を入手する
list_imgs_url = []
for i in soup.select(".section-result-image"):
    style = i.get("style")
    style_ = style.strip("background-image:url(").strip(")")
    list_imgs_url.append(style_)

# imagesからtargetに入れる
for i, url in enumerate(list_imgs_url):
    re = requests.get(url)
    # imgフォルダに格納
    with open("./" + date + "fig" + list_spot[i] + ".jpg", 'wb') as f:
        # .contentで画像データとして書き込む
        f.write(re.content)
# スクレイピング終了確認
print("画像保存が完了しました。")

# google map APIでスポットの緯度経度を取得
googleapikey = API_KEY
gmaps = googlemaps.Client(key=googleapikey)

df = pd.DataFrame()
df["spot"] = list_spot
list_lat = []
list_lng = []
for spot in list_spot:
    print(spot)
    result = gmaps.geocode(spot)
    lat = result[0]["geometry"]["location"]["lat"]
    lng = result[0]["geometry"]["location"]["lng"]
    list_lat.append(lat)
    list_lng.append(lng)
    time.sleep(10)
# dfに追加
df["lat"] = list_lat
df["lng"] = list_lng
df.head()
df.to_csv("spot_{}.csv".format(date))

# foliumにplot

gpx_file = open('./garmin/{}.gpx'.format(date), 'r')
gpx = gpxpy.parse(gpx_file)
# 緯度経度取得
points = []
for track in gpx.tracks:
    for segment in track.segments:
        for point in segment.points:
            points.append([point.latitude, point.longitude])

# foliumにplot
# ルートをplot
my_map = folium.Map(
    location=points[len(points) // 2],
    zoom_start=10,
    tiles='Stamen Terrain')
folium.PolyLine(points).add_to(my_map)
# spotのmerlerを追加
# markerを追加
for i, row in enumerate(df.itertuples()):
    fig = "./fig/{}.jpg".format(list_spot[i])
    folium.Marker(
        [row[2], row[3]],
        popup='<a>row[1]<img width="60" src=fig></a>',
        # popup=row[1],
        icon=folium.Icon(color='red')
    ).add_to(my_map)

my_map.save("html/folium.html")
