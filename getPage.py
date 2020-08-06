from lxml import etree
import requests
import pandas as pd
import numpy as np


def main():
    result = requests.get("https://www.travel.taipei/zh-tw/event-calendar/2018?page=1&fbclid=IwAR3r1ZMh5DdprGOwn5mVtwXu-9b7EvpC2Gh3R6v_otlpLYT_7VEW6WGZP8M")
    result.encoding = 'utf-8'
    data = parseTable(result)
    df = pd.DataFrame(data, columns=['activity', 'type', 'start_date', 'end_date', 'address', 'latitude', 'longitude'])
    df.drop_duplicates(keep='first')
    df.to_csv('output.csv')


def parseTable(result):
    data = []
    root = etree.fromstring(result.text, etree.HTMLParser())
    for inside in root.xpath("//ul[@class='event-season-list new']/li[position()>=1]"):
        href = inside.xpath("./a/@href")
        activity = inside.xpath("./a/h4/text()")
        type = inside.xpath("./a/p[@class='type']/text()")
        date = inside.xpath("./a/p[@class='date']/text()")
        try:
            start_date, end_date = date[0].split('～')
        except:
            start_date = date[0]
            end_date = date[0]
        inner = requests.get(
            "https://www.travel.taipei/" + href[0])
        inner.encoding = 'utf-8'
        inner_root = etree.fromstring(inner.text, etree.HTMLParser())
        for item in inner_root.xpath("//dl[@class='event-info-list']"):
            place = item.xpath("./dd[@class='info']/a[@class='btn-location-link']/text()")
            lng = item.xpath("./dd[@class='info']/a[@class='btn-location-link']/@href")
            if place == []:
                address = 'null'
            else:
                address = place[0]
            try:
                coordinate = lng[0].split('/')
                latitude, longitude = coordinate[5].split(',')
            except:
                address = 'null'
                latitude = 'null'
                longitude = 'null'
        print(activity[0], type[0], start_date, end_date, address, latitude, longitude)
        data.append([activity[0], type[0], start_date, end_date, address, latitude, longitude])
    return data

if __name__ == "__main__":
    main()